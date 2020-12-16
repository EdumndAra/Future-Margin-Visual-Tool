# -*- coding: utf-8 -*-
"""
期货对冲价差计算及可视化
Version 1.0.0
Base on:
    akshare:实时数据获取
    bokeh:可视化界面
    pandas:数据框架
Notice：
本文件(main.py)无法直接运行，请使用cmd命令行:
    bokeh serve main.py --show
运行后会自动打开内容网页(http://localhost:5006/main)
或执行run_main.bat文件直接运行
@author: Edumnd
"""
import time
import os
import configparser
import akshare as ak
import pandas as pd
from bokeh.models import TextInput,ColumnDataSource, Button, DataTable, DateFormatter, TableColumn,RadioButtonGroup
from bokeh.layouts import layout
from bokeh.plotting import curdoc, figure,show

#创建默认配置文件
def creat_config():
    config = configparser.ConfigParser()
    config['DEFAULT']={
        'futures1':'IH2012',#期货名称
        'futures2':"IC2012",
        'position1':1,#期货头寸
        'position2':1,
        'cost1':0,#期货持仓成本
        'cost2':0,
        'hedge':0#做多50为0做空为1
        }
    with open('config.ini', 'w') as configfile:#写入文件
        config.write(configfile)

#读取配置
def read_config():
    global futures1,futures2,position1,position2,cost1,cost2,hedge
    try:
        futures1=config['DEFAULT']['futures1']
        futures2=config['DEFAULT']['futures2']
        position1=config['DEFAULT']['position1']
        position2=config['DEFAULT']['position2']
        cost1=config['DEFAULT']['cost1']
        cost2=config['DEFAULT']['cost2']
        hedge=config['DEFAULT']['hedge']
    except:
        creat_config()
        read_config()

#保存配置
def save_config():
    global futures1,futures2,position1,position2,cost1,cost2,hedge
    futures1=text_input_futures1.value
    futures2=text_input_futures2.value
    position1=text_futures_position1.value
    position2=text_futures_position2.value
    cost1=text_cost1.value
    cost2=text_cost2.value
    hedge=radio_button_group1.active
    config['DEFAULT']['futures1']=futures1
    config['DEFAULT']['futures2']=futures2
    config['DEFAULT']['position1']=position1
    config['DEFAULT']['position2']=position2
    config['DEFAULT']['cost1']=cost1
    config['DEFAULT']['cost2']=cost2
    config['DEFAULT']['hedge']=str(hedge)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    #print('config had saved')

#运行按钮回调
callback_id = None
def buttonclick_run():
    #print("click_play")
    global callback_id
    if button_run.label=="运行":
        button_run.label="暂停"
        callback_id = curdoc().add_periodic_callback(time_update, 1000)#定时回调，即获取时间间隔，单位ms
    else:
        button_run.label="运行"
        curdoc().remove_periodic_callback(callback_id)

#清除按钮回调
def buttonclick_clear():
    #print("click_clear")
    source.data = { name : [] for name in ['index','time','futures1','futures2','diff_price','earning'] }
    #print(source.data)

#期货信息更改回调
def text_update(attr, old, new):
    buttonclick_clear()
    save_config()

#盈利更新
def earning_update(attr, old, new):
    save_config()
    position1=int(text_futures_position1.value)*(1-2*radio_button_group1.active)#原active为多0空1，1-2x转化后为多1空-1
    position2=int(text_futures_position2.value)*(1-2*radio_button_group2.active)
    cost1=float(text_cost1.value)
    cost2=float(text_cost2.value)
    data=source.to_df()
    data['earning']=round(position1*(data['futures1']-cost1)+position2*(data['futures2']-cost2),2)
    source.data=data.to_dict()

#多空框回调
def radio_button_change1(attr, old, new):
    radio_button_group2.update(active=1-radio_button_group1.active)
    save_config()
def radio_button_change2(attr, old, new):
    radio_button_group1.update(active=1-radio_button_group2.active)
    save_config()

#获取期货实时价格
def get_futures_price(futures):
    price_data=ak.futures_zh_spot(subscribe_list="nf_"+futures,market="FF",adjust="N")
    futures_price=price_data['current_price'][0]
    return futures_price

#自动更新数据
def time_update():
    now_time=(time.time()+8*60*60)*1000#时区转为北京时间（UTC+8）及秒级时间戳转毫秒级
    futures1=float(get_futures_price(text_input_futures1.value))
    futures2=float(get_futures_price(text_input_futures2.value))
    position1=int(text_futures_position1.value)*(1-2*radio_button_group1.active)#原active为多0空1，1-2x转化后为多1空-1
    position2=int(text_futures_position2.value)*(1-2*radio_button_group2.active)
    cost1=float(text_cost1.value)
    cost2=float(text_cost2.value)
    add_data=pd.DataFrame({'time':now_time,#时间
                           'futures1':futures1,#期货价格
                           'futures2':futures2
                           },index=[0])
    add_data['diff_price']=round(futures1-futures2,2)#价差
    add_data['earning']=round(position1*(futures1-cost1)+position2*(futures2-cost2),2)#盈利
    source.stream(add_data)

#读取配置文件
config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
else:
    creat_config()
    config.read('config.ini')
read_config()

#创建数据源
data = dict(
        time=[],
        futures1=[],
        futures2=[],
        diff_price=[],
        earning=[]
    )
data=pd.DataFrame(data)
source = ColumnDataSource(data)

# 创建控件
#运行按钮
button_run = Button(label="运行", width=60, button_type="primary")
button_run.on_click(buttonclick_run)

#清除按钮
button_clear=Button(label="清空",width=60,button_type="primary")
button_clear.on_click(buttonclick_clear)

#期货品种输入框
text_input_futures1 = TextInput(value=futures1, title="上证50主力合约")
text_input_futures1.on_change("value",text_update)
text_input_futures2 = TextInput(value=futures2, title="中证500主力合约")
text_input_futures2.on_change("value",text_update)

#期货头寸输入框
text_futures_position1=TextInput(value=position1, title="上证50头寸")
text_futures_position1.on_change("value",text_update)
text_futures_position2=TextInput(value=position2, title="中证500头寸")
text_futures_position2.on_change("value",text_update)

#期货成本价输入框
text_cost1=TextInput(value=cost1,title="上证50成本价")
text_cost1.on_change("value",earning_update)
text_cost2=TextInput(value=cost2,title="中证500成本价")
text_cost2.on_change("value",earning_update)

#数据表
columns = [
        TableColumn(field="time", title="时间",formatter=DateFormatter(format="%T")),
        TableColumn(field="futures1", title="上证50"),
        TableColumn(field="futures2", title="中证500"),
        TableColumn(field="diff_price", title="价差"),
        TableColumn(field="earning", title="盈亏")
    ]
data_table = DataTable(source=source,columns=columns)

#多空切换
LABELS = ["多", "空"]
radio_button_group1 = RadioButtonGroup(labels=LABELS, active=int(hedge))
radio_button_group1.on_change('active',radio_button_change1)
radio_button_group2 = RadioButtonGroup(labels=LABELS, active=1-int(hedge))
radio_button_group2.on_change('active',radio_button_change2)

#价差表
diff_price_plot= figure(title="实时价差", x_axis_label='时间', y_axis_label='价格',x_axis_type='datetime')
diff_price_plot.line(x='time',y='diff_price',source=source,legend_label="价差",line_color='black', line_width=2)
#plot.line(x='dates',y='futures1',source=source,legend_label="IH2012",line_color='red')
#plot.line(x='dates',y='futures2',source=source,legend_label="IC2012",line_color='blue')

#盈亏表
earning_plot= figure(title="实时盈亏", x_axis_label='时间', y_axis_label='价格',x_axis_type='datetime')
earning_plot.line(x='time',y='earning',source=source,legend_label="盈利",line_color='black', line_width=2)

# 设计界面
page=layout([
    [button_run,button_clear],
    [radio_button_group1,text_input_futures1,text_futures_position1,text_cost1],
    [radio_button_group2,text_input_futures2,text_futures_position2,text_cost2],
    [data_table,diff_price_plot,earning_plot]
    ])

#设置底层
curdoc().add_root(page)
curdoc().title="价差"
#show(page)#预览排版但是不能交互
