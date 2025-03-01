ANTLR_JAR=antlr-4.13.2-complete.jar
GRAMMAR=scheme.g4
OUTPUT_DIR=.

# Compila amb l'arxiu .jar de l'antlr
all:
	java -jar $(ANTLR_JAR) -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR) -o $(OUTPUT_DIR)

# Executa el programa amb la terminal com input
run:
	python3 scheme.py

# Neteja els arxius
clean:
	rm -f *.pyc *.tokens *.interp
	rm -rf __pycache__/
	rm schemeLexer.py schemeParser.py schemeVisitor.py