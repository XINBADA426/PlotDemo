#!/Bio/bin/Rscript
# @Author: MingJia
# @Date:   2020-12-12 09:32:25
# @Last Modified by:   MingJia
# @Last Modified time: 2022-09-19 00:11:52
library(optparse)
library(pheatmap)
library(logging)
basicConfig(level = "INFO")

#### Functions
parser_info <- function(fname,
                        sep = "\t",
                        header = FALSE,
                        ...) {
  loginfo("Parse the info %s", fname)
  res <- read.table(
    file = fname,
    sep = sep,
    row.names = 1,
    header = header,
    check.names = F,
    stringsAsFactors = F,
    ...
  )
  return(res)
}

plot_heatmap <- function(data,
                         fout,
                         title,
                         color,
                         scale,
                         cluster_col,
                         cluster_row,
                         show_rowname,
                         fontsize_row,
                         border_color,
                         cellwidth,
                         cellheight,
                         ...) {
  pheatmap(
    data,
    filename = fout,
    main = title,
    color = color,
    scale = scale,
    cluster_cols = cluster_col,
    cluster_rows = cluster_row,
    show_rownames = show_rowname,
    fontsize_row = fontsize_row,
    border_color = border_color,
    cellwidth = cellwidth,
    cellheight = cellheight,
    ...
  )
}

#### Command Parser
option_list <- list(
  make_option(c("-f", "--file"),
              type = "character",
              help = "The abundance table"),
  make_option(c("--scale"),
              default = "row",
              help = "Whether scale the data(none | column | row)[default= %default]"),
  make_option(
    c("--cluster_row"),
    action = "store_true",
    default = FALSE,
    help = "Whether cluster rows[default= %default]"
  ),
  make_option(
    c("--cluster_col"),
    action = "store_true",
    default = FALSE,
    help = "Whether cluster cols[default= %default]"
  ),
  make_option(
    c("--show_rowname"),
    action = "store_true",
    default = FALSE,
    help = "Whether show the row names[default= %default]"
  ),
  make_option(
    c("--hide_border"),
    action = "store_true",
    default = FALSE,
    help = "Whether hide the border[default= %default]"
  ),
  make_option(
    c("--group"),
    type = "character",
    default = NULL,
    help = "The group info file"
  ),
  make_option(
    c("--feature"),
    type = "character",
    default = NULL,
    help = "The feature class file"
  ),
  make_option(
    c("-c", "--color"),
    type = "character",
    default = "steelblue,white,red",
    help = "The color to use[default= %default]"
  ),
  make_option(c("--cwidth"),
              type = "double",
              help = "The cell width"),
  make_option(c("--cheight"),
              type = "double",
              help = "The cell height"),
  make_option(
    c("-t", "--title"),
    type = "character",
    default = "",
    help = "The title for the heatmap"
  ),
  make_option(
    c("-p", "--prefix"),
    type = "character",
    default = "./result",
    help = "The out put prefix[default= %default]"
  )
)
opts <- parse_args(
  OptionParser(
    usage = "%prog[options]",
    option_list = option_list,
    description = "\nHeatmpap plot script"
  ),
  positional_arguments = F
)

#### Main
color <- colorRampPalette(unlist(strsplit(opts$color,',')))(100)
if (opts$scale %in% c("none", "row", "column")) {
  scale <- opts$scale
} else {
  stop(logerror("scale param must be none | row | column"))
}
border_color <- ifelse(opts$hide_border, NA, "grey60")

loginfo("Parse the input table %s", opts$file)
data <- read.table(
  file = opts$file,
  header = T,
  row.names = 1,
  check.names = F,
  sep = "\t",
  quote = ""
)

loginfo("Remove the 0 rows")
clean_data <- as.matrix(data[which(rowSums(data) > 0), ])

gene_num <- nrow(clean_data)
if (gene_num <= 200) {
  fontsize_row <- 4
  cellheight <- 5
} else if (gene_num > 200 && gene_num <= 500) {
  fontsize_row <- 3
  cellheight <- 3
} else if (gene_num > 500 && gene_num <= 2000) {
  fontsize_row <- 2
  cellheight <- 2
} else {
  cellheight <- 4000 / gene_num
}

if (!is.null(opts$cwidth)) {
  cellwidth <- opts$cwidth
} else {
  cellwidth <- NA
}
if (!is.null(opts$cheight)) {
  cellheight <- opts$cheight
}

if (is.null(opts$group)) {
  info_group <- NA
} else {
  info_group <- parser_info(opts$group)
  colnames(info_group) <- c("Group")
}

if (is.null(opts$feature)) {
  info_feature <- NA
} else {
  info_feature <- parser_info(opts$feature)
  colnames(info_feature) <- c("Feature")
}

loginfo("Start to plot")
f_pdf <- paste(opts$prefix, "heatmap.pdf", sep = ".")
f_png <- paste(opts$prefix, "heatmap.png", sep = ".")

plot_heatmap(
  clean_data,
  f_pdf,
  opts$title,
  color,
  scale,
  opts$cluster_col,
  opts$cluster_row,
  opts$show_rowname,
  fontsize_row,
  border_color,
  cellwidth,
  cellheight,
  annotation_col = info_group,
  annotation_row = info_feature
)

loginfo("convert -density 300 %s to %s", f_pdf, f_png)
cmd <- paste("convert -density 300", f_pdf, f_png, sep = " ")
system(cmd)