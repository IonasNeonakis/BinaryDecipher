import androguard

from src.Instruction import Instruction
from src.Methode import Methode

from io import StringIO
from contextlib import redirect_stdout
import output_rapport

class Analyse:
    def __init__(self, apk_analisee, class_name):
        self._methodes = []
        self._apk_analisee = apk_analisee
        self._class_name = class_name

    def analyse_1(self, doitPrint, error_string_manager):
        methode_rencontre = []  # On stockera les methodes de la classe
        for classdef in self._apk_analisee[1]:  # Pour toutes les classes de l'APK
            c = classdef.get_class(self._class_name)  # On get la classe avec le nom souhaité
            if c:  # Si on a quelque chose, alors c'est la bonne classe
                for m in c.get_methods():  # Pour toutes ses méthodes
                    curr_method = Methode(m, self._class_name, error_string_manager)  # On créer une instance de Methode
                    curr_method.set_informations(m.get_information())  # On set les informations de base
                    curr_method.set_name(m.get_name())
                    curr_method.set_nb_reg(m.get_information().get("registers")[1] + 1 + len(
                        m.get_information().get("params", [])))  # On récupère le nombre de registre
                    curr_method_instr = []  # Cette liste contiendra toutes les instructions de la methode (instance d'Instruction)
                    for instruction in list(m.get_instructions()):  # Pour chacunes des instructions de la methode
                        instr = Instruction(instruction)  # On l'instancie dans l'objet Instruction
                        if instr._string is None:  # Si ce type d'instruction n'est pas gérer
                            print('\033[91m' +
                                  instruction.get_name() + " n'est pas prise en compte \033[0m")  # On l'affiche pour qu'on puisse l'ajouter
                            curr_method_instr.append(instr)
                        else:
                            curr_method_instr.append(instr)  # Sinon on ajoute l'instruction a la liste
                    curr_method.set_instructions(
                        curr_method_instr)  # On set la liste des instructions dans l'attribut de l'instance de la méthode
                    methode_rencontre.append(
                        curr_method)  # On ajoute la methode instanciée à la liste des méthodes de la classe
                for methode in methode_rencontre:  # Pour chacunes des méthodes de la classe
                    if doitPrint:
                        print("\n")
                        print(methode.print())
                        print("Description des instructions de la méthode par androguard :")
                        methode.get_androguard_method().show()
                    methode.compute_succ()  # On définit les offset des instructions et on calcule le successeur de chacunes
                    #print(methode.get_succ())
                    is_valide = methode.evaluate(doitPrint)  # On évalue la méthode
                    self._methodes.append(methode)
                    if not is_valide:
                        if doitPrint:
                            if methode.print():
                                error_string_manager.add_error_string("\n" + methode.print())
                return True
        return "Class not found"

    def analyse2(self):
        if not self._methodes:
            self.analyse_1(False, None)

        for methode in self._methodes:
            instructions = methode._instructions
            for instruction in instructions:
                pass

    def analyse3(self):
        if not self._methodes:
            self.analyse_1(False, None)
        a, d, dx = self._apk_analisee

        permissions = a.get_permissions()
        print("PERMISSIONS DEMANDÉES : ", permissions)

        declared_permissions = a.declared_permissions
        print("PERMISSIONS DECLARÉES : ", declared_permissions)

        for methode in self._methodes:
            tmp = methode.get_tmp_map_register()
            #print(tmp)
