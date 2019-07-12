#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-11 23:57:09
# @Last Modified by:   Ming
# @Last Modified time: 2019-07-12 10:53:46
import matplotlib as mpl

mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot.")
@click.option('-n', '--names',
              required=True,
              help="The names group you want to plot, sep by ,")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
@click.option('-x', '--xlab',
              required=False,
              help="The xlab for the plot")
@click.option('-y', '--ylab',
              required=False,
              help="The ylab for the plot.")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot.")
@click.option('-c', '--colors',
              required=False,
              help="The colors used for plot, html code split by ,")
def cli(input, names, prefix, xlab, ylab, title, colors):
    """
    Density plot with python.
    """
    df = pd.read_csv(input, header=0, names=None, sep='\t')

    names = names.strip().split(',')
    colors = colors.strip().split(',') if colors else None
    if colors and (len(names) != len(colors)):
        raise ValueError('Diff name and color number!')
    # draw
    figure, ax = plt.subplots(figsize=(16, 8), dpi=300)

    for i in range(len(names)):
        if colors:
            color = colors[i]
            ax = sns.kdeplot(df[df.iloc[:, 0] == names[i]].iloc[:, 1],
                             shade=False,
                             color=color, label=names[i], alpha=.7)
        else:
            ax = sns.kdeplot(df[df.iloc[:, 0] == names[i]].iloc[:, 1],
                             shade=False,
                             label=names[i], alpha=.7)

    if xlab:
        ax.set_xlabel(xlab, fontsize=15)
    if ylab:
        ax.set_ylabel(ylab, fontsize=15)
    if title:
        ax.set_title(title, fontsize=22)

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
