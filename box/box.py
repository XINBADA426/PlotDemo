#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-12 16:01:58
# @Last Modified by:   Ming
# @Last Modified time: 2019-07-16 00:07:28
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
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
def cli(input, xname, yname, huename, xorder, hueorder, huecolors, ylab, title,
        xrotation, prefix):
    """
    Box plot with python.
    """
    df = pd.read_csv(input, sep='\t')

    x_order = xorder.strip().split(',') if xorder else None
    hue_order = hueorder.strip().split(',') if hueorder else None
    hue_color = huecolors.strip().split(',') if huecolors else None

    # Draw
    figure, axis = plt.subplots(figsize=(16, 8), dpi=300)
    sns.boxplot(data=df, x=xname, y=yname, hue=huename, order=x_order,
                hue_order=hue_order, color=hue_color, ax=axis)

    axis.set_xticklabels(axis.get_xticklabels(), rotation=xrotation)
    axis.set(xlabel="", ylabel=ylab)
    axis.set_title(title, fontdict={'size': 22})

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
