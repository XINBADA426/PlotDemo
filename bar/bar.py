#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2019-07-20 19:49:02
# @Last Modified by:   MingJia
# @Last Modified time: 2019-09-20 17:36:31
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
import click

all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)


#### funcs ####
def parse_group(file_in):
    """
    Parse the group info.

    sampleA-1\tgroupA
    sampleA-2\tgroupA
    sampleA-3\tgroupA
    ...
    """
    res = {}
    with open(file_in, 'r') as IN:
        for line in IN:
            arr = line.strip().split('\t')
            res[arr[0]] = arr[1]
    return res


###############


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The input table file")
@click.option('-g', '--group',
              required=False,
              help="The group info of samples")
@click.option('--xname',
              required=True,
              help="The x column name for the plot")
@click.option('--yname',
              required=True,
              help="The y column name for the plot")
@click.option('--huename',
              required=False,
              default=True,
              show_default=None,
              help="The hue column name for the plot")
@click.option('--xorder',
              required=False,
              help="The order of x axis names(sep by ,)")
@click.option('--hueorder',
              default=None,
              required=False,
              show_default=True,
              help="The order of hue info(sep by ,)")
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
def cli(input, group, xname, yname, huename, xorder, hueorder, ylab, title,
        xrotation, color, prefix):
    """
    Bar plot with python.
    """
    df = pd.read_csv(input, sep='\t')
    x = df[xname]
    y = df[yname]
    x_order = xorder.strip().split(',') if xorder else None
    hue_order = hueorder.strip().split(',') if hueorder else None
    color_list = color.strip().split(',') if color else color

    # Sample Draw
    click.echo("Start to draw sample\n...")
    sample_number = len(x)
    sample_color = color_list if color_list else random.choices(
        all_colors, k=sample_number)
    figure, axis = plt.subplots(figsize=(16, 8), dpi=300)
    sns.barplot(data=df, x=xname, y=yname, hue=huename, order=x_order,
                hue_order=hue_order, palette=sample_color, ax=axis)

    axis.set_xticklabels(axis.get_xticklabels(), rotation=xrotation)
    axis.set(xlabel="", ylabel=ylab)
    axis.set_title(title, fontdict={'size': 22})

    plt.savefig(prefix + '.sample.svg', bbox_inches='tight')
    plt.savefig(prefix + '.sample.png', dpi=300, bbox_inches='tight')
    click.echo("End draw sample")

    # Group Draw
    if group:
        click.echo("\nStart to draw group\n...")
        group_info = parse_group(group)
        group_names = list(dict.fromkeys(group_info.values()))
        group_number = len(group_names)
        colors = random.choices(all_colors, k=group_number)
        group_color_info = {i: j for i, j in zip(group_names, colors)}
        group_color = []
        for value in group_info.values():
            group_color.append(group_color_info[value])

        figure, axis = plt.subplots(figsize=(16, 8), dpi=300)
        sns.barplot(x=x, y=y, order=x_order, palette=group_color, ax=axis)

        axis.set_xticklabels(axis.get_xticklabels(), rotation=xrotation)
        axis.set(xlabel="", ylabel=ylab)
        axis.set_title(title, fontdict={'size': 22})

        handlelist = [plt.plot([], marker="s", ls="", color=i)[0]
                      for i in colors]
        plt.legend(handlelist, group_names, bbox_to_anchor=(
            1, 1), loc=2, borderaxespad=0.)

        plt.savefig(prefix + '.group.svg', bbox_inches='tight')
        plt.savefig(prefix + '.group.png', dpi=300, bbox_inches='tight')
        click.echo("End draw group...")


if __name__ == "__main__":
    cli()
