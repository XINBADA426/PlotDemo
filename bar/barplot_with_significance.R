#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(optparse)
  library(ggplot2)
  library(ggsignif)
  library(dplyr)
  library(tidyr)
  library(logging)
  library(showtext)
})

# 字体设置
font_add("Arial", "/data1/NFS/home/rcb/.fonts/arial.ttf")
showtext_auto()

# 设置日志
setup_logging <- function(log_file = NULL) {
  if (is.null(log_file)) {
    basicConfig()
  } else {
    basicConfig(level = 'DEBUG')
    addHandler(writeToFile, file = log_file, level = 'DEBUG')
  }
  loginfo("Logging system initialized")
}

# 命令行参数解析
parse_arguments <- function() {
  option_list <- list(
    make_option(c("-d", "--data"), type = "character", default = NULL,
                help = "Input data file (TSV/CSV format with 2 columns: sample_name, value) [required]",
                metavar = "FILE"),

    make_option(c("-g", "--group"), type = "character", default = NULL,
                help = "Group information file (TSV/CSV format with 2 columns: sample_name, group) [required]",
                metavar = "FILE"),

    make_option(c("-o", "--output"), type = "character", default = "output",
                help = "Output file prefix [default: %default]",
                metavar = "PREFIX"),

    make_option(c("-m", "--method"), type = "character", default = "wilcox.test",
                help = "Statistical method: t.test, wilcox.test, anova, kruskal.test, auto [default: %default]",
                metavar = "METHOD"),

    make_option(c("-p", "--paired"), type = "logical", default = FALSE,
                action = "store_true",
                help = "Perform paired test (only for t.test and wilcox.test) [default: %default]"),

    make_option(c("-c", "--comparisons"), type = "character", default = NULL,
                help = "Specific comparisons in format 'group1,group2;group3,group4' [default: all pairwise]",
                metavar = "COMPARISONS"),

    make_option(c("--width"), type = "numeric", default = 89,
                help = "Figure width in mm (Nature single column: 89mm) [default: %default]",
                metavar = "WIDTH"),

    make_option(c("--height"), type = "numeric", default = 89,
                help = "Figure height in mm [default: %default]",
                metavar = "HEIGHT"),

    make_option(c("-t", "--title"), type = "character", default = "",
                help = "Plot title [default: none]",
                metavar = "TITLE"),

    make_option(c("-x", "--xlabel"), type = "character", default = "",
                help = "X-axis label [default: none]",
                metavar = "LABEL"),

    make_option(c("-y", "--ylabel"), type = "character", default = "",
                help = "Y-axis label [default: none]",
                metavar = "LABEL"),

    make_option(c("-l", "--log"), type = "character", default = NULL,
                help = "Log file path [default: print to console]",
                metavar = "FILE"),

    make_option(c("--error_bar"), type = "character", default = "se",
                help = "Error bar type: se (standard error), sd (standard deviation), ci (95% confidence interval) [default: %default]",
                metavar = "TYPE"),

    make_option(c("--palette"), type = "character", default = "nature",
                help = "Color palette: nature, npg, nejm, lancet, jama, jco, custom [default: %default]",
                metavar = "PALETTE"),

    make_option(c("--hide_ns"), type = "logical", default = FALSE,
                action = "store_true",
                help = "Hide non-significant comparisons [default: %default]")
  )

  opt_parser <- OptionParser(option_list = option_list,
                            description = "Generate publication-quality bar plots with significance annotations")
  opt <- parse_args(opt_parser)

  # 验证必需参数
  if (is.null(opt$data) || is.null(opt$group)) {
    print_help(opt_parser)
    stop("Both --data and --group files are required!", call. = FALSE)
  }

  return(opt)
}

# 读取数据文件
read_data_file <- function(file_path) {
  loginfo(sprintf("Reading file: %s", file_path))

  # 判断文件格式
  if (grepl("\\.csv$", file_path, ignore.case = TRUE)) {
    data <- read.csv(file_path, header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
  } else {
    data <- read.table(file_path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)
  }

  loginfo(sprintf("Successfully read %d rows from %s", nrow(data), file_path))
  return(data)
}

# 验证数据格式
validate_data <- function(data_df, group_df) {
  loginfo("Validating data format...")

  # 检查列数
  if (ncol(data_df) != 2) {
    stop("Data file must have exactly 2 columns: sample_name and value", call. = FALSE)
  }
  if (ncol(group_df) != 2) {
    stop("Group file must have exactly 2 columns: sample_name and group", call. = FALSE)
  }

  # 重命名列
  colnames(data_df) <- c("sample", "value")
  colnames(group_df) <- c("sample", "group")

  # 检查数值列
  data_df$value <- as.numeric(data_df$value)
  if (any(is.na(data_df$value))) {
    stop("Value column contains non-numeric values", call. = FALSE)
  }

  # 检查样本匹配
  if (!all(data_df$sample %in% group_df$sample)) {
    missing_samples <- setdiff(data_df$sample, group_df$sample)
    warning(sprintf("Some samples in data file are not in group file: %s",
                   paste(missing_samples, collapse = ", ")))
  }

  loginfo("Data validation completed successfully")
  return(list(data = data_df, group = group_df))
}

# 合并数据 - 保持分组顺序
merge_data <- function(data_df, group_df) {
  loginfo("Merging data and group information...")

  # 获取分组的原始顺序
  group_order <- unique(group_df$group)
  loginfo(sprintf("Group order from file: %s", paste(group_order, collapse = ", ")))

  merged_df <- merge(data_df, group_df, by = "sample", all.x = TRUE)

  # 移除没有分组信息的样本
  na_samples <- sum(is.na(merged_df$group))
  if (na_samples > 0) {
    warning(sprintf("Removing %d samples without group information", na_samples))
    merged_df <- merged_df[!is.na(merged_df$group), ]
  }

  # 将group转换为因子，并保持原始顺序
  merged_df$group <- factor(merged_df$group, levels = group_order)

  # 统计每组样本数
  group_counts <- table(merged_df$group)
  loginfo("Sample counts per group:")
  for (g in names(group_counts)) {
    loginfo(sprintf("  %s: %d samples", g, group_counts[g]))
  }

  loginfo(sprintf("Final dataset: %d samples in %d groups",
                 nrow(merged_df), length(unique(merged_df$group))))

  return(merged_df)
}

# 自动选择统计方法
auto_select_method <- function(data) {
  group_sizes <- table(data$group)
  min_size <- min(group_sizes)
  n_groups <- length(unique(data$group))

  if (min_size < 3) {
    logwarn("Sample size too small for statistical testing")
    return("none")
  } else if (min_size < 5) {
    return(ifelse(n_groups == 2, "wilcox.test", "kruskal.test"))
  } else if (min_size < 30) {
    # 检查正态性
    all_normal <- TRUE
    for (g in unique(data$group)) {
      group_data <- data$value[data$group == g]
      if (length(group_data) >= 3) {
        if (shapiro.test(group_data)$p.value < 0.05) {
          all_normal <- FALSE
          break
        }
      }
    }
    if (all_normal) {
      return(ifelse(n_groups == 2, "t.test", "anova"))
    } else {
      return(ifelse(n_groups == 2, "wilcox.test", "kruskal.test"))
    }
  } else {
    return(ifelse(n_groups == 2, "t.test", "anova"))
  }
}

# 计算统计量
calculate_summary <- function(data, error_type = "se") {
  loginfo(sprintf("Calculating summary statistics with error type: %s", error_type))

  summary_df <- data %>%
    group_by(group) %>%
    summarise(
      n = n(),
      mean = mean(value, na.rm = TRUE),
      sd = sd(value, na.rm = TRUE),
      se = sd / sqrt(n),
      ci = qt(0.975, df = n - 1) * se,
      .groups = 'drop'
    )

  # 根据error_type选择误差条
  if (error_type == "sd") {
    summary_df$error <- summary_df$sd
  } else if (error_type == "ci") {
    summary_df$error <- summary_df$ci
  } else {
    summary_df$error <- summary_df$se
  }

  return(summary_df)
}

# 解析比较组
parse_comparisons <- function(comparison_str, groups) {
  if (is.null(comparison_str)) {
    # 生成所有两两比较
    if (length(groups) > 1) {
      comparisons <- combn(as.character(groups), 2, simplify = FALSE)
    } else {
      comparisons <- list()
    }
  } else {
    # 解析用户指定的比较
    comparisons <- list()
    pairs <- strsplit(comparison_str, ";")[[1]]
    for (pair in pairs) {
      groups_pair <- trimws(strsplit(pair, ",")[[1]])
      if (length(groups_pair) == 2) {
        comparisons <- append(comparisons, list(groups_pair))
      } else {
        warning(sprintf("Invalid comparison pair: %s", pair))
      }
    }
  }

  loginfo(sprintf("Will perform %d comparisons", length(comparisons)))
  return(comparisons)
}

# 执行统计检验
perform_statistical_test <- function(group1_data, group2_data, method, paired = FALSE) {
  tryCatch({
    if (method == "t.test") {
      test <- t.test(group1_data, group2_data, paired = paired)
      return(test$p.value)
    } else if (method == "wilcox.test") {
      test <- wilcox.test(group1_data, group2_data, paired = paired, exact = FALSE)
      return(test$p.value)
    } else {
      return(NA)
    }
  }, error = function(e) {
    logwarn(sprintf("Statistical test failed: %s", e$message))
    return(NA)
  })
}

# 将p值转换为显著性标记
format_p_value <- function(p_value, hide_ns = FALSE) {
  if (is.na(p_value)) {
    return(NA)
  } else if (p_value < 0.001) {
    return("***")
  } else if (p_value < 0.01) {
    return("**")
  } else if (p_value < 0.05) {
    return("*")
  } else {
    return(ifelse(hide_ns, NA, "ns"))
  }
}

# 获取Nature配色方案
get_nature_colors <- function(palette_name, n_colors) {
  # Nature推荐的配色方案
  nature_palettes <- list(
    nature = c("#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4", "#91D1C2", "#DC0000"),
    npg = c("#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4", "#91D1C2", "#DC0000"),
    nejm = c("#BC3C29", "#0072B5", "#E18727", "#20854E", "#7876B1", "#6F99AD", "#FFDC91", "#EE4C97"),
    lancet = c("#00468B", "#ED0000", "#42B540", "#0099B4", "#925E9F", "#FDAF91", "#AD002A", "#ADB6B6"),
    jama = c("#374E55", "#DF8F44", "#00A1D5", "#B24745", "#79AF97", "#6A6599", "#80796B", "#0073C2"),
    jco = c("#0073C2", "#EFC000", "#868686", "#CD534C", "#7AA6DC", "#003C67", "#8F7700", "#3B3B3B")
  )

  if (palette_name %in% names(nature_palettes)) {
    colors <- nature_palettes[[palette_name]]
  } else {
    colors <- nature_palettes[["nature"]]
  }

  if (n_colors <= length(colors)) {
    return(colors[1:n_colors])
  } else {
    return(colorRampPalette(colors)(n_colors))
  }
}

# 创建柱形图 - 优化Nature风格
create_barplot <- function(data, summary_data, opt) {
  loginfo("Creating bar plot with Nature style...")

  # 检查ggplot2版本
  ggplot2_version <- as.numeric(substr(as.character(packageVersion("ggplot2")), 1, 3))
  use_linewidth <- ggplot2_version >= 3.4

  # Nature出版风格主题
  nature_theme <- theme_bw() +
    theme(
      # 字体设置 - Nature要求
      text = element_text(family = "Arial", size = 7),
      axis.text = element_text(size = 6, color = "black"),
      axis.title = element_text(size = 7, color = "black"),

      # 去除网格线
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),

      # 边框设置
      panel.border = element_blank(),

      # 图例设置
      legend.position = "none",

      # 标题设置
      plot.title = element_text(size = 8, face = "bold", hjust = 0),

      # 边距设置 - 紧凑型
      plot.margin = margin(2, 2, 2, 2, "mm"),

      # 刻度设置
      axis.ticks.length = unit(0.1, "cm")
    )

  # 根据版本添加轴线设置
  if (use_linewidth) {
    nature_theme <- nature_theme +
      theme(
        axis.line = element_line(color = "black", linewidth = 0.35),
        axis.ticks = element_line(color = "black", linewidth = 0.35)
      )
  } else {
    nature_theme <- nature_theme +
      theme(
        axis.line = element_line(color = "black", size = 0.35),
        axis.ticks = element_line(color = "black", size = 0.35)
      )
  }

  # 获取配色
  n_groups <- length(unique(data$group))
  colors <- get_nature_colors(opt$palette, n_groups)

  # 创建基础柱形图
  p <- ggplot(summary_data, aes(x = group, y = mean, fill = group))

  # 根据版本添加几何对象
  if (use_linewidth) {
    p <- p +
      geom_col(width = 0.6, color = "black", linewidth = 0.35) +
      geom_errorbar(aes(ymin = mean - error, ymax = mean + error),
                    width = 0.15, linewidth = 0.35, color = "black")
  } else {
    p <- p +
      geom_col(width = 0.6, color = "black", size = 0.35) +
      geom_errorbar(aes(ymin = mean - error, ymax = mean + error),
                    width = 0.15, size = 0.35, color = "black")
  }

  p <- p + nature_theme + labs(x = opt$xlabel, y = opt$ylabel)

  # 添加标题（如果提供）
  if (!is.null(opt$title) && opt$title != "") {
    p <- p + ggtitle(opt$title)
  }

  # 设置颜色
  p <- p + scale_fill_manual(values = colors)

  # 设置Y轴从0开始，留出顶部空间用于显著性标记
  max_value <- max(c(summary_data$mean + summary_data$error, data$value), na.rm = TRUE)
  p <- p + scale_y_continuous(expand = expansion(mult = c(0, 0.2)),
                             limits = c(0, max_value * 1.3))

  return(p)
}

# 添加显著性标注 - 使用ggsignif
add_significance_ggsignif <- function(plot, data, comparisons, method, paired = FALSE, hide_ns = FALSE) {
  loginfo(sprintf("Adding significance annotations using ggsignif with %s", method))

  if (length(comparisons) == 0 || method == "none") {
    loginfo("No comparisons to perform")
    return(plot)
  }

  # 准备显著性标注数据
  signif_data <- list()

  for (i in seq_along(comparisons)) {
    comp <- comparisons[[i]]
    group1_data <- data$value[data$group == comp[1]]
    group2_data <- data$value[data$group == comp[2]]

    # 执行统计检验
    p_value <- perform_statistical_test(group1_data, group2_data, method, paired)

    # 格式化p值
    label <- format_p_value(p_value, hide_ns)

    # 如果不是NA（即需要显示），添加到列表
    if (!is.na(label)) {
      signif_data[[length(signif_data) + 1]] <- list(
        comparisons = comp,
        label = label,
        p_value = p_value
      )
    }
  }

  # 如果有需要显示的比较，添加显著性标记
  if (length(signif_data) > 0) {
    # 计算Y轴位置
    max_value <- max(data$value, na.rm = TRUE)
    y_start <- max_value * 1.05
    y_step <- max_value * 0.05

    for (i in seq_along(signif_data)) {
      y_position <- y_start + (i - 1) * y_step

      plot <- plot + geom_signif(
        comparisons = list(signif_data[[i]]$comparisons),
        annotations = signif_data[[i]]$label,
        y_position = y_position,
        tip_length = 0.01,
        vjust = 0.5,
        textsize = 2.5,
        size = 0.35,
        color = "black"
      )
    }
  }

  return(plot)
}

# 保存图片 - 只保存PDF
save_plot <- function(plot, output_prefix, width_mm, height_mm) {
  loginfo("Saving plot as PDF...")

  # 转换单位（毫米到英寸）
  width_in <- width_mm / 25.4
  height_in <- height_mm / 25.4

  # 保存PDF（矢量图）
  pdf_file <- paste0(output_prefix, ".pdf")

  tryCatch({
    ggsave(pdf_file, plot, width = width_in, height = height_in,
           units = "in", device = cairo_pdf, dpi = 600)
    loginfo(sprintf("Saved PDF: %s", pdf_file))
  }, error = function(e) {
    warning("cairo_pdf not available, using standard pdf device")
    ggsave(pdf_file, plot, width = width_in, height = height_in,
           units = "in", device = "pdf", useDingbats = FALSE)
    loginfo(sprintf("Saved PDF: %s", pdf_file))
  })
}

# 保存统计结果
save_statistics <- function(data, comparisons, method, output_prefix, paired = FALSE) {
  loginfo("Calculating and saving statistical results...")

  results <- data.frame()

  for (comp in comparisons) {
    group1_data <- data$value[data$group == comp[1]]
    group2_data <- data$value[data$group == comp[2]]

    n1 <- length(group1_data)
    n2 <- length(group2_data)

    # 执行统计检验
    statistic <- NA
    p_value <- NA
    method_used <- method

    tryCatch({
      if (method == "t.test") {
        test_result <- t.test(group1_data, group2_data, paired = paired)
        statistic <- test_result$statistic
        p_value <- test_result$p.value
        method_used <- ifelse(paired, "Paired t-test", "Two-sample t-test")
      } else if (method == "wilcox.test") {
        test_result <- wilcox.test(group1_data, group2_data, paired = paired, exact = FALSE)
        statistic <- test_result$statistic
        p_value <- test_result$p.value
        method_used <- ifelse(paired, "Paired Wilcoxon test", "Wilcoxon rank-sum test")
      }
    }, error = function(e) {
      logwarn(sprintf("Test failed for %s vs %s: %s", comp[1], comp[2], e$message))
    })

    # 计算描述统计
    mean1 <- mean(group1_data, na.rm = TRUE)
    mean2 <- mean(group2_data, na.rm = TRUE)
    sd1 <- sd(group1_data, na.rm = TRUE)
    sd2 <- sd(group2_data, na.rm = TRUE)

    # 添加到结果
    results <- rbind(results, data.frame(
      Group1 = comp[1],
      Group2 = comp[2],
      n1 = n1,
      n2 = n2,
      Mean1 = round(mean1, 4),
      Mean2 = round(mean2, 4),
      SD1 = round(sd1, 4),
      SD2 = round(sd2, 4),
      P_value = p_value,
      Significance = format_p_value(p_value, FALSE),
      Method = method_used,
      stringsAsFactors = FALSE
    ))
  }

  # 保存结果
  stats_file <- paste0(output_prefix, "_statistics.tsv")
  write.table(results, stats_file, sep = "\t", row.names = FALSE, quote = FALSE)
  loginfo(sprintf("Saved statistics: %s", stats_file))

  return(results)
}

# 主函数
main <- function() {
  # 解析命令行参数
  opt <- parse_arguments()

  # 设置日志
  setup_logging(opt$log)

  tryCatch({
    # 记录参数
    separator <- paste(rep("=", 50), collapse = "")
    loginfo(separator)
    loginfo("Starting bar plot generation with parameters:")
    loginfo(sprintf("  Data file: %s", opt$data))
    loginfo(sprintf("  Group file: %s", opt$group))
    loginfo(sprintf("  Output prefix: %s", opt$output))
    loginfo(sprintf("  Statistical method: %s", opt$method))
    loginfo(sprintf("  Figure size: %dmm x %dmm", opt$width, opt$height))
    loginfo(sprintf("  Error bar type: %s", opt$error_bar))
    loginfo(sprintf("  Color palette: %s", opt$palette))
    loginfo(sprintf("  Hide non-significant: %s", opt$hide_ns))
    loginfo(separator)

    # 读取数据
    data_df <- read_data_file(opt$data)
    group_df <- read_data_file(opt$group)

    # 验证数据
    validated <- validate_data(data_df, group_df)

    # 合并数据
    merged_data <- merge_data(validated$data, validated$group)

    # 自动选择统计方法（如果指定）
    if (opt$method == "auto") {
      opt$method <- auto_select_method(merged_data)
      loginfo(sprintf("Auto-selected method: %s", opt$method))
    }

    # 计算汇总统计
    summary_data <- calculate_summary(merged_data, opt$error_bar)

    # 解析比较组
    groups <- levels(merged_data$group)
    comparisons <- parse_comparisons(opt$comparisons, groups)

    # 创建图形
    p <- create_barplot(merged_data, summary_data, opt)

    # 添加显著性标注（使用ggsignif）
    p <- add_significance_ggsignif(p, merged_data, comparisons, opt$method, opt$paired, opt$hide_ns)

    # 保存图片（只保存PDF）
    save_plot(p, opt$output, opt$width, opt$height)

    # 保存统计结果
    stats_results <- save_statistics(merged_data, comparisons, opt$method,
                                    opt$output, opt$paired)

    # 输出汇总信息
    loginfo(separator)
    loginfo("Summary:")
    loginfo(sprintf("  Total samples: %d", nrow(merged_data)))
    loginfo(sprintf("  Number of groups: %d", length(groups)))
    loginfo(sprintf("  Groups (in order): %s", paste(groups, collapse = ", ")))
    loginfo(sprintf("  Statistical method: %s", opt$method))
    loginfo(sprintf("  Comparisons performed: %d", length(comparisons)))

    # 输出显著性结果摘要
    if (nrow(stats_results) > 0) {
      sig_results <- stats_results[!is.na(stats_results$P_value) & stats_results$P_value < 0.05, ]
      if (nrow(sig_results) > 0) {
        loginfo(sprintf("  Significant comparisons (p < 0.05): %d", nrow(sig_results)))
        for (i in 1:nrow(sig_results)) {
          loginfo(sprintf("    %s vs %s: p = %.4f (%s)",
                         sig_results$Group1[i],
                         sig_results$Group2[i],
                         sig_results$P_value[i],
                         sig_results$Significance[i]))
        }
      } else {
        loginfo("  No significant comparisons found (p < 0.05)")
      }
    }

    loginfo(separator)
    loginfo("Analysis completed successfully!")

  }, error = function(e) {
    logerror(sprintf("Error: %s", e$message))
    stop(e$message, call. = FALSE)
  })
}

# 运行主函数
if (!interactive()) {
  main()
}