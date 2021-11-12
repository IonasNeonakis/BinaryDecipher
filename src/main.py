import androguard
import androguard.misc

from src.Instruction import Instruction
from src.Methode import Methode


def input_file(apk):
    a, d, dx = androguard.misc.AnalyzeAPK(apk)
    print(a)
    print("Nom de 1\'application : ", a.get_app_name())
    print("Permissions : ", a.get_permissions())
    print("Activité principale:\n ", a.get_main_activity())
    for act in a.get_activities():
        print("Activity:", act)
        print("Declares intent filters:\n", a.get_intent_filters('activity', act))
    for ser in a.get_services():
        print("Service:", ser)
        print("Declares intent filters:\n", a.get_intent_filters('service', ser))
    for rec in a.get_receivers():
        print("Activity:", rec)
        print("Declares intent filters:\n", a.get_intent_filters('receiverfl', rec))
    print("\n", "=" * 20)
    print("Récupération des classes DEX : \n")
    main = "L" + a.get_main_activity().replace(".", "/") + ";"
    for classdef in d:
        c = classdef.get_class(main)
        if c:
            break
    print("\n", "=" * 20, "\n", c)
    for methods in c.get_methods():
        methods.show()
        print(methods.get_information())
        print(methods.get_length() * 2)
        print("nb reg : ",
              methods.get_information().get("registers")[1] + 1 + len(methods.get_information().get("params", [])))

        for instr in list(methods.get_instructions()):
            print("length ", instr.get_length())
            print("literaux ", instr.get_literals())
        #     print("output " ,instr.get_output())


def analyse_1(apk_file, class_name):
    methode_rencontre = []  # On stockera les methodes de la classe
    apk_analisee = androguard.misc.AnalyzeAPK(apk_file)  # APK à analiser
    main = "L" + class_name.replace(".", "/") + ";"  # Nom de la classe à traiter
    for classdef in apk_analisee[1]:  # Pour toutes les classes de l'APK
        c = classdef.get_class(main)  # On get la classe avec le nom souhaité
        if c:  # Si on a quelque chose, alors c'est la bonne classe
            for m in c.get_methods():  # Pour toutes ses méthodes
                curr_method = Methode()  # On créer une instance de Methode
                curr_method.set_informations(m.get_information())  # On set les informations de base
                curr_method.set_nb_reg(m.get_information().get("registers")[1] + 1 + len(
                    m.get_information().get("params", [])))  # On récupère le nombre de registre
                curr_method_instr = []  # Cette liste contiendra toutes les instructions de la methode (instance d'Instruction)
                for instruction in list(m.get_instructions()):  # Pour chacunes des instructions de la methode
                    instr = Instruction(instruction)  # On l'instancie dans l'objet Instruction
                    if instr._string is None:  # Si ce type d'instruction n'est pas gérer
                        print(
                            instruction.get_name() + " n'est pas prise en compte")  # On l'affiche pour qu'on puisse l'ajouter
                    else:
                        curr_method_instr.append(instr)  # Sinon on ajoute l'instruction a la liste
                curr_method.set_instructions(
                    curr_method_instr)  # On set la liste des instructions dans l'attribut de l'instance de la méthode
                methode_rencontre.append(
                    curr_method)  # On ajoute la methode instanciée à la liste des méthodes de la classe
            for methode in methode_rencontre:  # Pour chacunes des méthodes de la classe
                methode.compute_succ()  # On définit les offset des instructions et on calcule le successeur de chacunes
                is_valide = methode.evaluate()  # On évalue la methode
                if not is_valide:
                    print("Erreur dans la methode : \n")
                    methode.print()
                    return False
            return True
    return "Class not found"


if __name__ == '__main__':
    # input_file("../apk/app-debug.apk")
    analyse_1("../apk/app-debug.apk", "fr.univ.secuapp.MainActivity")
