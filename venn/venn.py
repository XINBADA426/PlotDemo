#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chaobo Ren
# @Date:   2023/5/17 15:14
# @Last Modified by:   Ming
# @Last Modified time: 2023/5/17 15:14
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn import venn3
from pathlib import Path
import logging
import click
import sys

logger = logging.getLogger(__file__)
logger.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


#### Some Function
def read_info(f_name):
    """
    Read the input table file

    :param f_name: The input file name
    """
    res = {}
    with open(f_name, 'r') as IN:
        for line in IN:
            arr = line.strip().split("\t")
            res[arr[0]] = set(arr[1].strip().split(','))
    return res


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version="v1.0.0")
@click.option('-i', '--finput',
              required=True,
              type=click.Path(),
              help="The input file")
@click.option('-p', '--prefix',
              default='result',
              help="The out prefix.")
@click.option('--size',
              required=False,
              default="16,8",
              show_default=True,
              help="The figsize of pic")
def main(finput, prefix, size):
    """
    Venn plot for 2 or 3 group venn
    """
    f_in = Path(finput).absolute()
    d_out = Path(prefix).absolute().parent
    d_out.mkdir(exist_ok=True)
    f_stat = f"{prefix}.stat.tsv"

    logger.info(f"Parse the input file: {f_in}")
    info = read_info(f_in)

    logger.info(f"Start to plot")
    pic_size = tuple([int(i) for i in size.strip().split(',')])
    figure, axis = plt.subplots(figsize=pic_size)
    names = list(info.keys())
    if len(info) == 2:
        a = info[names[0]]
        b = info[names[1]]
        v = venn2(subsets=(a, b),
                  set_labels=(names[0], names[1]),
                  set_colors=("red", "blue"),
                  ax=axis)
        res = {"10": [names[0], a - b],
               "01": [names[1], b - a],
               "11": [f"{names[0]}∩{names[1]}", set.intersection(a, b)]}

    elif len(info) == 3:
        a = info[names[0]]
        b = info[names[1]]
        c = info[names[2]]
        v = venn3(subsets=(a, b, c),
                  set_labels=(names[0], names[1], names[2]),
                  set_colors=("red", "blue", "green"),
                  ax=axis)
        res = {"100": [names[0], a - set.union(b, c)],
               "010": [names[1], b - set.union(a, c)],
               "001": [names[2], c - set.union(a, b)],
               "110": [f"{names[0]}∩{names[1]}-{names[2]}", set.intersection(a, b) - c],
               "101": [f"{names[0]}∩{names[2]}-{names[1]}", set.intersection(a, c) - b],
               "011": [f"{names[1]}∩{names[2]}-{names[0]}", set.intersection(b, c) - a],
               "111": [f"{names[0]}∩{names[1]}∩{names[2]}", set.intersection(a, b, c)]}
    else:
        sys.exit(logger.error(f"Only support for 2/3 set venn plot, your set num is {len(info)}"))

    plt.savefig(prefix + '.svg', bbox_inches='tight')
    plt.savefig(prefix + '.png', dpi=300, bbox_inches='tight')
    with open(f_stat, 'w') as OUT:
        for i, j in res.items():
            print(*[i, j[0], len(j[1]), ','.join(j[1])], sep="\t", file=OUT)


if __name__ == "__main__":
    main()
