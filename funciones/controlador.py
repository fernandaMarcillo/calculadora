import sumar
import restar
import multiplicar
import dividir

class ControladorCalculadora:
    def __init__(self):
        self.num1 = ""
        self.op = None
        self.nuevo_numero = False

    def presionar_digito(self, texto_actual, digito):
        if texto_actual == "0" or self.nuevo_numero or texto_actual == "Error":
            self.nuevo_numero = False
            return digito
        else:
            return texto_actual + digito

    def presionar_operacion(self, texto_actual, operacion):
        self.num1 = texto_actual
        self.op = operacion
        self.nuevo_numero = True
        return texto_actual

    def presionar_c(self):
        self.num1 = ""
        self.op = None
        self.nuevo_numero = False
        return "0"

    def presionar_igual(self, texto_actual):
        if self.op is None or self.num1 == "":
            return texto_actual

        val1 = float(self.num1)
        val2 = float(texto_actual)
        resultado = 0

        if self.op == '+':
            resultado = sumar.ejecutar(val1, val2)
        elif self.op == '-':
            resultado = restar.ejecutar(val1, val2)
        elif self.op == '*':
            resultado = multiplicar.ejecutar(val1, val2)
        elif self.op == '/':
            resultado = dividir.ejecutar(val1, val2)

        self.op = None
        self.num1 = ""
        self.nuevo_numero = True

        if resultado == "Error":
            return "Error"
        elif resultado.is_integer():
            return str(int(resultado))
        else:
            return str(resultado)
