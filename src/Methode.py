class Methode():
    def __init__(self):
        self._nb_reg = None
        self._informations = None
        self._instructions = []
        self._succ = {}
        self._etat_reg = {}
        self._name = None

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

    def compute_succ(self):
        offset = 0
        for instr in self._instructions:
            if instr.get_name() == "":  # Gerer les cas ou la destination n'est pas explicite (comme les if ou les goto)
                pass
                # destination = offset + valeur a déterminer (par exemple le goto a une destination specifique
            elif instr.get_name()[:2] == "if":
                destination = offset + instr.get_destination()
            elif instr.get_name()[:6] == "return":
                destination = None  # Pas de destination sur le return !!!
            elif "goto" in instr.get_name():
                destination = instr.get_destination()
            else:
                destination = offset + instr.get_length()  # Juste l'instruction d'après (car c'est une instruction sequentiel
            self._succ[offset] = (instr, destination)
            offset += instr.get_length()  # Mise à jour de l'offset (adresse de l'instruction suivante

    def evaluate(self):
        print("\n")
        print("=" * 20)
        print("Début de l'analyse : Méthode " + self._name + "\n")
        offset = 0  # Début
        has_next = True
        is_valide = True
        while has_next:
            curr_instr, destination = self._succ.get(offset)
            print(curr_instr)
            if curr_instr.get_name()[:6] == "invoke":
                pass  # On n'attribut aucun type aux registre donc pas de changement
            elif curr_instr.get_name()[:6] == "return":  # TODO return void
                if not self._informations['return'] == self._etat_reg[curr_instr.get_registrer()[0]]:
                    print(
                        "Erreur de type de retour")  # TODO gérer ce cas précis :) genre IONAS par exemple car il a son cahier sur lui.
            elif curr_instr.get_name() == "const":
                pass
            elif curr_instr.get_name() in ['mul-int', 'div-int', 'rem-int', 'and-int', 'or-int', 'xor-int', 'shl-int',
                                           'shr-int', 'ushr-int', 'add-long', 'sub-long', 'mul-long', 'div-long',
                                           'rem-long', 'and-long', 'or-long', 'xor-long', 'shl-long', 'shr-long',
                                           'ushr-long', 'add-float', 'sub-float', 'mul-float', 'div-float', 'rem-float',
                                           'add-double', 'sub-double', 'mul-double', 'div-double', 'rem-double']:
                pass

            next_instr = self._succ.get(destination)  # On get l'instruction suivante
            if not next_instr:  # S'il n'y en a pas
                has_next = False  # On stop la boucle
            else:
                offset = destination  # Sinon on actualise l'offset pour le tour suivant
        print("Fin d'analyse : methode valide")
        return is_valide

    def print(self):
        print("Methode {\n    Informations : ", self._informations, "\n    Nombre de registre : ", self._nb_reg,
              "\n    Instruction : ", self._instructions, "\n}")
