class Instruction():
    def __init__(self, instr):
        name = instr.get_name()
        self._name = name
        if name == 'const-string':
            cm = instr.cm
            self._register = [instr.AA]
            self._string = "instruction " + self._name + " enregistre dans v" + str(
                self._register[0]) + " la valeur " + str(cm.get_string(instr.BBBB))
        if name[:6] == 'invoke':
            cm = instr.cm
            if instr.A == 0:
                self._register = []
            elif instr.A == 1:
                self._register = [instr.C]
            elif instr.A == 2:
                self._register = [instr.C, instr.D]
            elif instr.A == 3:
                self._register = [instr.C, instr.D, instr.E]
            elif instr.A == 4:
                self._register = [instr.C, instr.D, instr.E, instr.F]
            elif instr.A == 5:
                self._register = [instr.C, instr.D, instr.E, instr.F, instr.G]
            self._type = cm.get_type(instr.BBBB)
            self._field = None
            self._method = cm.get_method(instr.BBBB)
            self._string = "instruction " + self._name + " appel la methode : " + str(
                self._method) + " et utilise les registres : "
            for i in range(len(self._register)):
                self._string += " v" + str(self._register[i])
        if name[:4] == 'move':
            self._register = [instr.AA]
            self._string = "instruction " + self._name + " déplace le resultat de l'invoke-kind le plus récent dans v" + str(
                self._register[0])

    def to_string(self):
        print(self._string)
        # print(f'instruction {self._name}, enregistre dans v{self._register}', 'la valeur', self._string, " de type : ", self._type, " field : ", self._field)
