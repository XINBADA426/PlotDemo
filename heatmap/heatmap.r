#!/Bio/bin/Rscript
# @Author: MingJia
# @Date:   2020-12-12 09:32:25
# @Last Modified by:   MingJia
# @Last Modified time: 2020-12-12 20:23:52
.libPaths("/home/renchaobo/R/x86_64-unknown-linux-gnu-library/3.2")
library(optparse)
library(pheatmap)
library(logging)
basicConfig()

#### Functions
parser_info <- function(fname, sep = "\t", header = False, ...) {
  loginfo("Parse the info %s", fname)
  res <- read.table(file = fname,
                    sep = sep,
                    row.names = 1,
                    heaer = header,
                    check.names = F,
                    ...)
  return(res)
}

plot_heatmap <- function() {
  pass
}

#### Command Parser
option_list <- list(make_option(c("-f", "--file"),
                                type = "character",
                                help = "The abundance table"),
                    make_option(c("--scale"),
                                default = "none",
                                help = "Whether scale the data(none | column | row)[default= %default]"),
                    make_option(c("--cluster_row"),
                                action = "store_true",
                                default = FALSE,
                                help = "Whether cluster rows[default= %default]"),
                    make_option(c("--cluster_col"),
                                action = "store_true",
                                default = FALSE,
                                help = "Whether cluster cols[default= %default]"),
                    make_option(c("--show_rowname"),
                                action = "store_true",
                                default = FALSE,
                                help = "Whether show the row names[default= %default]"),
                    make_option(c("--hide_border"),
                                action = "store_true",
                                default = FALSE,
                                help = "Whether hide the border[default= %default]"),
                    make_option(c("--group"),
                                type = "character",
                                default = NULL,
                                help = "The group info file"),
                    make_option(c("--feature"),
                                type = "character",
                                default = NULL,
                                help = "The feature class file"),
                    make_option(c("-c", "--color"),
                                type = "character",
                                default = "steelblue,white,red",
                                help = "The color to use[default= %default]"),
                    make_option(c("-t", "--title"),
                                type = "character",
                                default = "",
                                help = "The title for the heatmap"),
                    make_option(c("-p", "--prefix"),
                                type = "character",
                                default = "./result",
                                help = "The out put prefix[default= %default]"))
opts <- parse_args(OptionParser(usage = "%prog[options]",
                                option_list = option_list,
                                description = "\nHeatmpap plot script"),
                   positional_arguments = F)

#### Main
color <- colorRampPalette(strsplit(opts$color, ',')[[1]])(256)
if (opts$scale %in% c("none", "row", "column")) {
  scale <- opts$scale
} else {
  stop(logerror("scale param must be none | row | column"))
}
border_color <- ifelse(opts$hide_border, NA, "grey60")

loginfo("Parse the input table %s", opts$file)
data <- read.table(file = opts$file,
                   header = T,
                   row.names = 1,
                   check.names = F,
                   sep = "\t",
                   quote = "")

loginfo("Remove the 0 rows")
clean_data <- as.matrix(data[which(rowSums(data) > 0),])

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

info_group <- ifelse(is.null(opts$group), NA, parser_info(opts$group))

info_feature <- ifelse(if.null(opts$feature), NA, parser_info(opts$feature))

loginfo("Start to plot")
f_pdf <- paste(opts$prefix, "heatmap.pdf", sep = ".")
f_png <- paste(opts$prefix, "heatmap.png", sep = ".")

if (is.null(opts$group)) {
  pheatmap(clean_data,
           filename = file_pdf,
           main = opts$title,
           color = color,
           scale = scale,
           cluster_cols = opts$cluster_col,
           cluster_rows = opts$cluster_row,
           show_rownames = opts$show_rowname,
           fontsize_row = fontsize_row,
           border_color = border_color,
           cellheight = cellheight)
} else {
  loginfo("Parse the group info %s", opts$group)
  group_info <- read.table(file = opts$group,
                           sep = '\t',
                           row.names = 1,
                           check.names = F)
  colnames(group_info) <- c("Group")
  annotation_col <- as.data.frame(group_info)
  pheatmap(clean_data,
           filename = file_pdf,
           main = opts$title,
           color = color,
           scale = scale,
           cluster_cols = F,
           cluster_rows = opts$cluster_row,
           show_rownames = opts$show_rowname,
           fontsize_row = fontsize_row,
           cellheight = cellheight,
           border_color = border_color,
           annotation_col = annotation_col)
}
loginfo("convert %s to %s", file_pdf, file_png)
cmd <- paste("/Bio/usr/bin/convert", file_pdf, file_png, sep = " ")
system(cmd)