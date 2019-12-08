from pylab import *
import random, math, os, shutil

class Function_Sketcher:
    def __init__(self, studentName):
        # Randomly generates the values and randomely makes them negative
        # This gurentees that the values are never zero
        constants = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
        for i in range(len(constants)):
            if random.randint(0, 101)  % 2 == 0:
                constants[i] = -1* constants[i]

        # Setting up the constants and cooefficients in a more workable variable name
        self.a = constants[0]
        self.k = constants[1]   # Turn out K is optional, but this is possibly for future programs
        self.c = constants[2]
        self.d = constants[3]

        self.question_num = studentName[-1]

        # to be determined by csv file
        self.studentName = studentName

        function_list = ["quadratic", "exponential", "sine", "cosine"]
        self.function_name = function_list[random.randint(0, 3)]
        #self.function_name = "sine"
        self.generate_function()
        
    def quadratic(self, x):
        return self.a*(x - self.c)**2 + self.d
    
    def exponential(self, x):
        return self.a*2**(x-self.c) + self.d

    def generate_function(self):
        # Setting up the string character for the translation variable
        if self.c < 0:
            c_char = "+" + str(-self.c)
        else:
            c_char = "-" + str(self.c)
        if self.d < 0:
            d_char = "+" + str(-self.d)
        else:
            d_char = "-" + str(self.d)

        if self.function_name not in ("sine", "cosine"):
            # Values of x must shift according to horizontal translation
            # We're aiming to have a spread of 3 data points in each direction
            x_min = -3 + self.c
            x_max = 3 + self.c
            self.X = np.linspace(x_min, x_max)
            
            if self.function_name == "quadratic":
                self.Y = self.quadratic(self.X)
                self.equation = str(self.a) + "(x" + c_char + ")^2" + d_char

            elif self.function_name == "exponential":
                self.Y = self.exponential(self.X)
                self.equation = str(self.a) + "(2^{(x" + c_char + ")})" + d_char
        
        #Generate sine and cosine functions 
        else:
            # Shift in radians
            self.c = np.pi/self.c
            x_min = -2*pi + self.c
            x_max = 2*np.pi + self.c
            self.X = np.linspace(x_min, x_max)
            # This makes it look like the shift is in degrees
            c_char = c_char[0] + str((180/np.pi) *abs(self.c))
            
            if self.function_name == "sine":
                self.Y = self.a *np.sin(self.X - self.c) + self.d
                self.equation = str(self.a) + "sin(x" + c_char + ")" + d_char
            elif self.function_name == "cosine":
                self.Y = self.a *np.sin(self.X - self.c) + self.d
                self.equation = str(self.a) + "cos(x" + c_char + ")" + d_char

        # This may be redundant as it was fixed in the graph generation
        # However, it gurentees the program works
        x_axis = []
        y_axis = []

        if self.function_name not in ("sine", "cosine"):
            for i in range(x_min, x_max + 1):
                x_axis.append(i)

            # populate y-axis ticks  
            y_max = int(max(self.Y))
            y_min = int(min(self.X))

            for i in range(y_min - 10, y_max + 10, 5):
                y_axis.append(i)
        
        # Constructing Axis for sine and cosine graph
        else:
            for i in range(-3, 4):
                x_axis.append(i*2*np.pi/3 )

            for i in range(-1*self.a - self.d, 1*self.a + self.d + 1):
                y_axis.append(i)
                y_axis.append(i+0.5)

        fig = figure()
        ax = fig.add_subplot(1,1,1)
        ax.xaxis.grid(color = "gray", linestyle = "dashed")
        ax.yaxis.grid(color = "gray", linestyle = "dashed")
        xticks(x_axis)
        yticks(y_axis)

        axes = gca()
        if self.function_name not in ("sine", "cosine"):
            axes.set_xlim(x_min,x_max)
            axes.set_ylim(y_min, y_max)
        else:
            axes.set_ylim(-abs(self.a) - abs(self.d), abs(self.a) + abs(self.d))
            axes.set_xlim(-self.c - 2*np.pi, 2*np.pi + self.c)
        plot(self.X, self.Y)
        savefig(self.studentName, dpi = 72)


    def LaTeXWrite(self):
        # Initialize read file
        file = self.studentName[:-1] +".tex"

        if os.path.exists(file):
            latexFile = open(file, 'r')
        else:
            latexFile = open('MCR3U Random Graph Assignment Template.tex', 'r')
        
        self.latexFileData = latexFile.readlines()
        
        n = 0
        for line in self.latexFileData:      
            # Insert student name and student number

            if line == "\hfill }\n":
                pass
                self.latexFileData[n] = self.studentName[:-1] +  " \hfill}\n"
            
            # Insert Questions into .tex file
            if line == "%INSERT QUESTION " + self.question_num +"\n":
                self.latexFileData[n] = "\\includegraphics[scale=0.6]{" + self.studentName + ".png}"
                print(self.latexFileData[n])

            # Insert Answers into .tex file
            if line == "% INSERT Q"+ self.question_num + " ANSWERS HERE\n":
                self.latexFileData[n] = "$" + self.equation + "$"
            n = n + 1
        
        outputFile = open(file, "w")
        outputFile.writelines(self.latexFileData)
        outputFile.close()
            
    def LaTeXCompile(self):
        # Building the LaTeX PDFs
        file = self.studentName[:-1] +".tex"
        latexOutput = "pdflatex -interaction=nonstopmode -halt-on-error " + file    
        os.system(latexOutput)

    # Moving files to the appropriate locations
        new_directory = "Graphing Assignment PDFs"
        if os.path.isdir(new_directory):
            #shutil.move(file[:-3]+"pdf", new_directory )
            if os.path.exists(new_directory+ "\\" + file[:-3]+"pdf"):
                os.remove(new_directory + "\\" + file[:-3]+"pdf")
        else:
            os.mkdir(new_directory)
        
        shutil.move(file[:-3]+"pdf", new_directory )
        
    # Cleaning up the directory of unnessessarry files
        os.remove(file[:-3] + "tex")
        os.remove(file[:-3] + "aux")
        os.remove(file[:-3] + "log")
        os.remove(file[:-4] + "1" + ".png")
        os.remove(file[:-4] + "2" + ".png")
    
if __name__ == "__main__":
    graph_1 = Function_Sketcher("Wilfred1")
    graph_1.LaTeXWrite()
    
    graph_2 = Function_Sketcher("Wilfred2")
    
    while graph_2.function_name == graph_1.function_name:
        os.remove("Wilfred2.png")
        graph_2 = Function_Sketcher("Wilfred2")

    graph_2.LaTeXWrite()
    graph_2.LaTeXCompile()
    
