# MINI-SCHEME

## Requisits
1. `Python 3.x`
2. `pip` amb les següents llibreries (`pip install nom_llibreria`):
    - antlr4-tools
    - antlr4-python3-runtime

## Executar el programa
1. Compilar amb la comanda `make` (has de tenir-ho instal·lat)
2. Executar el programa de dues maneres:
    - Escriure el programa via terminal amb la comanda `python3 scheme.py` o amb la comanda `make run`
    - Introduir el programa via un arxiu .scm amb la comanda `python3 scheme.py nom_programa.scm`
        - Es pot afegir input i output al programa amb la comanda `python3 scheme.py nom_programa.scm <nom_input.inp >nom_output.out`

## Documentació

### scheme.py
#### Descripció del Codi

Aquest codi és un intèrpret per al llenguatge Scheme, que utilitza ANTLR per analitzar l'entrada i un visitant (`EvalVisitor`) per avaluar expressions. El programa pot llegir un arxiu de codi Scheme o utilitzar l'entrada estàndard.

##### Lectura d'Entrada
- Si s'especifica un arxiu, es llegeix.
- Si no, es pren l'entrada per teclat.

##### Anàlisi
- Utilitza `schemeLexer` i `schemeParser` per generar l'arbre de sintaxi.

##### Avaluació
- L'arbre de sintaxi es recorre amb `EvalVisitor` per avaluar les expressions.

##### Errors
- Gestiona errors com arxius no trobats o sintaxi incorrecta.

---

### EvalVisitor.py

### EvalVisitor.py

#### Descripció
`EvalVisitor` hereta de `schemeVisitor` i s'encarrega d'avaluar les expressions de Scheme segons el context proporcionat. Aquesta classe manté una taula de símbols (`ts`) i disposa d'un conjunt de funcions predefinides per realitzar operacions aritmètiques i lògiques.

#### Atributs
- `funcions`: Diccionari que emmagatzema les funcions predefinides (operacions aritmètiques i lògiques com `+`, `-`, `*`, `not`, etc.).
- `ts`: Taula de símbols que actua com l'entorn d'avaluació. Al principi conté un sol diccionari amb la variable `else` per a les condicions.

#### Mètodes
##### `__init__(self)`
Inicialitza la classe creant una taula de símbols buida (`ts`) i assigna `else` al primer nivell de la taula.

##### Mètodes Auxiliars
- `print_display(self, entrada)`: Imprimeix de manera recursiva el valor de `entrada`. Suporta valors booleans, enters, flotants, cadenes, llistes i expressions.
- `visitar_define(self, ctx, entrada)`: Defineix funcions o variables en l'entorn d'execució. Comprova errors i gestiona funcions amb paràmetres.
- `visitar_display(self, entrada)`: Imprimeix un valor per consola. Comprova que només hi hagi un argument.
- `visitar_if(self, entrada)`: Avalua una condició `if`. Comprova que l'expressió condicional retorni un valor booleà.
- `visitar_operador_binari(self, entrada, nom_funcio)`: Aplica un operador binari (com `+`, `-`, etc.) a dos paràmetres.
- `visitar_funcio(self, entrada, nom_funcio, ts)`: Avalua una funció definida per l'usuari, comprovant els paràmetres i executant les expressions associades.
- `visitar_cond(self, entrada)`: Avalua l'expressió `cond`, executant la primera clàusula el valor de la qual sigui vertader.
- `visitar_let(self, entrada)`: Permet l'assignació de variables locals per al seu ús posterior dins d'una expressió.

##### Mètodes `visit`
Aquests mètodes implementen el recorregut de les estructures del llenguatge:

- `visitRoot(self, ctx)`: Inicia el recorregut de les declaracions.
- `visitLlistaEval(self, ctx)`: Avaluar una llista d'expressions. Comprova el tipus d'operació i gestiona casos com `define`, `if`, `let`, etc.
- `visitLlista(self, ctx)`: Retorna una llista d'expressions.
- `visitNumero(self, ctx)`: Converteix un node de número en el seu valor enter.
- `visitVariable(self, ctx)`: Busca el valor d'una variable a la taula de símbols.
- `visitBoolea(self, ctx)`: Converteix un valor booleà (`#t` o `#f`) en un valor de tipus `bool`.
- `visitString(self, ctx)`: Converteix una cadena en un valor de tipus `str`.

#### Funcions Suportades
- **Operadors Aritmètics**: `+`, `-`, `*`, `/`, `mod`
- **Operadors Relacionals**: `<`, `>`, `<=`, `>=`, `=`, `<>`
- **Operadors Lògics**: `and`, `or`, `not`
- **Condicionals**: `if`, `cond`
- **Estructures de Llistes**: `car`, `cdr`, `cons`, `null?`
- **Funcions d'Entrada/Sortida**: `display`, `read`, `newline`

#### Execució d'Expressions
El mètode `visitLlistaEval` s'encarrega de l'avaluació d'expressions, cercant funcions i operadors específics i cridant el mètode corresponent per a cadascun. Si es troba un error (per exemple, nombre incorrecte de paràmetres o funció no definida), es llança una excepció `Nothing`.

---

### exceptions.py
- `Nothing`: Petita classe que permet enviar els meus propis missatges d'error (inspiració del nom per part de Gerard Escudero).

---

### Jocs de prova:

#### prova1
Calcula la suma i el màxim d'una llista de números utilitzant recursió. La funció `suma-llista` retorna la suma dels elements, i `maxim` troba el valor màxim. La funció `procesa-lista` mostra els resultats.

#### prova2
Aquesta prova defineix dues funcions: `suma`, que suma dos nombres, i `producte`, que intenta multiplicar tres nombres, però es crida amb només dos, causant un error. La funció `main` llegeix dos números i mostra la suma, però genera un error en intentar calcular el producte.

#### prova3
Mostra errors comuns en Scheme:
- Error en la condició if per falta d'expressió a executar.
- Error en utilitzar variables no definides.
- Error en definir funcions dins d'altres funcions.

#### prova4
Mostra l'ús de la funció `aplica-dos-cops` que aplica una funció dues vegades a un valor. Es mostra el resultat de passar funcions com increment i doble, i un error quan s'intenta passar un número com a funció.

#### prova5
Defineix la funció `calcula` que realitza operacions sobre dos valors. Depenent del resultat de la resta, retorna la suma més el producte o la resta menys el producte. Es mostren els resultats per a les entrades `(4, 2)` i `(2, 4)`.

## Anotacions extra
- Les funcions a l'`EvalVisitor` que són de la gramàtica no estan en CamelCase perquè no he pogut canviar-ho (si ho canvio no compila). La resta del codi està en el format indicat (PEP8).
- Cada input es fa amb una línia.
- És necessari l'ús de la funció `main`. Si no es fa servir, s'envia un error. 
### Example
```scheme
(input) ; Suposem que es volen introduir els números 10 i 15
```
Output:
```
10
15
```
- Els errors que provoca el "define" es produeixen quan es criden a les funcions definides.
- He fet que amb la funció "read" no es puguin llegir llistes (per simplicitat).