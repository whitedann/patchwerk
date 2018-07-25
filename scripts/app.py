import fileinput
import os
from tkinter import Tk, Button, Entry, Label, StringVar
from shutil import copyfile

class Patchwerk():

    def __init__(self, master):

        #GUI stuff
        self.master = master
        master.title("Patchwerk")

        vcmd = master.register(self.validate)
        self.barcode_field = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.barcode_field.pack()

        self.submit_button = Button(master, text="Submit", command=self.generateFile)
        self.submit_button.pack()

        self.error_text = StringVar()
        self.error_text.set("")
        self.error_label = Label(master,textvariable=self.error_text)
        self.error_label.pack()

        #Script stuff
        self.barcode = None
        self.filenames = None

        self.inputPath = 'W:\Manufacturing\PAA H2OD Plate Data\\raw'
        self.finalPath = 'W:\Manufacturing\PAA H2OD Plate Data'

        os.chdir(self.inputPath)
        #os.chdir('W:\Employees\Danny\dev\patchwerk')
        ##Add other work path here###
        #os.chdir('/users/dwhite/patchwerk/patchwerk')
        ###

    def validate(self, new_text):
        if not new_text:
            self.barcode = None
            return True
        try:
            self.barcode = int(new_text)
            return True
        except ValueError:
            return False

    def generateFile(self):
        os.chdir(self.inputPath)
        if (self.confirmTargetFiles() == 1):
            self.error_text.set("Raw file not found")
        else:
            self.editFiles()

    def confirmTargetFiles(self):

        self.barcode = str(self.barcode)
        self.filenames = [self.barcode + "_SWP1.txt", self.barcode + "_SWP2.txt", self.barcode + "_SWP3.txt", self.barcode + "_SWP4.txt"]

        try:
            i = 0
            for fname in self.filenames:
                file = open(fname)
                file.close()
                i += 1
            if(i == 4):
                return 0
            else:
                return 1
        except IOError:
            return 1
        return 0

    def editFiles(self):
        output = self.barcode + "_backup.txt"
        i = 1
        f = open(output, "w")
        for fname in self.filenames:
            for line in fileinput.input([fname]):
                if(i == 1):
                    line = line.replace("Plate", "Blank1")
                elif(i == 2):
                    line = line.replace("Plate", "Blank2")
                elif(i == 3):
                    line = line.replace("Plate", "Sample1")
                elif(i ==4):
                    line = line.replace("Plate", "Sample2")
                f.write(line)
            i += 1
        os.chdir(self.finalPath)
        copyfile(f,)

root = Tk()
test = Patchwerk(root)
root.mainloop()
