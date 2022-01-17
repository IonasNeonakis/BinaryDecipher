class Instruction:
    def __init__(self, instr):
        # Global attributs
        self._length = instr.get_length()  # Taille de l'instruction
        self._name = instr.get_name()  # Nom de l'instruction
        self._register = []  # Registre utilisé par l'instruction
        self._string_value = None  # Contient le string utilisé par l'instruction
        self._constant = None  # Contient la constante utilisé par l'instruction
        self._type = None  # Contient le type utilisé par l'instruction
        self._method = None  # Contient la méthode utilisé par l'instruction
        self._string = None  # Le str pour print une desc de l'instruction
        self._destination = None  # Destination d'une instruction (dans le cadre d'un branchement)
        self._field = None  # Path vers un ressource (path vers une fonction comme println par exemple)

        if self._name == 'const-string':
            # const-string vAA, string@BBBB
            # A: destination register (8 bits)
            # B: string index
            self._register.append(instr.AA)
            self._string_value = instr.cm.get_string(instr.BBBB)
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} la valeur" \
                           f"{self._string_value}"

        elif self._name in ['move', 'move/from16', 'move/16']:
            if self._name == 'move':
                # move vA, vB
                # A: destination register (4 bits)
                # B: source register (4 bits)
                self._register.extend([instr.A, instr.B])

            elif self._name == 'move/from16':
                # move/from16 vAA, vBBBB
                # A: destination register (8 bits)
                # B: source register (16 bits)
                self._register.extend([instr.AA, instr.BBBB])

            elif self._name == 'move/16':
                # move/16 vAAAA, vBBBB
                # A: destination register (16 bits)
                # B: source register (16 bits)
                self._register.extend([instr.AAAA, instr.BBBB])
            self._string = f"instruction {self._name} déplace dans v{self._register[0]} l'element de v{self._register[1]}"

        elif self._name[:6] == 'invoke':
            # invoke-kind {vC, vD, vE, vF, vG}, meth@BBBB
            # A: argument word count (4 bits)
            # B: method reference index (16 bits)
            # C..G: argument registers (4 bits each)
            if instr.A == 1:
                self._register.append(instr.C)
            elif instr.A == 2:
                self._register.extend([instr.C, instr.D])
            elif instr.A == 3:
                self._register.extend([instr.C, instr.D, instr.E])
            elif instr.A == 4:
                self._register.extend([instr.C, instr.D, instr.E, instr.F])
            elif instr.A == 5:
                self._register.extend([instr.C, instr.D, instr.E, instr.F, instr.G])
            self._method = instr.cm.get_method(instr.BBBB)
            self._string = f"instruction {self._name} appelle la methode : {self._method} et utilise les registres : "
            for i in range(len(self._register)):
                self._string += f" v{self._register[i]}"

        elif self._name == 'move-result':
            # move-result vAA
            # A: destination register (8 bits)
            self._register.append(instr.AA)
            self._string = f"instruction {self._name} déplace le résultat de l'invoke-kind le plus récent dans" \
                           f" v{self._register[0]}"

        elif self._name == 'return-void':
            self._string = f"instruction : {self._name} ne fait rien (normal)"

        elif self._name == 'const':
            # const vAA, #+BBBBBBBB
            # A: destination register (8 bits)
            # B: arbitrary 32-bit constant
            self._register.append(instr.AA)
            self._constant = instr.BBBBBBBB
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} le/les litteraux suivant :" \
                           f" {self._constant}"

        elif self._name == 'check-cast':
            # check-cast vAA, type@BBBB
            # A: reference-bearing register (8 bits)
            # B: type index (16 bits)
            self._type = instr.cm.get_type(instr.BBBB)
            self._register.append(instr.AA)
            self._string = f"instruction {self._name} vérifie que la valeur du registre v{self._register[0]} soit de type {self._type}"

        elif self._name[:2] == 'if':
            # if-test vA, vB, +CCCC
            # 32: if-eq
            #     33: if-ne
            #     34: if-lt
            #     35: if-ge
            #     36: if-gt
            #     37: if-le
            # A: first register to test (4 bits)
            # B: second register to test (4 bits)
            # C: signed branch offset (16 bits)
            _, nom = self._name.split('-')
            if len(nom) == 2:
                self._register.extend([instr.A, instr.B])
                self._destination = instr.CCCC * 2

            else:
                # if-testz vAA, +BBBB
                # 38: if-eqz
                #     39: if-nez
                #     3a: if-ltz
                #     3b: if-gez
                #     3c: if-gtz
                #     3d: if-lez
                # A: register to test (8 bits)
                # B: signed branch offset (16 bits)
                self._register.append(instr.AA)
                self._destination = instr.BBBB * 2
            self._string = f"instruction : {self._name} vérifie les valeurs de v : {self._register[0]} en fonction du test" \
                           f" specifié. Et si le test est valide renvoie à l'adresse : {self._destination} bits suivant"

        elif self._name == 'new-instance':
            # new-instance vAA, type@BBBB
            # A: destination register (8 bits)
            # B: type index
            self._type = instr.cm.get_type(instr.BBBB)
            self._register.append(instr.AA)
            self._string = f"instruction : {self._name} crée une instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"

        elif self._name == 'const-class':
            # const-class vAA, type@BBBB
            # A: destination register (8 bits)
            # B: type index
            self._register.append(instr.AA)
            self._type = instr.cm.get_type(instr.BBBB)
            self._string = f"instruction : {self._name} déplace l'instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"

        elif self._name == 'const/4':
            # const/4 vA, #+B
            # A: destination register (4 bits)
            # B: signed int (4 bits)
            self._register.append(instr.A)
            self._constant = instr.B
            self._string = f"instruction : {self._name} met la valeur {self._constant} dans le registre {self._register[0]}"

        elif self._name == 'const/16':
            # const/16 vAA, #+BBBB
            # A: destination register (8 bits)
            # B: signed int (16 bits)
            self._register.append(instr.AA)
            self._constant = instr.BBBB
            self._string = f"instruction : {self._name} met la valeur {self._constant} dans le registre {self._register[0]}"

        elif self._name == 'goto':
            # goto +AA
            # A: signed branch offset (8 bits)
            self._destination = instr.AA * 2
            self._string = f"instruction : {self._name} saute de {self._destination} offset"

        elif self._name in ['add-int', 'sub-int', 'mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int',
                            'shl-int',
                            'shr-int', 'ushr-int',
                            'add-long', 'sub-long', 'mul-long', 'div-long', 'rem-long', 'and-long', 'or-long',
                            'xor-long',
                            'shl-long', 'shr-long', 'ushr-long', 'add-float', 'sub-float', 'mul-float', 'div-float',
                            'rem-float', 'add-double', 'sub-double', 'mul-double', 'div-double', 'rem-double']:
            # binop vAA, vBB, vCC
            # 90: add-int
            # 91: sub-int
            # [ .... ]
            # A: destination register or pair (8 bits)
            # B: first source register or pair (8 bits)
            # C: second source register or pair (8 bits)
            operator, type = self._name.split("-")
            self._register.extend([instr.AA, instr.BB, instr.CC])
            self._string = f"instruction : {self._name} execute l'opération {operator} entre les valeurs de" \
                           f" v{self._register[1]} et v{self._register[2]} et le stocke dans {self._register[0]}"

        elif self._name[-4:] == 'lit8' or self._name[-5:] == 'lit16':
            operator, rest = self._name.split('-')
            _, litvalue = rest.split('/')
            if litvalue == 'lit8':
                # binop/lit8 vAA, vBB, #+CC
                # d8: add-int/lit8
                # [ .... ]
                # e2: ushr-int/lit8
                # A: destination register (8 bits)
                # B: source register (8 bits)
                # C: signed int constant (8 bits)
                self._register.extend([instr.AA, instr.BB])
                self._constant = instr.CC
            elif litvalue == 'lit16':
                # binop/lit16 vA, vB, #+CCCC
                # d0: add-int/lit16
                # [ .... ]
                # d7: xor-int/lit16
                # A: destination register (4 bits)
                # B: source register (4 bits)
                # C: signed int constant (16 bits)
                self._register.extend([instr.A, instr.B])
                self._constant = instr.CCCC

            self._string = f"instruction : {self._name} execute l'opération {operator} entre les valeurs de" \
                           f" v{self._register[1]} et la valeur entiere {self._constant} et le stocke dans v" \
                           f"{self._register[0]}"

        elif self._name[-5:] == '2addr':
            # binop/2addr vA, vB
            # b0: add-int/2addr
            # [ .... ]
            # A: destination and first source register or pair (4 bits)
            # B: second source register or pair (4 bits)
            operator, _ = self._name.split("-")
            self._register.extend([instr.A, instr.B])
            self._string = f"instruction : {self._name} execute l'opération {operator} entre les valeurs de" \
                           f" v{self._register[0]} et v{self._register[1]} et le stocke dans {self._register[0]}"

        elif self._name == 'return':
            # return vAA
            # A: return value register (8 bits)
            self._register.append(instr.AA)
            self._string = f"instruction : {self._name} renvoie la valeur contenue dans le registre v{self._register[0]}"

        elif self._name[:4] in ['sget', 'sput']:
            # sstaticop vAA, field@BBBB
            # 60: sget
            # 61: sget-wide
            # 62: sget-object
            # 63: sget-boolean
            # 64: sget-byte
            # 65: sget-char
            # 66: sget-short
            # 67: sput
            # 68: sput-wide
            # 69: sput-object
            # 6a: sput-boolean
            # 6b: sput-byte
            # 6c: sput-char
            # 6d: sput-short
            # A: value register or pair; may be source or dest (8 bits)
            # B: static field reference index (16 bits)
            self._register.append(instr.AA)
            self._field = instr.cm.get_field(instr.BBBB)
            self._string = f"instruction : {self._name} stock le champs {self._field} dans v{self._register[0]}"

        else:
            self._string = None

    def __repr__(self):
        return self._string

    def to_string(self):
        print(self._string)

    def get_length(self):
        return self._length

    def get_name(self):
        return self._name

    def get_register(self):
        return self._register

    def get_string_value(self):
        return self._string_value

    def get_constant(self):
        return self._constant

    def get_type(self):
        return self._type

    def get_method(self):
        return self._method

    def get_string(self):
        return self._string

    def get_destination(self):
        return self._destination

    def get_field(self):
        return self._field
