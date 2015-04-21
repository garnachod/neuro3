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
from time import time
from operator import add,mul


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

	if len(sys.argv) != 6:
		print "Error en la llamada. Se esperan los siguientes argumentos:"
		print "\t1.- Nombre del fichero con los datos del problema."
		print "\t2.- El porcentaje del conjunto de train. Expresar como un numero entre 0 y 1 utilizando el punto como divisor decimal."
		print "\t3.- La tasa de aprendizaje."
		print "\t4.- El numero de neuronas de la capa oculta."
		print "\t5.- El nombre del fichero donde debe escribirse el error cuadratico medio en cada epoca. Se borrara el fichero si ya existe."
		print "Ejemplo de llamada: python main.py xor.txt 1 0.1 2 xor_error.txt"
		sys.exit(-1)

	
	f_ori = open(sys.argv[1], 'r')
	f_fin = open("aux_temp.txt", 'w')
	adaptaFicheroSerie(f_ori, f_fin, 5 , 1)
	f_ori.close()
	f_fin.close()
	lector = LectorNeuroContinuo()
	instances = lector.leerFichero("aux_temp.txt")

	
	porcentajeParticionado = float(sys.argv[2])
	particionado = DivisionPorcentual()
	particionado.setPorcentajeTrain(porcentajeParticionado)
	particion = particionado.generaParticiones(instances, False)
	
	
	print "Multilayer Perceptron"
	clasificador = RedNeuronalTemporal()
	clasificador.setParameters('nNeuronas=' + sys.argv[4])
	clasificador.setParameters('alpha=' + sys.argv[3])
	clasificador.setParameters('nEpocas=1000')
	clasificador.setParameters('debugFile=' + sys.argv[5])
	clasificador.setDebug(True)
	start_time = time()
	clasificador.buildClassifier(particion.getTrain())
	elapsed_time = time() - start_time
	print("Elapsed time: %0.10f seconds." % elapsed_time)

	print "Error TRAIN:"
	f_deb = open("aux_temp_deb.txt", 'w')
	calculaError(clasificador, particion.getTrain(),f_deb)
	if porcentajeParticionado != 1.0:
		print "Error TEST:"
		calculaError(clasificador, particion.getTest(),f_deb)

	f_deb.close()
	#fout = open("predicciones_nnet.txt", "w")

	# clasificador del nuevo
	"""instances = lector.leerFichero(sys.argv[6])
	for instance in instances.getListInstances():
		clase = clasificador.classifyInstance(instance)
		if int(clase) == 0:
			fout.write('0 1\n')
		else:
			fout.write('1 0\n')
"""
	#print clasificador.classifyInstance(instances.getListInstances()[4])
	#print (instances.getListInstances()[4]).getClase()

