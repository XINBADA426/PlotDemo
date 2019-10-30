# 一些绘图时常用的功能

## 主题
```python
# 查看所有可用主题
plt.style.available

# 主题设置
plt.style.use('seaborn-white')
```

## Title设置 
```python
axis.set_title(title, fontsize=25)
```    

## 颜色的选取
```python
# 从colormap `Spectral`中选择颜色
c = [plt.cm.Spectral(i / float(len(data) - 1)) for i in range(len(data))]
```

## 去除边框
```python
axis.spines['right'].set_color("none")
axis.spines['top'].set_color("none")
```
