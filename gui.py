import tkinter
import customtkinter

class NavBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width = 150, height=200)
        self.master = master
        self.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.grid_propagate(0)
        acc = customtkinter.CTkButton(self,width= 30, text = "Home", corner_radius=20, fg_color="grey")
        acc.grid(row=0, column=0, padx = 15, pady = 5,sticky=tkinter.NSEW)
        classe = customtkinter.CTkButton(self,width= 30, text = "Nos classes", corner_radius=20, fg_color="grey")
        classe.grid(row=1, column=0, padx = 15, sticky=tkinter.EW)
        our_students = customtkinter.CTkButton(self,width= 30, text = "Nos élèves",corner_radius=20, fg_color="grey")
        our_students.grid(row=2, column=0, padx = 15, pady = 5,sticky=tkinter.EW)
        our_teachers = customtkinter.CTkButton(self,width= 30, text = "Nos Enseignants",corner_radius=20, fg_color="grey")
        our_teachers.grid(row=3, column=0, padx = 15,sticky=tkinter.EW)




class Acceuil(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(self, master)



class StudentsGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title = "Students"
        self.resizable(width=True, height=True)
        self.minsize(700, 700)
        self.rowconfigure(0, weight=1)
        mine = NavBar(self)

app  =StudentsGUI()
app.mainloop()