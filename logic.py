def take_input(data, nature, condition = ""):
    if not nature in (int, float, str ):
        return "Le type choisi n'est pas correcte."
    while True:
        try:
            result = nature(input(data))
            break
        except ValueError:
            print("Veuillez renseigner une valeur correcte")
    if condition == "+":
        if result <= 0:
            print("Veuillez renseigner une valeur positive")
            result = take_input(data, nature, condition)
    elif "-" in condition:
        debut, fin =  tuple(condition.split("-"))
        debut = int(debut)
        fin = int(fin)
        if not(result in range(debut, fin + 1)):
            print(f"Veuillez renseignez une valeur entre {debut} et {fin} ")
            result = take_input(data, nature, condition)
    elif " " in condition:
        choices = condition.split(" ")
        if not str(result) in choices:
            print("Veuillez effectuez un choix conforme aux diverses propositions ")
            result = take_input(data, nature, condition)
    return result

class Level:
    def __init__(self, level):
        self.level = level

class Classroom(Level):
    def __init__(self, level):
        super().__init__(level)
        self.students = []
        self.matters = {}
        self.matters_teachers = {}

    def add_matter(self, matter, coeff):
        self.matters[matter] = coeff


class Student(object):
    def __init__(self, matricule, surname, name, date, sex):
        self.name = name
        self.matricule = matricule
        self.surname = surname
        self.date = date
        self.sex = sex

    def __str__(self):
        return f"{self.surname:<20} {self.name:<20}"

class Parent:
    def __init__(self, name, surname, contact, profession):
        self.name = name
        self.surname = surname
        self.contact = contact
        self.profession = profession

    def __str__(self):
        return f"{self.surname:<20} {self.name:<20}"

class Teacher:
    def __init__(self, surname, name, speciality, contact):
        self.name = name
        self.surname = surname
        self.speciality = speciality
        self.contact = contact

    def __str__(self):
        return f"{self.surname:<20} {self.name:<20}"

class Matter:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name:<20}"