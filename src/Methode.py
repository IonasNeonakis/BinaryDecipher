class Methode:
    def __init__(self, method, class_name):
        self._nb_reg = None
        self._androguard_method = method
        self._informations = None
        self._instructions = []
        self._succ = {}
        self._etat_reg = {}
        self._name = None
        self._isStatic = 'static' in method.get_access_flags_string()
        self._class_name = class_name
        self._dalvik_to_primitive = {'V': 'void', 'B': 'byte', 'C': 'char', 'J': 'long', 'D': 'double', 'Z': 'boolean',
                                     'S': 'short', 'I': 'int', 'F': 'float'}
        self._primitive_to_dalvik = {'void': 'V', 'byte': 'B', 'char': 'C', 'long': 'J', 'double': 'D', 'boolean': 'Z',
                                     'short': 'S', 'int': 'I', 'float': 'F'}

    def set_name(self, name):
        self._name = name

    def set_corps(self, corps):
        self._corps = corps

    def set_nb_reg(self, nb_reg):
        self._nb_reg = nb_reg
        for i in range(nb_reg):
            self._etat_reg[i] = None

    def set_instructions(self, instructions):
        self._instructions = instructions

    def set_informations(self, informations):
        self._informations = informations

    def get_succ(self):
        return self._succ

    def get_parents_instruction(self, number):
        # Return liste des parents de l'instruction donnée en parametre
        res = []
        for num, elem in self._succ.items():
            if number in elem[1]:
                res.append(elem[0])
        return res

    def compute_succ(self):
        offset = 0
        for instr in self._instructions:
            destination = []
            if instr.get_name() == "":  # Gerer les cas ou la destination n'est pas explicite (comme les if ou les goto)
                pass
                # destination = offset + valeur a déterminer (par exemple le goto a une destination specifique
            elif instr.get_name()[:2] == "if":
                destination = [offset + instr.get_destination(), offset + instr.get_length()]
            elif "goto" in instr.get_name():
                destination.append(instr.get_destination() + offset)
            elif "return" in instr.get_name():
                destination = []
            else:
                destination.append(
                    offset + instr.get_length())  # Juste l'instruction d'après (car c'est une instruction sequentiel
            self._succ[offset] = (instr, destination, offset)
            offset += instr.get_length()  # Mise à jour de l'offset (adresse de l'instruction suivante

    def get_method_params(self, m):
        # Renvoie la liste des params de la méthode appellé dans un invoke
        res = {}
        res['entry'] = []
        entry_params, exit_type = m[2]
        print("param ", entry_params, " ", exit_type)
        res['exit'] = self._dalvik_to_primitive.get(exit_type)
        entry_params = entry_params.replace("(", "").replace(")", "")
        entry_params = list(entry_params.split(" "))
        for param in entry_params:
            res['entry'].append(self._dalvik_to_primitive.get(param, param))
        return res

    def evaluate(self):
        print("\n")
        print("=" * 20)
        print("Début de l'analyse : Méthode " + self._name + "\n")
        offset = 0  # Début
        to_do = [self._succ.get(offset)]
        is_valide = True
        params = self._informations.get('params', [])
        print(self._informations)
        for num_reg, type in params:
            # Initialisation des types des registres en fonction des parametres de la methode
            if type not in self._primitive_to_dalvik.keys():
                type = 'L'+type.replace(".", "/")+";"
            self._etat_reg[num_reg] = type
        if not self._isStatic:
            self._etat_reg[self._informations['registers'][1]] = self._class_name
        while len(to_do) > 0:
            curr_instr, destination, offset = to_do[0]
            parents = self.get_parents_instruction(offset)
            print(curr_instr)
            if curr_instr.get_name()[:6] == "invoke":
                m = curr_instr.get_method()
                if self._isStatic:
                    pass  # Todo
                else:
                    if m[0] not in self._etat_reg.get(curr_instr.get_register()[0]):
                        print(
                            '\033[91m Erreur dans l\'appel a la methode ' + curr_instr.get_name() + ' : contexte invalide. )\033[0m')
                    method_params = self.get_method_params(m)
                    for i in range(1, len(curr_instr.get_register())):
                        if self._etat_reg.get(curr_instr.get_register()[i]) != method_params.get('entry')[i-1]:
                            print(
                                '\033[91m Erreur dans l\'appel a la methode ' + curr_instr.get_name() + ', le type du registre v' +
                                str(curr_instr.get_register()[
                                    i]) + ' ne correspond pas au type du parametre de la methode )\033[0m')

            elif curr_instr.get_name() == "return":
                if not self._informations['return'] == self._etat_reg[curr_instr.get_register()[0]]:
                    print("Erreur de type de retour")
                    return False
            elif curr_instr.get_name() == "move-result":
                last_exit = method_params.get('exit', None)
                self._etat_reg[curr_instr.get_register()[0]] = last_exit
            elif curr_instr.get_name()[:4] in ['sget', 'sput']:
                self._etat_reg[curr_instr.get_register()[0]] = curr_instr.get_field()
            elif curr_instr.get_name() == "const-string":
                self._etat_reg[curr_instr.get_register()[0]] = 'Ljava/lang/String;'
            elif curr_instr.get_name() == "const":  # Todo : fusionner les deux const?
                self._etat_reg[curr_instr.get_register()[0]] = 'int'
            elif curr_instr.get_name() == 'const/16' or curr_instr.get_name() == 'const/4':
                self._etat_reg[curr_instr.get_register()[0]] = 'int'
            elif curr_instr.get_name() in ['mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int', 'shl-int',
                                           'shr-int', 'ushr-int']:
                tab = curr_instr.get_register()
                if self._etat_reg[tab[1]] != 'int' or self._etat_reg[tab[2]] != 'int':
                    print('Erreur dans les registres, ce ne sont pas des int')
                self._etat_reg[tab[0]] = 'int'
            elif curr_instr.get_name() in ['add-int', 'sub-int', 'mul-int', 'div-int', 'rem-int', 'and-int', 'or-int',
                                           'xor-int', 'shl-int', 'shr-int', 'ushr-int', 'add-long', 'sub-long',
                                           'mul-long', 'div-long', 'rem-long', 'and-long', 'or-long', 'xor-long',
                                           'shl-long', 'shr-long', 'ushr-long', 'add-float', 'sub-float', 'mul-float',
                                           'div-float', 'rem-float', 'add-double', 'sub-double', 'mul-double',
                                           'div-double', 'rem-double']:  # Binop
                _, type = curr_instr.get_name().split("-")
                tab = curr_instr.get_register()
                if self._etat_reg[tab[1]] != type or self._etat_reg[tab[2]] != type:
                    print(
                        '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des ' + type + ' )\033[0m')
                    return False
                self._etat_reg[tab[0]] = type
            elif curr_instr.get_name()[-4:] == 'lit8' or curr_instr.get_name()[-5:] == 'lit16':
                tab = curr_instr.get_register()
                if self._etat_reg[tab[1]] != 'int':
                    print(
                        '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des int)  \033[0m')
                    return False
                self._etat_reg[tab[0]] = 'int'
            elif curr_instr.get_name()[-5:] == '2addr':  # exemple :  sub-int/2addr
                tab = curr_instr.get_register()
                nom, type = curr_instr.get_name()[:-6].split('-')
                if self._etat_reg[tab[0]] != type or self._etat_reg[tab[1]] != type:
                    print(
                        '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des ' + type + ')\033[0m')
                    # return False
                # v0 ne change pas de type
            elif curr_instr.get_name() == 'return-void':
                if not self._informations['return'] == 'void':
                    print(
                        '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', le type de retour ne correspond pas.)\033[0m')
            elif curr_instr.get_name()[:2] == 'if':
                _, name = curr_instr.get_name().split('-')
                if len(name) == 2:  # si on est là ,if-eq,if-ne,if-lt,if-ge,if-gt,if-le
                    if self._etat_reg[curr_instr.get_register()[0]] != self._etat_reg[curr_instr.get_register()[1]]:
                        print(
                            '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ',test d\'egalite sur des types differents)\033[0m')
                else:  # si on est là ,if-eqz,if-nez,if-ltz,if-gez,if-gtz,if-lez
                    if self._etat_reg[curr_instr.get_register()[0]] == 'None':
                        print(
                            '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', le type \'None\' n\'est pas comparable avec 0.)\033[0m')
                        # return False
            elif curr_instr.get_name() == 'goto':
                pass
            else:
                print(
                    '\033[91m' + curr_instr.get_name() + " n'est pas encore pris en compte dans Methode.py" + '\033[0m')

            to_do.pop(0)
            for child in destination:
                to_do.append(self._succ.get(child))
        print("Fin d'analyse : methode valide")
        return is_valide

    def get_androguard_method(self):
        return self._androguard_method

    def print(self):
        print("Methode {\n    Informations : ", self._informations, "\n    Nombre de registre : ", self._nb_reg,
              "\n    Instruction : ", self._instructions, "\n}")
