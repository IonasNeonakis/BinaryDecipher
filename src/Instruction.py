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
        self._prototype = None  # Prototype d'un methode (dans const-method-type par exemple)
        self._method_handle = None  # Methode Handle (dans const-method-handle par exemple)

        if self._name[:4] == "move":
            if self._name in ['move', 'move-wide', 'move-object']:
                # Tout ces elements ont les mêmes attributs, exemple avec la doc de move
                # move vA, vB
                # A: destination register (4 bits)
                # B: source register (4 bits)
                self._register.extend([instr.A, instr.B])
                self._string = f"instruction {self._name} déplace de v{self._register[1]} vers v{self._register[0]}"

            elif self._name in ['move/from16', 'move-wide/from16', 'move-object/from16']:
                # Tout ces elements ont les mêmes attributs, exemple avec la doc de move/from16
                # move/from16 vAA, vBBBB
                # A: destination register (8 bits)
                # B: source register (16 bits)
                self._register.extend([instr.AA, instr.BBBB])
                self._string = f"instruction {self._name} déplace de v{self._register[1]} vers v{self._register[0]}"

            elif self._name in ['move/16', 'move-wide/16', 'move-object/16']:
                # Tout ces elements ont les mêmes attributs, exemple avec la doc de move/16
                # move/16 vAAAA, vBBBB
                # A: destination register (16 bits)
                # B: source register (16 bits)
                self._register.extend([instr.AAAA, instr.BBBB])
                self._string = f"instruction {self._name} déplace de v{self._register[1]} vers v{self._register[0]}"

            else:
                # Dans ce cas il s'agit d'un move-result, move-result-wide, move-result-object, move-exception
                # Exemple avec la doc de move-result
                # move-result vAA
                # A: destination register (8 bits)
                self._register.append(instr.AA)
                self._string = f"instruction {self._name} déplace dans v{self._register[0]} le résultat de l'invoke précédant"

        elif self._name == 'return-void':
            self._string = f"instruction : {self._name} ne fait rien (normal)"

        elif self._name[:6] == 'return':
            # return, return-wide et return-object. Exemple avec la doc de return-object
            # return-object vAA
            # A: return value register (8 bits)
            self._register.append(instr.AA)
            self._string = f"instruction {self._name} renvoie la valeur de v{self._register[0]}"

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

        elif self._name == 'const':
            # const vAA, #+BBBBBBBB
            # A: destination register (8 bits)
            # B: arbitrary 32-bit constant
            self._register.append(instr.AA)
            self._constant = instr.BBBBBBBB
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} le/les litteraux suivant :" \
                           f" {self._constant}"

        elif self._name == 'const/high16':
            # const/high16 vAA, #+BBBB0000
            # A: destination register (8 bits)
            # B: signed int (16 bits)
            self._register.append(instr.AA)
            self._constant = instr.BBBB0000
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} le/les litteraux suivant :" \
                           f" {self._constant}"

        elif self._name[:10] == 'const-wide':
            # const-wide vAA, #+BBBBBBBBBBBBBBBB	A: destination register (8 bits)
            # B: arbitrary double-width (64-bit) constant
            self._register.append(instr.AA)
            if self._name == 'const-wide/16':
                self._constant = instr.BBBB
            elif self._name == 'const-wide/32':
                self._constant = instr.BBBBBBBB
            elif self._name == 'const-wide':
                self._constant = instr.BBBBBBBBBBBBBBBB
            elif self._name == 'const-wide/high16':
                self._constant = instr.BBBB000000000000
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} le/les litteraux suivant :" \
                           f" {self._constant}"

        elif self._name == 'const-string':
            # const-string vAA, string@BBBB
            # A: destination register (8 bits)
            # B: string index
            self._register.append(instr.AA)
            self._string_value = instr.cm.get_string(instr.BBBB)
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} la valeur" \
                           f"{self._string_value}"

        elif self._name == 'const-string/jumbo':
            # const-string/jumbo vAA, string@BBBBBBBB
            # A: destination register (8 bits)
            # B: string index
            self._register.append(instr.AA)
            self._string_value = instr.cm.get_string(instr.BBBBBBBB)
            self._string = f"instruction {self._name} enregistre dans v{self._register[0]} la valeur" \
                           f"{self._string_value}"

        elif self._name == 'const-class':
            # const-class vAA, type@BBBB
            # A: destination register (8 bits)
            # B: type index
            self._register.append(instr.AA)
            self._type = instr.cm.get_type(instr.BBBB)
            self._string = f"instruction : {self._name} déplace l'instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"

        elif self._name[:7] == 'monitor':
            # monitor-enter ou monitor-exit
            # monitor-enter vAA
            # A: reference-bearing register (8 bits)
            self._register.append(instr.AA)
            self._string = f"instruction : {self._name} libère ou récupère le moniteur pour l'objet indiqué par la " \
                           f"réference contenu dans v{self._register[0]}"

        elif self._name == 'check-cast':
            # check-cast vAA, type@BBBB
            # A: reference-bearing register (8 bits)
            # B: type index (16 bits)
            self._type = instr.cm.get_type(instr.BBBB)
            self._register.append(instr.AA)
            self._string = f"instruction {self._name} vérifie que la valeur du registre v{self._register[0]} " \
                           f"soit de type {self._type}"

        elif self._name == 'instance-of':
            # instance-of vA, vB, type@CCCC
            # A: destination register (4 bits)
            # B: reference-bearing register (4 bits)
            # C: type index (16 bits)
            self._register.extend([instr.A, instr.B])
            self._type = instr.cm.get_type(instr.CCCC)
            self._string = f"instruction {self._name} stock dans {self._register[0]} 1 si l'élément référencé " \
                           f"dans v{self._register[1]} est du type {self._type}"

        elif self._name == 'array-length':
            # array-length vA, vB
            # A: destination register (4 bits)
            # B: array reference-bearing register (4 bits)
            self._register.extend([instr.A, instr.B])
            self._string = f"instruction {self._name} stock dans v{self._register[0]} la taille en nombre d'entré " \
                           f"de la liste référencé dans v{self._register[1]}"

        elif self._name == 'new-instance':
            # new-instance vAA, type@BBBB
            # A: destination register (8 bits)
            # B: type index
            self._type = instr.cm.get_type(instr.BBBB)
            self._register.append(instr.AA)
            self._string = f"instruction : {self._name} crée une instance de type {self._type} et la stocke dans" \
                           f"v{self._register[0]}"

        elif self._name == 'new-array':
            # new-array vA, vB, type@CCCC
            # A: destination register (4 bits)
            # B: size register
            # C: type index
            self._register.extend([instr.A, instr.B])
            self._type = instr.cm.get_type(instr.CCCC)
            self._string = f"instruction {self._name} construit dans v{self._register[0]} une array de taille x " \
                           f"contenu dans v{self._register[1]} de type {self._type}"

        elif self._name == 'filled-new-array':
            # filled-new-array {vC, vD, vE, vF, vG}, type@BBBB
            # A: array size and argument word count (4 bits)
            # B: type index (16 bits)
            # C..G: argument registers (4 bits each)
            self._type = instr.cm.get_type(instr.BBBB)
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
            self._string = f"instruction {self._name} construit une Array de taille {instr.A} de type {self._type}"

        elif self._name == 'filled-new-array/range':
            # filled-new-array/range {vCCCC .. vNNNN}, type@BBBB
            # A: array size and argument word count (8 bits)
            # B: type index (16 bits)
            # C: first argument register (16 bits)
            # N = A + C - 1
            # Unhandle
            pass  # todo

        elif self._name == 'fill-array-data':
            # fill-array-data vAA, +BBBBBBBB (with supplemental data as specified below in "fill-array-data-payload Format")
            # A: array reference (8 bits)
            # B: signed "branch" offset to table data pseudo-instruction (32 bits)
            pass  # Todo

        elif self._name == 'throw':
            # throw vAA
            # A: exception-bearing register (8 bits)
            self._register.append(instr.AA)
            self._string = f"instruction {self._name} jette l'instruction contenu dans le registre v{self._register[0]}"

        elif self._name == 'goto':
            # goto +AA
            # A: signed branch offset (8 bits)
            self._destination = instr.AA * 2
            self._string = f"instruction : {self._name} saute de {self._destination} offset"

        elif self._name == 'goto/16':
            # goto/16 +AAAA
            # A: signed branch offset (16 bits)
            self._destination = instr.AAAA * 2
            self._string = f"instruction : {self._name} saute de {self._destination} offset"

        elif self._name == 'goto/32':
            # goto/32 +AAAAAAAA
            # A: signed branch offset (32 bits)
            self._destination = instr.AAAAAAAA * 2
            self._string = f"instruction : {self._name} saute de {self._destination} offset"

        elif self._name == 'packed-switch':
            pass  # todo

        elif self._name == 'sparse-switch':
            pass  # todo

        elif self._name[:3] == 'cmp':
            # cmpkind vAA, vBB, vCC
            # 2d: cmpl-float (lt bias)
            # 2e: cmpg-float (gt bias)
            # 2f: cmpl-double (lt bias)
            # 30: cmpg-double (gt bias)
            # 31: cmp-long
            # A: destination register (8 bits)
            # B: first source register or pair
            # C: second source register or pair
            # Perform the indicated floating point or long comparison, setting a to 0 if b == c, 1 if b > c,
            # or -1 if b < c. The "bias" listed for the floating point operations indicates how NaN comparisons are
            # treated: "gt bias" instructions return 1 for NaN comparisons, and "lt bias" instructions return -1.
            self._register.extend([instr.AA, instr.BB, instr.CC])
            self._string = f"instruction {self._name} effectue la comparaison souhaité entre les float ou long dans" \
                           f" les registres v{self._register[1]} et v{self._register[2]}. Le resultat est " \
                           f"stocké dans v{self._register[0]}"

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

        elif self._name[:4] in ["aget", "aput"]:
            # arrayop vAA, vBB, vCC
            # 44: aget
            # 45: aget-wide
            # 46: aget-object
            # 47: aget-boolean
            # 48: aget-byte
            # 49: aget-char
            # 4a: aget-short
            # 4b: aput
            # 4c: aput-wide
            # 4d: aput-object
            # 4e: aput-boolean
            # 4f: aput-byte
            # 50: aput-char
            # 51: aput-short
            # A: value register or pair; may be source or dest (8 bits)
            # B: array register (8 bits)
            # C: index register (8 bits)
            self._register.extend([instr.AA, instr.BB, instr.CC])
            self._string = f"instruction {self._name} effectue l'operation identifié sur l'objet d'index " \
                           f"contenu dans v{self._register[2]} de l'array identifié par le registre" \
                           f" v{self._register[1]} stockant ou sourçant le valeur dans v{self._register[0]}"

        elif self._name[:4] in ["iget", "iput"]:
            # iinstanceop vA, vB, field@CCCC
            # 52: iget
            # 53: iget-wide
            # 54: iget-object
            # 55: iget-boolean
            # 56: iget-byte
            # 57: iget-char
            # 58: iget-short
            # 59: iput
            # 5a: iput-wide
            # 5b: iput-object
            # 5c: iput-boolean
            # 5d: iput-byte
            # 5e: iput-char
            # 5f: iput-short
            # A: value register or pair; may be source or dest (4 bits)
            # B: object register (4 bits)
            # C: instance field reference index (16 bits)
            self._register.extend([instr.A, instr.B])
            self._field = instr.cm.get_field(instr.CCCC)
            self._string = f"instruction {self._name} effectue l'operation identifié sur l'instance d'un objet" \
                           f" stocké dans v{self._register[1]}, sur le champs {self._field} et stock/charge " \
                           f"dans v{self._register[0]}"

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
            self._string = f"instruction : {self._name} stock/charge le champs {self._field} avec le registre v{self._register[0]}"

        elif self._name[
             :6] == 'invoke' and '/range' not in self._name and 'custom' not in self._name and 'polymorphic' not in self._name:
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

        elif self._name[:6] == 'invoke' and '/range' in self._name:
            # invoke-kind/range {vCCCC .. vNNNN}, meth@BBBB
            # 74: invoke-virtual/range
            # 75: invoke-super/range
            # 76: invoke-direct/range
            # 77: invoke-static/range
            # 78: invoke-interface/range
            # A: argument word count (8 bits)
            # B: method reference index (16 bits)
            # C: first argument register (16 bits)
            # N = A + C - 1
            for i in range(instr.A):
                self._register.append(instr.CCCC + i)
            self._method = instr.cm.get_method(instr.BBBB)

        elif self._name in ['not-int', 'neg-int', 'neg-long', 'not-long', 'neg-float', 'neg-double', 'int-to-long',
                            'int-to-float', 'int-to-double', 'long-to-int', 'long-to-float', 'long-to-double',
                            'float-to-int',
                            'float-to-long', 'float-to-double', 'double-to-int', 'double-to-long', 'double-to-float',
                            'int-to-byte', 'int-to-char', 'int-to-short']:
            # unop vA, vB
            # 7b: neg-int
            # 7c: not-int
            # 7d: neg-long
            # 7e: not-long
            # 7f: neg-float
            # 80: neg-double
            # 81: int-to-long
            # 82: int-to-float
            # 83: int-to-double
            # 84: long-to-int
            # 85: long-to-float
            # 86: long-to-double
            # 87: float-to-int
            # 88: float-to-long
            # 89: float-to-double
            # 8a: double-to-int
            # 8b: double-to-long
            # 8c: double-to-float
            # 8d: int-to-byte
            # 8e: int-to-char
            # 8f: int-to-short	A: destination register or pair (4 bits)
            # B: source register or pair (4 bits)
            self._register.extend([instr.A, instr.B])
            self._string = f"instruction {self._name} effectue l'opération identifié sur le " \
                           f"registre v{self._register[1]} et stock le resultat dans v{self._register[0]}"

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

        elif self._name == 'invoke-polymorphic':
            # invoke-polymorphic {vC, vD, vE, vF, vG}, meth@BBBB, proto@HHHH
            # A: argument word count (4 bits)
            # B: method reference index (16 bits)
            # C: receiver (4 bits)
            # D..G: argument registers (4 bits each)
            # H: prototype reference index (16 bits
            pass  # Todo

        elif self._name == 'const-method-handle':
            # const-method-handle vAA, method_handle@BBBB
            # A: destination register (8 bits)
            # B: method handle index (16 bits)
            self._register.append(instr.AA)
            self._method_handle = instr.cm.get_method_handle(instr.BBBB)
            self._string = f"instruction {self._name} stock dans v{self._register[0]} une référence vers le method handler {self._method_handle}"

        elif self._name == 'const-method-type':
            # const-method-handle vAA, method_handle@BBBB
            # A: destination register (8 bits)
            # B: method handle index (16 bits)
            self._register.append(instr.AA)
            self._prototype = instr.cm.get_proto(instr.BBBB)
            self._string = f"instruction {self._name} stock dans v{self._register[0]} une référence du prototype de methode : {self._prototype}"

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

    def get_method_handle(self):
        return self._method_handle

    def get_prototype(self):
        return self._prototype
