#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2019-10-15 17:41:59
# @Last Modified by:   MingJia
# @Last Modified time: 2019-10-15 20:07:59
import matplotlib as mpl

mpl.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import click


#### Some Functions ####
def format_legend(label, value, allvals, plot_type):
    """
    Get the legent label show the percent.
    """
    if plot_type == 'percent':
        absolute = value / np.sum(allvals) * 100
        return "{}: {:.1f}%".format(label, absolute)
    else:
        return "{}: {}".format(label, value)


########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The input table file")
@click.option('--name',
              required=True,
              help="The column name for Pie plot")
@click.option('--number',
              required=True,
              help="The number column name for the plot")
@click.option('--plot_type',
              default='percent',
              type=click.Choice(['percent', 'count']),
              show_default=True,
              help="The data show type")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot")
@click.option('--reorder',
              default=False,
              type=click.BOOL,
              show_default=True,
              is_flag=True,
              help="Whether reorder the sample by number")
@click.option('--color',
              default=None,
              required=False,
              show_default=True,
              help="The order of colors(sep by ,)")
@click.option('-p', '--prefix',
              default='result',
              show_default=True,
              help="The out prefix")
def cli(input, name, number, plot_type, title, reorder, color, prefix):
    """
    Pie plot with python
    """
    df = pd.read_csv(input, sep='\t', usecols=[name, number])
    if reorder:
        df.sort_values(number, axis=0, ascending=False, inplace=True)
    data = df[number]
    categories = df[name]
    explode = [0.005] * len(data)  # 留白
    labels = pd.Series([format_legend(label, value, data, plot_type)
                        for label, value in zip(categories, data)], name=name)

    # deal color
    # norm = mpl.colors.Normalize(vmin=0, vmax=len(data))
    # all_colors = plt.cm.get_cmap('gist_rainbow')
    # c = [all_colors(norm(i)) for i in range(len(data))]
    c = [plt.cm.Spectral(i / float(len(data) - 1))
         for i in range(len(data))]
    c = color.strip().split(',') if color else c

    # Plot data
    click.echo("Start to draw\n...")
    plt.style.use('seaborn-white')
    fig, axis = plt.subplots(
        figsize=(8, 8), subplot_kw=dict(aspect="equal"), dpi=300)
    wedges, texts = axis.pie(data,
                             colors=c,
                             startangle=180,  # 起始的角度
                             explode=explode)
    axis.legend(wedges, labels, loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))
    axis.set_title(title, fontsize=25)

    # save
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')
    plt.savefig(prefix + '.svg', bbox_inches='tight')

    click.echo("End draw sample")


if __name__ == "__main__":
    cli()
