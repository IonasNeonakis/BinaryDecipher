import androguard
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import androguard.misc

def inputFile(apk):
    a = androguard.misc.AnalyzeAPK(apk)[0]
    print(a)
    print("Nom de 1\'application : ",a.get_app_name())
    print("Permissions : ",a.get_permissions())
    print("Activité principale:\n ",a.get_main_activity())
    for act in a.get_activities():
        print("Activity:", act)
        print("Declares intent filters:\n", a.get_intent_filters('activity', act))
    for ser in a.get_services():
        print("Service:", ser)
        print("Declares intent filters:\n", a.get_intent_filters('service', ser))
    for rec in a.get_receivers():
        print("Activity:", rec)
        print("Declares intent filters:\n", a.get_intent_filters('receiverfl', rec))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputFile("../apk/app-debug.apk")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
