#!/Bio/User/renchaobo/software/miniconda3/envs/R3.6.1/bin/Rscript
# Title     : Box plot with ggpubr with p value
# Created by: MingJia
# Created on: 2021/4/24
options(warn = -1)
library(optparse)
library(ggpubr)
library(reshape2)
library(stringr)
library(logging)
basicConfig()

#### Argument parser ####
option_list <- list(
  make_option(c("-f", "--file"),
              type = "character",
              help = "The table include expression info"),
  make_option(c("--compare"),
              type = "character",
              help = "The file contain compare info"),
  make_option(
    c("-p", "--prefix"),
    type = "character",
    default = "result",
    help = "The out prefix"
  ),
  make_option(c("-x", "--xlab"),
              type = "character",
              help = "The x lab name"),
  make_option(c("-y", "--ylab"),
              type = "character",
              help = "The y lab name"),
  make_option(
    c("--method"),
    type = "character",
    default = "kruskal.test",
    help = "Which method to be used for comparing means [default %default]"
  ),
  make_option(
    c("--convert"),
    type = "character",
    default = "/Bio/usr/bin/convert",
    help = "The convert program to convert pdf to png[default %default]"
  )
)
opts <- parse_args(
  OptionParser(
    usage = "%prog[options]",
    option_list = option_list,
    description = "\nBox plot with compare p value by ggpubr"
  ),
  positional_arguments = F
)
#########################
methods <- c("t.test", "wilcox.test", "anova", "kruskal.test")
if (!(opts$method %in% methods)) {
  logerror("method must one of %s", methods)
  quit(status = 1)
}

loginfo("Parse the input table %s", opts$file)
df <- read.table(
  file = opts$file,
  header = T,
  row.names = 1,
  check.names = F,
  sep = "\t",
  quote = ""
)

loginfo("Parse the compare info file %s", opts$compare)
tmp <- read.table(
  file = opts$compare,
  check.names = F,
  sep = "\t",
  quote = "",
  stringsAsFactors = F
)
info.compare <- lapply(split(tmp, seq(nrow(tmp))), as.character)

loginfo("Melt the data")
tag <- colnames(df)[1]
info.data <- melt(df, ID = tag)

loginfo("Plot")
file_pdf <- str_c(opts$prefix, "pdf", sep = '.')
file_png <- str_c(opts$prefix, "png", sep = '.')

g <- ggboxplot(info.data,
               x = "variable",
               y = "value",
               color = "variable") +
  stat_compare_means(comparisons = info.compare,
                     method = opts$method) +
  theme(legend.title = element_blank(),
        legend.position = "right")

if (!is.null(opts$xlab)) {
  g <- g + xlab(opts$xlab)
}
if (!is.null(opts$ylab)) {
  g <- g + ylab(opts$ylab)
}

ggsave(g,
       file = file_pdf,
       width = 7,
       height = 6)
cmd <- str_c(opts$convert, file_pdf, file_png, sep = " ")
system(cmd)
