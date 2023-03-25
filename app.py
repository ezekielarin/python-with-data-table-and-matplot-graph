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


drawdown_count = 0;

buildup_count = 0;
n=0

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
     
        
        ttk.Label(canv, text ="Draw Down").grid(column = 0, row = 0, padx = 30, pady = 30)
         
        
        return frame;
        

window = tk.Tk()

window.title("Well Testt")
window.geometry("1000x750")



############ Frames for tab 1
top_frame = Frame(window, bg='cyan', width=1080, height=50, pady=3)
center_l1 = Frame(window, bg='grey', width=1080, height=25, padx=3, pady=3)
center = Frame(window, bg='grey', width=1080, height=900, padx=3, pady=3)
btm_frame = Frame(window, bg='white', width=1080, height=45, pady=3)
 

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
    wrapper2 = LabelFrame(top, text="Pressure")
    wrapper3 = LabelFrame(top, text="DT")
    
    wrapper1.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper2.pack(fill="both", expand="yes", padx="20",pady="10")
    wrapper3.pack(fill="both", expand="yes", padx="20",pady="10")
    
    imp = ttk.Button(wrapper2, text='Import file', command  = lambda: import_file())
    #new_button.pack()
    imp.grid(column=0, row=1, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Drawdwon', command  = lambda: addtab("drawdown"))
    #new_button.pack()
    imp.grid(column=1, row=1, sticky=tk.W, padx=5, pady=0)
    
    imp = ttk.Button(wrapper2, text='Plot Buildup', command  = lambda: addtab("buildup"))
    #new_button.pack()
    imp.grid(column=2, row=1, sticky=tk.W, padx=5, pady=0)
    
    trv = ttk.Treeview(wrapper1, columns=(1,2,3), show="headings", height="20")
    trv.pack()
    
    trv.heading(1, text="time")
    trv.heading(2, text="pressure")
    trv.heading(3, text="DP")
    trv.bind('Double 1', getrow)

    pass

def addtab(plot_type):
    import numpy as np
    
    index = len(notebook.tabs())-1
    frame = tk.Frame(notebook)
    
    tab_title = plot_type+" "+str(index)
    canv = Frame(frame, bg='white', width=1000, height=900, padx=3, pady=3)
    canv.grid(row=1, sticky="nsew")
    
    notebook.insert(index, frame, text=tab_title)
    notebook.select(index)
    
    data = dataframe
    #print(data)
    
    if(plot_type=="drawdown"):
        
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
        
        canvas = FigureCanvasTkAgg(fig, master = canv);
        canvas.draw()
        
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, canv)
        toolbar.update()
        canvas.get_tk_widget().pack()
        
    if(plot_type=="buildup"):
        Qo = 1
        Uo = 1
        ct = 1
        rw = 1
        h = 1;
        np=1
        

        pi = data['pi'].values[0]
        psi = data['psi'].values[0]
        Ti = data['time'].values[0]
        
        
        
        data['dp'] = data.pressure - psi;
       

        t = data.loc[:,"time"];
        data['log_time'] = t;
        
        dp = data.loc[:,"dp"]; 
       
        p = data.loc[:,"pressure"]; 
        
        if 'tp' not in data:
            data['tp'] = t;
            
        if 'np' not in data:
            data['dt'] = data.loc[:,"time"];
            
        tp = data.loc[:,"tp"]; 
        data['dt'] = tp-Ti 
        dt = data.loc[:,"dt"];

        tpdt = (tp+dt)/dt;
       


        fig = Figure(figsize = (12, 6), dpi = 100); 
       
        semi_log = fig.add_subplot(221); 
        
        semi_log.title.set_text('Horners plot - Semi Log Plot');
       # semi_log.semilogx(t, p); 
        semi_log.scatter(tpdt,p);  
        semi_log.grid(True, which="both")
        
        plot2 = fig.add_subplot(222);
        plot2.loglog(); 
        plot2.scatter(t,dp); 
        plot2.title.set_text('Log-log Plot'); 
        plot2.grid(True, which="both")
        canvas = FigureCanvasTkAgg(fig, master = canv);
        canvas.draw()
        
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, canv)
        toolbar.update()
        canvas.get_tk_widget().pack()
    
   
    
    
	

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
    #df = pd.read_csv(filename)
  #  headers = ['time', 'pressure']
    
    df = pd.read_excel(filename)
    dd_data = df
   
    global drawdown_count
    global buildup_count
    print(drawdown_count)

 
 
#plot graph with this function
def abline(slope, intercept, graph):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')
    

window.mainloop()
