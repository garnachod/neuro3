from Instance import Instance

class InstanceMatriz(Instance):
	def getVectorObjetivoSalida(self, nclases = None):
		return sefl.getBipolarVectorObjetivoSalida(nclases)
		
	def getBipolarVectorObjetivoSalida(self, nclases = None):
		if self.bipVectorObjetivo == None:
			self.generaBipolarVectorObjetivoSalida(nclases)

		return self.bipVectorObjetivo

	def generaBipolarVectorObjetivoSalida(self, nclases):
		tam = len(self.listaDatos)
		self.bipVectorObjetivo = []
		for indice in range(tam - nclases, tam):
			if(self.listaDatos[indice] == 0):
				self.bipVectorObjetivo.append(-1)
			else:
				self.bipVectorObjetivo.append(1)

	def duplica(self):
		instanceRetorno = InstanceMatriz()
		instanceRetorno.listaDatos = list(self.listaDatos)
		instanceRetorno.instances = self.instances
		instanceRetorno.bipVectorObjetivo = list(self.bipVectorObjetivo)
		return instanceRetorno