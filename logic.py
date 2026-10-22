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

import json
from pathlib import Path

class School:
    def __init__(self, path="school_data.json"):
        self.path = Path(path)
        self.classes = {}    # nom de classe -> Classroom
        self.teachers = {}   # id enseignant -> Teacher

    def add_class(self, level, name):
        if name in self.classes:
            return f"La classe {name} existe déjà."
        self.classes[name] = Classroom(level, name)
        return f"La classe {name} a été créée."

    def remove_class(self, name):
        if name not in self.classes:
            return f"La classe {name} n'existe pas."
        del self.classes[name]
        return f"La classe {name} a été supprimée."

    def add_teacher(self, surname, name, speciality, contact):
        teacher = Teacher(surname, name, speciality, contact)
        if teacher.id in self.teachers:
            return f"L'enseignant {teacher.id} existe déjà."
        self.teachers[teacher.id] = teacher
        return f"L'enseignant {teacher.id} a été ajouté."

    def update_teacher(self, teacher_id, surname, name, speciality, contact):
        teacher = self.teachers.get(teacher_id)
        if teacher is None:
            return f"L'enseignant {teacher_id} n'existe pas."
        new_id = surname.upper().strip() + " " + name.lower().strip()
        if new_id != teacher_id and new_id in self.teachers:
            return f"L'enseignant {new_id} existe déjà."
        del self.teachers[teacher_id]
        teacher.update(surname, name, speciality, contact)
        self.teachers[teacher.id] = teacher
        return f"L'enseignant {teacher.id} a été modifié."

    def assignments(self, teacher):
        """Liste des (classe, matière) dont l'enseignant a la charge."""
        return [(c.name, m) for c in self.classes.values()
                for m, t in c.matters_teachers.items() if t is teacher]

    def remove_teacher(self, teacher_id):
        teacher = self.teachers.pop(teacher_id, None)
        if teacher is None:
            return f"L'enseignant {teacher_id} n'existe pas."
        for classe in self.classes.values():
            for matter, t in classe.matters_teachers.items():
                if t is teacher:
                    classe.matters_teachers[matter] = None
        return f"L'enseignant {teacher_id} a été supprimé."

    def all_students(self):
        for classe in self.classes.values():
            yield from classe

    def save(self):
        data = {
            "teachers": [t.to_dict() for t in self.teachers.values()],
            "classes": [c.to_dict() for c in self.classes.values()],
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self):
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        for t in data["teachers"]:
            teacher = Teacher(t["surname"], t["name"], t["speciality"], t["contact"])
            self.teachers[teacher.id] = teacher
        for c in data["classes"]:
            classe = Classroom.from_dict(c, self.teachers)
            self.classes[classe.name] = classe

    def top_students(self, n=5):
        scored = [(s, s.average()) for s in self.all_students()]
        scored = [(s, a) for s, a in scored if a is not None]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:n]

EVALS = ("Int1", "Int2", "Int3", "Devoir", "Compo")


def matter_average(grades):
    """Moyenne d'une matière pour un relevé {"Int1": ..., "Compo": ...}.
    moyenne de classe = (moyenne des interros + devoir) / 2
    moyenne matière   = (moyenne de classe + composition) / 2
    Les notes manquantes ("") sont ignorées. Renvoie None s'il n'y a aucune note."""
    ints = [grades[k] for k in ("Int1", "Int2", "Int3") if grades[k] != ""]
    class_parts = []
    if ints:
        class_parts.append(sum(ints) / len(ints))
    if grades["Devoir"] != "":
        class_parts.append(grades["Devoir"])
    class_avg = sum(class_parts) / len(class_parts) if class_parts else None
    final = [x for x in (class_avg, grades["Compo"] if grades["Compo"] != "" else None)
             if x is not None]
    return sum(final) / len(final) if final else None


class Level:
    def __init__(self, level):
        self.level = level

class Classroom(Level):
    def __init__(self, level, name):
        super().__init__(level)
        self.name = name
        self.students = {}
        self.matters = {}
        self.matters_teachers = {}

    def __str__(self):
        return f"Classe: {self.name:<20} Effectif: {self.numbers}"

    def __iter__(self):
        for i in self.students.values():
            yield i

    @property
    def numbers(self):
        return len(self.students)


    def add_matter(self, matter, coeff):
        if matter in self.matters:
            return f"Cette matière et déjà inscrite"
        self.matters[matter.name] = coeff
        self.matters_teachers[matter.name] = None
        for student in self.students.values():
            student.record[matter.name] = {"Coeff": coeff,"Int1": "", "Int2":"", "Int3":"", "Devoir":"", "Compo":""}
        return f"La matière {matter} a été ajouté"

    def remove_matter(self, name):
        if name not in self.matters:
            return f"La matière {name} n'est pas enseignée en {self.name}"
        del self.matters[name]
        del self.matters_teachers[name]
        for student in self.students.values():
            student.record.pop(name, None)
        return f"La matière {name} a été supprimée"


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
        for student in self.students.values():
            if id_ == student.id:
                return f"L'élève {id_} est déjà inscrit en {self.name}."
            if matricule == student.matricule:
                return f"Le matricule {matricule} est déjà présent en {self.name}."
        self.students[matricule] = Student(matricule, surname, name, date, sex, self)
        return f"L'élève {id_} a été ajouté avec succès en {self.name}."

    def remove_student(self, id_ = None, matricule = None):
        if not (matricule is None):
            if matricule in self.students:
                del self.students[matricule]
                return f"L'élève au matricule {matricule} a bien été retiré de la classe {self.name}"
            return f"L'élève au matricule {matricule} n'est pas inscrit en {self.name}"
        if not (id_ is None):
            for stu in self.students.values():
                if id_ == stu.id:
                    del self.students[stu.matricule]
                    return f"L'élève {stu.id} a bien été retiré de la classe {self.name}"
            return f"L'élève {id_} n'est pas inscrit en {self.name}"
        return None

    def display_students(self):
        dis = f"{str(self)}\nListe des élèves:"
        if not self.students:
            dis += "\nAucun élève inscrit pour l'instant"
        for stu in self.students.values():
            dis += "\n"+str(stu)
        return dis

    def affect_teacher(self, matter, teacher):
        if matter not in self.matters_teachers:
            return f"La matière {matter} n'est pas enseignée en {self.name}."
        self.matters_teachers[matter] = teacher
        return f"{teacher.id} est désormais en charge de {matter}"

    def to_dict(self):
        return {
            "level": self.level,
            "name": self.name,
            "matters": self.matters,
            "teachers": {m: (t.id if t else None) for m, t in self.matters_teachers.items()},
            "students": [s.to_dict() for s in self.students.values()],
        }

    def display_teachers(self):
        dis = f"{str(self)}\nListe des professeurs:"
        if any(self.matters_teachers.values()):
            for matter, teacher in self.matters_teachers.items():
                if teacher:
                    dis += f"\n{matter} : {teacher.surname} {teacher.name}"
        else:
            dis += "\nAucun professeur n'a encore été affecté à cette classe"
        return dis

    def ranking(self):
        scored = [(s, s.average()) for s in self.students.values()]
        scored = [(s, a) for s, a in scored if a is not None]
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def rank_of(self, student):
        avg = student.average()
        if avg is None:
            return None
        return sum(1 for _, a in self.ranking() if a > avg) + 1

    def class_average(self):
        avgs = [a for _, a in self.ranking()]
        return sum(avgs) / len(avgs) if avgs else None

    @classmethod
    def from_dict(cls, data, teachers):
        classe = cls(data["level"], data["name"])
        for name, coeff in data["matters"].items():
            classe.add_matter(Matter(name), coeff)
        for matter, teacher_id in data["teachers"].items():
            classe.matters_teachers[matter] = teachers.get(teacher_id)
        for s in data["students"]:
            classe.add_student(s["matricule"], s["surname"], s["name"], s["date"], s["sex"])
            classe.students[s["matricule"]].record = s["record"]
        return classe

    def __iter__(self):
        for stu in self.students.values():
            yield stu



class Student(object):
    class Parent:
        def __init__(self, name, surname, contact, profession):
            self.name = name
            self.surname = surname
            self.contact = contact
            self.profession = profession

        def __str__(self):
            return f"{self.surname:<20} {self.name:<20}"

    def __init__(self, matricule, surname, name, date, sex, classe):
        self.name = name
        self.matricule = matricule
        self.surname = surname
        self.id = surname.upper().strip() +" " +name.lower().strip()
        self.date = date
        self.sex = sex
        #Grâce à l'attribut self.classe j'aurais accès aux matières de la classe de l'élève
        self.classe = classe
        #Le problème est de déterminer la structure du recueil de notes de l'élève.
        #Je pensais à une structure{Matière:{"Int1":"", "Int2":"", "Int3":"", "Devoir":, "Compo":, }}
        self._record = {matter:{"Coeff": classe.matters[matter],"Int1": "", "Int2":"", "Int3":"", "Devoir":"", "Compo":""} for matter in classe.matters}
        #Il faudrait maintenant que cette liste de matière se mette à jour automatiquement
        # dès qu'une nouvelle matière est ajoutée à la classe
        #Je pense utiliser un setter, mais j'ignore concrètement comment y parvenir
        #Mission accomplie. J'y suis arrivé en effectuant une mise à jour dans le code de la classe
        #notamment au niveau de l'ajout d'une matière pour avoir un effet en cascade.

    @property
    def record(self):
        return self._record
    @record.setter
    def record(self, record):
        self._record = record

    def input_note(self, matter, evalt, note):
        if matter not in self.classe.matters:
            return "Cet élève ne compose pas cette matière"
        if evalt not in EVALS:
            return "Type d'évaluation inconnu"
        if str(note).strip() == "":
            self._record[matter][evalt] = ""
            return "Note effacée"
        try:
            note = float(str(note).replace(",", "."))
        except ValueError:
            return "La note doit être un nombre"
        if not 0 <= note <= 20:
            return "La note doit être comprise entre 0 et 20"
        self._record[matter][evalt] = note
        return "Note ajoutée avec succès"

    def average(self):
        total = coeffs = 0
        for grades in self._record.values():
            m = matter_average(grades)
            if m is not None:
                total += m * grades["Coeff"]
                coeffs += grades["Coeff"]
        return total / coeffs if coeffs else None

    def update(self, surname, name, date, sex):
        self.surname = surname
        self.name = name
        self.id = surname.upper().strip() + " " + name.lower().strip()
        self.date = date
        self.sex = sex

    def to_dict(self):
        return {"matricule": self.matricule, "surname": self.surname, "name": self.name,
                "date": str(self.date), "sex": self.sex, "record": self.record}

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

    def update(self, surname, name, speciality, contact):
        self.surname = surname
        self.name = name
        self.id = surname.upper().strip() + " " + name.lower().strip()
        self.speciality = speciality
        self.contact = contact

    def to_dict(self):
        return {"surname": self.surname, "name": self.name,
                "speciality": self.speciality, "contact": self.contact}

class Matter:
    def __init__(self, name):
        self.name = name.strip()
    def __str__(self):
        return self.name


if __name__ == "__main__":
    school = School()
    school.add_class(6, "6emeA")
    school.add_teacher("DOSSOU", "Marc", "Maths", "0102030405")
    classe = school.classes["6emeA"]
    classe.add_matter(Matter("Mathématiques"), 5)
    classe.affect_teacher("Mathématiques", school.teachers["DOSSOU marc"])
    classe.add_student("123456", "AHOUMENOU", "Royal", "01/02/03", "M")
    school.save()

    school2 = School()
    school2.load()
    print(school2.classes["6emeA"].display_teachers())


