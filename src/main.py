import androguard
import androguard.misc
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
    methode_rencontrer = []
    apk_analisee = androguard.misc.AnalyzeAPK(apk_file)
    main = "L" + class_name.replace(".", "/") + ";"
    for classdef in apk_analisee[1]:
        c = classdef.get_class(main)
        if c:
            break
    for m in c.get_methods():
        instructions = []
        nb_reg = m.get_information().get("registers")[1] + 1 + len(m.get_information().get("params", []))
        offset = 0
        for instr in list(m.get_instructions()):
            instructions.append((offset, instr.get_name(), instr.get_output()))
            offset += instr.get_length()
        methode = Methode()
        methode.set_instructions(instructions)
        methode.set_nb_reg(nb_reg)
        methode.set_informations(m.get_information())
        methode_rencontrer.append(methode)
    for m in methode_rencontrer:
        m.print()
        message, is_valide = m.evaluate()
        if not is_valide:
            return message
    return message


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    input_file("../apk/app-debug.apk")
    analyse_1("../apk/app-debug.apk", "fr.univ.secuapp.MainActivity")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
