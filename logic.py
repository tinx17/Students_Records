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
    def __init__(self, level, name):
        super().__init__(level)
        self.name = name
        self.students = []
        self.matters = {}
        self.matters_teachers = {}

    def __str__(self):
        return f"Classe: {self.name:<20} Effectif: {self.numbers}"

    @property
    def numbers(self):
        return len(self.students)


    def add_matter(self, matter, coeff):
        if matter in self.matters:
            return f"Cette matière et déjà inscrite"
        self.matters[matter] = coeff
        self.matters_teachers[matter] = None
        return f"La matière {matter} a été ajouté"

    def remove_matter(self, matter):
        if matter in self.matters:
            del self.matters[matter]
            return f"La matière {matter} a été supprimé avec succès"
        return f"La matière {matter} n'est pas comprise dans les matières de cette classe "

    def display_matters(self):
        dis = f"{str(self)}\nListe des matières:"
        if not self.matters:
            dis += "\nAucune matière attribuée à cette classe "
        else:
            for matter in self.matters:
                dis += f"\n◄◄◄◄{str(matter):<20} | Coefficient:{self.matters[matter]:<20}"
        return dis


    def add_student(self,  matricule, surname, name, date, sex):
        id_ = surname.upper().strip() +" " +name.lower().strip()
        for student in self.students:
            if id_ == student.id:
                return f"L'élève {id_} est déjà inscrit en {self.name}."
            if matricule == student.matricule:
                return f"Le matricule {matricule} est déjà présent en {self.name}."
        self.students.append(Student(matricule, surname, name, date, sex))
        return f"L'élève {id_} a été ajouté avec succès en {self.name}."

    def remove_student(self, id_):
        if id_ in self.students:
            self.students.remove(id_)
            return f"L'élève {id_} a été retiré avec succèès de la classe {self.name}. "
        return f"L'élève {id_} n'est pas inscrit dans la classe {self.name}."

    def display_students(self):
        dis = f"{str(self)}\nListe des élèves:"
        if not self.students:
            dis += "\nAucun élève inscrit pour l'instant"
        for student in self.students:
            dis += "\n"+str(student)
        return dis

    def affect_teacher(self, matter, surname, name, speciality, contact):
        if matter in self.matters_teachers:
            self.matters_teachers[matter] = Teacher(surname, name, speciality, contact)
            return f"L'enseignant(e) {surname.upper().strip() +" " +name.lower().strip()} est désormais en charge de la matières {matter}"
        return f"La matière {matter} n'est pas enseigné en {self.name}."

    def display_teachers(self):
        dis = f"{str(self)}\nListe des professeurs:"
        if any(self.matters_teachers.values()):
            for matter, teacher in self.matters_teachers.items():
                if teacher:
                    dis += f"\n{matter} : {teacher.surname} {teacher.name}"
        else:
            dis += "\nAucun professeur n'a encore été affecté à cette classe"
        return dis





class Student(object):
    class Parent:
        def __init__(self, name, surname, contact, profession):
            self.name = name
            self.surname = surname
            self.contact = contact
            self.profession = profession

        def __str__(self):
            return f"{self.surname:<20} {self.name:<20}"

    def __init__(self, matricule, surname, name, date, sex):
        self.name = name
        self.matricule = matricule
        self.surname = surname
        self.id = surname.upper().strip() +" " +name.lower().strip()
        self.date = date
        self.sex = sex

    def __str__(self):
        return f"◄◄◄◄◄|{self.matricule:<20} |{self.surname:<20} |{self.name:<20} |{str(self.date):<20} |{self.sex}"


class Teacher:
    def __init__(self, surname, name, speciality, contact):
        self.name = name
        self.surname = surname
        self.id = surname.upper().strip() + " " +name.lower().strip()
        self.speciality = speciality
        self.contact = contact

    def __str__(self):
        return f"{self.surname:<20} {self.name:<20}"

class Matter:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name:<20}"


if __name__ =="__main__":
    classe = Classroom(2, "6emeA")
    print(classe.display_students())

    classe.add_student("123456", "AHOUMENOU", "Royal", "01/02/03", "M")
    classe.add_student("123698", "AHOUMENOU", "Belfort", "01/02/03", "M")
    classe.add_student("123698", "AHOUMENOU", "Beauchamp", "01/02/03", "M")
    classe.add_student("123698", "AHOUMENOU", "Ladislas", "01/02/03", "M")
    classe.add_student("123698", "AHOUMENOU", "Ashen", "01/02/03", "M")

    classe.add_matter(Matter("Mathématiques"), 5)
    classe.add_matter("Pct", 4)
    classe.add_matter("Anglais", 3)
    classe.affect_teacher("Pct", "aerr", "aze", "pct", "0102030405")
    classe.affect_teacher("Anglais", "ac", "avrt", "anglais", "0205080709")
    print(classe.display_teachers())
    print(classe.matters_teachers.items())


