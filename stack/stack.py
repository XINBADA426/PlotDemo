#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2019-10-12 17:01:24
# @Last Modified by:   MingJia
# @Last Modified time: 2019-10-12 18:05:08
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
              help="The table input to plot box")
@click.option('--plot_type',
              default='percent',
              type=click.Choice(['percent', 'count']),
              show_default=True,
              help="The stack plot type")
@click.option('-x', '--xlab',
              required=False,
              help="The xlab for the plot")
@click.option('-y', '--ylab',
              required=False,
              help="The ylab for the plot")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot")
@click.option('--xrotation',
              default=0,
              type=int,
              show_default=True,
              help="The x ticks lable rotation")
@click.option('--color',
              default=None,
              required=False,
              show_default=True,
              help="The order of colors(sep by ,)")
@click.option('-p', '--prefix',
              default='result',
              show_default=True,
              help="The out prefix")
def cli(input, plot_type, xlab, ylab, title, xrotation, color, prefix):
    """
    Stack plot with python.
    """
    df = pd.read_csv(input, sep='\t', index_col=0)
    if plot_type == 'percent':
        df = df / df.sum(axis=0)

    click.echo("Start to draw\n...")
    plt.style.use('seaborn-white')
    row_number, col_number = df.shape
    norm = mpl.colors.Normalize(vmin=0, vmax=row_number)
    all_colors = plt.cm.get_cmap('gist_rainbow')
    c = [all_colors(norm(i)) for i in range(row_number)]
    c = color.strip().split(',') if color else c

    figure, axis = plt.subplots(figsize=(8, 8))

    df.T.plot(kind='bar', stacked=True, ax=axis, color=c, width=0.8)

    if xlab:
        axis.set_xlabel(xlab, fontsize=18)
    if ylab:
        axis.set_ylabel(ylab, fontsize=18)
    if title:
        axis.set_title(title, fontsize=22)

    axis.spines['right'].set_color("none")
    axis.spines['top'].set_color("none")

    handles, labels = axis.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1],
               bbox_to_anchor=(1.05, 0.5), loc=6, borderaxespad=0.)

    plt.savefig(prefix + '.stack.svg', bbox_inches='tight')
    plt.savefig(prefix + '.stack.png', dpi=300, bbox_inches='tight')
    click.echo("End draw sample")


if __name__ == "__main__":
    cli()
