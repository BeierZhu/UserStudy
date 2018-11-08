#coding:utf-8
from Tkinter import *
from PIL import Image
import random as rd
from PIL import ImageTk
import time
import tkMessageBox
import os

class Application(Tk):
    # Application构造函数，master为窗口的父控件
    def __init__(self, master=None, synthesis_path='./data/synthesis'):
        # 初始化Application的Frame部分
        Tk.__init__(self, master)
        self.geometry('1000x600')
        # 显示窗口，并使用grid布局
        self.grid()
        self.columnconfigure(0, weight=18)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=18)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        # 创建控件
        self.createWidgets()
        # 加载数据
        self.img1_idx = None
        self.img2_idx = None

        self.img1 = None
        self.img2 = None

        self.cont_idx = None 
        self.styl_idx = None 

        self.N = 0 # 标注总张数
        self.Nmax = 50 # 总标注个数

        self.synthesis_path = synthesis_path # 合成图片总目录
        self.cont_styl_list = {} # 合成图片列表
        self.loadContStylList()
        self.genPair()
        
        # 输出
        self.result = list()

    def outputresult(self):
        if not os.path.exists('./result'):
            os.mkdir('./result')
        name = time.strftime('./result/%Y%m%d_%H_%M_%S.txt',time.gmtime())
        fout = open(name,'w')
        for item in self.result:
                fout.write(' '.join(map(str,item)))
                fout.write('\n')
        return name

    def loadContStylList(self):
        for root, dirs, _ in os.walk(self.synthesis_path):  
            for dir in dirs:
                dir = os.path.join(root, dir)
                cont_styl_image_list = []
                for _, _, files in os.walk(dir):
                    for file in files:
                        if file == '.DS_Store': # 跳过OS X的.DS_Store文件
                            continue
                        cont_styl_image_list.append(file) 
                self.cont_styl_list[dir] = cont_styl_image_list

    def resizeImg(self, im):
        norm_height = 500.
        width, height = im.size
        width = int((norm_height * width)/height)
        height = int(norm_height)
        im = im.resize((width, height))
        return im
    
    def getContStylIdx(self, cont_styl_pair_path):
        cont_styl_idx = cont_styl_pair_path.split('/')[-1]
        cont_styl_idx = cont_styl_idx.split('_')
        self.cont_idx = cont_styl_idx[0]
        self.styl_idx = cont_styl_idx[1]
    
    def getImgIdx(self, img1_path, img2_path):
        self.img1_idx = img1_path.split('.')[0]
        self.img2_idx = img2_path.split('.')[0]
        
    def genPair(self):
        cont_styl_pair_path = rd.choice(self.cont_styl_list.keys())
        self.getContStylIdx(cont_styl_pair_path)

        image1_path, image2_path = rd.sample(self.cont_styl_list[cont_styl_pair_path], 2)
        self.getImgIdx(image1_path, image2_path)

        image1 = Image.open(os.path.join(cont_styl_pair_path, image1_path))
        image2 = Image.open(os.path.join(cont_styl_pair_path, image2_path))
        image1, image2 = self.resizeImg(image1), self.resizeImg(image2)
        self.img1, self.img2  = ImageTk.PhotoImage(image1), ImageTk.PhotoImage(image2)
        
        self.leftImg.configure(image = self.img1 )
        self.rightImg.configure(image = self.img2 )
        self.leftImg.image = self.img1
        self.rightImg.image = self.img2

        # 状态更新
        if(self.N >= self.Nmax):
            name = self.outputresult()#输出结果
            tkMessageBox.showinfo("Alarm","任务完成！文件存储于%s"%(name))
            self.quit()

        self.N += 1
        self.Timer.configure(text='任务\n %d / %d'%(self.N,self.Nmax))
        print 'Content: ' + self.cont_idx + ' Style: ' + self.styl_idx \
            + ' Img1: ' + self.img1_idx + ' Img2: ' + self.img2_idx


    # 创建控件
    def createWidgets(self):
        # 控件变量
        self.strCont = StringVar()
        self.strStyl = StringVar()
        self.strButton = StringVar()
        self.strButton.set('查看原图')
        self.state = 0
        # 显示图像
        self.leftImg= Label(self, width = 20,height = 20, bg = "White")
        self.leftImg.grid(row=0, column=0, sticky=W+N+S+E, padx=15)
        self.rightImg= Label(self,width = 20, height = 20, bg = "White")
        self.rightImg.grid(row=0, column=2, sticky=W+N+S+E, padx=15)
        self.Timer= Label(self,bg = "White")
        self.Timer.grid(row=0, column=1, sticky=W+N+S+E)
        # 两个 Label 一个按钮
        self.leftLabel = Label(self, bg="White", textvariable=self.strCont)
        self.leftLabel.grid(row=1, column=0, sticky=W+E+S+N,padx=15)
        self.rightLabel = Label(self, bg="White", textvariable=self.strStyl)
        self.rightLabel.grid(row=1, column=2, sticky=W+E+S+N,padx=15)

        self.midBtn = Button(self,textvariable=self.strButton,command=self.CheckOri)
        self.midBtn.bind('<Up>', self.CheckOri)
        self.midBtn.bind('<Left>', self.Left)
        self.midBtn.bind('<Down>', self.Unsure)
        self.midBtn.bind('<Right>', self.Right)
        self.midBtn.focus_set()
        self.midBtn.grid(row=1,column=1,sticky=W+E+S+N,padx=15)

        #三个按钮
        self.btnL = Button(self,text='左图好',command=self.Left)
        # self.btnL.focus_set()
        self.btnL.grid(row=2,column=0,sticky=W+E+S+N,padx=15)
        
        self.btnM = Button(self,text='不确定',command=self.Unsure)
        # self.btnM.focus_set()
        self.btnM.grid(row=2,column=1,sticky=W+E+S+N,padx=2)

        self.btnR = Button(self,text='右图好',command=self.Right)
        # self.btnR.focus_set()
        self.btnR.grid(row=2,column=2,sticky=W+E+S+N,padx=15)
    
    def CheckOri(self, event=None):
        if self.state == 0:
            cont_img_path = './data/origin/content/' + self.cont_idx + '.png'
            styl_img_path = './data/origin/style/' + self.styl_idx + '.png'
            cont_img = Image.open(cont_img_path)
            cont_img = self.resizeImg(cont_img)
            styl_img = Image.open(styl_img_path)
            styl_img = self.resizeImg(styl_img)
            cont_img, styl_img = ImageTk.PhotoImage(cont_img), ImageTk.PhotoImage(styl_img)

            self.leftImg.configure(image = cont_img)
            self.rightImg.configure(image = styl_img)
            self.leftImg.image = cont_img
            self.rightImg.image = styl_img

            self.strCont.set('Content')
            self.strStyl.set('Style')
            self.strButton.set('返回原图')

            self.state = 1
        else:
            self.leftImg.configure(image = self.img1 )
            self.rightImg.configure(image = self.img2 )
            self.leftImg.image = self.img1
            self.rightImg.image = self.img2

            self.strCont.set('')
            self.strStyl.set('')
            self.strButton.set('查看原图')
            self.state = 0 

    def Left(self, event=None):
        print "Choose Left"
        self.result.append([self.cont_idx[2:], self.styl_idx[3:], self.img1_idx, self.img2_idx, 0])
        self.genPair()

    def Right(self, event=None):
        print "Choose Right"
        self.result.append([self.cont_idx[2:], self.styl_idx[3:], self.img1_idx, self.img2_idx, 1])
        self.genPair()

    def Unsure(self, event=None):
        print "Choose Mid"
        self.result.append([self.cont_idx[2:], self.styl_idx[3:], self.img1_idx, self.img2_idx, -1])
        self.genPair()
        
    
# 创建一个Application对象app
app = Application()
# 设置窗口标题为'First Tkinter'
app.title( 'UserStudy UI')
# 主循环开始
app.mainloop()

