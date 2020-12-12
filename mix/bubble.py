#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2020-11-16 17:22:50
# @Last Modified by:   MingJia
# @Last Modified time: 2020-11-17 15:00:00
import matplotlib as mpl

mpl.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white')
import matplotlib.colors
from matplotlib.lines import Line2D

import logging
import click

#### Some Functions ####
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
__version__ = '1.0.0'

########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option('--up',
              required=True,
              type=click.Path(),
              help="The up info table")
@click.option('--down',
              required=True,
              type=click.Path(),
              help="The down info table")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
def cli(up, down, prefix):
    """
    GDR5616_sup_4
    """
    logging.info(f"Read the input file {up}")
    df_u = pd.read_csv(up, sep="\t")
    df_u["x"] = df_u["Group"].apply(lambda x: 0.25 if x == "PS-NH2" else 0.75)
    df_u["-log10(p value)"] = -np.log10(df_u["p value"])
    logging.info(f"Read the input file {down}")
    df_d = pd.read_csv(down, sep="\t")
    df_d["x"] = df_d["Group"].apply(lambda x: 0.25 if x == "PS-NH2" else 0.75)
    df_d["-log10(p value)"] = -np.log10(df_d["p value"])

    logging.info(f"Plot...")
    figure, axis = plt.subplots(1, 2, figsize=(4, 10))

    # up
    cmap_u = matplotlib.colors.LinearSegmentedColormap.from_list(
        "", ["#F5A6C3", "#ff0066"])
    axis[0].set_xlim([0, 1])
    axis[0].set_ylim([-1, 16])
    im_u = axis[0].scatter('x', "Pathway",
                           data=df_u,
                           s=df_u["count"] * 100,
                           c="-log10(p value)",
                           cmap=cmap_u)
    # figure.colorbar(im_u,ax = axis[0],pad=0.1, orientation="horizontal")
    cbaxes = figure.add_axes([-0.4, 0.08, 0.3, 0.01])
    cb = plt.colorbar(im_u, cax=cbaxes, orientation="horizontal")
    cb.set_label('-log10(p value)')
    cb.outline.set_visible(False)
    axis[0].set_xticks([0.25, 0.75])
    axis[0].set_xticklabels(['PS-NH2', 'PS-COOH'], rotation=45, ha='right')
    axis[0].spines['right'].set_color("none")

    # down
    cmap_d = matplotlib.colors.LinearSegmentedColormap.from_list(
        "", ["#87B5FF", "#0066ff"])
    axis[1].set_xlim([0, 1])
    axis[1].set_ylim([-1, 16])
    im_d = axis[1].scatter('x', "Pathway",
                           data=df_d,
                           s=df_d["count"] * 100,
                           c="-log10(p value)",
                           cmap=cmap_d)
    cbaxes = figure.add_axes([1.1, 0.08, 0.3, 0.01])
    cb = plt.colorbar(im_d, cax=cbaxes, orientation="horizontal")
    cb.outline.set_visible(False)
    cb.set_label('-log10(p value)')
    cb.ax.set_xticklabels([2.0, 4.0])
    axis[1].set_xticks([0.25, 0.75])
    axis[1].set_xticklabels(['PS-NH2', 'PS-COOH'], rotation=45, ha='right')
    axis[1].yaxis.set_ticks_position("right")
    axis[1].spines['left'].set_color("none")
    axis[1].tick_params(axis='both', which='both', length=0)

    plt.subplots_adjust(wspace=0.)

    # legend 处理
    legend_elements = [
        Line2D([0], [0], marker='o', color="w", markerfacecolor='black',
               markersize=10, label='1'),
        Line2D([0], [0], marker='o', color="w", markerfacecolor='black',
               markersize=20, label='5'),
        Line2D([0], [0], marker='o', color="w", markerfacecolor='black',
               markersize=30, label='10')]
    axis[1].legend(handles=legend_elements,
                   title="Count",
                   bbox_to_anchor=(1.9, 1),
                   loc=2,
                   borderaxespad=0.,
                   labelspacing=1.5,
                   frameon=False)

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    cli()
