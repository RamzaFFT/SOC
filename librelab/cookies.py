import json

# ------------------ Notas ------------------ #
# tps = third parties | tp = third party
# fps = first parties | fp = first party


# ------------------ Funciones ------------------ #

# Crea dos listas:
# nodes = lista con todas las fps con formato de gephi, 
# almacena firstParty para diferenciar entre tp y fp en gephi 
# first_parties = lista con todas las fps
def createNodes():
	nodes = []
	nodes.append("Id;FirstParty\n")

	for website in data.values():
		if website['firstParty']:
			nodes.append("{};{}\n".format(website['hostname'], True))
			first_parties.append(website['hostname'])

	with open('{}_nodes.csv'.format(file_name), 'w') as nodes_file:
		nodes_file.writelines(nodes)


# Crea la lista de aristas
def createEdges():
	edges = []
	edges.append("Source;Target;Type\n")

	for website in data.values():
		if website['firstParty']:
			for third_party in website['thirdParties']:
				edges.append("{};{};Directed\n".format(website['hostname'], third_party))
		else:
			for first_party in website['firstPartyHostnames']:
				edges.append("{};{};Directed\n".format(first_party, website['hostname']))

	with open('{}_edges.csv'.format(file_name), 'w') as edges_file:
		edges_file.writelines(edges)


# Para visualizar una fp y sus tps
# Crea dos listas:
# source_nodes = nodos de la fp source y sus tps
# source_edges = aristas entre la fp source y sus tps
def createSources():
	for source in sources:
		source_nodes = []
		source_nodes.append("Id;FirstParty\n")
		source_nodes.append("{};True\n".format(source))

		source_edges = []
		source_edges.append("Source;Target;Type\n")

		for website in data.values():
			if website['firstParty'] and website['hostname'] == source:
				for third_party in website['thirdParties']:
					source_nodes.append("{};False\n".format(third_party))
					source_edges.append("{};{};Directed\n".format(source, third_party))

		with open('{}_nodes.csv'.format(source), 'w') as nodes_file:
			nodes_file.writelines(source_nodes)

		with open('{}_edges.csv'.format(source), 'w') as edges_file:
			edges_file.writelines(source_edges)


# Para visualizar una tp y las tps o fps que apuntan hacia ella
# Crea dos listas:
# target_nodes = nodos de la tp target y las tps o fps que apuntan hacia ella
# target_edges = aristas entre la tp target y las tps o fps que apuntan hacia ella
def createTargets():
	for target in targets:
		target_nodes = []
		target_nodes.append("Id;FirstParty\n")
		target_nodes.append("{};False\n".format(target))

		target_edges = []
		target_edges.append("Source;Target;Type\n")

		for website in data.values():
			if not website['firstParty'] and website['hostname'] == target:
				for first_party_hostname in website['firstPartyHostnames']:
					if first_party_hostname in first_parties:
						target_nodes.append("{};True\n".format(first_party_hostname))
					else:
						target_nodes.append("{};False\n".format(first_party_hostname))
					target_edges.append("{};{};Directed\n".format(first_party_hostname, target))

		with open('{}_nodes.csv'.format(target), 'w') as nodes_file:
			nodes_file.writelines(target_nodes)

		with open('{}_edges.csv'.format(target), 'w') as edges_file:
			edges_file.writelines(target_edges)


# Crea una lista de aristas entre tps, no aparece ninguna fp
def thirdPartyRelations():
	tps_edges = []
	tps_edges.append("Source;Target;Type\n")

	for website in data.values():
		if not website['firstParty']:
			for first_party_hostname in website['firstPartyHostnames']:
				if first_party_hostname not in first_parties:
					tps_edges.append("{};{};Directed\n".format(first_party_hostname, website['hostname']))

	with open('tps_edges.csv', 'w') as edges_file:
		edges_file.writelines(tps_edges)


# Crea una lista de aristas entre fps, no aparece ninguna tp
def firstPartyRelations():
	fps_edges = []
	fps_edges.append("Source;Target;Type\n")

	for website in data.values():
		if website['firstParty']:
			for third_party in website['thirdParties']:
				if third_party in first_parties:
					fps_edges.append("{};{};Directed\n".format(website['hostname'], third_party))

	with open('fps_edges.csv', 'w') as edges_file:
		edges_file.writelines(fps_edges)


# Crea un archivo csv con las fps que apuntan a las tps target,
# busca la comunes entre ellas y las guarda
# Se usa para saber de todas las fps cuantas usan las tps target
def findNodesWhitTarget(filename, tps_targets):
	list_tps = []
	found_fps = []

	for target in tps_targets:
		for website in data.values():
			if website['hostname'] in first_parties and target in website['thirdParties']:
				found_fps.append(website['hostname'])
		list_tps.append([target, found_fps])
		found_fps = []

	common_fps = []
	found = True
	for target in list_tps[0][1]:
		for row in list_tps:
			if target in row[1]:
				continue
			else:
				print(target)
				break
		common_fps.append(target)

	with open('{}.csv'.format(filename), 'w') as file:
		for row in list_tps:
			file.write('\n# ---------- {} ---------- #\n'.format(row[0]))
			for fp in row[1]:
				file.write('{}\n'.format(fp))

		file.write('\n# --------------- COMMON FPS --------------- #\n')
		for fp in common_fps:
			file.write('{}\n'.format(fp))



# ------------------ Variables ------------------ #

# Nombre del archivo del grafo completo
# Se usa en createNodes y createEdges
file_name = 'librelab'

# En esta lista se guardan las first parties en createNodes
# Se usa para comparar si un nodo es una first party o no
first_parties = []

# Contiene los 3 nodos con más grado de salida 
# Se usa en createSource
sources = ['www.google.es', 'www.minecraftforum.net', 'www.linuxadictos.com']

# Contiene los 3 nodos con más grado de entrada
# Se usa en createTarget
targets = ['fonts.googleapis.com', 'fonts.gstatic.com', 'www.google-analytics.com']

# Contiene las 3 tps con más grado de salida
# Se usa en findNodesWithTarget
top3TPsOutDegree = ['www.pccomponentes.com', 'linuxzone.es', 'www.crunchbase.com']

# Contiene las 3 tps con más grado de entrada
# Se usa en findNodesWithTarget
top3TPsInDegree = ['fonts.googleapis.com', 'fonts.gstatic.com', 'www.google-analytics.com']

# Cargamos el archivo json en el diccionario data
with open('{}.json'.format(file_name), 'r') as data_file:
	data = json.load(data_file)


# ------------------ Main ------------------ #

createNodes()
createEdges()
createSources()
createTargets()
thirdPartyRelations()
firstPartyRelations()

findNodesWhitTarget('top3TPsInDegree', top3TPsInDegree)
findNodesWhitTarget('top3TPsOutDegree', top3TPsOutDegree)