# -*- coding: utf-8 -*-
import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from Clasificadores.RedNeuronalTemporal import RedNeuronalTemporal
from Particionado.DivisionPorcentual import DivisionPorcentual
from Particionado.Particion import Particion
from RW.LectorNeuroContinuo import LectorNeuroContinuo
from RW.AdaptaFicheroSerie import *
from Instance import Instance
from Instances import Instances
from InstanceContinua import InstanceContinua
from time import time
from operator import add,mul
import pdb


def calculaError(clasificador, instances, f_test=None):
	cuadratico = 0.0

	for instance in instances.getListInstances():
		vectorObj = instance.getVectorObjetivoSalida()
		prediccion = clasificador.classifyInstance(instance)
		if f_test != None:
			f_test.write(str(prediccion[0]) + '\n')

		#print "clase: " + str(clase) + " prediccion: " + str(prediccion)
		cuadratico_instancia = reduce(add, map((lambda x, y: (x - y)**2), vectorObj, prediccion))
		cuadratico += cuadratico_instancia

	print "error cuadratico = " + str(cuadratico/instances.getNumeroInstances())

def calculaErrorSimple(clasificador, na, instances):
	cuadratico = 0.0

	for instance in instances.getListInstances():
		vectorObj = instance.getVectorObjetivoSalida()
		# print("\to " + ", ".join(map(str, vectorObj)))

		prediccion = map(lambda x: instance.getElementAtPos(na - 1), vectorObj)
		# print("\tp " + ", ".join(map(str, prediccion)))

		#print "clase: " + str(clase) + " prediccion: " + str(prediccion)
		cuadratico_instancia = reduce(add, map((lambda x, y: (x - y)**2), vectorObj, prediccion))
		cuadratico += cuadratico_instancia

	print "error cuadratico simple = " + str(cuadratico/instances.getNumeroInstances())

def prediceRecursivamente(clasificador, instance, na, nf, f=None):
	instanceRecursive = InstanceContinua()

	# Primero hacemos una copia
	for i in range(0, na):
		instanceRecursive.addElement(instance.getElementAtPos(i))

	# Vamos creando cada predicción usando las anteriores
	for _ in range(0, nf):
		prediccion = clasificador.classifyInstance(instanceRecursive)
		if f != None:
			f.write(str(prediccion[0]) + '\n')
		instanceRecursive.shiftAndAdd(round(prediccion[0], 2))
	

def returnError(clasificador, instances):
	error = 0.0

	for instance in instances.getListInstances():
		clase = instance.getClase()
		prediccion = clasificador.classifyInstance(instance)
		#print "clase: " + str(clase) + " prediccion: " + str(prediccion)

		if prediccion != clase:
			error += 1.0

	procentajeError = error / float(instances.getNumeroInstances())
	return procentajeError



if __name__ == '__main__':

	if len(sys.argv) != 10:
	 	print "Error en la llamada. Se esperan los siguientes argumentos:"
	 	print "\t1.- Nombre del fichero con los datos del problema."
	 	print "\t2.- Na."
	 	print "\t3.- Ns."
	 	print "\t4.- Nf."
	 	print "\t5.- Lista con los puntos desde los que se debe empezar a predecir recursivamente."
	 	print "\t6.- El porcentaje del conjunto de train. Expresar como un numero entre 0 y 1 utilizando el punto como divisor decimal."
	 	print "\t7.- La tasa de aprendizaje."
	 	print "\t8.- El numero de neuronas de la capa oculta."
	 	print "\t9.- El nombre del fichero donde debe escribirse el error cuadratico medio en cada epoca. Se borrara el fichero si ya existe."
	 	print "Ejemplo de llamada: python main_temporal.py p3_serie2.txt 5 1 50 \"0 100 200 300 400\" 0.5 0.001 40 out.txt"
	 	sys.exit(-1)


	f_in = sys.argv[1]
	na = int(sys.argv[2])
	ns = int(sys.argv[3])
	nf = int(sys.argv[4])

	if sys.argv[5] != '[]':
		listaDeComienzos = map(int, sys.argv[5].split())
		listaDeComienzos.sort()
	else:
	 	listaDeComienzos = []

	porcentajeParticionado = float(sys.argv[6])
	alpha = sys.argv[7]
	nNeuronas = sys.argv[8]
	debugFile = sys.argv[9]

	goodFile = f_in +  '_' + str(na) + '-' + str(ns)

	if not os.path.isfile(goodFile):
		f1 = open(f_in, 'r')
		f2 = open(goodFile, 'w')
		adaptaFicheroSerie(f1, f2, na, ns)
		f1.close()
		f2.close()


	lector = LectorNeuroContinuo()
	instances = lector.leerFichero(goodFile)

	
	particionado = DivisionPorcentual()
	particionado.setPorcentajeTrain(porcentajeParticionado)
	particion = particionado.generaParticiones(instances, False)
	
	
	print "Multilayer Perceptron"
	clasificador = RedNeuronalTemporal()
	clasificador.setParameters('nNeuronas=' + nNeuronas)
	clasificador.setParameters('alpha=' + alpha)
	clasificador.setParameters('nEpocas=1000')
	clasificador.setParameters('debugFile=' + debugFile)
	clasificador.setDebug(True)
	start_time = time()
	clasificador.buildClassifier(particion.getTrain())
	elapsed_time = time() - start_time
	print("Elapsed time: %0.10f seconds." % elapsed_time)


	print "Error TRAIN:"
	f_deb = open("aux_temp_deb.txt", 'w')
	calculaError(clasificador, particion.getTrain(), f_deb)
	calculaErrorSimple(clasificador, na, particion.getTrain())

	if porcentajeParticionado != 1.0:
		print "Error TEST:"
		calculaError(clasificador, particion.getTest(), f_deb)
		calculaErrorSimple(clasificador, na, particion.getTest())

	if nf > 0 and listaDeComienzos:
		instancesList = instances.getListInstances()
		for i in listaDeComienzos:
			# pdb.set_trace()
			f_deb.write("Predicción de " + str(nf) + " puntos empezando en " + str(i) + ":\n")
			prediceRecursivamente(clasificador, instancesList[i], na, nf, f_deb)



	f_deb.close()

