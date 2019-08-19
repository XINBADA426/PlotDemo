#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2019-08-19 17:59:18
# @Last Modified by:   Ming
# @Last Modified time: 2019-08-19 21:49:43
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The input table file")
@click.option('--xname',
              required=True,
              help="The x column name for the plot")
@click.option('--yname',
              required=True,
              help="The y column name for the plot")
@click.option('-x', '--xlab',
              required=False,
              help="The xlab for the plot")
@click.option('-y', '--ylab',
              required=False,
              help="The ylab for the plot")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot")
@click.option('-c', '--color',
              required=False,
              default='grey',
              show_default=True,
              help="The scatter color")
@click.option('-p', '--prefix',
              default='result',
              show_default=True,
              help="The out prefix")
def cli(input, xname, yname, xlab, ylab, title, color, prefix):
    """
    Scatter plot with python
    """
    df = pd.read_csv(input, sep='\t')
    x = df[xname]
    y = df[yname]

    # Draw
    figure, axis = plt.subplots(figsize=(8, 8), dpi=300)
    plt.scatter(x, y,
                s=10,
                c=color)

    axis.set_xlabel(xlab, fontsize=15)
    axis.set_ylabel(ylab, fontsize=15)
    axis.set_title(title, fontdict={'size': 22})

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
