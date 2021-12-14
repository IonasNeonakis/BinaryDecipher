import tkinter
from tkinter import *
from tkinter import filedialog, ttk

import androguard

from src.analyses import analyse_1


class GUI():
    def __init__(self):
        self._root = Tk()  # Init de la fenetre principal
        self._root.resizable(False, False);
        frame = ttk.Frame(self._root, padding=(24, 24, 24, 24));
        frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self._titleLabel = Label(frame, text="BinaryDecipher")  # Titre
        self._subtitleLabel = Label(frame, text="Par LegitIT")  # Sous titre
        self._titleLabel.grid(column=1, row=0, sticky=(N, S, E, W));
        self._subtitleLabel.grid(column=1, row=1, sticky=(N, S, E, W));

        self._browseLabel = Label(frame, text="Choix du fichier APK")
        self._browseLabel.grid(column=0, row=2, sticky=(N, S, E, W));
        self._apkName = "En attente de l'APK"
        self._apkNameLabel = Label(frame, text=self._apkName).grid(column=0, row=3, sticky=(N, S, E, W));
        Button(frame, text="Parcourir", command=self.browse).grid(column=0, row=4, sticky=(N, S, E, W));

        self._liste_class = ["Choisir une APK d'abord"]
        self._default = StringVar()
        self._default.set(self._liste_class[0])
        self._optionClass = OptionMenu(frame, self._default, *self._liste_class)
        self._optionClass.grid(column=1, row=2, sticky=(N, S, E, W));

        self._analyse = tkinter.IntVar()
        Label(frame, text="Choix analyse").grid(column=2, row=2, sticky=(N, S, E, W));
        Radiobutton(frame, text='Analyse 1', variable=self._analyse, value=1).grid(column=2, row=3,
                                                                                   sticky=(N, S, E, W));
        Radiobutton(frame, text='Analyse 2', variable=self._analyse, value=2).grid(column=2, row=4,
                                                                                   sticky=(N, S, E, W));
        Radiobutton(frame, text='Analyse 3', variable=self._analyse, value=3).grid(column=2, row=5,
                                                                                   sticky=(N, S, E, W));

        Button(frame, text="Analyser !", command=self.start_analyse).grid(column=2, row=6, sticky=(N, S, E, W));

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
            initialdir='../apk/',
            title="Select a File",
            filetypes=(("APK",
                        "*.apk*"),
                       ("all files",
                        "*.*"))).name
        self._apkNameLabel['text'] = self._apkName
        self.load_class()
