#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: Ming
# @Date:   2020-05-24 10:58:40
# @Last Modified by:   Ming
# @Last Modified time: 2020-05-24 15:57:37
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import click
import logging

#### Some Functions ####
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
__version__ = '1.0.0'

sns.set(style='white')
sns.set_palette("Set3")


def get_first_level_pos(df):
    """
    """
    res = {}
    pos = 0
    info_l1 = set()
    info_l2 = set()
    for l1, l2 in df.index.values:
        if l1 not in info_l1 and l2 not in info_l2:
            if len(res) == 0:
                pass
            else:
                pos += 1
            start = pos
            res[l1] = [start, start]
            info_l1.add(l1)
            info_l2.add(l2)
        elif l1 in info_l1 and l2 not in info_l2:
            pos += 1
            end = pos
            res[l1][1] = end
            info_l2.add(l2)
        else:
            pass
    return res


def plot_first_level(axis, position, df):
    """
    """
    offset_y = 0.1
    offset_x = df.max() / 100

    for name, position in position.items():
        x = max(df.loc[name].max(), df.max() / 2)
        axis.plot([x + offset_x, x + offset_x],
                  [position[0] - offset_y, position[1] + offset_y],
                  lw=0.5,
                  color='black')
        axis.text(x + offset_x * 2, np.mean(position), name,
                  horizontalalignment='left',
                  verticalalignment='center')


########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option('-i', '--input',
              required=True,
              type=click.Path(),
              help="The input table two level file to plot")
@click.option('--xname',
              required=True,
              help="The x column name for the plot")
@click.option('--huename',
              default=False,
              show_default=True,
              help="The hue column name for the plot")
@click.option('--hueorder',
              default=None,
              required=False,
              show_default=True,
              help="The order of hue info(sep by ,)")
@click.option('--color',
              default=None,
              required=False,
              show_default=True,
              help="The order of colors(sep by ,)")
@click.option('-p', '--prefix',
              default='./result',
              show_default=True,
              help="The out put preifx")
def cli(input, xname, huename, hueorder, color, prefix):
    """
    Two level plot with matplotlib

    The first two column must be level1 and level2 index
    """
    hue_order = hueorder.strip().split(',') if hueorder else None
    sample_color = color.strip().split(',') if color else None

    logging.info(f'Reading input file {input}...')
    df = pd.read_csv(input, sep='\t', index_col=[0, 1])
    df.sort_index(inplace=True)

    logging.info(f'Start to draw...')
    figure, axis = plt.subplots(figsize=(4, 12))

    if huename:
        sns.barplot(data=df, x=xname, y=[i[1] for i in df.index.values],
                    hue=huename, hue_order=hue_order,
                    palette=sample_color, ax=axis)
    else:
        sns.barplot(data=df, x=xname, y=[i[1] for i in df.index.values],
                    palette=sample_color, ax=axis)

    # first level positon info
    positon_levle1 = get_first_level_pos(df)
    plot_first_level(axis, positon_levle1, df[xname])

    # 边框设置
    axis.spines['right'].set_color("none")
    axis.spines['top'].set_color("none")

    # legend设置
    plt.legend(bbox_to_anchor=(1.05, 0.5), loc=6, borderaxespad=0.)

    plt.savefig(f'{prefix}.svg', bbox_inches='tight')
    plt.savefig(f'{prefix}.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
