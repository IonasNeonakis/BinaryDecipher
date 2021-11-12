class Methode():
    def __init__(self):
        self._nb_reg = None
        self._informations = None
        self._instructions = []
        self._succ = {}

    def set_corps(self, corps):
        self._corps = corps

    def set_nb_reg(self, nb_reg):
        self._nb_reg = nb_reg

    def set_instructions(self, instructions):
        self._instructions = instructions

    def set_informations(self, informations):
        self._informations = informations

    def compute_succ(self):
        offset = 0
        for instr in self._instructions:
            if instr.get_name() == "":  # Gerer les cas ou la destination n'est pas explicite (comme les if ou les goto)
                pass
                # destination = offset + valeur a déterminer (par exemple le goto a une destination specifique
            elif instr.get_name()[:2] == "if":
                destination = offset + instr.get_destination()
            else:
                destination = offset + instr.get_length()  # Juste l'instruction d'après (car c'est une instruction sequentiel
            self._succ[offset] = (instr, destination)
            offset += instr.get_length()  # Mise à jour de l'offset (adresse de l'instruction suivante

    def evaluate(self):
        return True

    def print(self):
        print("Methode {\n    Informations : ", self._informations, "\n    Nombre de registre : ", self._nb_reg,
              "\n    Instruction : ", self._instructions, "\n}")
