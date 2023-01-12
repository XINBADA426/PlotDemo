#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chaobo Ren
# @Date:   2023/1/9 10:44
# @Last Modified by:   Ming
# @Last Modified time: 2023/1/9 10:44
import logging

import click
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo

# from pyecharts.globals import ThemeType

logger = logging.getLogger(__file__)
logger.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version="v1.0.0")
@click.option('--data',
              required=True,
              type=click.Path(),
              help="The input data file")
@click.option('--pcolor',
              default="grey",
              show_default=True,
              help="The province region color")
@click.option('--ccolor',
              default="black",
              show_default=True,
              help="The city point color")
@click.option('--pfx',
              default="cn_map",
              show_default=True,
              type=click.Path(),
              help="The The prefix for the output")
def main(data, pcolor, ccolor, pfx):
    """
    中国地图绘制

    金博那边中国疾控的需求
    """
    logger.info("Read the input data")
    df = pd.read_csv(data, sep="\t")
    logger.info("Start to draw")
    # 省份信息
    opts_province = [opts.GeoRegionsOpts(name=i,
                                         is_selected=False,
                                         itemstyle_opts=opts.ItemStyleOpts(area_color=pcolor,
                                                                           opacity=0.5)) for i in df["省"]]
    # 地级市位点标注
    cn_geo = Geo(init_opts=opts.InitOpts(width="1800px",
                                         height="1000px",
                                         renderer="svg"))
    cn_geo.add_schema(maptype="china",
                      regions_opts=opts_province,
                      label_opts=opts.LabelOpts(is_show=False),
                      itemstyle_opts=opts.ItemStyleOpts(color="white"))
    for i in zip(df["City"], df["X"], df["Y"]):
        cn_geo.add_coordinate(i[0], i[1], i[2])
    data_city = [[i, int(j)] for i, j in zip(df["City"], df["Data"])]
    cn_geo.add(series_name="",
               data_pair=data_city,
               is_selected=False,
               symbol_size=8,
               color=ccolor,
               label_opts=opts.LabelOpts(is_show=True,
                                         position="bottom",
                                         font_family="Arial",
                                         font_weight="bold",
                                         formatter='{b}'))
    # 隐藏图例
    cn_geo.set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                           )

    # 输出
    cn_geo.render(f"{pfx}.html")


if __name__ == "__main__":
    main()
