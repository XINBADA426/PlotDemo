#!/usr/bin/Rscript
# Title     : TreePlot.R
# Objective : Phylogenetic Tree Plot
# Created by: MingJia
# Created on: 2021/5/10
options(warn = -1)
suppressPackageStartupMessages({
  library(optparse)
  library(ggplot2)
  library(ggtree)
  library(yaml)
  library(stringr)
  library(dplyr)
  library(funr)
  library(logging)
})
basicConfig()

#### Some Functions ####
plot_tree <- function(obj,
                      branch.length = NULL,
                      layout = "circular",
                      tree.size = 2,
                      tiplap.size = 1.5,
                      tiplap.hjust = -.3,
                      ...) {
  p <- ggtree(obj,
              branch.length = branch.length,
              layout = layout,
              size = tree.size) +
    geom_tiplab(hjust = tiplap.hjust,
                size = tiplap.size) +
    geom_treescale(0, 0)
  return(p)
}

add_tippoint <- function(obj.ggplot,
                         color = NULL,
                         size = 1.5,
                         ...) {
  p <- obj.ggplot +
    geom_tippoint(size = size,
                  aes_string(col = color))
  return(p)
}

add_cladeline <- function(obj.ggplot,
                          color = NULL,
                          size = 2,
                          offset = 1,
                          ...) {
  data <- obj.ggplot$data %>%
    as.data.frame() %>%
    filter(isTip == "TRUE")
  p <- obj.ggplot +
    geom_segment(
      data = data,
      size = size,
      aes(
        x = x + offset,
        xend = x + offset,
        y = y,
        yend = y + 1,
        color = data[, color]
      )
    )
  return(p)
}


########################


option_list <- list(
  make_option(c("--tree"),
              type = "character",
              help = "The tree file to plot"),
  make_option(c("--yaml"),
              type = "character",
              help = "The yaml config file for Phylogenetic tree"),
  make_option(c("--annot"),
              type = "character",
              help = "The annot file used to modify the tree"),
  make_option(c("--tippoint"),
              type = "character",
              help = "The column name to regard as tippoint color in annot file"),
  make_option(c("--cladeline"),
              type = "character",
              help = "The column name to regard as cladeline color in annot file"),
  make_option(c("--layout"),
              type = "character",
              help = "The layout for the tree"),
  make_option(c("--fontsize"),
              type = "character",
              help = "The text font size for species name"),
  make_option(c("-p", "--prefix"),
              type = "character",
              default = "result",
              help = "The out prefix[default= %default]"),
  make_option(c("--convert"),
              type = "character",
              default = "/usr/bin/convert",
              help = "The convert program to convert pdf to png[default= %default]")
)
opts <- parse_args(
  OptionParser(
    usage = "%prog[options]",
    option_list = option_list,
    description = "\nScript of Phylogenetic Tree plot"
  ),
  positional_arguments = F
)


#### Some Functions ####
########################
loginfo("Load the yaml file %s", opts$yaml)
if (is.null(opts$yaml)) {
  BIN <- dirname(sys.script())
  opts$yaml <- str_c(BIN, "PhyTree.yml", sep = "/")
}
config <- yaml.load_file(opts$yaml)
if (is.null(config$tree$brach.length)) {
  config$tree$brach.length <- "none"
}
if (!is.null(opts$layout)) {
  config$tree$layout <- opts$layout
}

if (!is.null(opts$fontsize)) {
  config$tiplab$size <- as.double(opts$fontsize)
}

loginfo("Load the tree file %s", opts$tree)
tree <- read.tree(opts$tree)

loginfo("Draw the tree")
p <- plot_tree(
  tree,
  branch.length = config$tree$brach.length,
  layout = config$tree$layout,
  tree.size = config$tree$size,
  tiplap.size = config$tiplab$size,
  tiplap.hjust = config$tiplab$hjust
)

if (!is.null(opts$annot)) {
  loginfo("Load the annotation file %s", opts$annot)
  annot <- read.table(opts$annot,
                      sep = "\t",
                      header = 1,
                      check.names = F)
  p <- p %<+% annot
  if (!is.null(opts$tippoint)) {
    loginfo("Add tip point")
    p <- add_tippoint(p,
                      color = opts$tippoint,
                      size = config$tippoint$size)
  }
  if (!is.null(opts$cladeline)) {
    loginfo("Add clade line")
    p <- add_cladeline(
      p,
      color = opts$cladeline,
      size = config$cladeline$size,
      offset = config$cladeline$offset
    )
  }
}

p <- p + theme_tree()
loginfo("Save the plot")
file_pdf <- str_c(opts$prefix, "pdf", sep = '.')
ggsave(file_pdf, p, limitsize = FALSE)
file_png <- str_c(opts$prefix, "png", sep = '.')
system(str_c(opts$convert, "-density 300 -colorspace RGB", file_pdf, file_png, sep = " "))