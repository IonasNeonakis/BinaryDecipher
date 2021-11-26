import tkinter

import androguard
import androguard.misc

from src.GUI import GUI
from src.analyses import analyse_1


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


if __name__ == '__main__':
    #gui = GUI()
    # input_file("../apk/app-debug.apk")
    analyse_1("../apk/app-debug.apk", "Lfr/univ/secuapp/MainActivity;")
    #analyse_1("../apk/fibo.apk", "Lcom/example/fiboapksan/MainActivity;")
