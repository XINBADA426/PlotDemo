# Plot Demos

> 一些绘图的脚本，今后不再局限于用那种语言了~

## Line Plot

![Line Plot](line/line.png)

```bash
python line.py -i line.data -x Time -y Value --hue Deal --size 8,6 --order 5,4,3,2,1,0 --colors red,green -p line
```

[脚本路径](line/line.py)

### 线性拟合图

![lm.png](line%2Flm.png)

```bash
Rscript lm.R --table lm.data
```

[脚本路径](line%2Flm.R)

## Scatter Plot

![Scatter Plot](scatter/scatter.png)

```bash
python scatter -i scatter.data --xname RNA_log2FC --yname Meth_diff -x Log2FC -y 'abs(meth.diff)' -p scatter
```

[脚本路径](scatter/scatter.py)

[数据路径1](scatter/scatter.data)

## Bar Plot

![Bar Plot](bar/result.sample.png)

```bash
python bar.py -i bar.data -g group.txt --xname Sample --yname Number -y Number

# With Hue
python bar.py -i bar_hue.data --xname region --yname number --huename 'type' --hueorder hyper,hypo --color red,green
```

[脚本路径](bar/bar.py)

[数据路径1](bar/bar.data)

[数据路径2](bar/group.txt)

### Two Levle Bar plot

![Two Level Plot](bar/two_level.png)

```bash
python two_level.py -i two_level.data --xname Number --huename Group -p two_level
```

[脚本路径](bar/two_level.py)

[数据路径1](bar/two_level.data)

### Population Pyramid Plot

![Population Pyramid Plot](bar/PopulationPyramidPlot.png)

```bash
python /Bio/User/renchaobo/Scripts/PopulationPyramidPlot.py -i PopulationPyramidPlot.data -ic 0 -lc 1 -rc 2 -p PopulationPyramidPlot 
```

## Box Plot

![Box Plot](box/box.png)

```bash
python box.py -i box.data --xname Gene --yname Exp --huename Group --xrotation 90 -p box
```

[脚本路径](box/box.py)

[数据路径](box/box.data)

![box_ggpubr](box/box_ggpubr.png)

```bash
box_ggpubr.R -f box_ggpubr.data --compare box_ggpubr.compare -p box_ggpubr
```

## Pie Plot

![Pie Plot](pie/pie.png)

```bash
python pie.py -i pie.data --name Name --number Number --plot_type percent -t "Pie Plot" -p pie
```

[脚本路径](pie/pie.py)

[数据路径](pie/pie.data)

## Violin Plot

![Violin Plot](violin/violin.png)

```bash
python violin.py -i violin.data --xname Sample --yname Exp -p violin
```

[脚本路径](violin/violin.py)

[数据路径](violin/violin.data)

## Density Plot

![Density Plot](density/density.png)

```bash
python density.py -i density.data -n mRNA,lncRNA -p density -y Density -x "Median log10(FPKM)" -t "Density Plot" -c "black,red"
```

[脚本路径](density/density.py)

[数据路径](density/density.data)

## Stack Plot

![Stack Plot](stack/stack.stack.png)

```bash
python stack.py -i stack.data -x Sample -y Percent -t "Stack Plot" -p stack
```

[脚本路径](stack/stack.py)

[数据路径](stack/stack.data)

## volcano plot

![Volcano Plot](volcano/volcano.png)

```bash
python volcano.py -i volcano.data -p volcano
# 加入tag
python volcano.py -i volcano.data --annot tag.txt -p volcano.tag
# R语言的方案
/Bio/User/renchaobo/software/miniconda3/envs/R3.6.1/bin/Rscript tag_volcano.r -f volcano.data 
```

[脚本路径](volcano/volcano.py)

[数据路径](volcano/volcano.data)

[数据路径](volcano/tag.txt)

## Mix Plot

多种类型图片的混合

### box_rectangle Plot

![box_rectangle.svg](mix/box_rectangle.png)

```bash
python box_rectangle.py -i box_rectangle.data -r box_rectangle.pearson --xname Gene --yname Exp --huename Group --xorder TCONS_00009919,TCONS_00009928,TCONS_00009929,TEA028107.1 -p box_rectangle
```

[脚本路径](mix/box_rectangle.py)

[数据路径1](mix/box_rectangle.data)

[数据路径2](mix/box_rectangle.pearson)

### buble plot

![bubble.png](mix/bubble.png)

```bash
python bubble.py --up bubble_UP.tsv --down bubble_DOWN.tsv -p bubble
```

[脚本路径](mix/bubble.py)

[数据路径1](mix/bubble_UP.tsv)

[数据路径2](mix/bubble_DOWN.tsv)

### Heatmap

![heatmap.png](heatmap/result.heatmap.png)

```bash
Rscript heatmap.r -f heatmap.data --cluster_row --cluster_col --group group.tsv --feature feature.tsv -c "#2F70AD,#FFFFFF,#BA2831"
```

### GSEA multi plot

![GSEA multi plot](mix/gsea_multi_plot.png)

```shell
python gsea_multi_plot.py --edb gsea_multi_plot.edb --rnk gsea_multi_plot.rnk -t gsea_multi_plot.list
```

### tree

![Tree plot](tree/PhyTree.png)

```shell
PhyTree.R
```

### Venn

两组或三组数据的venn图分析，圈的大小不同
![Venn plot](venn/venn.png)

```shell
python venn.py -i venn.data -p venn
```
