import threading
import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import androguard
from io import StringIO
from contextlib import redirect_stdout

from src import output_rapport
from src.analyses import *


class GUI():
    def __init__(self):
        self.app = tkinter.Tk()
        self.app.title("BinaryDecipher")
        self._apkName = ''
        self.app.minsize(274, 570)

        # Creation des widgets
        self.imgFile = Image.open("../logo/logo_large.png")
        self.img = ImageTk.PhotoImage(self.imgFile.resize((self.imgFile.width//6, self.imgFile.height//6)))
        self.panel = tkinter.Label(self.app, image=self.img)
        self.mainframe = tkinter.LabelFrame(self.app, text="BinaryDecipher")

        self.creditframe = tkinter.LabelFrame(self.mainframe, text="Crédit")
        self.creditLabel1 = tkinter.Label(self.creditframe, text="Pierre-Louis Bertrand")
        self.creditLabel2 = tkinter.Label(self.creditframe, text="Ionas Neonakis")
        self.creditLabel3 = tkinter.Label(self.creditframe, text="Thomas Quetier")
        self.creditLabel4 = tkinter.Label(self.creditframe, text="Samir Toularhmine")

        self.choixduprogframe = tkinter.LabelFrame(self.mainframe, text="Analyse")
        self.label1 = tkinter.Label(self.choixduprogframe, text="Choix de l'APK")
        self.btnBrowse = tkinter.Button(self.choixduprogframe, text='Parcourir', command=self.browse)

        self.label3 = tkinter.Label(self.choixduprogframe, text="Classe à analyser")
        self._liste_class = ["Choisir une APK d'abord"]
        self._default = tkinter.StringVar()
        self._default.set(self._liste_class[0])
        self._optionClass = tkinter.OptionMenu(self.choixduprogframe, self._default, *self._liste_class)

        self.label2 = tkinter.Label(self.choixduprogframe, text="Type d'analyse")
        vals = [1, 2, 3]
        etiqs = ['Analyse 1', 'Analyse 2', 'Analyse 3']
        self.varGr = tkinter.StringVar()
        self.varGr.set(vals[0])
        self.rb = []
        for i in range(3):
            b = tkinter.Radiobutton(self.choixduprogframe, variable=self.varGr, text=etiqs[i], value=vals[i])
            self.rb.append(b)

        self.startbtn = tkinter.Button(self.choixduprogframe, text="Analyser !", command=self.start_analyse, state=tkinter.DISABLED)

        # Affichage des widget
        self.panel.pack(fill="both", expand=1, pady=10, padx=10)
        self.mainframe.pack(expand=1, fill="both", padx=10, pady=10)
        self.choixduprogframe.pack(expand=1, fill="both", pady=10, padx=10)
        self.label1.pack()
        self.btnBrowse.pack(fill="x", padx=10)
        self.label3.pack(fill="x", padx=10)
        self._optionClass.pack(fill="x", padx=10)
        self.label2.pack()
        for radiobtn in self.rb:
            radiobtn.pack()
        self.startbtn.pack(fill="both", pady=10, padx=10)

        self.creditframe.pack(side="bottom", fill="x", pady=10, padx=10)
        self.creditLabel1.pack()
        self.creditLabel2.pack()
        self.creditLabel3.pack()
        self.creditLabel4.pack()

        self.app.mainloop()

    def browse(self):
        self._apkName = filedialog.askopenfile(
            initialdir='../apk/',
            title="Select a File").name
        self.btnBrowse['text'] = self._apkName
        self.load_class()

    def start_analyse(self):
        buffer_stdout = StringIO()
        error_string_manager = output_rapport.ErrorStringManager()
        with redirect_stdout(buffer_stdout):
            print("Rapport d'analyse BinaryDecipher\n")
            print("apk analysée : " + str(self._apkName))
            print("classe analysée : " + str(self._default.get()))
            print("type d'analyse : " + str(self.varGr.get()) + "\n")
            if str(self.varGr.get()) == '1':
                print("Début de l'analyse 1 (vérification de bytecode simple)")

                analyse = Analyse(self.apk_analisee, self._default.get())
                resultat_analyse = analyse.analyse_1(True, error_string_manager)

                if resultat_analyse == "Class not found":
                    print("Class not found")
                else:
                    output_rapport.output_success_report(self._default.get(), buffer_stdout)
                    error_string_manager.output_error_report(self._default.get())
            elif str(self.varGr.get()) == '2':
                print("Début de l'analyse 2 (bonne initialisation des objets)")

                analyse = Analyse(self.apk_analisee, self._default.get())
                resultat_analyse = analyse.analyse_2()

                if resultat_analyse == "Class not found":
                    print("Class not found")
                else:
                    output_rapport.output_success_report(self._default.get(), buffer_stdout)
                    error_string_manager.output_error_report(self._default.get())
            if str(self.varGr.get()) == '3':
                print("Début de l'analyse 3 (extraction des communications)")

                analyse = Analyse(self.apk_analisee, self._default.get())
                resultat_analyse = analyse.analyse3()

                if resultat_analyse == "Class not found":
                    print("Class not found")
                else:
                    output_rapport.output_success_report(self._default.get(), buffer_stdout)
                    error_string_manager.output_error_report(self._default.get())


    def load_class(self):
        self._liste_class = []
        self.apk_analisee = androguard.misc.AnalyzeAPK(self._apkName)  # APK à analiser
        package_name = self.apk_analisee[0].get_package()
        package_name = "L" + package_name.replace(".", "/")
        for classdef in self.apk_analisee[1]:  # Pour toutes les classes de l'APK
            for classe in classdef.get_classes():
                if (classe.get_name()[:len(package_name)] == package_name):
                    classname_a_traiter = classe.get_name().split("/")
                    if not classname_a_traiter[-1] == "R;" and not classname_a_traiter[-1][:2] == "R$" and not \
                            classname_a_traiter[-1] == "BuildConfig;":
                        self._liste_class.append(classe.get_name())

        self._default.set(self._liste_class[0])
        self._optionClass['menu'].delete(0, 'end')
        for c_name in self._liste_class:
            self._optionClass['menu'].add_command(label=c_name, command=tkinter._setit(self._default, c_name))
        self.startbtn['state'] = tkinter.NORMAL


