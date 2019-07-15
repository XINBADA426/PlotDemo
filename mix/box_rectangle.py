#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-12 16:01:58
# @Last Modified by:   Ming
# @Last Modified time: 2019-07-15 21:39:03
from collections import defaultdict

import matplotlib as mpl

mpl.use('Agg')
import pandas as pd
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import seaborn as sns
import click


####
def parse_relation(file_in):
    """

    :param file_in:
    :return:
    """
    res = defaultdict(dict)
    with open(file_in, 'r') as IN:
        for line in IN:
            arr = line.strip().split('\t')
            res[arr[0]][arr[1]] = float(arr[2])
    return res


####


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot box")
@click.option('-r', '--relation',
              required=True,
              type=click.Path(),
              help="The relationshi file.")
@click.option('--xname',
              required=True,
              help="The x column name for the plot.")
@click.option('--yname',
              required=True,
              help="The y column name for the plot.")
@click.option('--huename',
              required=False,
              help="The hue column name for the plot.")
@click.option('--xorder',
              required=False,
              help="The order of x axis names(sep by ,)")
@click.option('--hueorder',
              required=False,
              help="The order of hue names(sep by ,).")
@click.option('--huecolors',
              required=False,
              help="The colors for hue infos(sep by ,).")
@click.option('-y', '--ylab',
              required=False,
              help="The ylab for the plot.")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot.")
@click.option('--pearson',
              default=0.4,
              type=float,
              show_default=True,
              help="The min pearson relationship.")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
def cli(input, relation, xname, yname, huename, xorder, hueorder, huecolors,
        ylab, title, pearson, prefix):
    """
    Mix Plot of box plot and rectangle.

    """
    df = pd.read_csv(input, sep='\t')
    relation_info = parse_relation(relation)

    x_order = xorder.strip().split(',') if xorder else None
    hue_order = hueorder.strip().split(',') if hueorder else None
    hue_color = huecolors.strip().split(',') if huecolors else None

    # Draw
    plt.style.use('ggplot')
    figure, axis = plt.subplots(2, 1, figsize=(10, 6), dpi=300,
                                gridspec_kw={'height_ratios': [3, 1]})
    # 上部盒形图
    sns.boxplot(data=df, x=xname, y=yname, hue=huename, order=x_order,
                hue_order=hue_order, color=hue_color, ax=axis[0])

    if x_order is None:
        x_order = [i.get_text() for i in axis[0].get_xticklabels()]
    # 下部位置关系
    # 在不调整 width 的情况下，盒形图的 bar 宽度之和都为0.5，左右各有0.1的空白
    # 从-0.5开始。
    axis[1].set_xlim(axis[0].get_xlim())
    axis[1].axhline(0.5, lw=1, c='black', zorder=0)
    # 虚线的参数
    style = dict(arrowstyle="Simple,head_width=4,head_length=6",
                 linestyle='--', lw=2, color="r")
    for i in range(len(x_order)):
        gene = x_order[i]
        x, y, width, height = -0.3 + i, 0.4, 0.6, 0.2
        color = 'red' if gene in relation_info else 'blue'
        rect_plot = patches.Rectangle((x, y),
                                      width=width, height=height,
                                      fill=True, color=color)
        axis[1].add_patch(rect_plot)
        if color == 'red':
            for mRNA, pearson_val in relation_info[gene].items():
                if abs(pearson_val) > pearson:
                    end = x_order.index(mRNA)
                    rad = 0.2 if i < end else -0.2
                    arc_plot = patches.FancyArrowPatch((i, 0.4), (end, 0.4),
                                                       connectionstyle=f"arc3,rad={rad}",
                                                       **style)
                    axis[1].add_patch(arc_plot)

    # 杂项
    axis[0].set(xlabel="", ylabel=ylab)
    axis[0].set_title(title, fontdict={'size': 22})
    axis[1].axis('off')

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
