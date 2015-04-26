# -*- coding: utf-8 -*-
import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from Clasificadores.RedNeuronalMatriz import RedNeuronalMatriz
from Particionado.DivisionPorcentual import DivisionPorcentual
from Particionado.Particion import Particion
from RW.LectorNeuroMatriz import LectorNeuroMatriz
from InstanceMatriz import InstanceMatriz
from Instances import Instances
from time import time
import random

def calculaError(clasificador, instances, debug = False):
	nErrorMedio = 0
	nLetrasFalladas = 0
	i = 0
	for instance in instances.getListInstances():
		i += 1
		nError = 0
		vectorSalida = clasificador.computeInstance(instance)
		vectorObjetivo = instance.getBipolarVectorObjetivoSalida()
		for indice in range(len(vectorSalida)):
			if vectorSalida[indice] > 0:
				vectorSalida[indice] = 1.0
			else:
				vectorSalida[indice] = -1.0
			if vectorSalida[indice] != vectorObjetivo[indice]:
				nError += 1

		if debug == True:
			if nError > 0:
				print "Error en la letra: " + str(i)
		if nError > 0:
			nLetrasFalladas += 1
		nErrorMedio += nError


	print "#letras falladas:" + str(nLetrasFalladas)
	print "#letras acertadas: " + str(instances.getNumeroInstances() - nLetrasFalladas)

	return nErrorMedio/float(instances.getNumeroInstances())


def generaInstanciasRuidosaFromInstance(nInstanciasAGenerar, instanciaBase, f):
	arrayInstances = []
	nElementos = len(instanciaBase.getAllElements())
	tamEntrada = nElementos/2

	for i in range(nInstanciasAGenerar):
		instancia = instanciaBase.duplica()
		arrayElem = instancia.getAllElements()
		#print "antes : " + str(arrayElem[:35])
		for j in range(f):
			indiceAModificar = int(random.random()*tamEntrada)
			#print "cambio en " + str(indiceAModificar)
			if arrayElem[indiceAModificar] == 0.0:
				arrayElem[indiceAModificar] = 1.0
			else: 
				arrayElem[indiceAModificar] = 0.0
		#print "despues : " + str(arrayElem[:35])
		arrayInstances.append(instancia)

	return arrayInstances

if __name__ == '__main__':
	F = 5
	NintanciasGenerarEntrenamiento = 5
	ruidoTest = False
	ruidoEntrenamiento = False
	lector = LectorNeuroMatriz()
	instances = lector.leerFichero("../data/alfabeto_dat.txt")

	clasificador = RedNeuronalMatriz()
	clasificador.setParameters('nNeuronas=12')
	clasificador.setParameters('alpha=0.1')
	clasificador.setParameters('nEpocas=3000')

	if ruidoEntrenamiento == True:
		instanciasAnyadir = []
		for instance in instances.getListInstances():
			arrayIntances = generaInstanciasRuidosaFromInstance(NintanciasGenerarEntrenamiento, instance, F)
			for instanceIntroduce in arrayIntances:
				instanciasAnyadir.append(instanceIntroduce)

		for instance in instanciasAnyadir:
			instances.addInstance(instance)


	start_time = time()
	clasificador.buildClassifier(instances)
	elapsed_time = time() - start_time
	print("Elapsed time: %0.10f seconds." % elapsed_time)
	print "Train:"

	errorMedio = calculaError(clasificador,instances, True)
	print errorMedio

	if ruidoTest == True:
		instanciasAnyadir = []
		nInstances = 26
		i = 0
		for instance in instances.getListInstances():
			if i >= nInstances:
				break
			arrayIntances = generaInstanciasRuidosaFromInstance(10, instance, F)
			for instanceIntroduce in arrayIntances:
				instanciasAnyadir.append(instanceIntroduce)

			i+=1

		for instance in instanciasAnyadir:
			instances.addInstance(instance)
	print "Test:"
	errorMedio = calculaError(clasificador,instances, True)
	print errorMedio
