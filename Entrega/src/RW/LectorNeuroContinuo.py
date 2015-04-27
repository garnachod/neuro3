# -*- coding: utf-8 -*-
#solo usar para debug
import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
#fin de solo usar para debug
import re
from src.Instances import Instances
from src.InstanceContinua import InstanceContinua

class LectorNeuroContinuo(object):
	"""docstring for LectorNeuro"""
	def __init__(self):
		super(LectorNeuroContinuo, self).__init__()
		self.delimiters = r' |,|\t|\n|\r|\{|\}'


	def leerFichero(self, nombre_fichero):
		f = open(nombre_fichero,'r')
		#instancias al estilo WEKA
		instances = Instances()

		primeraLinea = f.readline()
		cadenasLinea = re.split(self.delimiters, primeraLinea)
		numeroEntradas = int(cadenasLinea[0])
		numeroClases = int(cadenasLinea[1])

		for i in range(0, numeroEntradas):
			instances.addColumna(str(i), "REAL")

		for i in range(0, numeroClases):
			instances.addClase(str(i))

		for line in iter(lambda: f.readline(), ''):
			tokens = self.privateLimpiaVacioTokens(re.split(self.delimiters, line))
			#print tokens
			if len(tokens) <= 0:
				break
			#instancia al estilo WEKA
			instance = InstanceContinua()
			#se anyaden las entradas del perceptron
			for i in range(0, numeroEntradas):
				instance.addElement(float(tokens[i]))

			#solo funcionara con salidas numericas
			for i in range(numeroEntradas, numeroEntradas + numeroClases):
				instance.addElement(float(tokens[i]))

			instance.getVectorObjetivoSalida(numeroClases)
			instances.addInstance(instance)

		f.close()
		return instances

	def privateLimpiaVacioTokens(self, tokens):
		lista = []
		for token in tokens:
			if token == '':
				pass
			else:
				lista.append(token)

		return lista