# -*- coding: utf-8 -*-

from math import *

from variabledirection import *

f = lambda t,x,y: 2*t*x**4*(y+3)**3-12*x*x*t*t*(y+3)**3-6*(y+3)*x**4*t*t

phi = lambda x,y: 0

psi1 = lambda t,y: 0
psi2 = lambda t,y: t*t*(y+3)**3
psi3 = lambda t,x: 27*x**4*t*t
psi4 = lambda t,x: 64*x**4*t*t

################################

M = 50
K = 50
N = 1000
t0 = 0
T = 1
x0 = 0
X = 1
y0 = 0
Y = 1

tau=(T-t0)/float(N)
h1=(X-x0)/float(M)
h2=(Y-y0)/float(K)

Min = -0.05
Max = 65.0
    
import sys
from math import log
from PyQt4.Qt import QApplication, QCoreApplication, QString, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel, QSizePolicy, QSpacerItem, SIGNAL, QObject, QProgressBar, QTimer, QImage, QPainter, QScrollArea, QColor, QPushButton, QFileDialog
import threading


class mythread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.Images = []
           
    def run(self):
        
        self.exit = False

        global psi1, psi2, psi3, psi4, M, N, x0, X, y0, Y, t0, T, n, f, phi
        
        global Max, Min        
              
        U0 = []
        
        global K
        
        for k in xrange(K+1):
                U0.append([phi(x0+m*h1,y0+k*h2) for m in xrange(M+1)]) 
        
        #self.MU.append(U0)
        
        img = QImage(M+1,K+1,QImage.Format_RGB32)
        
        c = QColor()
        
        U = U0
            
        for i in xrange(len(U)):
            for j in xrange(len(U[0])):
                c.setHsvF(0.833333333*(1.0-(U[i][j]-Min)/(Max-Min)),1,1)
                img.setPixel(i,j,c.rgb())
        
        self.Images.append(img)
        
        global u,tau
        
        for n in xrange(N+1):
            U = vardir(f, U0, psi1, psi2, psi3, psi4, M, K, N, x0, X, y0, Y, t0, T, n)
            #U=[]
            #for k in xrange(K+1):
            #    U.append([u(t0+n*tau,x0+m*h1,y0+k*h2) for m in xrange(M+1)]) 
            U0 = []
            for k in xrange(K+1):
                U0.append(U[k])
            #self.MU.append(U0)
            
            #print (n/float(N)*100)
            
            img = QImage(M+1,K+1,QImage.Format_RGB32)
            
            c = QColor()
            
            for i in xrange(len(U)):
                for j in xrange(len(U[0])):
                    #print U[i][j] 
                    fl = min(max(0, 0.833333333*(1.0-(U[i][j]-Min)/(Max-Min))), 1)
                    c.setHsvF(fl,1,1)
                    img.setPixel(i,j,c.rgb())
                    
            self.Images.append(img)
            
            self.progr = (int(n/float(N)*100))
            
            if(self.exit):
                break

class Plot(QWidget):
    
    def __init__(self, pbar, *args):
        QWidget.__init__(self, *args)
               
        self.pbar = pbar
            
        global K,M, x0, X, y0, Y
        
        self.mt = mythread()  
        
        self.mt.progr = 0
                
        self.mt.MU = []
        
        self.mt.start()
        
        self.layer = 0
        
        while(len(self.mt.Images) < 1):
            pass
     
        self.image = self.mt.Images[0]
        
        self.repaint()
        
    def Update(self, layer):
        
        if(self.mt.isAlive() and len(self.mt.Images) <= layer):
            layer = len(self.mt.Images)-1
            self.slider.setValue(layer)
        
        self.layer = layer
        
        global t0, tau
                
        self.label.setText('t='+str(t0+layer*tau))
          
        self.image = self.mt.Images[layer]
                
        self.repaint()
        
    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        p.drawImage(0,0,self.image)
        p.end()
        
    def timerEvent(self):
        if(self.mt.isAlive()):
            self.pbar.setValue(self.mt.progr)
        else:
            self.timer.stop()
            self.pbar.setValue(100)

    def onClose(self):
        self.mt.exit = True
        
    def Save(self):
        d = QFileDialog(self)
        s = d.getSaveFileName()
        
        l = len(self.mt.Images)
        
        for i in xrange(l):
            self.mt.Images[i].save(s+'.'+str(i)+'.png')
            
        f = open(s,"w")
        f.write(str(l))
        f.close()
        
    def Open(self):
        d = QFileDialog(self)
        s = d.getOpenFileName()
        
        self.mt.exit = True
        
        f = open(s,"r")
        l = int(f.readline())
        f.close()
        
        self.mt.Images = []
        
        for i in xrange(l):
            self.mt.Images.append(QImage(s+'.'+str(i)+'.png'))

def main(args):
    app = QApplication(args)
    
    w = QWidget()
    
    mainLayout2 = QVBoxLayout()
    
    mainLayout = QHBoxLayout()
    
    mainLayout2.addLayout(mainLayout)
    
    pbar = QProgressBar()
    pbar.setOrientation(2)
    pbar.setValue(0)
    
    p = Plot(pbar)
    
    mainLayout.addWidget(p)

    slider = QSlider(w)
    slider.setMinimum(int(t0*N))
    slider.setMaximum(int(T*N))
    
    p.slider = slider
    
    mainLayout.addWidget(slider)
    
    Layout2 = QVBoxLayout()
    
    Label1 = QLabel('T='+str(T), w)
    Label2 = QLabel('t='+str(t0+slider.value()*tau), w)
    Label2.setFixedWidth(50)
    Label3 = QLabel('t0='+str(t0), w)
    
    Layout2.addWidget(Label1)
    
    Layout2.addItem( QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) )
    
    Layout2.addWidget(Label2)
    
    Layout2.addItem( QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) )
    
    Layout2.addWidget(Label3)
    
    mainLayout.addLayout(Layout2)
    
    image = QImage() 
    
    mainLayout.addWidget(pbar)
    
    p.label = Label2
    
    p.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred));
    
    w.show()
    w.resize(600, 400)
    
    timer = QTimer()
    
    QObject.connect(slider, SIGNAL('valueChanged(int)'), p.Update)
    QObject.connect(timer, SIGNAL('timeout()'), p.timerEvent)
    
    QObject.connect(app, SIGNAL('lastWindowClosed()'), p.onClose)    
    
    timer.start(100)
    
    p.timer = timer
    
    blay= QHBoxLayout()
    
    b1 = QPushButton("Save")
    b2 = QPushButton("Open")
    
    blay.addWidget(b1)
    blay.addWidget(b2)
    
    mainLayout2.addLayout(blay)
    
    w.setLayout(mainLayout2)
    
    QObject.connect(b1, SIGNAL('clicked()'), p.Save)
    QObject.connect(b2, SIGNAL('clicked()'), p.Open)

    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
