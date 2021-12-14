from androguard.core.bytecodes.dvm import Instruction23x


class Instruction():
    def __init__(self, instr):
        name = instr.get_name()
        self._length = instr.get_length()
        self._name = name
        if name == 'const-string':
            cm = instr.cm
            self._register = [instr.AA]
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} la valeur" \
                           f"{cm.get_string(instr.BBBB)}"
        elif name[:6] == 'invoke':
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
            self._string = f"instruction {self._name} appelle la methode : {self._method} et utilise les registres : "
            for i in range(len(self._register)):
                self._string += f" v{self._register[i]}"
        elif name[:4] == 'move':
            self._register = [instr.AA]
            self._string = f"instruction {self._name} déplace le résultat de l'invoke-kind le plus récent dans" \
                           f"v{self._register[0]}"
        elif name == 'return-void':
            self._string = f"instruction : {name} ne fait rien (normal)"
        elif name == 'const':
            try:
                self._register = [instr.AA]
                self._value = [instr.BBBBBBBB]
            except:
                self._register = [instr.A]

            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} le/les litteraux suivant :" \
                           f" {instr.get_literals()}"
        elif name == 'check-cast':
            self._type = instr.cm.get_type(instr.BBBB)
            self._string = f"instruction {name} vérifie que la valeur du registre v{instr.AA} soit de type {self._type}"
        elif name[:2] == 'if':  # si on est là ,if-eq,if-ne,if-lt,if-ge,if-gt,if-le
            _, nom = name.split('-')
            if len(nom) == 2:
                self._register = [instr.A, instr.B]
                self._destination = instr.CCCC * 2

            else:  # si on est là ,if-eqz,if-nez,if-ltz,if-gez,if-gtz,if-lez
                self._register = [instr.AA]
                self._destination = instr.BBBB * 2
            self._string = f"instruction : {name} vérifie les valeurs de v : {self._register} en fonction du test" \
                           f"specifié. Et si le test est valide renvoie à l'adresse : {self._destination} bits suivant"
        elif name == 'new-instance':
            self._type = instr.cm.get_type(instr.BBBB)
            self._register = [instr.AA]
            self._string = f"instruction : {name} crée une instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"
        elif name == 'const-class':
            self._register = [instr.AA]
            self._type = instr.cm.get_type(instr.BBBB)
            self._string = f"instruction : {name} déplace l'instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"
        elif name == 'const/4':
            self._register = [instr.A]
            self._value = instr.B
            self._string = f"instruction : {name} met la valeur {self._value} dans le registre {self._register[0]}"
        elif name == 'const/16':
            self._register = [instr.AA]
            self._value = instr.BBBB
            self._string = f"instruction : {name} met la valeur {self._value} dans le registre {self._register[0]}"
        elif name == 'goto':
            self._destination = instr.AA * 2
            self._string = f"instruction : {name} saute à l'offset {self._destination}"
        elif name in ['add-int', 'sub-int', 'mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int', 'shl-int',
                      'shr-int', 'ushr-int',
                      'add-long', 'sub-long', 'mul-long', 'div-long', 'rem-long', 'and-long', 'or-long', 'xor-long',
                      'shl-long', 'shr-long', 'ushr-long', 'add-float', 'sub-float', 'mul-float', 'div-float',
                      'rem-float', 'add-double', 'sub-double', 'mul-double', 'div-double', 'rem-double']:  # Binop
            operator, type = self._name.split("-")
            self._register = [instr.AA, instr.BB, instr.CC]
            self._string = f"instruction : {name} execute l'opération {operator} entre les valeurs de" \
                           f"v{self._register[1]} et v{self._register[2]} et le stocke dans {self._register[0]}"

        elif name[-4:] == 'lit8' or name[-5:] == 'lit16':
            operator, rest = self._name.split('-')
            _, litvalue = rest.split('/')
            if litvalue == 'lit8':
                self._register = [instr.AA, instr.BB, instr.CC]
            elif litvalue == 'lit16':
                self._register = [instr.A, instr.B, instr.CCCC]
            self._string = f"instruction : {name} execute l'opération {operator} entre les valeurs de" \
                           f"v{self._register[1]} et la valeur entiere {self._register[2]} et le stocke dans" \
                           f"{self._register[0]}"

        elif name[-5:] == '2addr':  # exemple sub-int/2addr
            operator, _ = self._name.split("-")
            self._register = [instr.A, instr.B]
            self._string = f"instruction : {name} execute l'opération {operator} entre les valeurs de" \
                           f"v{self._register[0]} et v{self._register[1]} et le stocke dans {self._register[0]}"

        elif name == 'return':
            self._register = [instr.AA]
            self._string = f"instruction : {name} renvoie la valeur contenue dans le registre v{self._register[0]}"
        else:
            self._string = None

    def __repr__(self):
        return self._string

    def get_destination(self):
        return self._destination

    def get_register(self):
        return self._register

    def get_name(self):
        return self._name

    def get_length(self):
        return self._length

    def get_value(self):
        return self._value

    def to_string(self):
        print(self._string)
        # print(f'instruction {self._name}, enregistre dans v{self._register}', 'la valeur', self._string, " de type : ", self._type, " field : ", self._field)
