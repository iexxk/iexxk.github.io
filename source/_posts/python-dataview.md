---
title: python-dataview
date: 2020-09-24 11:46:46
updated: 2020-09-24 17:44:18
categories: python
tags: [python]
---

# python数据可视化

Pandas支持的[可视化后端](https://pandas.pydata.org/pandas-docs/dev/ecosystem.html#visualization):matplotlib、bokeh、plotly等

## Pandas-matplotlib

老版绘图工具，不支持交互，但是资料较多，支持图表多，pandas的默认绘图后端

```python
import matplotlib.pyplot as plt
x = [0, 1]
y = [0, 1]
plt.figure()
plt.plot(x, y)
plt.savefig("test.jpg")
plt.show()
#--pandas使用--
df = pd.DataFrame(result)
df.plot()
plt.show()
```

## [Pandas-Bokeh](https://github.com/PatrikHlobil/Pandas-Bokeh)



## Pandas-plotly



## Pandas-[hvplot](https://hvplot.holoviz.org/)

hvPlot提供了基于HoloViews和Bokeh的高级绘图API



## Pyecharts

[pyecharts](https://github.com/pyecharts)/**[pyecharts](https://github.com/pyecharts/pyecharts)**

支持交互，基于Echarts，运行后会生成个html在项目目录，要在浏览器打开就可以看到图标了

```python
import pyecharts.options as opts
from pyecharts.charts import Line
    x = [0, 1]
    y = [0, 1]
    line = (
        Line()
        .add_xaxis(x)
        .add_yaxis("y", y)
    )
    line.render()
```

## 

#### 参考

[09-选择适合你的Python可视化工具](https://www.pythonf.cn/read/36686)



