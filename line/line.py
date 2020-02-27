#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2020-02-26 16:38:07
# @Last Modified by:   MingJia
# @Last Modified time: 2020-02-27 10:30:07
import matplotlib as mpl

mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot.")
@click.option('-x', '--xname',
              required=True,
              help="The column name of x axis")
@click.option('-y', '--yname',
              required=True,
              help="The column name of y axis")
@click.option('--hue',
              required=False,
              help="The column name of hue")
@click.option('--order',
              required=False,
              help="The x name order for plot")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
@click.option('--xlab',
              required=False,
              help="The xlab name for the plot")
@click.option('--ylab',
              required=False,
              help="The ylab name for the plot.")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot.")
@click.option('-c', '--colors',
              required=False,
              help="The colors used for plot, html code split by ,")
@click.option('--size',
              required=False,
              default="16,8",
              show_default=True,
              help="The figsize of pic")
def cli(input, xname, yname, hue, order, prefix, xlab, ylab, title, colors,
        size):
    """
    Line plot with python
    """
    df = pd.read_csv(input, dtype={xname: str}, header=0, names=None, sep='\t')

    if order:
        dfs = [df[df[xname] == i] for i in order.strip().split(',')]
        df = pd.concat(dfs, ignore_index=True)

    if colors:
        hue_values = []
        colors = colors.strip().split(',')
        color_palette = {}
        for i, j in df.groupby(hue):
            hue_values.append(i)
        for i in range(len(hue_values)):
            color_palette[hue_values[i]] = colors[i % len(colors)]
    else:
        color_palette = None

    # draw
    figure, ax = plt.subplots(
        figsize=([float(i) for i in size.strip().split(',')]), dpi=300)

    sns.lineplot(data=df, x=xname, y=yname, hue=hue, palette=color_palette,
                 lw=1, markers=True, sort=False, ax=ax)

    if xlab:
        ax.set_xlabel(xlab, fontsize=15)
    if ylab:
        ax.set_ylabel(ylab, fontsize=15)
    if title:
        ax.set_title(title, fontsize=22)

    plt.legend(bbox_to_anchor=(1.05, 0.5), loc=6, borderaxespad=0.)

    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
