# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk,filedialog
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import jieba.analyse as analyse
from scipy.misc import imread
from os import path
from PIL import Image
import random

win=tk.Tk()

win.title("Draw pic")

w=350
h=250
screenwidth = win.winfo_screenwidth()
screenheight = win.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (w, h, (screenwidth-w)/2, (screenheight-h)/2)
win.geometry(alignstr)
win.maxsize(350,250)
win.minsize(350,250)


#获取图片路径
def search_pic():
    picname = filedialog.askopenfilename(title=u"选择背景图片")
    return picname

#获取文本路径
def search_text():
    textname = filedialog.askopenfilename(title=u"选择文字文本")
    return textname


#自选配色方案
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):

    return "hsl(210, 100%%, %d%%)" % random.randint(10, 80)



def done():
    textname=search_text()
    picname=search_pic()

    comment_text = open(textname, 'r').read()
    cut_text = " ".join(jieba.cut(comment_text))
    result = jieba.analyse.textrank(cut_text, topK=1000, withWeight=True)

    keywords = dict()

    for i in result:
        keywords[i[0]] = i[1]


    d = path.dirname(__file__)
    color_mask = imread(picname)

    #词云图片生成参数
    cloud = WordCloud(
    	#如果要使用中文文本，字体必不可少，请将字体与.py文件放到同一文件夹下
        font_path="font.ttf",
        width=400,
        height=300,
        #设置背景色
        background_color='white',
        mask=color_mask,
        #允许最大词汇
        max_words=5000,
        #设置最大的字体
        max_font_size=80,
        random_state=30,
    )
    #获取图片原色配色
    img_color = ImageColorGenerator(color_mask)
    word_cloud = cloud.generate(cut_text)
    #重置配色，color_func可选color_func，img_color。前者使用三原色配色，后者使用图片原色配配色
    cloud.recolor(color_func=color_func)
    #保存生成图片
    word_cloud.to_file("pic.png")
    #生成后打开图片
    #img = Image.open('pic.png')
    #img.show()
Submit = ttk.Button(win, text="选择文本文字", command=done)
Submit.place(x=130, y=94)




win.mainloop()
