#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-11 23:57:09
# @Last Modified by:   Ming
# @Last Modified time: 2019-07-11 23:57:09
import matplotlib as mpl

mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot.")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
@click.option('-t', '--title',
              required=False,
              help="The title for the plot.")
@click.option('-c', '--color',
              required=False,
              help="The colors used for plot, html code split by \,")
def cli(input, prefix, title, color):
    """
    """
    df = pd.read_table(input, header=T)


if __name__ == "__main__":
    cli()
