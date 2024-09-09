#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-12 16:01:58
# @Last Modified by:   MingJia
# @Last Modified time: 2019-10-16 10:54:17
import logging
import matplotlib as mpl

mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import click

logger = logging.getLogger(__file__)
logger.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot box")
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
@click.option('--xrotation',
              default=0,
              type=int,
              show_default=True,
              help="The x ticks lable rotation.")
@click.option('--showfliers',
              default=False,
              type=click.BOOL,
              show_default=True,
              help="Whether show the fliers")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
@click.option('--width',
              default=8,
              show_default=True,
              type=float,
              help="The width of the plot.")
@click.option('--height',
              default=6,
              show_default=True,
              type=float,
              help="The height of the plot.")
def cli(input, xname, yname, huename, xorder, hueorder, huecolors, ylab, title,
        xrotation, showfliers, prefix, width, height):
    """
    Box plot with python.
    """
    logger.info(f"Input: {input}")
    df = pd.read_csv(input, sep='\t')

    x_order = xorder.strip().split(',') if xorder else None
    hue_order = hueorder.strip().split(',') if hueorder else None
    hue_color = huecolors.strip().split(',') if huecolors else None

    # Draw
    logger.info("Start to draw the box plot.")
    if not huecolors:
        sns.set_palette("Set1")
    figure, axis = plt.subplots(figsize=(width, height))
    sns.boxplot(data=df, x=xname, y=yname, hue=huename, order=x_order,
                showfliers=showfliers, hue_order=hue_order, color=hue_color,
                width=0.6, ax=axis)

    # 去除图例边框
    handles, labels = axis.get_legend_handles_labels()  # 获取图例句柄和标签（如果需要的话）
    legend = axis.legend(handles, labels,
                         frameon=False,
                         loc='center left',
                         bbox_to_anchor=(1, 0.5),
                         borderaxespad=0.)  # 创建一个新的图例并关闭边界框

    if hasattr(axis, 'legend_') and axis.legend_ is not None:
        axis.legend_.set_title('')

    # 隐藏上面和右面的边框
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)

    axis.set_xticks(axis.get_xticks())
    axis.set_xticklabels(axis.get_xticklabels(), rotation=xrotation)
    axis.set(xlabel="", ylabel=ylab)
    axis.set_title(title, fontdict={'size': 22})

    plt.savefig(prefix + '.pdf', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
