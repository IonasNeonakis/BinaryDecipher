import copy


class Methode():
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
        self._tmp_map_register = {}

    def set_name(self, name):
        self._name = name

    def set_corps(self, corps):
        self._corps = corps

    def set_nb_reg(self, nb_reg):
        self._nb_reg = nb_reg
        for i in range(nb_reg):
            self._etat_reg[i] = (None, None)

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
                res.append(elem)
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
        res['exit'] = self._dalvik_to_primitive.get(exit_type)
        entry_params = entry_params.replace("(", "").replace(")", "")
        entry_params = list(entry_params.split(" "))
        for param in entry_params:
            res['entry'].append(self._dalvik_to_primitive.get(param, param))
        return res

    def evaluate(self, doitPrint):
        string_builder = ""
        offset = 0  # Début
        to_do = [self._succ.get(offset)]
        is_valide = True
        params = self._informations.get('params', [])
        print(self._informations)
        last_move = (None, None)
        for num_reg, type in params:
            # Initialisation des types des registres en fonction des parametres de la methode
            if type not in self._primitive_to_dalvik.keys():
                type = 'L' + type.replace(".", "/") + ";"
            self._etat_reg[num_reg] = (type, None)
        if not self._isStatic:
            self._etat_reg[self._informations['registers'][1]] = (self._class_name, None)

        self._tmp_map_register = {}
        for instruction_offset in self._succ.keys():
            self._tmp_map_register[instruction_offset] = self._etat_reg

        while len(to_do) > 0:
            curr_instr, destination, offset = to_do[0]
            parents = self.get_parents_instruction(offset)
            # string_builder +=  curr_instr #FIXME je viens de le changer jsp si faut le print :) Ionas à 14h45 le 19/01
            if len(parents) > 1:
                for instr_parent, _, offset_parent in parents:
                    parent_registers = self._tmp_map_register.get(offset_parent)
                    for register, value in self._etat_reg.items():
                        if value[0] and value[0][0] == 'L':
                            if value[0] != parent_registers.get(register)[0]:
                                # CheckHeritage
                                pass  # Todo
                        else:
                            if value[0] != parent_registers.get(register)[0]:
                                string_builder +=  f"Erreur de type sur la jointures des registres à l'instruction {curr_instr.get_name()}\n"
                                is_valide = False

            if self.check_registers_accessibility(curr_instr.get_register()):
                if curr_instr.get_name()[:4] == "move":
                    if curr_instr.get_name() in ['move', 'move-wide', 'move-object', 'move/from16', 'move-wide/from16',
                                                 'move-object/from16', 'move/16', 'move-wide/16', 'move-object/16']:
                        if 'wide' in curr_instr.get_name():
                            if curr_instr.get_register()[0] + 1 in self._etat_reg.keys():
                                self._etat_reg[curr_instr.get_register()[0]] = self._etat_reg[
                                    curr_instr.get_register()[1]]
                                self._etat_reg[curr_instr.get_register()[0] + 1] = self._etat_reg[
                                    curr_instr.get_register()[1] + 1]
                                self._etat_reg[curr_instr.get_register()[1]] = (None, None)
                                self._etat_reg[curr_instr.get_register()[1] + 1] = (None, None)
                            else:
                                string_builder +=  f"Erreur à l'instruction {curr_instr.get_name()}\n"
                                is_valide = False
                        else:
                            self._etat_reg[curr_instr.get_register()[0]] = self._etat_reg.get(
                                curr_instr.get_register()[1])
                            self._etat_reg[curr_instr.get_register()[1]] = (None, None)
                    else:
                        if last_move == (None, None):
                            string_builder +=  f"Erreur à l'instruction {curr_instr.get_name()}\n"
                            is_valide = False
                        else:
                            self._etat_reg[curr_instr.get_register()[0]] = last_move

                elif curr_instr.get_name() == 'return-void':
                    if not self._informations['return'] == 'void':
                        string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', le type de retour ne correspond pas.)\033[0m\n'

                elif curr_instr.get_name() in ['const/4', 'const/16', 'const', 'const/high16']:
                    self._etat_reg[curr_instr.get_register()[0]] = ('int', curr_instr.get_constant())

                elif curr_instr.get_name()[:10] == 'const-wide':
                    if curr_instr.get_register()[0] + 1 in self._etat_reg.keys():
                        self._etat_reg[curr_instr.get_register()[0]] = ('int', curr_instr.get_constant())
                        self._etat_reg[curr_instr.get_register()[0] + 1] = ('int', curr_instr.get_constant())
                    else:
                        string_builder +=  f"Erreur à l'instruction {curr_instr.get_name()}\n"
                        is_valide = False

                elif 'const-string' in curr_instr.get_name():
                    self._etat_reg[curr_instr.get_register()[0]] = ('Ljava/lang/String;', curr_instr.get_string())

                elif curr_instr.get_name() == 'const-class':
                    self._etat_reg[curr_instr.get_register()[0]] = (curr_instr.get_type(), None)

                elif curr_instr.get_name() == "return":
                    if not self._informations['return'] == self._etat_reg[curr_instr.get_register()[0]][0]:
                        string_builder +=  "Erreur de type de retour\n"
                        is_valide = False

                elif curr_instr.get_name()[
                     :6] == "invoke" and 'custom' not in curr_instr.get_name() and 'polymorphic' not in curr_instr.get_name():
                    m = curr_instr.get_method()
                    if m[0] not in self._etat_reg.get(curr_instr.get_register()[0]):
                        string_builder +=  '\033[91m Erreur dans l\'appel a la methode ' + curr_instr.get_name() + ' : contexte invalide. )\033[0m\n'
                    method_params = self.get_method_params(m)

                    for i in range(1, len(curr_instr.get_register())):
                        if self._etat_reg.get(curr_instr.get_register()[i])[0] != method_params.get('entry')[i - 1]:
                            string_builder +=  '\033[91m Erreur dans l\'appel a la methode ' + curr_instr.get_name() + ', le type du registre v' + str(curr_instr.get_register()[i]) + ' ne correspond pas au type du parametre de la methode )\033[0m\n'
                        else:
                            last_move = (method_params.get('exit'), None)

                elif curr_instr.get_name()[:4] in ["aget", "aput"]:
                    if curr_instr.get_name() in ["aget", "aput"]:
                        self._etat_reg[curr_instr.get_register()[0]] = ('int',
                                                                        self._etat_reg[curr_instr.get_register()[1]][1][
                                                                            self._etat_reg[
                                                                                curr_instr.get_register()[2]][1]])
                    else:
                        op, type = curr_instr.get_name().split('-')
                        if type == "wide":
                            self._etat_reg[curr_instr.get_register()[0]] = ('int', None)
                            self._etat_reg[curr_instr.get_register()[0] + 1] = ('int', None)
                        elif type in ["boolean", "byte", "char", "short"]:
                            self._etat_reg[curr_instr.get_register()[0]] = (type, None)

                elif curr_instr.get_name()[:4] in ['sget', 'sput']:
                    self._etat_reg[curr_instr.get_register()[0]] = curr_instr.get_field()

                elif curr_instr.get_name() in ['mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int',
                                               'shl-int',
                                               'shr-int', 'ushr-int']:
                    tab = curr_instr.get_register()
                    if self._etat_reg[tab[1]][0] != 'int' or self._etat_reg[tab[2]][0] != 'int':
                        string_builder +=  'Erreur dans les registres, ce ne sont pas des int\n'
                    self._etat_reg[tab[0]] = ('int', None)
                elif curr_instr.get_name() in ['add-int', 'sub-int', 'mul-int', 'div-int', 'rem-int', 'and-int',
                                               'or-int',
                                               'xor-int', 'shl-int', 'shr-int', 'ushr-int', 'add-long', 'sub-long',
                                               'mul-long', 'div-long', 'rem-long', 'and-long', 'or-long', 'xor-long',
                                               'shl-long', 'shr-long', 'ushr-long', 'add-float', 'sub-float',
                                               'mul-float',
                                               'div-float', 'rem-float', 'add-double', 'sub-double', 'mul-double',
                                               'div-double', 'rem-double']:  # Binop
                    _, type = curr_instr.get_name().split("-")
                    tab = curr_instr.get_register()
                    if self._etat_reg[tab[1]][0] != type or self._etat_reg[tab[2]][0] != type:
                        string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des ' + type + ' )\033[0m\n'
                        is_valide = False
                    self._etat_reg[tab[0]] = (type, None)  # Todo
                elif curr_instr.get_name()[-4:] == 'lit8' or curr_instr.get_name()[-5:] == 'lit16':
                    tab = curr_instr.get_register()
                    if self._etat_reg[tab[1]][0] != 'int':
                        string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des int)  \033[0m\n'
                        is_valide = False
                    self._etat_reg[tab[0]] = ('int', None)
                elif curr_instr.get_name()[-5:] == '2addr':  # exemple :  sub-int/2addr
                    tab = curr_instr.get_register()
                    nom, type = curr_instr.get_name()[:-6].split('-')
                    if self._etat_reg[tab[0]][0] != type or self._etat_reg[tab[1]][0] != type:
                        string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', ce ne sont pas des ' + type + ')\033[0m\n'
                        # return False
                    # v0 ne change pas de type
                elif curr_instr.get_name()[:2] == 'if':
                    _, name = curr_instr.get_name().split('-')
                    if len(name) == 2:  # si on est là ,if-eq,if-ne,if-lt,if-ge,if-gt,if-le
                        if self._etat_reg[curr_instr.get_register()[0]][0] != \
                                self._etat_reg[curr_instr.get_register()[1]][0]:
                            string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ',test d\'egalite sur des types differents)\033[0m\n'
                    else:  # si on est là ,if-eqz,if-nez,if-ltz,if-gez,if-gtz,if-lez
                        if self._etat_reg[curr_instr.get_register()[0]][0] == 'None':
                            string_builder +=  '\033[91m' + 'Erreur dans les registres(méthode :  ' + curr_instr.get_name() + ', le type \'None\' n\'est pas comparable avec 0.)\033[0m\n'
                            # return False
                elif curr_instr.get_name() == 'goto':
                    pass

                elif curr_instr.get_name() == "new-array":
                    if self._etat_reg.get(curr_instr.get_register()[1])[0] != 'int':  # pour la taille
                        string_builder +=  f"Erreur à l'instruction {curr_instr.get_name()}\n"
                        is_valide = False
                    else:
                        self._etat_reg[curr_instr.get_register()[0]] = (curr_instr.get_type(), [])

                elif curr_instr.get_name() == "fill-array-data":
                    offset_payload = curr_instr.get_destination() + curr_instr.get_length()
                    data = self._succ.get(offset_payload + offset - curr_instr.get_length())[0].get_constant()
                    self._etat_reg[curr_instr.get_register()[0]] = (
                    self._etat_reg[curr_instr.get_register()[0]][0], data)
                    # Todo check type
                else:
                    string_builder +=  '\033[91m' + curr_instr.get_name() + " n'est pas encore pris en compte dans Methode.py" + '\033[0m\n'

            else:
                str += f"\033[91mErreur dans les registres (méthode : {curr_instr.get_name()}, la méthode accède à des registres inaccessibles)\033[0m\n"
            self._tmp_map_register[offset] = copy.deepcopy(self._etat_reg)
            to_do.pop(0)
            for child in destination:
                to_do.insert(0, self._succ.get(child))

        if doitPrint:
            print(str)
        return is_valide

    # méthode qui vérifie que les registres demandés par l'instruction sont bien accessibles dans le code
    def check_registers_accessibility(self, registres_methode):
        for registre in registres_methode:
            if registre not in self._etat_reg.keys():
                return False
        return True

    def get_androguard_method(self):
        return self._androguard_method

    def print(self):
        print("Methode {\n    Informations : ", self._informations, "\n    Nombre de registre : ", self._nb_reg,
              "\n    Instruction : ", self._instructions, "\n}")

    def get_tmp_map_register(self):
        return self._tmp_map_register
