from schemeVisitor import schemeVisitor
from exceptions import Nothing


class EvalVisitor(schemeVisitor):
    # - ATRIBUTS - #

    funcions = {
        # Operadors aritmètics
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x/y,
        'mod': lambda x, y: x % y,
        # Condicions booleanes
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '=': lambda x, y: x == y,
        '<>': lambda x, y: x != y,
        'and': lambda x, y: x and y,
        'or': lambda x, y: x or y,
        'not': lambda x: not x
    }

    # - MÈTODES - #

    def __init__(self):
        """"
        Métode per inicialitzar la classe: inicialitza la taula de símbols i afegeix l'else com a variable per poder-se utilitzar en la funció 'cond'
        """
        self.ts = [{}]  # Llista de taula de simbols
        # Variables que hi són sompre
        self.ts[0]['else'] = True

    # - Funcions auxiliars per visitar les expressions - #

    def print_display(self, entrada):
        if isinstance(entrada, bool):
            print('#t' if entrada else '#f', end='')
        elif isinstance(entrada, int) or isinstance(entrada, float):
            print(int(entrada), end='')
        elif isinstance(entrada, list):
            if entrada:  # Si "entrada" és no buida, llavors imprimeix coses
                # Imprimir primer element de la llista
                self.print_display(entrada[0])
                # Si té més d'un element, s'imprimeixen recursivament
                if len(entrada) > 1:
                    print(' ', end='')
                    self.print_display(entrada[1:len(entrada)])
        elif isinstance(entrada, str):
            print(entrada, end='')
        elif entrada is None:
            raise Nothing('\nError: no es pot imprimir un valor nul')
        else:
            self.print_display(self.visit(entrada))

    def visitar_define(self, ctx, entrada):
        # Comprovar errors
        if ctx.depth() != 2:
            raise Nothing('\nError: No es poden definir funcions dins de funcions')

        nom = entrada[2]
        children = list(nom.getChildren())
        # Variable constant (no hi ha paràmetres)
        if len(children) == 1:
            assignacio = entrada[3]
            self.ts[0][nom.getText()] = self.visit(assignacio)
        # Definició de funció (hi ha paràmetres)
        else:
            nom_func = children[1].getText()
            parametres = children[2:-1]
            nom_parametres = [par.getText() for par in parametres]
            # self.ts[index][nom_funció] = (nom_parametres, expressions a evaluar)
            self.ts[0][nom_func] = (nom_parametres, entrada[3:-1])

    def visitar_display(self, entrada):
        # Comprovar errors
        if len(entrada) != 4:
            raise Nothing('\nError: display només accepta un argument')

        valor = self.visit(entrada[2])
        if isinstance(valor, list):
            print('(', end='')
            self.print_display(valor)
            print(')', end='')
        else:
            self.print_display(valor)

    def visitar_if(self, entrada):
        # Comprovar errors
        if len(entrada) != 6:
            raise Nothing("\nError: 'if' necessita la condició a cumplir, l'expressió a executar si és certa i l'expressió a executar si és falsa")

        cond = entrada[2]
        ifTrue = entrada[3]
        ifFalse = entrada[4]

        valor = self.visit(cond)
        if not isinstance(valor, bool):
            raise Nothing(f'\nError: l\'expressió "{cond.getText()}" no retorna un booleà')
        if self.visit(cond):
            return self.visit(ifTrue)
        return self.visit(ifFalse)

    def visitar_operador_binari(self, entrada, nom_funcio):
        # Comprovar errors
        if len(entrada) != 5:
            raise Nothing(
                "\nError: en una operació binaria ha d'haver-hi només 2 paràmetres")

        parametre1 = self.visit(entrada[2])
        parametre2 = self.visit(entrada[3])
        try:
            valor = self.funcions[nom_funcio](parametre1, parametre2)
        except Exception as e:
            raise Nothing(f"\nError al aplicacar un operador binari: {e}")

        return valor

    def visitar_funcio(self, entrada, nom_funcio, ts):
        parametres = entrada[2:-1]
        # Parsejar paràmetres
        valor_parametres = [self.visit(parametre) for parametre in parametres]

        if isinstance(ts[nom_funcio], tuple):
            nom_parametres, expressions = ts[nom_funcio]
        else:
            raise Nothing(f'\nError: {nom_funcio} no és una funció')

        if len(nom_parametres) != len(valor_parametres):
            raise Nothing(
                f'\nError: El número de paràmetres de la funció "{nom_funcio}" no es correcte')

        # Nova taula de símbols de la funció
        ts_funcio = {a: b for a, b in zip(nom_parametres, valor_parametres)}
        # Apilar els paràmetres a la taula de símbols
        self.ts.append(ts_funcio)

        # Recórrer les expressions a evaluar
        for exp in expressions:
            valor = self.visit(exp)

        # Desapilar la darrera ts
        self.ts.pop()
        return valor

    def visitar_cond(self, entrada):
        exps = entrada[2:-1]
        for exp in exps:
            children = list(exp.getChildren())
            cond = self.visit(children[1])
            if cond:
                expresions_a_evaluar = list(children[2:-1])
                for expressio in expresions_a_evaluar:
                    value = self.visit(expressio)
                return value

    def visitar_let(self, entrada):
        assignacions = list(entrada[2].getChildren())
        expressions = entrada[3:-1]
        if not expressions: raise Nothing('La funció "let" espera les expressions')

        # Assignar les variables
        variables_locals = {}

        for assig in assignacions:
            if assig.getText() == '(' or assig.getText() == ')':
                continue

            llista = list(assig.getChildren())
            nom_variable = llista[1].getText()
            variable = self.visit(llista[2])
            variables_locals[nom_variable] = variable

        # Afegir a la taula de símbols
        self.ts.append(variables_locals)
        # Evaluar les expressions
        for expressio in expressions:
            valor = self.visit(expressio)
        # Eliminar de la taula de símbols
        self.ts.pop()

        return valor

    # - Visits - #

    # Root

    def visitRoot(self, ctx):
        statements = list(ctx.getChildren())
        for stat in statements:
            self.visit(stat)

    # Expression
    def visitLlistaEval(self, ctx):
        entrada = list(ctx.getChildren())
        funcio = entrada[1]
        nom_funcio = funcio.getText()

        # Operació de define
        if nom_funcio == 'define':
            self.visitar_define(ctx, entrada)

        # Operació de display
        elif nom_funcio == 'display':
            self.visitar_display(entrada)

        # Operació de if
        elif nom_funcio == 'if':
            return self.visitar_if(entrada)

        # Operador Binari
        elif nom_funcio in self.funcions:
            if nom_funcio == 'not':
                return self.funcions[nom_funcio](self.visit(entrada[2]))
            return self.visitar_operador_binari(entrada, nom_funcio)

        # cond (switch)
        elif nom_funcio == 'cond':
            return self.visitar_cond(entrada)

        # car (per llistes): primer element
        elif nom_funcio == 'car':
            return self.visit(self.visit(entrada[2])[0])

        # cdr (per llistes): tots els elements menys el primer
        elif nom_funcio == 'cdr':
            valor = self.visit(entrada[2])
            return valor[1:len(valor)]

        # cons (per llistes): afegir un element al principi de la llista
        elif nom_funcio == 'cons':
            element = self.visit(entrada[2])
            llista = self.visit(entrada[3])
            return [element] + llista

        # null? (per llistes): comprova si la llista és buida
        elif nom_funcio == 'null?':
            llista = self.visit(entrada[2])
            if not isinstance(llista, list):
                raise Nothing("\nError: L'argument de null? ha de ser una lista")
            return len(llista) == 0

        # let -> assigna valors per ser utilitzats en la següent expressió
        elif nom_funcio == 'let':
            return self.visitar_let(entrada)

        elif nom_funcio == 'read':
            # Entrada del valor
            i = input()
            # Parsejar el valor: bool, int, string
            # Bool
            if i == '#t':
                return True
            if i == '#f':
                return False
            # Int
            try:
                return int(i)
            except ValueError:
                pass
            try:
                if i[0] == "'" and i[1] == '(' and i[len(i) - 1] == ')':
                    raise Nothing("Error: no es permeten llegir les llistes")
            except ValueError:
                pass
            # String
            return i

        elif nom_funcio == 'newline':
            print()

        else:
            # Executar una funcio
            for ts in reversed(self.ts):
                if nom_funcio in ts:
                    return self.visitar_funcio(entrada, nom_funcio, ts)

            # Cas de funció no definida
            raise Nothing(f'\nError: La funció "{nom_funcio}" no està definida')

    def visitLlista(self, ctx):
        entrada = list(ctx.getChildren())
        return entrada[2:-1]

    def visitNumero(self, ctx):
        [numero] = list(ctx.getChildren())
        return int(numero.getText())

    def visitVariable(self, ctx):
        [word] = list(ctx.getChildren())
        for taula_s in reversed(self.ts):
            if (word.getText() in taula_s):
                return taula_s[word.getText()]

        raise Nothing(
            f'\nError: La variable "{word.getText()}" no ha estat declarada')

    def visitBoolea(self, ctx):
        [bool] = list(ctx.getChildren())
        if bool.getText() == '#t':
            return True
        elif bool.getText() == '#f':
            return False
        # En teoria no s'ha d'executar mai
        raise Nothing("\nError inesperat: no s'ha crear un booleà correctament")

    def visitString(self, ctx):
        [str] = list(ctx.getChildren())
        return str.getText()[1:-1]
