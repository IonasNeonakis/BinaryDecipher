class Methode():
    def __init__(self):
        self._nb_reg = None
        self._informations = None
        self._instructions = []

    def set_corps(self, corps):
        self._corps = corps

    def set_nb_reg(self, nb_reg):
        self._nb_reg = nb_reg

    def set_instructions(self, instructions):
        self._instructions = instructions

    def set_informations(self, informations):
        self._informations = informations

    def evaluate(self):
        return "message d'erreur", True

    def print(self):
        print("Methode {\n    Informations : ", self._informations, "\n    Nombre de registre : ", self._nb_reg, "\n    Instruction : ", self._instructions, "\n}")
