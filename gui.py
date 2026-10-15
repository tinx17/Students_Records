import customtkinter
from tkinter import messagebox
from logic import School, Matter, EVALS, matter_average

FONT = ("Open Sans", 14)
ACTIVE = "#1f6aa5"
INACTIVE = "grey"
DANGER = "#c0392b"
NONE = "— Aucun —"

def clear(widget):
    for child in widget.winfo_children():
        child.destroy()


class FormDialog(customtkinter.CTkToplevel):
    """Fenêtre de saisie. fields = [(clé, libellé)] ou [(clé, libellé, [choix])].
    on_submit(data) renvoie un message d'erreur, ou None si tout va bien."""

    def __init__(self, master, title, fields, on_submit):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.on_submit = on_submit
        self.widgets = {}
        for row, field in enumerate(fields):
            key, label = field[0], field[1]
            values = field[2] if len(field) > 2 else None
            customtkinter.CTkLabel(self, text=label, font=FONT).grid(
                row=row, column=0, padx=15, pady=8, sticky="w")
            if values:
                widget = customtkinter.CTkComboBox(self, values=values, state="readonly")
                widget.set(values[0])
            else:
                widget = customtkinter.CTkEntry(self, width=200)
            widget.grid(row=row, column=1, padx=15, pady=8)
            self.widgets[key] = widget
        self.error = customtkinter.CTkLabel(self, text="", text_color="#e5484d")
        self.error.grid(row=len(fields), column=0, columnspan=2)
        customtkinter.CTkButton(self, text="Valider", command=self.submit).grid(
            row=len(fields) + 1, column=0, columnspan=2, pady=15)
        self.after(100, self.grab_set)

    def submit(self):
        data = {key: w.get().strip() for key, w in self.widgets.items()}
        error = self.on_submit(data)
        if error:
            self.error.configure(text=error)
        else:
            self.destroy()

class NavBar(customtkinter.CTkFrame):
    ITEMS = [
        ("home", "Home"),
        ("classes", "Nos classes"),
        ("students", "Nos élèves"),
        ("teachers", "Nos enseignants"),
        ("info", "About us"),
    ]

    def __init__(self, master, on_select, on_quit):
        super().__init__(master, width=180)
        self.grid_propagate(False)
        self.buttons = {}
        for row, (key, label) in enumerate(self.ITEMS):
            btn = customtkinter.CTkButton(
                self, text=label, corner_radius=20, fg_color=INACTIVE, font=FONT,
                command=lambda k=key: on_select(k))
            btn.grid(row=row, column=0, padx=10, pady=15, sticky="ew")
            self.buttons[key] = btn
        self.columnconfigure(0, weight=1)
        self.rowconfigure(len(self.ITEMS), weight=1)
        customtkinter.CTkButton(
            self, text="Quitter", corner_radius=20, fg_color=INACTIVE, font=FONT,
            command=on_quit).grid(row=len(self.ITEMS) + 1, column=0, padx=10, pady=15, sticky="ew")

    def set_active(self, key):
        for k, btn in self.buttons.items():
            btn.configure(fg_color=ACTIVE if k == key else INACTIVE)


class View(customtkinter.CTkFrame):
    """Gabarit commun : un en-tête (titre, recherche...) et un corps."""
    title = ""

    def __init__(self, master, school):
        super().__init__(master, fg_color="transparent")
        self.school = school
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.navigate = lambda key: None

        self.header = customtkinter.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        customtkinter.CTkLabel(
            self.header, text=self.title, font=("Open Sans", 24, "bold")
        ).pack(side="left", padx=15, pady=15)

        self.body = customtkinter.CTkFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

    def refresh(self):
        """Appelée à chaque affichage de la vue pour recharger les données."""
        pass


class HomeView(View):
    title = "Accueil"

    def __init__(self, master, school):
        super().__init__(master, school)
        self.body.columnconfigure((0, 1), weight=1)
        self.body.rowconfigure(1, weight=1)

        self.cards = customtkinter.CTkFrame(self.body, fg_color="transparent")
        self.cards.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.cards.columnconfigure((0, 1, 2), weight=1)

        self.classes_panel = customtkinter.CTkScrollableFrame(self.body, label_text="Classes")
        self.classes_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        self.classes_panel.columnconfigure(0, weight=1)
        self.top_panel = customtkinter.CTkScrollableFrame(
            self.body, label_text="Meilleurs élèves (toutes classes)")
        self.top_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        self.top_panel.columnconfigure(1, weight=1)

    def refresh(self):
        # Cartes cliquables : elles ouvrent la vue correspondante
        clear(self.cards)
        stats = (
            ("Classes", len(self.school.classes), "classes"),
            ("Élèves", sum(c.numbers for c in self.school.classes.values()), "students"),
            ("Enseignants", len(self.school.teachers), "teachers"),
        )
        for col, (label, value, target) in enumerate(stats):
            card = customtkinter.CTkFrame(self.cards)
            card.grid(row=0, column=col, sticky="ew", padx=5)
            number = customtkinter.CTkLabel(card, text=str(value), font=("Open Sans", 32, "bold"))
            number.pack(pady=(15, 0))
            text = customtkinter.CTkLabel(card, text=label, font=FONT)
            text.pack(pady=(0, 15))
            for widget in (card, number, text):
                widget.bind("<Button-1>", lambda e, t=target: self.navigate(t))

        # Classes : effectif et moyenne de classe
        clear(self.classes_panel)
        if not self.school.classes:
            customtkinter.CTkLabel(self.classes_panel, text="Aucune classe pour l'instant").grid(
                row=0, column=0, pady=10)
        for i, classe in enumerate(self.school.classes.values()):
            avg = classe.class_average()
            customtkinter.CTkLabel(self.classes_panel, text=classe.name, font=FONT, anchor="w").grid(
                row=i, column=0, sticky="ew", padx=8, pady=3)
            customtkinter.CTkLabel(self.classes_panel, text=f"{classe.numbers} élève(s)").grid(
                row=i, column=1, padx=8)
            customtkinter.CTkLabel(
                self.classes_panel, text="—" if avg is None else f"Moy. {avg:.2f}"
            ).grid(row=i, column=2, padx=8)

        # Meilleurs élèves
        clear(self.top_panel)
        top = self.school.top_students()
        if not top:
            customtkinter.CTkLabel(self.top_panel, text="Aucune note saisie pour l'instant").grid(
                row=0, column=0, columnspan=4, pady=10)
        for i, (s, avg) in enumerate(top):
            customtkinter.CTkLabel(self.top_panel, text=f"{i + 1}.").grid(row=i, column=0, padx=8, pady=3)
            customtkinter.CTkLabel(
                self.top_panel, text=f"{s.surname.upper()} {s.name}", font=FONT, anchor="w"
            ).grid(row=i, column=1, sticky="ew", padx=8)
            customtkinter.CTkLabel(self.top_panel, text=s.classe.name).grid(row=i, column=2, padx=8)
            customtkinter.CTkLabel(self.top_panel, text=f"{avg:.2f}", font=FONT).grid(
                row=i, column=3, padx=8)


class InfoView(View):
    title = "À propos"

    def __init__(self, master, school):
        super().__init__(master, school)
        content = customtkinter.CTkFrame(self.body, fg_color="transparent")
        content.pack(expand=True)
        customtkinter.CTkLabel(
            content, text="Gestion scolaire", font=("Open Sans", 28, "bold")
        ).pack(pady=(0, 5))
        customtkinter.CTkLabel(content, text="Version 1.0", text_color="grey").pack()
        customtkinter.CTkLabel(
            content, font=FONT, justify="center",
            text="Gestion des classes, des matières, des élèves,\n"
                 "des enseignants et des notes d'un établissement."
        ).pack(pady=20)
        customtkinter.CTkLabel(
            content, text="Python · CustomTkinter · JSON", text_color="grey"
        ).pack()

class ClassesView(View):
    title = "Nos classes"

    def __init__(self, master, school):
        super().__init__(master, school)
        self.selected = None

        customtkinter.CTkButton(
            self.header, text="+ Nouvelle classe", font=FONT, command=self.new_class
        ).pack(side="right", padx=15)

        self.body.columnconfigure(1, weight=1)
        self.body.rowconfigure(0, weight=1)

        # Colonne de gauche : liste des classes
        self.list_frame = customtkinter.CTkScrollableFrame(self.body, width=230)
        self.list_frame.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)

        # Colonne de droite : détail de la classe sélectionnée
        self.detail = customtkinter.CTkFrame(self.body, fg_color="transparent")
        self.detail.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.detail.columnconfigure(0, weight=1)
        self.detail.rowconfigure(1, weight=1)

        top = customtkinter.CTkFrame(self.detail, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.class_label = customtkinter.CTkLabel(top, text="", font=("Open Sans", 18, "bold"))
        self.class_label.pack(side="left")
        self.delete_btn = customtkinter.CTkButton(
            top, text="Supprimer", width=100, fg_color=DANGER, command=self.delete_class)
        self.delete_btn.pack(side="right")

        self.tabs = customtkinter.CTkTabview(self.detail)
        self.tabs.grid(row=1, column=0, sticky="nsew")
        for name in ("Matières", "Élèves", "Enseignants"):
            self.tabs.add(name)
            self.tabs.tab(name).columnconfigure(0, weight=1)
            self.tabs.tab(name).rowconfigure(0, weight=1)

    # ---------- affichage ----------
    def refresh(self):
        if self.selected not in self.school.classes:
            self.selected = next(iter(self.school.classes), None)
        self.render_list()
        self.render_detail()

    def render_list(self):
        clear(self.list_frame)
        if not self.school.classes:
            customtkinter.CTkLabel(self.list_frame, text="Aucune classe").pack(pady=10)
        for name, classe in self.school.classes.items():
            customtkinter.CTkButton(
                self.list_frame, text=f"{name}  ·  {classe.numbers} élève(s)", font=FONT,
                fg_color=ACTIVE if name == self.selected else INACTIVE,
                command=lambda n=name: self.select(n)
            ).pack(fill="x", pady=4)

    def render_detail(self):
        classe = self.school.classes.get(self.selected)
        if classe is None:
            self.class_label.configure(text="Aucune classe sélectionnée")
            self.delete_btn.configure(state="disabled")
            for name in ("Matières", "Élèves", "Enseignants"):
                clear(self.tabs.tab(name))
            return
        self.class_label.configure(text=f"{classe.name}  (niveau {classe.level})")
        self.delete_btn.configure(state="normal")
        self.render_matters(classe)
        self.render_students(classe)
        self.render_teachers(classe)

    def render_matters(self, classe):
        tab = self.tabs.tab("Matières")
        clear(tab)
        rows = customtkinter.CTkScrollableFrame(tab)
        rows.grid(row=0, column=0, sticky="nsew")
        rows.columnconfigure(0, weight=1)
        if not classe.matters:
            customtkinter.CTkLabel(rows, text="Aucune matière pour l'instant").grid(row=0, column=0, pady=10)
        for i, (name, coeff) in enumerate(classe.matters.items()):
            customtkinter.CTkLabel(rows, text=name, font=FONT).grid(row=i, column=0, sticky="w", padx=10, pady=4)
            customtkinter.CTkLabel(rows, text=f"Coeff. {coeff}").grid(row=i, column=1, padx=10)
            customtkinter.CTkButton(
                rows, text="✕", width=30, fg_color=DANGER,
                command=lambda n=name: self.remove_matter(classe, n)
            ).grid(row=i, column=2, padx=10)

        add = customtkinter.CTkFrame(tab, fg_color="transparent")
        add.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        name_entry = customtkinter.CTkEntry(add, placeholder_text="Matière", width=180)
        name_entry.pack(side="left", padx=(0, 10))
        coeff_entry = customtkinter.CTkEntry(add, placeholder_text="Coeff.", width=70)
        coeff_entry.pack(side="left", padx=(0, 10))
        customtkinter.CTkButton(
            add, text="Ajouter", width=90,
            command=lambda: self.add_matter(classe, name_entry, coeff_entry)
        ).pack(side="left")

    def render_students(self, classe):
        tab = self.tabs.tab("Élèves")
        clear(tab)
        rows = customtkinter.CTkScrollableFrame(tab)
        rows.grid(row=0, column=0, sticky="nsew")
        if not classe.students:
            customtkinter.CTkLabel(rows, text="Aucun élève inscrit pour l'instant").grid(row=0, column=0, pady=10)
            return
        headers = ("Matricule", "Nom", "Prénom", "Naissance", "Sexe")
        for col, text in enumerate(headers):
            rows.columnconfigure(col, weight=1)
            customtkinter.CTkLabel(rows, text=text, font=("Open Sans", 14, "bold")).grid(
                row=0, column=col, padx=8, pady=4, sticky="w")
        for i, s in enumerate(classe, start=1):
            for col, text in enumerate((s.matricule, s.surname, s.name, s.date, s.sex)):
                customtkinter.CTkLabel(rows, text=str(text)).grid(row=i, column=col, padx=8, pady=2, sticky="w")

    def render_teachers(self, classe):
        tab = self.tabs.tab("Enseignants")
        clear(tab)
        rows = customtkinter.CTkScrollableFrame(tab)
        rows.grid(row=0, column=0, sticky="nsew")
        if not classe.matters:
            customtkinter.CTkLabel(rows, text="Ajoute d'abord des matières à cette classe").grid(row=0, column=0, pady=10)
            return
        if not self.school.teachers:
            customtkinter.CTkLabel(rows, text="Aucun enseignant enregistré (voir « Nos enseignants »)").grid(row=0, column=0, pady=10)
            return
        ids = [NONE] + list(self.school.teachers)
        for i, matter in enumerate(classe.matters):
            customtkinter.CTkLabel(rows, text=matter, font=FONT).grid(row=i, column=0, sticky="w", padx=10, pady=6)
            teacher = classe.matters_teachers.get(matter)
            combo = customtkinter.CTkComboBox(
                rows, values=ids, state="readonly", width=220,
                command=lambda value, m=matter: self.assign(classe, m, value))
            combo.set(teacher.id if teacher else NONE)
            combo.grid(row=i, column=1, padx=10, pady=6)

    # ---------- actions ----------
    def select(self, name):
        self.selected = name
        self.refresh()

    def new_class(self):
        def submit(data):
            if not data["name"]:
                return "Le nom est obligatoire."
            if not data["level"].isdigit():
                return "Le niveau doit être un nombre."
            if data["name"] in self.school.classes:
                return "Cette classe existe déjà."
            self.school.add_class(int(data["level"]), data["name"])
            self.selected = data["name"]
            self.refresh()
        FormDialog(self, "Nouvelle classe", [("name", "Nom"), ("level", "Niveau")], submit)

    def delete_class(self):
        if self.selected and messagebox.askyesno(
                "Supprimer", f"Supprimer la classe {self.selected} et tous ses élèves ?"):
            self.school.remove_class(self.selected)
            self.selected = None
            self.refresh()

    def add_matter(self, classe, name_entry, coeff_entry):
        name = name_entry.get().strip()
        try:
            coeff = float(coeff_entry.get().replace(",", "."))
        except ValueError:
            coeff = 0
        if not name or coeff <= 0:
            messagebox.showwarning("Matière", "Renseigne un nom et un coefficient positif.")
            return
        if name in classe.matters:
            messagebox.showwarning("Matière", "Cette matière est déjà inscrite.")
            return
        classe.add_matter(Matter(name), int(coeff) if coeff.is_integer() else coeff)
        self.render_detail()

    def remove_matter(self, classe, name):
        if messagebox.askyesno("Supprimer", f"Supprimer {name} ? Les notes associées seront perdues."):
            classe.remove_matter(name)
            self.render_detail()

    def assign(self, classe, matter, value):
        if value == NONE:
            classe.matters_teachers[matter] = None
        else:
            classe.affect_teacher(matter, self.school.teachers[value])

class StudentsView(View):
    title = "Nos élèves"
    ALL = "Toutes les classes"

    def __init__(self, master, school):
        super().__init__(master, school)
        self.selected = None          # (nom de la classe, matricule)
        self.entries = {}

        customtkinter.CTkButton(
            self.header, text="+ Nouvel élève", font=FONT, command=self.new_student
        ).pack(side="right", padx=15)
        self.class_filter = customtkinter.CTkComboBox(
            self.header, values=[self.ALL], state="readonly", width=170,
            command=lambda _: self.render_list())
        self.class_filter.set(self.ALL)
        self.class_filter.pack(side="right", padx=5)
        self.search = customtkinter.CTkEntry(
            self.header, placeholder_text="Rechercher (nom, prénom, matricule)", width=260)
        self.search.pack(side="right", padx=5)
        self.search.bind("<KeyRelease>", lambda e: self.render_list())

        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)
        self.body.rowconfigure(1, weight=1)
        self.list_frame = customtkinter.CTkScrollableFrame(self.body)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.detail = customtkinter.CTkFrame(self.body)
        self.detail.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    # ---------- données ----------
    def find(self, key):
        if key is None:
            return None
        classe = self.school.classes.get(key[0])
        student = classe.students.get(key[1]) if classe else None
        return (classe, student) if student else None

    def filtered(self):
        query = self.search.get().strip().lower()
        wanted = self.class_filter.get()
        for classe in self.school.classes.values():
            if wanted != self.ALL and classe.name != wanted:
                continue
            for s in classe:
                if query and query not in f"{s.matricule} {s.surname} {s.name}".lower():
                    continue
                yield classe, s

    # ---------- affichage ----------
    def refresh(self):
        names = [self.ALL] + list(self.school.classes)
        self.class_filter.configure(values=names)
        if self.class_filter.get() not in names:
            self.class_filter.set(self.ALL)
        if self.find(self.selected) is None:
            self.selected = None
        self.render_list()
        self.render_detail()

    def render_list(self):
        clear(self.list_frame)
        headers = ("Matricule", "Nom", "Prénom", "Classe", "Moyenne")
        for col, text in enumerate(headers):
            self.list_frame.columnconfigure(col, weight=1)
            customtkinter.CTkLabel(
                self.list_frame, text=text, font=("Open Sans", 14, "bold"), anchor="w"
            ).grid(row=0, column=col, padx=8, pady=4, sticky="ew")
        count = 0
        for i, (classe, s) in enumerate(self.filtered(), start=1):
            avg = s.average()
            values = (s.matricule, s.surname, s.name, classe.name,
                      "—" if avg is None else f"{avg:.2f}")
            key = (classe.name, s.matricule)
            color = ACTIVE if key == self.selected else "transparent"
            for col, text in enumerate(values):
                label = customtkinter.CTkLabel(
                    self.list_frame, text=text, fg_color=color, anchor="w")
                label.grid(row=i, column=col, padx=2, pady=1, sticky="ew")
                label.bind("<Button-1>", lambda e, k=key: self.select(k))
            count += 1
        if count == 0:
            customtkinter.CTkLabel(self.list_frame, text="Aucun élève trouvé").grid(
                row=1, column=0, columnspan=5, pady=10)

    def render_detail(self):
        clear(self.detail)
        self.entries = {}
        found = self.find(self.selected)
        if not found:
            customtkinter.CTkLabel(
                self.detail, text="Sélectionne un élève pour voir son relevé de notes"
            ).pack(expand=True)
            return
        classe, s = found

        top = customtkinter.CTkFrame(self.detail, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))
        customtkinter.CTkLabel(
            top, text=f"{s.surname.upper()} {s.name}", font=("Open Sans", 18, "bold")
        ).pack(side="left")
        customtkinter.CTkButton(
            top, text="Supprimer", width=100, fg_color=DANGER, command=self.delete_student
        ).pack(side="right")
        customtkinter.CTkButton(
            top, text="Modifier", width=100, command=self.edit_student
        ).pack(side="right", padx=10)

        customtkinter.CTkLabel(
            self.detail,
            text=f"Matricule {s.matricule}  ·  {classe.name}  ·  né(e) le {s.date}  ·  {s.sex}"
        ).pack(anchor="w", padx=10)
        avg, rank = s.average(), classe.rank_of(s)
        result = "Moyenne générale : " + ("—" if avg is None else f"{avg:.2f}/20")
        if rank:
            result += f"   ·   Rang : {rank}/{classe.numbers}"
        customtkinter.CTkLabel(self.detail, text=result, font=FONT).pack(
            anchor="w", padx=10, pady=(0, 5))

        if not classe.matters:
            customtkinter.CTkLabel(
                self.detail, text="Cette classe n'a pas encore de matières"
            ).pack(pady=10)
            return

        customtkinter.CTkButton(
            self.detail, text="Enregistrer les notes", command=lambda: self.save_notes(s)
        ).pack(side="bottom", anchor="e", padx=10, pady=10)
        grid = customtkinter.CTkScrollableFrame(self.detail)
        grid.pack(fill="both", expand=True, padx=10, pady=5)

        headers = ("Matière", "Coeff.") + EVALS + ("Moyenne",)
        for col, text in enumerate(headers):
            customtkinter.CTkLabel(grid, text=text, font=("Open Sans", 14, "bold")).grid(
                row=0, column=col, padx=6, pady=4, sticky="w" if col == 0 else "")
        for i, (matter, grades) in enumerate(s.record.items(), start=1):
            customtkinter.CTkLabel(grid, text=matter, font=FONT).grid(
                row=i, column=0, padx=6, pady=3, sticky="w")
            customtkinter.CTkLabel(grid, text=str(grades["Coeff"])).grid(row=i, column=1, padx=6)
            for col, ev in enumerate(EVALS, start=2):
                entry = customtkinter.CTkEntry(grid, width=60, justify="center")
                if grades[ev] != "":
                    entry.insert(0, f"{grades[ev]:.2f}")
                entry.grid(row=i, column=col, padx=4, pady=3)
                self.entries[(matter, ev)] = entry
            m = matter_average(grades)
            customtkinter.CTkLabel(grid, text="—" if m is None else f"{m:.2f}").grid(
                row=i, column=len(EVALS) + 2, padx=6)

    # ---------- actions ----------
    def select(self, key):
        self.selected = key
        self.render_list()
        self.render_detail()

    def save_notes(self, student):
        errors = []
        for (matter, ev), entry in self.entries.items():
            msg = student.input_note(matter, ev, entry.get().strip())
            if not msg.startswith("Note"):      # "Note ajoutée..." / "Note effacée"
                errors.append(f"{matter} / {ev} : {msg}")
        if errors:
            messagebox.showwarning("Notes invalides", "\n".join(errors))
        self.render_list()
        self.render_detail()

    def new_student(self):
        if not self.school.classes:
            messagebox.showwarning("Élève", "Crée d'abord une classe dans « Nos classes ».")
            return

        def submit(data):
            for key, label in (("matricule", "Le matricule"), ("surname", "Le nom"),
                               ("name", "Le prénom"), ("date", "La date de naissance")):
                if not data[key]:
                    return f"{label} est obligatoire."
            classe = self.school.classes[data["classe"]]
            msg = classe.add_student(data["matricule"], data["surname"], data["name"],
                                     data["date"], data["sex"])
            if "succès" not in msg:
                return msg
            self.class_filter.set(self.ALL)
            self.search.delete(0, "end")
            self.selected = (classe.name, data["matricule"])
            self.refresh()

        FormDialog(self, "Nouvel élève", [
            ("classe", "Classe", list(self.school.classes)),
            ("matricule", "Matricule"),
            ("surname", "Nom"),
            ("name", "Prénom"),
            ("date", "Naissance (jj/mm/aaaa)"),
            ("sex", "Sexe", ["M", "F"]),
        ], submit)

    def edit_student(self):
        classe, s = self.find(self.selected)

        def submit(data):
            for key, label in (("surname", "Le nom"), ("name", "Le prénom"),
                               ("date", "La date de naissance")):
                if not data[key]:
                    return f"{label} est obligatoire."
            new_id = data["surname"].upper().strip() + " " + data["name"].lower().strip()
            if any(o.id == new_id and o is not s for o in classe):
                return f"L'élève {new_id} est déjà inscrit en {classe.name}."
            s.update(data["surname"], data["name"], data["date"], data["sex"])
            self.refresh()

        FormDialog(self, "Modifier l'élève", [
            ("surname", "Nom"),
            ("name", "Prénom"),
            ("date", "Naissance (jj/mm/aaaa)"),
            ("sex", "Sexe", ["M", "F"]),
        ], submit, initial={"surname": s.surname, "name": s.name, "date": s.date, "sex": s.sex})

    def delete_student(self):
        classe, s = self.find(self.selected)
        if messagebox.askyesno("Supprimer", f"Supprimer {s.id} de {classe.name} ?"):
            classe.remove_student(matricule=s.matricule)
            self.selected = None
            self.refresh()

class TeachersView(View):
    title = "Nos enseignants"

    def __init__(self, master, school):
        super().__init__(master, school)
        self.selected = None          # id de l'enseignant

        customtkinter.CTkButton(
            self.header, text="+ Nouvel enseignant", font=FONT, command=self.new_teacher
        ).pack(side="right", padx=15)
        self.search = customtkinter.CTkEntry(
            self.header, placeholder_text="Rechercher (nom, prénom, spécialité)", width=280)
        self.search.pack(side="right", padx=5)
        self.search.bind("<KeyRelease>", lambda e: self.render_list())

        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)
        self.body.rowconfigure(1, weight=1)
        self.list_frame = customtkinter.CTkScrollableFrame(self.body)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.detail = customtkinter.CTkFrame(self.body)
        self.detail.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    def filtered(self):
        query = self.search.get().strip().lower()
        for t in self.school.teachers.values():
            if query and query not in f"{t.id} {t.speciality}".lower():
                continue
            yield t

    # ---------- affichage ----------
    def refresh(self):
        if self.selected not in self.school.teachers:
            self.selected = None
        self.render_list()
        self.render_detail()

    def render_list(self):
        clear(self.list_frame)
        headers = ("Nom", "Prénom", "Spécialité", "Contact", "Affectations")
        for col, text in enumerate(headers):
            self.list_frame.columnconfigure(col, weight=1)
            customtkinter.CTkLabel(
                self.list_frame, text=text, font=("Open Sans", 14, "bold"), anchor="w"
            ).grid(row=0, column=col, padx=8, pady=4, sticky="ew")
        count = 0
        for i, t in enumerate(self.filtered(), start=1):
            values = (t.surname, t.name, t.speciality, t.contact,
                      str(len(self.school.assignments(t))))
            color = ACTIVE if t.id == self.selected else "transparent"
            for col, text in enumerate(values):
                label = customtkinter.CTkLabel(
                    self.list_frame, text=text, fg_color=color, anchor="w")
                label.grid(row=i, column=col, padx=2, pady=1, sticky="ew")
                label.bind("<Button-1>", lambda e, k=t.id: self.select(k))
            count += 1
        if count == 0:
            customtkinter.CTkLabel(self.list_frame, text="Aucun enseignant trouvé").grid(
                row=1, column=0, columnspan=5, pady=10)

    def render_detail(self):
        clear(self.detail)
        teacher = self.school.teachers.get(self.selected)
        if teacher is None:
            customtkinter.CTkLabel(
                self.detail, text="Sélectionne un enseignant pour voir ses affectations"
            ).pack(expand=True)
            return

        top = customtkinter.CTkFrame(self.detail, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))
        customtkinter.CTkLabel(
            top, text=f"{teacher.surname.upper()} {teacher.name}", font=("Open Sans", 18, "bold")
        ).pack(side="left")
        customtkinter.CTkButton(
            top, text="Supprimer", width=100, fg_color=DANGER, command=self.delete_teacher
        ).pack(side="right")
        customtkinter.CTkButton(
            top, text="Modifier", width=100, command=self.edit_teacher
        ).pack(side="right", padx=10)

        customtkinter.CTkLabel(
            self.detail, text=f"Spécialité : {teacher.speciality}  ·  Contact : {teacher.contact}"
        ).pack(anchor="w", padx=10, pady=(0, 10))

        customtkinter.CTkLabel(
            self.detail, text="Affectations", font=("Open Sans", 14, "bold")
        ).pack(anchor="w", padx=10)
        rows = customtkinter.CTkScrollableFrame(self.detail)
        rows.pack(fill="both", expand=True, padx=10, pady=5)
        assignments = self.school.assignments(teacher)
        if not assignments:
            customtkinter.CTkLabel(
                rows, text="Aucune affectation (à faire depuis « Nos classes », onglet Enseignants)"
            ).pack(anchor="w", pady=5)
        for classe_name, matter in assignments:
            customtkinter.CTkLabel(rows, text=f"{classe_name}  —  {matter}", font=FONT).pack(
                anchor="w", padx=5, pady=2)

    # ---------- actions ----------
    def select(self, key):
        self.selected = key
        self.render_list()
        self.render_detail()

    def new_teacher(self):
        def submit(data):
            for key, label in (("surname", "Le nom"), ("name", "Le prénom")):
                if not data[key]:
                    return f"{label} est obligatoire."
            msg = self.school.add_teacher(
                data["surname"], data["name"], data["speciality"], data["contact"])
            if "ajouté" not in msg:
                return msg
            self.search.delete(0, "end")
            self.selected = data["surname"].upper().strip() + " " + data["name"].lower().strip()
            self.refresh()

        FormDialog(self, "Nouvel enseignant", [
            ("surname", "Nom"),
            ("name", "Prénom"),
            ("speciality", "Spécialité"),
            ("contact", "Contact"),
        ], submit)

    def edit_teacher(self):
        teacher = self.school.teachers[self.selected]

        def submit(data):
            for key, label in (("surname", "Le nom"), ("name", "Le prénom")):
                if not data[key]:
                    return f"{label} est obligatoire."
            msg = self.school.update_teacher(
                teacher.id, data["surname"], data["name"], data["speciality"], data["contact"])
            if "modifié" not in msg:
                return msg
            self.selected = teacher.id       # l'id a pu changer avec le nom
            self.refresh()

        FormDialog(self, "Modifier l'enseignant", [
            ("surname", "Nom"),
            ("name", "Prénom"),
            ("speciality", "Spécialité"),
            ("contact", "Contact"),
        ], submit, initial={"surname": teacher.surname, "name": teacher.name,
                            "speciality": teacher.speciality, "contact": teacher.contact})

    def delete_teacher(self):
        teacher = self.school.teachers[self.selected]
        count = len(self.school.assignments(teacher))
        extra = f" Il sera retiré de {count} affectation(s)." if count else ""
        if messagebox.askyesno("Supprimer", f"Supprimer {teacher.id} ?{extra}"):
            self.school.remove_teacher(teacher.id)
            self.selected = None
            self.refresh()

class InfoView(View):
    title = "À propos"


class StudentsGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion scolaire")
        self.minsize(900, 600)

        self.school = School()
        self.school.load()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nav = NavBar(self, self.show_view, self.on_close)
        self.nav.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.views = {
            "home": HomeView(self.container, self.school),
            "classes": ClassesView(self.container, self.school),
            "students": StudentsView(self.container, self.school),
            "teachers": TeachersView(self.container, self.school),
            "info": InfoView(self.container, self.school),
        }
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
            view.navigate = self.show_view
        self.show_view("home")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_view(self, key):
        view = self.views[key]
        view.refresh()
        view.tkraise()
        self.nav.set_active(key)

    def on_close(self):
        self.school.save()
        self.destroy()


if __name__ == "__main__":
    app = StudentsGUI()
    app.mainloop()