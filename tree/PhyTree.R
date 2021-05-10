#!/Bio/User/renchaobo/software/miniconda3/envs/R4.0.3/bin/R
# Title     : TODO
# Objective : TODO
# Created by: MingJia
# Created on: 2021/5/10
library(optparse)
library(ggplot2)
library(ggtree)
library(yaml)
library(logging)
basicConfig()

option_list <- list(make_option(c("--tree"),
                                type = "character",
                                help = "The tree file to plot"),
                    make_option(c("--yaml"),
                                type = "character",
                                help = "The yaml config file for Phylogenetic tree"),
                    make_option(c("--annot"),
                                type = "character",
                                help = "The annot file used to modify the tree"),
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
                                description = "\nScript of Phylogenetic Tree plot"),
                   positional_arguments = F)


#### Some Functions ####
########################
loginfo("Load the yaml file %s", opts$yaml)
config <- load(opts$yaml)

loginfo("Load the tree file %s", opts$tree)
tree <- read.tree(opts$tree)

if (!is.null(opts$annot)) {
  loginfo("Load the annotation file %s", opts$annot)
  annot <- read.table(opts$annot,
                      sep = "\t",
                      check.names = F)
}

logginfo("Start to draw")
p <- ggtree(tree, branch.length = 'none', layout = 'circular', size = 0.5) +
  geom_tippoint(size = 1.5) +
  geom_tiplab(hjust = -.3, size = 1.5)








