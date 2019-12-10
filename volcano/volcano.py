#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2019-12-10 10:57:08
# @Last Modified by:   MingJia
# @Last Modified time: 2019-12-10 14:46:24
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import click
import math


#### Some Functions #####
def add_annot(info, axis):
    xy = (info['x'], info['y'])
    xytext = (info['xtext'], info['ytext'])
    axis.annotate(info['tag'],
                  xy=xy,
                  xytext=xytext,
                  arrowprops=dict(arrowstyle="->"),
                  horizontalalignment='right',
                  verticalalignment='bottom',
                  clip_on=True)


#########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot volcano")
@click.option('-x', '--xname',
              default="log2(FC)",
              show_default=True,
              help="The log2(FC) column name")
@click.option('-y', '--yname',
              default='FDR',
              show_default=True,
              help="The FDR column name")
@click.option('--hlimit',
              default=0.05,
              type=float,
              show_default=True,
              help="The FDR limit")
@click.option('--vlimit',
              default=1,
              type=float,
              show_default=True,
              help="The log2(FC) limit")
@click.option('--xlab',
              default="log2(FC)",
              show_default=True,
              help="The xlab for the plot")
@click.option('--ylab',
              default="-1*log10(FDR)",
              show_default=True,
              help="The ylab for the plot")
@click.option('-t', '--title',
              default="Volcano Plot",
              show_default=True,
              help="The title for the plot")
@click.option('--annot',
              help="The annot info")
@click.option('-p', '--prefix',
              default='result',
              show_default=True,
              help="The out prefix")
def cli(input, xname, yname, hlimit, vlimit, xlab, ylab, title, annot, prefix):
    """
    Volcano plot with python
    """
    df = pd.read_csv(input, sep='\t')
    x = df[xname]
    y = df[yname].apply(math.log10) * (-1)

    df_red = df[(df[xname] > vlimit) & (df[yname] < hlimit)]
    x_red = df_red[xname]
    y_red = df_red[yname].apply(math.log10) * (-1)
    df_green = df[(df[xname] < -vlimit) & (df[yname] < hlimit)]
    x_green = df_green[xname]
    y_green = df_green[yname].apply(math.log10) * (-1)

    click.echo(click.style("Start to draw\n...", fg='green'))
    figure, axis = plt.subplots(figsize=(9, 8), dpi=300)

    plt.scatter(x, y, s=8, c='grey', alpha=0.8)
    plt.scatter(x_red, y_red, s=8, c='red', alpha=0.8)
    plt.scatter(x_green, y_green, s=8, c='green', alpha=0.8)

    plt.axvline(vlimit, color='grey', alpha=1,
                linewidth=1, linestyle='dashdot')
    plt.axvline(-vlimit, color='grey', alpha=1,
                linewidth=1, linestyle='dashdot')
    plt.axhline(-math.log10(hlimit), color='grey', alpha=1,
                linewidth=1, linestyle='dashdot')

    if annot:
        with open(annot, 'r') as IN:
            for line in IN:
                info = {}
                arr = line.strip().split('\t')
                info['tag'] = arr[0]
                info['x'] = float(arr[1])
                info['y'] = -math.log10(float(arr[2]))
                info['xtext'] = float(arr[3])
                info['ytext'] = float(arr[4])
                add_annot(info, axis)

    axis.set_xlabel(xlab, fontsize=15)
    axis.set_ylabel(ylab, fontsize=15)
    axis.set_title(title, fontdict={'size': 22})

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')
    click.echo(click.style("End draw ...", fg='green'))


if __name__ == "__main__":
    cli()
