#!/Bio/User/renchaobo/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: MingJia
# @Date:   2021-02-02 10:56:25
# @Last Modified by:   MingJia
# @Last Modified time: 2021-02-02 16:15:59
import matplotlib as mpl

mpl.use('Agg')
# import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import xml.etree.ElementTree as ET
import numpy as np
import logging
import click

#### Some Functions ####
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
__version__ = '1.0.0'


def get_total_number(file_rnk):
    """
    Get the total gene number
    """
    res = 0
    with open(file_rnk, 'r') as IN:
        for line in IN:
            res += 1
    return res


def get_target(file_target):
    """
    Get the target info
    """
    res = []
    with open(file_target, 'r') as IN:
        for line in IN:
            res.append(line.strip())
    return res


def parse_edb(file_edb, total):
    """
    Parse the edb file
    """
    res = {}
    root = ET.parse(file_edb).getroot()
    for child in root:
        name = child.attrib["GENESET"].strip().split("#")[1]
        es = np.array([0, *child.attrib["ES_PROFILE"].split(), 0], dtype=float)
        index = np.array(
            [1, *child.attrib["HIT_INDICES"].split(), total], dtype=int)
        res[name] = [index, es]
    return res


def es_plot(axis, x, y, color="green"):
    """
    ES value line plot
    """
    axis.plot(x, y, c=color)


def gene_plot(axis, data, xlim, color="black"):
    """
    Gene position plot
    """
    for i in data[1:-1]:
        axis.axvline(x=i, c=color)
    axis.spines['left'].set_color("none")
    axis.spines['right'].set_color("none")
    axis.spines['top'].set_color("none")
    axis.spines['bottom'].set_color("none")
    axis.axes.xaxis.set_visible(False)
    axis.axes.yaxis.set_visible(False)
    axis.set_xlim([0, xlim])


########################


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option("--edb",
              required=True,
              type=click.Path(),
              help="The GSEA edb file")
@click.option("--rnk",
              required=True,
              type=click.Path(),
              help="The GSEA rnk file")
@click.option("-t", "--target",
              required=True,
              type=click.Path(),
              help="The gene sets you want to plot")
@click.option("-p", "--prefix",
              default="./result",
              show_default=True,
              help="The out put prefix")
def cli(edb, rnk, target, prefix):
    """
    GSEA multi plot
    """
    logging.info("Get the basic info")
    total_gene_num = get_total_number(rnk)
    logging.info(f"Total Gene number: {total_gene_num}")
    target = get_target(target)
    total_target_num = len(target)
    logging.info(f"Choose Gene Set number: {total_target_num}")
    info = parse_edb(edb, total_gene_num)

    logging.info("Start to plot")
    norm = mpl.colors.Normalize(vmin=0, vmax=total_target_num)
    all_colors = plt.cm.get_cmap('rainbow')
    colors = [all_colors(norm(i)) for i in range(total_target_num)]
    figure, axis = plt.subplots(total_target_num + 1, 1,
                                figsize=(10, 6 + total_target_num),
                                gridspec_kw={'height_ratios': [6] + [
                                    0.6] * total_target_num})
    legend_elements = []
    flag = 1
    for tg in target:
        name = tg
        if tg not in info:
            logging.warning(f"{name} not in the file {edb}")
        index = info[tg][0]
        es = info[tg][1]
        es_plot(axis[0], index, es, color=colors[flag - 1])
        gene_plot(axis[flag], index, total_gene_num, color=colors[flag - 1])
        legend_elements.append(Line2D([0], [0],
                                      color=colors[flag - 1],
                                      markerfacecolor=colors[flag - 1],
                                      markersize=10,
                                      label=name))
        flag += 1

    axis[0].set_title("GSEA", fontsize=22)
    axis[0].set_ylabel("Enrichment Score", fontsize=20)
    axis[0].set_xlim([0, total_gene_num])
    axis[0].axhline(y=0, c="grey")
    axis[0].spines['right'].set_color("none")
    axis[0].spines['top'].set_color("none")
    axis[0].spines['bottom'].set_color("none")
    axis[0].axes.xaxis.set_visible(False)

    ncol = total_target_num // 10 + 1 if total_target_num % 10 else total_target_num // 10

    axis[0].legend(handles=legend_elements,
                   bbox_to_anchor=(1, 1),
                   loc="upper left",
                   frameon=False,
                   ncol=ncol,
                   borderaxespad=0.)

    plt.subplots_adjust(left=0.125, bottom=0.1,
                        right=0.9, top=0.9,
                        wspace=0.2, hspace=0)
    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')
    logging.info("Finish")


if __name__ == "__main__":
    cli()
