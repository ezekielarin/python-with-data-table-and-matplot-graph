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
p1 = 0
pihr = 0

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
window.geometry("900x700")

skin_factor = StringVar(); 
drawdown_slope = StringVar();
shape_factor = StringVar();
wellbore = StringVar();


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
        
        global skin_factor
        global drawdown_slope
        global welbore
        global shape_factor
        global drawdown_intercept
        global pskin
        
        global cartesian_slope
        global cartesian_intercept
        
        global loglog_slope
        global loglog_intercept
        
        
        U = float(U_.get())
        Bo = float(Bo_.get())
        ct = float(ct_.get())
        h = float(h_.get())
        rw = float(rw_.get())
        Qo = float(Qo_.get())

        n = float(n_.get())

        phai = float(phai_.get())
        
        
        
        def onclick(plot_type):
            pass
        


        index = len(notebook.tabs())-1
        frame = tk.Frame(notebook)
        
        tab_title = plot_type+" "+str(index)
        canv = Frame(frame, bg='white', width=1000, height=900, padx=3, pady=3)
        canv.grid(row=1, sticky="nsew")
        
        results = Frame(frame, width=1000, height=200)
        results.grid(row=2, sticky="nw")
        
        skin_val = StringVar(); 
        slope_val = StringVar();
        shape_val = StringVar();
        wellbore_val = StringVar();
        
        skin = tk.Label(results, text = 'Skin factor:', font=('calibre',10, 'bold'))
        skin.grid(row=0,column=0)
        
        skin = tk.Label(results, textvariable=skin_val, text = 'Skin factor:', font=('calibre',10, 'bold'))
        skin.grid(row=0,column=1)
        
        wellbore = tk.Label(results, text = 'Well bore Storage:', font=('calibre',10, 'bold'))
        wellbore.grid(row=1,column=0)
        
        wellbore = tk.Label(results, textvariable=wellbore_val,  text = 'Skin factor:', font=('calibre',10, 'bold'))
        wellbore.grid(row=1,column=1)
        
 
        slope = tk.Label(results, text = 'Slope M:', font=('calibre',10, 'bold'))
        slope.grid(row=2,column=0)
        
        slope = tk.Label(results, textvariable=slope_val, font=('calibre',10, 'bold'))
        slope.grid(row=2,column=1)
        
        shape_factor= tk.Label(results, text = 'Shape factor:', font=('calibre',10, 'bold'))
        shape_factor.grid(row=3,column=0)
        
        shape_factor = tk.Label(results, textvariable=shape_val, font=('calibre',10, 'bold'))
        shape_factor.grid(row=3,column=1)
        
        
        imp = ttk.Button(results, text='WellBore Storage', command  = lambda: wellbore_popup())
        #new_button.pack()
        imp.grid(column=2, row=8, sticky=tk.W, padx=5, pady=0)
        
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

            pi = data['pressure'].values[0]
            data['log_time'] = np.log(data.time);
            data['dp'] = pi - data.pressure ;
            
            
           
            
            if 'dt' not in data:
                data['dt'] = data.time
            
            fig = Figure(figsize = (10, 6), dpi = 100)
            t = data.loc[:,"time"]
            log_t = data.loc[:,"log_time"]
            dp = data.loc[:,"dp"]
            p = data.loc[:,"pressure"]
            # print(dp)
            

            plot1 = fig.add_subplot(221); 
            plot1.title.set_text('Semi Log Plot');
            plot1.grid(True, which="both")
            plot1.semilogx(t,p)
            plot1.scatter(t,p)
            
            slope, intercept =  calculate_slope(t, p)
            pihr = round(intercept, 4)
           # slope = (slope, 4)
            
            #trendline_data = plot_trendline(plot1, t, slope, intercept)
           
            k = drawdown_k(Qo, Bo, U, slope, h)
            print("k:", k)
            drawdown_slope = (slope, 4);
            skin_factor = drawdown_s(pi, intercept, slope, U, ct, k, rw, h, phai);
            welbore = (slope, 4); 
            shape_factor = (slope, 4);
            drawdown_intercept = intercept
            welbore = wellbore_c(Qo, Bo, dp)
            
            
            
           
            
            plot2 = fig.add_subplot(222);
            # plot2.plot(log_t, p); 
            plot2.scatter(t, p)
            plot2.grid(True, which="both")
            plot2.title.set_text('Cartesian Plot'); 
            
            slope, intercept =  calculate_slope(t, p)
            cartesian_slope = slope
            cartesian_intercept = intercept
            
            
             
            plot3 = fig.add_subplot(223)
            plot3.loglog();
            plot3.scatter(t,dp,);
            plot3.grid(True, which="both")
            plot3.title.set_text('MDH Log log'); #
            
            slope, intercept =  calculate_slope(t, dp)
            loglog_slope = slope
            loglog_intercept = intercept
           
            ca = drawdown_CA(pihr, slope, pi, loglog_slope)
            
 
    
            canvas = FigureCanvasTkAgg(fig, master = canv);
            fig.canvas.mpl_connect('button_press_event', onclick)
            canvas.draw()
            
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, canv)
            toolbar.update()
           
            canvas.get_tk_widget().pack()
            drawdown_results()
            
        if(plot_type=="buildup"):
              
            
            pi = data['pressure'].values[0]
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
    wrapper2 = LabelFrame(top, text="Data parameters")
    wrapper3 = LabelFrame(top, text="Well Perimeter")
    
    wrapper1.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper2.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper3.pack(fill="both", expand="yes", padx="20",pady="10")
    
    
    
    imp = ttk.Button(wrapper2, text='Import file', command  = lambda: import_file())
    #new_button.pack()
    imp.grid(column=0, row=8, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Drawdwon', command  = lambda: addtab("drawdown"))
    #new_button.pack()
    imp.grid(column=1, row=8, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Buildup', command  = lambda: addtab("buildup"))
    #new_button.pack()
    imp.grid(column=2, row=8, sticky=tk.W, padx=5, pady=0)
    
    
    
    name_label = tk.Label(wrapper2, text = 'µ', font=('calibre',10, 'bold'))
    U_ = tk.Entry(wrapper2,textvariable = 'U_', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=0)
    U_.grid(row=1,column=0)
    
    name_label = tk.Label(wrapper2, text = 'Bo', font=('calibre',10, 'bold'))
    Bo_ = tk.Entry(wrapper2,textvariable = 'b_', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=1)
    Bo_.grid(row=1,column=1)
    
   
    
    name_label = tk.Label(wrapper2, text = 'ct', font=('calibre',10, 'bold'))
    ct_ = tk.Entry(wrapper2,textvariable = 'ct_', font=('calibre',10,'normal'))
    name_label.grid(row=0,column=2)
    ct_.grid(row=1,column=2)
    
    
    
    name_label = tk.Label(wrapper2, text = 'Qo', font=('calibre',10, 'bold'))
    Qo_ = tk.Entry(wrapper2,textvariable = 'Qo', font=('calibre',10,'normal'))
    name_label.grid(row=2,column=0)
    Qo_.grid(row=3,column=0)
    
    
    name_label = tk.Label(wrapper2, text = 'h', font=('calibre',10, 'bold'))
    h_ = tk.Entry(wrapper2,textvariable = 'h_', font=('calibre',10,'normal'))
    name_label.grid(row=2,column=1)
    h_.grid(row=3,column=1)
 
    
   
    name_label = tk.Label(wrapper2, text = 'rw', font=('calibre',10, 'bold'))
    rw_ = tk.Entry(wrapper2,textvariable = 'rw_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=0)
    rw_.grid(row=5,column=0)
    
    name_label = tk.Label(wrapper2, text = 'Porosity ɸ', font=('calibre',10, 'bold'))
    phai_ = tk.Entry(wrapper2,textvariable = 'phai_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=1)
    phai_.grid(row=5,column=1)
    
    name_label = tk.Label(wrapper2, text = 'n', font=('calibre',10, 'bold'))
    n_ = tk.Entry(wrapper2,textvariable = 'n_', font=('calibre',10,'normal'))
    name_label.grid(row=4,column=2)
    n_.grid(row=5,column=2)
    
   

    
    #///oil well parameters
    
   # aa = tk.Label(wrapper3, text = 'Aa', font=('calibre',10, 'bold'))
    #Aa_ = tk.Entry(wrapper3,textvariable = 'Aa_', font=('calibre',10,'normal'))
    #aa.grid(row=0,column=0)
    #Aa_.grid(row=1,column=0)
    
    #odt = tk.Label(wrapper3, text = 'ODt', font=('calibre',10, 'bold'))
   # ODt_ = tk.Entry(wrapper3,textvariable = 'ODt_', font=('calibre',10,'normal'))
   # odt.grid(row=0,column=1)
   # ODt_.grid(row=1,column=1)
    
   # odt = tk.Label(wrapper3, text = 'IDc', font=('calibre',10, 'bold'))
    #IDc_ = tk.Entry(wrapper3,textvariable = 'IDc_', font=('calibre',10,'normal'))
   # odt.grid(row=0,column=2)
    #IDc_.grid(row=1,column=2)
    
   # Vwb = tk.Label(wrapper3, text = 'Vwb', font=('calibre',10, 'bold'))
   # Vwb_ = tk.Entry(wrapper3,textvariable = 'Vwb_', font=('calibre',10,'normal'))
   # Vwb.grid(row=2,column=0)
    #Vwb_.grid(row=3,column=0)
    
    #Cwb = tk.Label(wrapper3, text = 'Cwb', font=('calibre',10, 'bold'))
    #Cwb_ = tk.Entry(wrapper3,textvariable = 'Cwb_', font=('calibre',10,'normal'))
    #Cwb.grid(row=2,column=1)
    #Cwb_.grid(row=3,column=1)
    
   # odt = tk.Label(wrapper3, text = 'IDc', font=('calibre',10, 'bold'))
    #IDc_ = tk.Entry(wrapper3,textvariable = 'IDc_', font=('calibre',10,'normal'))
   # odt.grid(row=2,column=2)
   # IDc_.grid(row=3,column=2)
    
      
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

def clear_plots():
    
    pass

def drawdown_results():
    win = Toplevel(window)
    win.geometry("300x400")
    win.title("Results")
    
    #print("shape:", drawdown_slope)
    
    
    skin = tk.Label(win, text = 'Semi log parameters', font=('calibre',10, 'bold'))
    skin.grid(row=0,column=0)
    
    skin = tk.Label(win, text = 'Skin factor:', font=('calibre',10, 'bold'))
    skin.grid(row=1,column=0)
    
    skin = tk.Label(win,  text = skin_factor, font=('calibre',10, 'bold'))
    skin.grid(row=1,column=1)
    
    wellbore = tk.Label(win, text = 'Well bore Storage:', font=('calibre',10, 'bold'))
    wellbore.grid(row=2,column=0)
    
    wellbore = tk.Label(win,  text = welbore, font=('calibre',10, 'bold'))
    wellbore.grid(row=2,column=1)
    

    slope = tk.Label(win, text = 'Slope M:', font=('calibre',10, 'bold'))
    slope.grid(row=3,column=0)
    
    slope = tk.Label(win, text=drawdown_slope, font=('calibre',10, 'bold'))
    slope.grid(row=3,column=1)
    
    slope = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    slope.grid(row=4,column=0)
    
    slope = tk.Label(win, text=drawdown_intercept, font=('calibre',10, 'bold'))
    slope.grid(row=4,column=1)
    
    shape_factor= tk.Label(win, text = 'Shape factor:', font=('calibre',10, 'bold'))
    shape_factor.grid(row=5,column=0)
    
    shape_factor= tk.Label(win, text = shape_factor, font=('calibre',10, 'bold'))
    shape_factor.grid(row=5,column=1)
    
    
    #Cartesian
    skin = tk.Label(win, text = 'Catesian Plot', font=('calibre',10, 'bold'))
    skin.grid(row=6,column=0)
    
    
    skin = tk.Label(win, text = 'Slope', font=('calibre',10, 'bold'))
    skin.grid(row=7,column=0)
    
    skin = tk.Label(win,  text = cartesian_slope, font=('calibre',10, 'bold'))
    skin.grid(row=7,column=1)
    
    wellbore = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    wellbore.grid(row=8,column=0)
    
    wellbore = tk.Label(win,  text = cartesian_intercept, font=('calibre',10, 'bold'))
    wellbore.grid(row=8,column=1)
    
    
    #Cartesian
    skin = tk.Label(win, text = 'Log-log Plot', font=('calibre',10, 'bold'))
    skin.grid(row=9,column=0)
    
    
    skin = tk.Label(win, text = 'Slope', font=('calibre',10, 'bold'))
    skin.grid(row=10,column=0)
    
    skin = tk.Label(win,  text = loglog_slope, font=('calibre',10, 'bold'))
    skin.grid(row=10,column=1)
    
    wellbore = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    wellbore.grid(row=11,column=0)
    
    wellbore = tk.Label(win,  text = loglog_intercept, font=('calibre',10, 'bold'))
    wellbore.grid(row=11,column=1)

    
def buildup_results():
    win = Toplevel(window)
    win.geometry("300x400")
    win.title("Results")
    
    #print("shape:", drawdown_slope)
    
    
    skin = tk.Label(win, text = 'Semi log parameters', font=('calibre',10, 'bold'))
    skin.grid(row=0,column=0)
    
    skin = tk.Label(win, text = 'Skin factor:', font=('calibre',10, 'bold'))
    skin.grid(row=1,column=0)
    
    skin = tk.Label(win,  text = skin_factor, font=('calibre',10, 'bold'))
    skin.grid(row=1,column=1)
    
    wellbore = tk.Label(win, text = 'Well bore Storage:', font=('calibre',10, 'bold'))
    wellbore.grid(row=2,column=0)
    
    wellbore = tk.Label(win,  text = welbore, font=('calibre',10, 'bold'))
    wellbore.grid(row=2,column=1)
    

    slope = tk.Label(win, text = 'Slope M:', font=('calibre',10, 'bold'))
    slope.grid(row=3,column=0)
    
    slope = tk.Label(win, text=drawdown_slope, font=('calibre',10, 'bold'))
    slope.grid(row=3,column=1)
    
    slope = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    slope.grid(row=4,column=0)
    
    slope = tk.Label(win, text=drawdown_intercept, font=('calibre',10, 'bold'))
    slope.grid(row=4,column=1)
    
    shape_factor= tk.Label(win, text = 'Shape factor:', font=('calibre',10, 'bold'))
    shape_factor.grid(row=5,column=0)
    
    shape_factor= tk.Label(win, text = shape_factor, font=('calibre',10, 'bold'))
    shape_factor.grid(row=5,column=1)
    
    
    #Cartesian
    skin = tk.Label(win, text = 'Catesian Plot', font=('calibre',10, 'bold'))
    skin.grid(row=6,column=0)
    
    
    skin = tk.Label(win, text = 'Slope', font=('calibre',10, 'bold'))
    skin.grid(row=7,column=0)
    
    skin = tk.Label(win,  text = drawdown_slope, font=('calibre',10, 'bold'))
    skin.grid(row=7,column=1)
    
    wellbore = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    wellbore.grid(row=8,column=0)
    
    wellbore = tk.Label(win,  text = welbore, font=('calibre',10, 'bold'))
    wellbore.grid(row=8,column=1)
    
    
    #Cartesian
    skin = tk.Label(win, text = 'Log-log Plot', font=('calibre',10, 'bold'))
    skin.grid(row=9,column=0)
    
    
    skin = tk.Label(win, text = 'Slope', font=('calibre',10, 'bold'))
    skin.grid(row=10,column=0)
    
    skin = tk.Label(win,  text = drawdown_slope, font=('calibre',10, 'bold'))
    skin.grid(row=10,column=1)
    
    wellbore = tk.Label(win, text = 'Intercept:', font=('calibre',10, 'bold'))
    wellbore.grid(row=11,column=0)
    
    wellbore = tk.Label(win,  text = welbore, font=('calibre',10, 'bold'))
    wellbore.grid(row=11,column=1)
    
    
   
    

def calculate_slope(time_data, pressure_data):
   # log_time_data = np.log10(time_data)
    slope, intercept = np.polyfit(time_data, pressure_data, 1)
    return slope, intercept


def plot_trendline(ax, time_data, slope, intercept):
    log_time_data = time_data#np.log10(time_data)
    trendline_data = 10 ** (log_time_data * slope + intercept)
    ax.plot(time_data, trendline_data, '--', label="Trendline")
    return trendline_data
 
def drawdown_k(Qo, Bo, Uo, m, h):

    k = (162.6*Qo*Bo*Uo)/abs(m)*h
    print("k",k)
    return round(k,4)

def drawdown_s(pi, pihr, m, U, ct, k, rw, h, phai):
   
    s = 1.151*((pi-pihr)/m*h - np.log(k/(phai*U*ct*rw)) + 3.23)
 
    return round(s,4)

def drawdown_CA(pihr, m, Pint, ml):
    print("phir",pihr)
    print("m",m)
    print("pint",Pint)
    print("ml",ml)
    ca = 5.456*(abs(m)/abs(ml) * np.exp(Pint/abs(m)))
   # print(ca)
    return round(ca,4)

def drawdown_m(pwf, pihr, t):
    m = (pwf - pihr)/np.log(t)
    return round(m,4)


def buildup_m(x1, x2, y1, y2):
    m = (y2-y1)/(x2-x1)
    return round(m,4)


## Build Up
def buildup_k(qo, Bo, Uo, m, h):
    k = (162.6*qo*Bo*Uo)/abs(m)*h
    return round(k,4)

def buildup_tp(Np, Qo):
    tp = (24*Np)/Qo
    return round(tp, 4)

def buildup_s(pi, pihr, phai, h, m, U, ct, k, rw):
    s = 1.151*((pi-pihr)/m*h - np.log(k/(phai*U*ct * np.square(rw))) + 3.23)
    return round(s,4)


def buildup_CA(Pihr, m, ml, Pint):
    ca = 5.456*(m/ml * np.exp(2.303*(Pihr - Pint)/m))
    return round(ca,4)

def wellbore_c(Qo, Bo, dp):
    c = (Qo*Bo*107)/(24 * 903)
    return round(c,4)

def cfl(IDc, ODt, den):
    Aa = 3.143*(np.square(IDc) - np.square(ODt)) / 4*(144)
    c = 144*Aa/5.615* den
    return round(c,4)

def cfe(Vwb, Cwb):
    c = Vwb * Cwb;

    return round(c, 4)

window.mainloop()
