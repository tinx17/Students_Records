import tkinter
import customtkinter


def home_view():
    pass

def classes_view():
    pass

def students_view():
    pass

def teacher_view():
    pass

def info_view():
    pass

class NavBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width = 150, height=200)
        self.master = master
        self.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.grid_propagate(False)

        acc = customtkinter.CTkButton(self,width= 30, text = "Home", corner_radius=20, fg_color="grey", font=("Open Sans", 14), command= home_view, hover_color="red")
        acc.grid(row=0, column=0, padx = 10,sticky=tkinter.NSEW)
        classe = customtkinter.CTkButton(self,width= 30, text = "Nos classes", corner_radius=20, fg_color="grey", font=("Open Sans", 14), command= classes_view)
        classe.grid(row=1, column=0, padx = 10, pady = 30,sticky=tkinter.EW)
        our_students = customtkinter.CTkButton(self,width= 30, text = "Nos élèves",corner_radius=20, fg_color="grey", font=("Open Sans", 14), command = students_view)
        our_students.grid(row=2, column=0, padx = 10, sticky=tkinter.EW)
        our_teachers = customtkinter.CTkButton(self,width= 30, text = "Nos Enseignants",corner_radius=20, fg_color="grey", font=("Open Sans", 14), command =teacher_view)
        our_teachers.grid(row=3, column=0, padx = 10,pady = 30,sticky=tkinter.EW)
        about_us = customtkinter.CTkButton(self, width=30, text="About us", corner_radius=20, fg_color="grey", font=("Open Sans", 14), command= info_view)
        about_us.grid(row=4, column=0, padx=10, sticky=tkinter.EW)
        quit_button = customtkinter.CTkButton(self, width=30, text="Quitter", corner_radius=20, fg_color="grey", font=("Open Sans", 14), command=quit)
        quit_button.grid(row=5, column=0, padx=10, pady = 5,sticky=tkinter.EW)


class Aframe(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=400, height = 250, fg_color="blue")
        self.master = master
        self.grid(row=0, column=0, pady = 10,sticky=tkinter.NSEW)
        tr = customtkinter.CTkLabel(self,width= 40, height= 250, fg_color="blue", text="AFrame \nIci ou dans CFrame  sera inscrit un outil de recherche. Ou juste le titre de la section")
        tr.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

class BFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=400, fg_color="red")
        self.master = master
        self.grid(row=1, column=0, sticky=tkinter.NSEW)
        tr = customtkinter.CTkLabel(self,width= 40, height= 250, fg_color="blue", text="BFrame \nIci ou dans CFrame  sera inscrit un outil de recherche. Ou juste le titre de la section")
        tr.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
class CFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=200, fg_color="purple")
        self.master = master
        self.grid(row=0, column=1, pady= 10, padx= 15,sticky=tkinter.NSEW)
        tr = customtkinter.CTkLabel(self,width= 40, height= 250, fg_color="blue", text="CFrame \nVoir AFrame")
        tr.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
class DFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color= "white")
        self.master = master
        self.grid(row=1, column=1, padx= 15,sticky=tkinter.NSEW)
        tr = customtkinter.CTkLabel(self, width=40, height=250, fg_color="blue", text="DFrame \nIci se présenteront des informations détaillés sur des objets")
        tr.place(relx = .5, rely=.5, anchor = tkinter.CENTER)


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=500)
        self.grid(row=0, column=1, padx=20, sticky=tkinter.NSEW)
        self.grid_propagate(False)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        mine = Aframe(self)
        yours = BFrame(self)
        tmine = CFrame(self)
        tyours = DFrame(self)




class StudentsGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title = "Students"
        self.resizable(width=True, height=True)
        self.minsize(700, 700)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        nav = NavBar(self)
        cont = MainFrame(self)

app  =StudentsGUI()
app.mainloop()