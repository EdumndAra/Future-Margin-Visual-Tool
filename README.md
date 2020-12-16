# Future-Margin-Visual-Tool
该工具为本人在量化私募实习时独立编写的小工具，用于实时显示对冲期货价差。<br>
This tool is a small tool that I wrote independently during an internship in a quant PE to display the margin of hedging futures.<br>


项目要求
--
1.实时显示两对冲期货价格，并可视化价差。<br>
2.可以选择对冲期货的品种和持仓量，显示总持仓的价值<br>

Project requirement
--
1.Real-time display futures' price & margin.<br>
2.Can put in futures contract & spot, showing the value of the portfolio.<br>

技术栈
--
语言：Python（3.7）<br>
数据处理：Pandas、NumPy <br>
可视化：Bokeh <br>
数据获取：AkShare <br>

Technology Stack
--
Language: Python（3.7）<br>
Data Processing: Pandas NumPy <br>
Data Visualization: Bokeh <br>
Futures Data Capturing: AkShare <br>

项目文件
--
`main.py` 主文件 <br>
`run_main.bat` 启动文件 <br>

The project file
--
`main.py`: main code file <br>
`run_main.bat`: run to start the project <br>

如何运行该项目
--
由于本项目使用Bokeh进行可视化，结果将以网页方式显示。需要安装Python3.7以上版本并安装所需库（推荐安装Anaconda），运行方式如下：<br>
方法一.运行`run_main.bat`<br>
方法二.用`cmd`于`main.py`所在目录运行如下代码：<br>
  
   
    bokeh serve main.py --show
按照默认设置，结果将输出于http://localhost:5006/main <br>

Run this project
--
Because this porject is based on Bokeh ,result will be showed by web page.Needing Python(version>=3.7) with required framework(recommended Anaconda).The operation mode is as follows. <br>
Mode 1: run`run_main.bat`<br>
Mode 2: use`cmd` to run this code in `main.py`'s directory:<br>
  
   
    bokeh serve main.py --show
In default set,the result will show in http://localhost:5006/main <br>
