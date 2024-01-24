#!/usr/bin/Rscript
# Title     : TreePlot.R
# Objective : Phylogenetic Tree Plot
# Created by: MingJia
# Created on: 2021/5/10
options(warn = -1)
suppressPackageStartupMessages({
  library(optparse)
  library(ggplot2)
  library(reshape2)
  library(stringr)
  library(dplyr)
  library(logging)
})
basicConfig()

#### 函数

#### 参数
option_list <- list(
  make_option(c("--table"),
              type = "character",
              help = "The input table"),
  make_option(c("-o", "--out"),
              default = "./",
              type = "character",
              help = "The input dir[default = %default]"),
  make_option(c("-x", "--xlab"),
              default = "",
              type = "character",
              help = "The x lab name[default = %default]"),
  make_option(c("-y", "--ylab"),
              default = "",
              type = "character",
              help = "The y lab name[default = %default]"),
  make_option(c("-t", "--title"),
              default = "",
              type = "character",
              help = "The title name[default = %default]"),
  make_option(c("-p", "--prefix"),
              type = "character",
              default = "result",
              help = "The out prefix[default= %default]")
)
opts <- parse_args(
  OptionParser(
    usage = "%prog[options]",
    option_list = option_list,
    description = "\nScript of lm line plot"
  ),
  positional_arguments = F
)
#### Main
opts$table <- normalizePath(opts$table)
opts$out <- normalizePath(opts$out)

loginfo("Set work directory to %s ", opts$out)
if (!dir.exists(opts$out)) {
  dir.create(opts$out)
}
setwd(opts$out)

loginfo("Read the input table %s", opts$tabel)
df <- read.table(opts$table,
                 sep = "\t",
                 header = TRUE,
                 check.names = FALSE)
col.id <- colnames(df)[1]
ndf <- melt(df, id.vars = col.id)
colnames(ndf)[1] <- "x"
print(head(ndf))

loginfo("Start lm stat")
fit <- lm(ndf$value ~ ndf$x)
l <- list(
  a = format(as.numeric(coefficients(fit)[2]), digits = 4),
  b = format(as.numeric(abs(coefficients(fit)[1])), digits = 4),
  r2 = format(as.numeric(summary(fit)$r.squared), digits = 4),
  p = format(as.numeric(summary(fit)$coefficients[2, 4]), digits = 4)
)

loginfo("Start to plot")
expr <- substitute(italic(y) == ~a ~ ~italic(x) ~ "+" ~ b ~ "," ~ italic(R)^2 ~ "=" ~ r2 ~ "," ~ italic(P) ~ "=" ~ p, l)
p <- ggplot(ndf, aes(x = x, y = value)) +
  geom_smooth(method = "lm", formula = y ~ x) +
  geom_point() +
  labs(x = opts$xlab,
       y = opts$ylab,
       title = opts$title) +
  theme_bw() +
  theme() +
  geom_text(aes(x = 50, y = 0, label = as.character(as.expression(expr))), parse = TRUE)
ggsave(
  p,
  file = str_c(opts$prefix, "pdf", sep = "."),
  width = 7,
  height = 6
)









