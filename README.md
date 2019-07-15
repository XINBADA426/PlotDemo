# Plot Demos
> 一些使用 Python 绘图的脚本

## Bar Plot

## Density Plot
![Density Plot](density/density.png)

```python
python density.py -i density.data -n mRNA,lncRNA -p density -y Density -x "Median log10(FPKM)" -t "Density Plot" -c "black,red"
```

[脚本路径](density/density.py)

[数据路径](density/density.data)

## Mix Plot
多种类型图片的混合
### box_rectangle
![box_rectangle.svg](mix/box_rectangle.png)
```python
python box_rectangle.py -i box_rectangle.data -r box_rectangle.pearson --xname Gene --yname Exp --huename Group --xorder TCONS_00009919,TCONS_00009928,TCONS_00009929,TEA028107.1 -p box_rectangle
```

[脚本路径](mix/box_rectangle.py)

[数据路径1](mix/box_rectangle.data)

[数据路径2](mix/box_rectangle.pearson)


