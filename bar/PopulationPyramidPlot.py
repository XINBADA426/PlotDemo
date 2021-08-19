#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2020-09-17 09:24:56
# @Last Modified by:   MingJia
# @Last Modified time: 2020-09-17 14:22:00
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import click
import re

#### Some Functions ####
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
__version__ = '1.0.0'


def change_bar_width(ax, new_value):
    for patch in ax.patches:
        current_height = patch.get_height()
        diff = current_height - new_value

        # we change the bar heigth
        patch.set_height(new_value)

        # we recenter the bar
        patch.set_y(patch.get_y() + diff * .5)


########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The table input to plot population pyramid")
@click.option('-ic', '--indexcolumn',
              default=0,
              show_default=True,
              type=int,
              help="The index column number for the plot")
@click.option('-lc', '--leftcolumn',
              default=1,
              show_default=True,
              type=int,
              help="The left column number for the plot")
@click.option('-rc', '--rightcolumn',
              default=2,
              show_default=True,
              type=int,
              help="The right column number for the plot")
@click.option('--color',
              default="red,green",
              show_default=True,
              help="The left and right color for plot")
@click.option('-p', '--prefix',
              default='result',
              show_default=True,
              help="The out prefix")
def cli(input, indexcolumn, leftcolumn, color, rightcolumn, prefix):
    """
    Populaation Pyramid Plot with python
    """
    logging.info(f"Parse the input file {input}...")
    df = pd.read_csv(input, sep='\t')
    index = df.iloc[:, indexcolumn]
    logging.info(f"Index column name {index.name}")
    left = df.iloc[:, leftcolumn]
    max_l = max(left)
    logging.info(f"Index column name {left.name}")
    right = df.iloc[:, rightcolumn]
    max_r = max(right)
    logging.info(f"Index column name {right.name}")

    logging.info("Start to draw...")
    new_df = pd.DataFrame({index.name: index,
                           left.name: -left,
                           right.name: right})
    colors = color.strip().split(',')
    plt.rc('ytick', labelsize=12)
    figure, axis = plt.subplots(figsize=(10, 6), dpi=300)
    sns.barplot(x=left.name,
                y=index.name,
                data=new_df,
                color=colors[1],
                label=left.name,
                ax=axis)
    sns.barplot(x=right.name,
                y=index.name,
                data=new_df,
                color=colors[0],
                label=right.name,
                ax=axis)
    change_bar_width(axis, .5)
    # add text
    categories = axis.get_yticks()
    for i in range(len(categories)):
        lx = -left[i]
        rx = right[i]
        axis.text(lx, i, f'{-lx}',
                  ha='right', va='center',
                  size=8,
                  color='black')
        axis.text(rx, i, f'{rx}',
                  ha='left', va='center',
                  size=8,
                  color='black')

    # set x limit
    max_value = max(max_l, max_r)
    axis.set_xlim([-max_value, max_value])

    # hide tick line
    axis.tick_params(axis='y', length=0, pad=20)

    # set x tick lable
    plt.draw()  # When you call plt.draw() the tick labels are populated
    locs, labels = plt.xticks()
    for i in labels:
        new_label = re.findall('\\d+.*', i.get_text())[0]
        i.set_text(new_label)
    axis.set_xticks(locs)
    axis.set_xticklabels(labels)

    axis.set_xlabel("")
    axis.set_ylabel("")

    axis.spines['left'].set_color("none")
    axis.spines['right'].set_color("none")
    axis.spines['top'].set_color("none")

    plt.legend(bbox_to_anchor=(1, 1),
               frameon=False,
               loc=2)

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', bbox_inches='tight')
    logging.info("Finish")


if __name__ == "__main__":
    cli()
