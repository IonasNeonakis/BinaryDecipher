import codecs
import os


# classe qui gère une string qui "collecte" les erreurs
class ErrorStringManager:
    def __init__(self):
        self.error_string = ""

    def add_error_string(self, error_string):
        if error_string is not None:
            self.error_string += error_string + "\n"

    def get_error_string(self):
        return self.error_string

    def output_error_report(self, class_name):
        make_sure_out_folder_exists()
        f = codecs.open(f"../out/{class_name.replace('/', '.')}-error.report", "w", "utf-8")
        f.write(self.error_string)
        f.close()
        self.error_string = ""


def make_sure_out_folder_exists():
    path = "../out/"
    if not os.path.exists(path):
        os.makedirs(path)


def output_success_report(class_name, buffer):
    make_sure_out_folder_exists()
    f = codecs.open(f"../out/{class_name.replace('/', '.')}.report", "w", "utf-8")
    f.write(buffer.getvalue())
    f.close()
