import sys

# f_ori y f_fin son ficheros ya abiertos
# na y ns enteros > 0
def adaptaFicheroSerie(f_ori, f_fin, na, ns):
	data = f_ori.read().split('\n')

	f_fin.write(str(na) + ' ' + str(ns))

	for i in range(0, len(data) - na - ns):
		f_fin.write('\n')

		for j in range(0, na):
			f_fin.write(data[i + j] + ' ')

		for k in range(0, ns - 1):
			f_fin.write(data[i + na + k] + ' ')
		f_fin.write(data[i + na + ns - 1]) # separamos el bucle por el espacio final



if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Se requieren 4 argumentos. f_ori, f_fin, na, ns."
		sys.exit(0)

	f_ori = open(sys.argv[1], 'r')
	f_fin = open(sys.argv[2], 'w')

	adaptaFicheroSerie(f_ori, f_fin, int(sys.argv[3]), int(sys.argv[4]))

	f_ori.close()
	f_fin.close()