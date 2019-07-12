#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-12 16:01:58
# @Last Modified by:   Ming
# @Last Modified time: 2019-07-12 16:01:58
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
              help="The order of x axis names")
@click.option('--hueorder',
              required=False,
              help="The order of hue names.")
@click.option('--huecolors',
              required=False,
              help="The colors for hue infos(sep by ,).")
@click.option('-y', '--ylab',
              required=False,
              help="The ylab for the plot.")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot.")
def cli(input):
    """
    Mix Plot of box plot and rectangle.
    """
    df = pd.read_csv(input, names=None, sep='\t')

    # Draw
    figure, ax = plt.subplots(figsize=(16, 8), dpi=300)


if __name__ == "__main__":
    cli()
