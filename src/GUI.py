import tkinter
from tkinter import *
from tkinter import filedialog

import androguard

from src.analyses import analyse_1


class GUI():
    def __init__(self):
        self._root = Tk()  # Init de la fenetre principal

        # Les différentes sections
        header = Frame(self._root).pack()
        selection_APK = Frame(self._root).pack()
        selection_class = Frame(self._root).pack()
        selection_analyse = Frame(self._root).pack()

        self._titleLabel = Label(header, text="BinaryDecipher")  # Titre
        self._subtitleLabel = Label(header, text="Par LegitIT")  # Sous titre
        self._titleLabel.pack()
        self._subtitleLabel.pack()

        self._browseLabel = Label(selection_APK, text="Choix du fichier APK")
        self._browseLabel.pack()
        self._apkName = "En attente de l'APK"
        Button(selection_APK, text="Parcourir", command=self.browse).pack()
        self._apkNameLabel = Label(selection_APK, text=self._apkName)
        self._apkNameLabel.pack()

        self._liste_class = ["Choisir une APK d'abord"]
        self._default = StringVar()
        self._default.set(self._liste_class[0])
        self._optionClass = OptionMenu(selection_class, self._default, *self._liste_class)
        self._optionClass.pack()

        self._analyse = tkinter.IntVar()
        Label(selection_analyse, text="Choix analyse").pack()
        Radiobutton(selection_analyse, text='Analyse 1', variable=self._analyse, value=1).pack()
        Radiobutton(selection_analyse, text='Analyse 2', variable=self._analyse, value=2).pack()
        Radiobutton(selection_analyse, text='Analyse 3', variable=self._analyse, value=3).pack()

        Button(self._root, text="Analyser !", command=self.start_analyse).pack()

        mainloop()

    def start_analyse(self):
        print("apk : " + str(self._apkName))
        print("class : " + str(self._default.get()))
        print("analyse : " + str(self._analyse.get()))
        if self._analyse.get() == 1:
            analyse_1(apk_file=str(self._apkName), class_name=str(self._default.get()))

    def load_class(self):
        self._liste_class = []
        apk_analisee = androguard.misc.AnalyzeAPK(self._apkName)  # APK à analiser
        package_name = apk_analisee[0].get_package()
        package_name = "L" + package_name.replace(".", "/")
        for classdef in apk_analisee[1]:  # Pour toutes les classes de l'APK
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
        print("done")

    def browse(self):
        self._apkName = filedialog.askopenfile(
            title="Select a File",
            filetypes=(("APK",
                        "*.apk*"),
                       ("all files",
                        "*.*"))).name
        self._apkNameLabel['text'] = self._apkName
        self.load_class()
