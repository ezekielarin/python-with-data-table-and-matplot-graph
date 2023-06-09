import tkinter as tk 
from tkinter import *
from tkinter import ttk

import pandas as pd
import numpy as np
import csv
import math
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.widgets import Cursor




drawdown_count = 0;

buildup_count = 0;
n=0


points = 0

global xpoints 
global ypoints 
xpoints = []
ypoints = []

filedata = []


def handleTabChange(event):
    
    if notebook.select() == notebook.tabs()[-1]:
        
        index = len(notebook.tabs())-1
        frame = tk.Frame(notebook)
        tab_title = "plot "+str(index)
        
        canv = Frame(frame, bg='white', width=1000, height=900, padx=3, pady=3)
        canv.grid(row=1, sticky="nsew")
        
        
        notebook.insert(index, frame, text=tab_title)
        notebook.select(index)
     
        
       # ttk.Label(canv, text ="Draw Down").grid(column = 0, row = 0, padx = 30, pady = 30)
         
        
        return frame;
        

window = tk.Tk()

window.title("Well Testt")
window.geometry("1000x750")



############ Frames for tab 1
top_frame = Frame(window, bg='cyan', width=1080, height=50, pady=3)
center_l1 = Frame(window, bg='grey', width=1080, height=25, padx=3, pady=3)
center = Frame(window, bg='grey', width=1080, height=900, padx=3, pady=3)
btm_frame = Frame(window, bg='white', width=1080, height=45, pady=3)
 

# results = LabelFrame(btm_frame, text="Result")
# results.pack(fill="both", expand="yes", padx="20",pady="10")
# layout all of the main containers
# tab1.grid_rowconfigure(1, weight=1)
# tab1.grid_columnconfigure(0, weight=2)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")


cold = ttk.Button(top_frame, text='Collect Data', command  = lambda: popwin())
#new_button.pack()
cold.grid(column=0, row=1, sticky=tk.W, padx=5, pady=0)


notebook = ttk.Notebook(center)
notebook.bind("<<NotebookTabChanged>>", handleTabChange)
notebook.pack(fill="both", expand=True)

frame = tk.Frame(center)
notebook.add(frame, text="+")


def popwin():
    top = Toplevel(window)
    top.geometry("600x700")
    top.title("Collect Data")

    def addtab(plot_type):
     
        def onclick(event):
          global points
          global x1 
          global x2 
          global y1 
          global y2
          
          
          # print([event.xdata, event.ydata])
          if event.inaxes is not None:
              ax = event.inaxes
              # you now have the axes object for that the user clicked on
              # you can use ax.children() to figure out which img artist is in this
              # axes and extract the data from it   
            #  print(ax)
              xpoints.append(event.xdata)
              ypoints.append(event.ydata)

              event.inaxes.plot(event.xdata, event.ydata, 'o')
             # event.inaxes.axline((xpoints), (ypoints), linewidth=1, color='r')
             # print(xpoints)
              event.inaxes.plot((xpoints), (ypoints))
             
              event.canvas.draw()
              
              
              if points ==0:
                  x1 = event.xdata
                  y1 = event.ydata
                  print("y1: ",y1)
              
              if points==1:
                  x2 = event.xdata
                  y2 = event.ydata
                  print("x2: ",x2)
                  
              points = points + 1
              if points ==2:

                  points = 0
                  m = buildup_m(x1, x2, y1, y2)
                  xpoints.clear()
                  ypoints.clear()
                  skin_val.set(m);
                  
                  

        index = len(notebook.tabs())-1
        frame = tk.Frame(notebook)
        
        tab_title = plot_type+" "+str(index)
        canv = Frame(frame, bg='white', width=1000, height=900, padx=3, pady=3)
        canv.grid(row=1, sticky="nsew")
        
        results = Frame(frame, width=1000, height=200)
        results.grid(row=2, sticky="nw")
        
        skin_val = StringVar(); 
        slope_val = StringVar();
        slope_val = StringVar();
        
        skin = tk.Label(results, text = 'Skin factor:', font=('calibre',10, 'bold'))
        skin.grid(row=0,column=0)
        
        skin = tk.Label(results, textvariable=skin_val, text = 'Skin factor:', font=('calibre',10, 'bold'))
        skin.grid(row=0,column=1)
        
        wellbore = tk.Label(results, text = 'Well bore Storage:', font=('calibre',10, 'bold'))
        wellbore.grid(row=1,column=0)
        
        wellbore = tk.Label(results, textvariable=skin_val,  text = 'Skin factor:', font=('calibre',10, 'bold'))
        wellbore.grid(row=1,column=1)
        
 
        slope = tk.Label(results, text = 'Slope M:', font=('calibre',10, 'bold'))
        slope.grid(row=2,column=0)
        
        slope = tk.Label(results, textvariable=slope_val, font=('calibre',10, 'bold'))
        slope.grid(row=2,column=1)
        
        skin_val.set(0);

        notebook.insert(index, frame, text=tab_title)
        notebook.select(index)
        
        if 'dataframe' in globals():
            
            pass
           
        else:
            tk.messagebox.showinfo(title=None, message="No data Imported")
            return
        
        data = dataframe
        
        #print(data)

        if(plot_type=="drawdown"):

            pi = pi_.get()
            pihr = pihr_.get()
            m =  pi_.get()
            Uo = Uo_.get()
            Bo = Bo_.get()
            ct = ct_.get()
            k = pi_.get()
            rw = rw_.get()
            Qo = Qo_.get()
            Qw = Qw_.get()
            n = n_.get()
            
            print("RW: ", rw)
            
            pi = data['pi'].values[0]
            data['log_time'] = np.log(data.time);
            data['dp'] = data.pressure - pi;
           
            
            if 'dt' not in data:
                data['dt'] = data.time
            
            fig = Figure(figsize = (10, 6), dpi = 100);
            t = data.loc[:,"time"]; 
            log_t = data.loc[:,"log_time"]; 
            dp = data.loc[:,"dp"];
            p = data.loc[:,"pressure"]; 
            

            plot1 = fig.add_subplot(221); 
            plot1.title.set_text('Semi Log Plot');
            plot1.grid(True, which="both")
            plot1.semilogx(t,p)
            plot1.scatter(t,p)
            Cursor(plot1, color='green', linewidth=2)
            
           
            
            plot2 = fig.add_subplot(222);
           # plot2.plot(log_t, p); 
            plot2.scatter(t, p)
            plot2.grid(True, which="both")
            plot2.title.set_text('Cartesian Plot'); 
            
             
            plot3 = fig.add_subplot(223)
            plot3.loglog();
            plot3.scatter(t,dp,);
            plot3.grid(True, which="both")
            plot3.title.set_text('MDH Log log'); #
            Cursor(plot3, color='green', linewidth=2)
            
            canvas = FigureCanvasTkAgg(fig, master = canv);
            fig.canvas.mpl_connect('button_press_event', onclick)
            canvas.draw()
            
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, canv)
            toolbar.update()
           
            canvas.get_tk_widget().pack()
            
        if(plot_type=="buildup"):
              
            
            pi = data['pi'].values[0]
            psi = data['psi'].values[0]
            Ti = data['time'].values[0]
            
            
            
            data['dp'] = data.pressure - psi;
           

            t = data.loc[:,"time"];
            data['log_time'] = np.log(t);
            
            dp = data.loc[:,"dp"]; 
           
            p = data.loc[:,"pressure"]; 
            
            if 'tp' not in data:
                data['tp'] = t;
                
            if 'np' not in data:
                data['dt'] = data.loc[:,"time"];
                
            tp = data.loc[:,"tp"]; 
            data['dt'] = tp-Ti 
            dt = data.loc[:,"dt"];
            logt = data.loc[:,"log_time"];

            tpdt = (tp+dt)/dt;
           


            fig = Figure(figsize = (12, 6), dpi = 100); 
           
            semi_log = fig.add_subplot(221); 
            
            semi_log.title.set_text('Horners plot - Semi Log Plot');
           # semi_log.semilogx(t, p); 
            semi_log.scatter(tpdt,p);  
            semi_log.grid(True, which="both")
            Cursor(semi_log, color='green', linewidth=2)
            
            plot2 = fig.add_subplot(222);
            plot2.loglog(); 
            plot2.scatter(logt, dp); 
            plot2.title.set_text('Log-log Plot'); 
            plot2.grid(True, which="both")

            
            canvas = FigureCanvasTkAgg(fig, master = canv);
            fig.canvas.mpl_connect('button_press_event', onclick)
            canvas.draw()
            
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, canv)
            toolbar.update()
            canvas.get_tk_widget().pack()
        

    def update_row(rows):
       
        global filedata
        trv.delete(*trv.get_children())
        for i in rows:
            trv.insert('','end',values=i)
        pass
    
    
    def import_file():
        global dataframe
        
        
        filetypes = (
            ('csv', '*.csv'),
            ('excel', '*.xlsx'),
           
        )
        
       # filedata.clear()
        filename = fd.askopenfilename(title='Open a file', initialdir='/documents', filetypes=filetypes)
       
        with open(filename) as fl:
         df = csv.reader(fl, delimiter=",")
      #  headers = ['time', 'pressure']
        
         daf = pd.read_csv(filename)
         dataframe = daf
         for i in df:
            filedata.append(i)
        
        update_row(filedata)
        
        pass
   

    t1 = StringVar()
    t2 = StringVar()
    t3 = StringVar()
    
    wrapper1 = LabelFrame(top, text="Data Set")
    wrapper2 = LabelFrame(top, text="Control")
    wrapper3 = LabelFrame(top, text="Result")
    
    wrapper1.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper2.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper3.pack(fill="both", expand="yes", padx="20",pady="10")
    
    
    
    imp = ttk.Button(wrapper2, text='Import file', command  = lambda: import_file())
    #new_button.pack()
    imp.grid(column=0, row=7, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Drawdwon', command  = lambda: addtab("drawdown"))
    #new_button.pack()
    imp.grid(column=1, row=7, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Buildup', command  = lambda: addtab("buildup"))
    #new_button.pack()
    imp.grid(column=2, row=7, sticky=tk.W, padx=5, pady=0)
    
    
    
    name_label = tk.Label(wrapper2, text = 'Uo', font=('calibre',10, 'bold'))
    Uo_ = tk.Entry(wrapper2,textvariable = 'Uo', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=0)
    Uo_.grid(row=1,column=0)
    
    name_label = tk.Label(wrapper2, text = 'Q', font=('calibre',10, 'bold'))
    Q_ = tk.Entry(wrapper2,textvariable = 'Q', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=1)
    Q_.grid(row=1,column=1)
    
    name_label = tk.Label(wrapper2, text = 'ct', font=('calibre',10, 'bold'))
    ct_ = tk.Entry(wrapper2,textvariable = 'ct', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=2)
    ct_.grid(row=1,column=2)
    
    
    
    name_label = tk.Label(wrapper2, text = 'Qo', font=('calibre',10, 'bold'))
    Qo_ = tk.Entry(wrapper2,textvariable = 'Qo', font=('calibre',10,'normal'))
    name_label.grid(row=2,column=0)
    Qo_.grid(row=3,column=0)
    
    name_label = tk.Label(wrapper2, text = 'Qw', font=('calibre',10, 'bold'))
    Qw_ = tk.Entry(wrapper2,textvariable = 'Qw', font=('calibre',10,'normal'))
    name_label.grid(row=2,column=1)
    Qw_.grid(row=3,column=1)
    
    name_label = tk.Label(wrapper2, text = 'Bo', font=('calibre',10, 'bold'))
    Bo_ = tk.Entry(wrapper2,textvariable = 'Bo', font=('calibre',10,'normal'))
    name_label.grid(row=2,column=2)
    Bo_.grid(row=3,column=2)
    
    name_label = tk.Label(wrapper2, text = 'rw', font=('calibre',10, 'bold'))
    rw_ = tk.Entry(wrapper2,textvariable = 'rw_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=0)
    rw_.grid(row=5,column=0)
    
    name_label = tk.Label(wrapper2, text = 'phai', font=('calibre',10, 'bold'))
    phai = tk.Entry(wrapper2,textvariable = 'phai_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=1)
    phai.grid(row=5,column=1)
    
    name_label = tk.Label(wrapper2, text = 'n', font=('calibre',10, 'bold'))
    n = tk.Entry(wrapper2,textvariable = 'n_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=2)
    n.grid(row=5,column=2)
      
    trv = ttk.Treeview(wrapper1, columns=(1,2,3), show="headings", height="8")
    trv.pack()
    
    trv.heading(1, text="time")
    trv.heading(2, text="pressure")
    trv.heading(3, text="DP")
    trv.bind('Double 1', getrow)
    
    pass


def getrow():
    pass



def select_file(graph):
    filetypes = (
        ('csv', '*.csv'),
        ('excel', '*.xlsx'),
       
    )
    global dd_data
 
    filename = fd.askopenfilename(
        title='Open a file', initialdir='/documents', filetypes=filetypes)
    # df = pd.read_csv(filename)
    # headers = ['time', 'pressure']
    
    df = pd.read_excel(filename)
    dd_data = df
   
    global drawdown_count
    global buildup_count
   
    print(drawdown_count)

def calculate_pressure():

    k = 2  #permeability
    t = 2  #time, hour
    s = 3  #skin factor
    
    Qo = 1
    Uo = 1
    ct = 1
    rw = 1
    h = 1;
    pi = 2
    Pwf = pi - ((162.6*Qo*Bo*Uo)/k*h)(log(k*t/O*U*ct*rwˆ2) - 3.23+0.87*s)
    return Pwf
 
def drawdown_k(qo, Bo, Uo, m, h):

    k = (162.6*qo*Bo*Uo)/m*h
    return k

def drawdown_s(pi, pihr, m, U, ct, k, rw, h, phai):
    s = 1.151*((pi-pihr)/m*h - np.log(k/(phai*U*ct*rw)) + 3.23)
    return s

def drawdown_CA(pihr, m, Pint, ml):
    ca = 5.456*(m/ml * np.exp(-Pint/m))
    return ca

def buildup_m(x1, x2, y1, y2):
    m = (y2-y1)/(x2-x1)
    return m


## Build Up
def buildup_k(qo, Bo, Uo, m, h):
    k = (162.6*qo*Bo*Uo)/m*h
    return k

def buildup_tp(Np, Qo):
    tp = (24*Np)/Qo
    return tp

def buildup_s(pi, pihr,phai, h, m, U, ct, k, rw):
    s = 1.151*((pi-pihr)/m*h - np.log(k/(phai*U*ct * np.square(rw))) + 3.23)
    return s


def buildup_CA(Pihr, m, ml, Pint):
    ca = 5.456*(m/ml * np.exp(2.303*(Pihr - Pint)/m))
    return ca

window.mainloop()
