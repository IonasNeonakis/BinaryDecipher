import androguard
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import androguard.misc

map_methods = {}
map_instructions = {}


def inputFile(apk):
    analyzedAPK = androguard.misc.AnalyzeAPK(apk)
    a = analyzedAPK[0]
    print("Infos générales : \n")
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
    d = analyzedAPK[1]
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


# def ŝeudo eijf:
#     nosMethodes = []
#     pour chaque methode de la classe:
#         instructions = []
#         nbreg = get le nombre de registre
#         offset = 0
#         pour chaque instructions:
#             corps = instr.get_output()
#             instructions.append((offset, corps))
#             on incr offset += instr.get_length()
#         m = Methode()
#         m.setInstr(instructions)
#         m.setnbRegister(nbreg)
#         nosMethodes.append(m)
#     for m in nosMethodes:
#         strOutput, bool = m.evaluate()
#         if !bool:
#             strOutput > Crapport
#     "fini succès" > Crapport


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputFile("../apk/app-debug.apk")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
