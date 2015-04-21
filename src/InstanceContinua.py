from Instance import Instance

class InstanceContinua(Instance):

	def getVectorObjetivoSalida(self, nclases = None):
		if self.bipVectorObjetivo == None:
			tam = len(self.listaDatos)
			self.bipVectorObjetivo = []
			for indice in range(tam - nclases, tam):
				self.bipVectorObjetivo.append(self.listaDatos[indice])
				
		return self.bipVectorObjetivo