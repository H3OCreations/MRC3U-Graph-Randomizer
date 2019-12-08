import os, csv, math, random, collections, fileinput, shutil, sys
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog  



class MainMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.top_frame = tk.Frame(self, bg='cyan', width=250, height=50, pady=3)
        self.center_frame = tk.Frame(self, bg='gray2', width=50, height=40, padx=3, pady=3)
        self.bottom_frame = tk.Frame(self, bg='white', width=250, height=45, pady=3)

        self.top_frame.grid(row = 1, sticky = "ew")
        self.center_frame.grid(row = 2, sticky = "nsew")
        self.bottom_frame.grid(row = 3, sticky = "nsew")

        title = tk.Label(self.top_frame, text = "Welcome")
        title.pack()

        initButton = tk.Button(self.center_frame, text = "Create Assessments", width = 15, pady = 10)
        initButton.bind("<Button-1>", self.initialize)
        initButton.pack()
           
        exitButton = tk.Button(self.bottom_frame, text = "Exit", width = 15)
        exitButton.bind("<Button-1>", self.exitWindow)
        exitButton.pack(side = "right")

    def exitWindow(self, event):
        self.withdraw()
        self.destroy()

    def initialize(self, event):
        '''
        Initializes directories by creating file structures the program will use 
        for the program itself
        '''
                    
        # Set up the student data and format the directories for student Data
        tk.messagebox.showinfo("Alert", "Select the TeachAssist Classlist")  
        classListPath = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select Class list", filetypes = (("CSV files", "*.csv"),("TXT files", "*.txt"), ("All files", "*.*")))
        
        # formatting for section path name
        delim1 = (classListPath[::-1]).index("/")
        delim2 = len(classListPath) - classListPath.index("_")
        className = classListPath[-delim1:-delim2]
        classDirectory = className
         
        try:
            os.mkdir(classDirectory)
            tk.messagebox.showinfo("Done", "Initialization Complete!")    
                            
        except FileExistsError:
            tk.messagebox.showinfo("Alert", "This unit has already been created.  To reinitialize a unit, you must delete the %s class folder" %(className))

            
        

    
    

if __name__ == "__main__":
    root = MainMenu()
    winWidth = "300"
    winLength = "250"
    root.geometry('{}x{}'.format(winWidth, winLength))
    root.title("Main Menu")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()