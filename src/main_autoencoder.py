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

def calculaError(clasificador, instances):
	nError = 0
	for instance in instances.getListInstances():
		vectorSalida = clasificador.computeInstance(instance)
		vectorObjetivo = instance.getBipolarVectorObjetivoSalida()
		for indice in range(len(vectorSalida)):
			if vectorSalida[indice] > 0:
				vectorSalida[indice] = 1.0
			else:
				vectorSalida[indice] = -1.0
			if vectorSalida[indice] != vectorObjetivo[indice]:
				nError += 1

	print nError
if __name__ == '__main__':
	lector = LectorNeuroMatriz()
	instances = lector.leerFichero("../data/alfabeto_dat.txt")

	clasificador = RedNeuronalMatriz()
	clasificador.setParameters('nNeuronas=12')
	clasificador.setParameters('alpha=0.1')
	clasificador.setParameters('nEpocas=3000')


	start_time = time()
	clasificador.buildClassifier(instances)
	elapsed_time = time() - start_time
	print("Elapsed time: %0.10f seconds." % elapsed_time)

	calculaError(clasificador,instances)
