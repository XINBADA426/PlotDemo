#!/Bio/User/renchaobo/software/miniconda3/envs/R3.6.1/bin/Rscript
# @Author: MingJia
# @Date:   2021-2-27 09:32:25
# @Last Modified by:   MingJia
# @Last Modified time: 2021-2-27 20:23:52
.libPaths("/home/renchaobo/R/x86_64-conda_cos6-linux-gnu-library/3.6")
library(optparse)
library(ggrepel)
library(scales)
library(logging)
basicConfig()

option_list <- list(make_option(c("-f", "--file"),
                                type = "character",
                                help = "The table input to plot volcano"),
                    make_option(c("-x", "--xname"),
                                type = "character",
                                default = "log2(FC)",
                                help = "The log2(FC) column name[default= %default]"),
                    make_option(c("-y", "--yname"),
                                type = "character",
                                default = "FDR",
                                help = "The FDR column name[default= %default]"),
                    make_option(c("--hlimit"),
                                type = "double",
                                default = 0.05,
                                help = "The FDR limit[default= %default]"),
                    make_option(c("--vlimit"),
                                type = "double",
                                default = 1,
                                help = "The log2(FC) limit[default= %default]"),
                    make_option(c("--xlab"),
                                type = "character",
                                default = "log2(FC)",
                                help = "The xlab for the plot[default = %default]"),
                    make_option(c("--ylab"),
                                type = "character",
                                default = "-1*log10(FDR)",
                                help = "The ylab for the plot[default= %default]"),
                    make_option(c("-t", "--title"),
                                type = "character",
                                default = "Volcano Plot",
                                help = "The title for the plot[default= %default]"),
                    make_option(c("--tag"),
                                type = "character",
                                help = "The tag info"),
                    make_option(c("-p", "--prefix"),
                                type = "character",
                                default = "result",
                                help = "The out prefix"),
                    make_option(c("--convert"),
                                type = "character",
                                default = "/Bio/usr/bin/convert",
                                help = "The convert program to convert pdf to png[default= %default]"))
opts <- parse_args(OptionParser(usage = "%prog[options]",
                                option_list = option_list,
                                description = "\nScript of volcano plot with tag"),
                   positional_arguments = F)

#### Some params ####
mytheme <- theme_bw() +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.border = element_rect(color = "#000000", size = 1),
    axis.text = element_text(color = "#000000", size = 12),
    axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = 0.5),
    axis.text.y = element_text(hjust = 1, vjust = 0.5),
    axis.title = element_text(color = "#000000", size = 16, face = "bold"),
    axis.title.x = element_text(margin = margin(2.5, 0, 2.5, 0, "mm")),
    axis.title.y = element_text(margin = margin(0, 2.5, 0, 2.5, "mm")),
    axis.ticks = element_line(color = "#000000", size = 0.6),
    axis.ticks.length = unit(0.13, 'cm'),
    legend.title = element_blank(),
    plot.title = element_text(size = 20, face = "bold", hjust = 0.5))

# pic params
width <- 8
height <- 7
colors <- c('#F9766D', '#00000032', '#609DFF')
#####################


loginfo("Parse the input table %s", opts$file)
df <- read.table(file = opts$file,
                 header = T,
                 row.names = 1,
                 check.names = F,
                 sep = "\t",
                 quote = "")

data <- df[, c(opts$xname, opts$yname)]

# Set the color
data$color <- "nosig"
data[data[, opts$xname] > opts$vlimit & data[, opts$yname] < opts$hlimit, "color"] <- "up"
data[data[, opts$xname] < -opts$vlimit & data[, opts$yname] < opts$hlimit, "color"] <- "down"
data$color <- factor(data$color, levels = c("up", "nosig", "down"))
colors <- colors[sort(unique(data$color))]

data$tag <- ""
if (!is.null(opts$tag)) {
  loginfo("Parse the tag info %s", opts$tag)
  info_tag <- read.table(file = opts$tag,
                         header = F,
                         row.names = 1,
                         check.names = F,
                         sep = "\t",
                         quote = "",
                         stringsAsFactors = F)
  tag_label <- row.names(info_tag)
  data[tag_label, "tag"] <- info_tag[tag_label, 1]
}

loginfo("Start to plot")
data[, opts$yname] <- -1 * log10(data[, opts$yname])
ymax <- max(data[, opts$yname]) * 1.1
xmax <- max(abs(data[, opts$xname])) * 1.1

p <- ggplot(data, aes(data[, opts$xname], data[, opts$yname], label = tag, color = color)) +
  geom_text_repel(box.padding = 0.5, max.overlaps = Inf) +
  geom_point(size = 1, shape = 19) +
  scale_x_continuous(breaks = pretty_breaks(5), limits = c(-xmax, xmax)) +
  scale_y_continuous(breaks = pretty_breaks(5), limits = c(0, ymax)) +
  scale_color_manual(values = colors) +
  geom_hline(yintercept = -log10(opts$hlimit), linetype = 2) +
  geom_vline(xintercept = c(-opts$vlimit, opts$vlimit), linetype = 2) +
  labs(x = opts$xlab, y = opts$ylab, title = opts$title) +
  mytheme +
  guides(color = guide_legend(override.aes = list(size = 3)))

file_pdf <- paste0(opts$prefix, ".pdf")
file_png <- paste0(opts$prefix, ".png")
ggsave(file_pdf, p,
       width = width,
       height = height)


cmd <- paste(opts$convert, file_pdf, file_png, sep = " ")
system(cmd)

