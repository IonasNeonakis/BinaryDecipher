import androguard

from src.Instruction import Instruction
from src.Methode import Methode


def analyse_1(apk_analisee, class_name):
    methode_rencontre = []  # On stockera les methodes de la classe
    for classdef in apk_analisee[1]:  # Pour toutes les classes de l'APK
        c = classdef.get_class(class_name)  # On get la classe avec le nom souhaité
        if c:  # Si on a quelque chose, alors c'est la bonne classe
            if c.get_superclassname() == "Ljava/lang/Object;":  # vérification de la super classe de la classe actuelle
                # si la classe parent est Object c'est que c'est une classe de base
                classe_parent = None  # La classe actuelle n'"extends" pas une autre classe intéressante
            else:
                classe_parent = c.get_superclassname()  # La classe actuelle "extends" une autre classe
            for m in c.get_methods():  # Pour toutes ses méthodes
                curr_method = Methode(m, class_name)  # On créer une instance de Methode
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
                    elif instr.get_name()[:6] == "invoke":  # on doit stocker le type de l'invoke car il est suivi d'un move-result, qui mettera le résultat de l'invoke dans un registre
                        # type_dernier_invoke = instr.get_type()
                        curr_method_instr.append(instr)
                    elif instr.get_name()[:4] == "move":  # on récupère le type du dernier invoke et on le met dans le type de l'instruction
                        # instr.set_type(type_dernier_invoke)
                        # type_dernier_invoke = None
                        curr_method_instr.append(instr)
                    else:
                        curr_method_instr.append(instr)  # Sinon on ajoute l'instruction a la liste
                curr_method.set_instructions(
                    curr_method_instr)  # On set la liste des instructions dans l'attribut de l'instance de la méthode
                methode_rencontre.append(
                    curr_method)  # On ajoute la methode instanciée à la liste des méthodes de la classe
            for methode in methode_rencontre:  # Pour chacunes des méthodes de la classe
                methode.get_androguard_method().show()
                methode.compute_succ()  # On définit les offset des instructions et on calcule le successeur de chacunes
                print(methode.get_succ())
                methode.evaluate()
                is_valide = True#methode.evaluate()  # On évalue la methode
                if not is_valide:
                    print("Erreur dans la methode : \n")
                    methode.print()
                    return False
            return True
    return "Class not found"
