import json

# ------------------ Notas ------------------ #
# website[0] = source
# website[1] = target
# website[4] = usesCookies
# website[5] = isVisited
# website[6] = isSecure


# ------------------ Funciones ------------------ #

# Crea la la lista de nodos y aristas del grafo completo y las guarda
def generateAll():
	edges = list(format_edges)
	nodes = list(default_nodes)

	format_nodes = []
	format_nodes.append("Id;FirstParty\n")
	for node in nodes:
		format_nodes.append("{};{}\n".format(node, True))

	for website in data:
		if website[0] != website[1]:
			edges.append("{};{};Directed;{};{}\n".format(website[0], website[1], website[4], website[6]))
		if website[0] not in nodes:
			nodes.append(website[0])
			format_nodes.append("{};{}\n".format(website[0], False))

	with open('{}_edges.csv'.format(file_name), 'w') as edges_file:
	    edges_file.writelines(edges)

	with open('{}_nodes.csv'.format(file_name), 'w') as nodes_file:
		nodes_file.writelines(format_nodes)


# Crea una lista de aristas con la fp source y sus tps
def generateSource(source):
	edges = list(format_edges)

	for website in data:
		if website[0] != website[1]:			
			if website[0] == source and not website[5]:
				edges.append("{};{};Directed;{};{}\n".format(website[0], website[1], website[4], website[6]))

	with open('Source: {}.csv'.format(source), 'w') as edges_file:
	    edges_file.writelines(edges)


# Crea una lista de aristas con la tp target y las fps y tps que apuntan a ella
def generateTarget(target):
	edges = list(format_edges)

	for website in data:
		if website[0] != website[1]:
			if website[1] == target and not website[5]:
				edges.append("{};{};Directed;{};{}\n".format(website[0], website[1], website[4], website[6]))

	with open('Target: {}.csv'.format(target), 'w') as edges_file:
	    edges_file.writelines(edges)


# Crea una lista de aristas con las relaciones entre las tps, sin ninguna fp
def thirdPartyRelations():
	tps_edges = list(format_edges)

	for website in data:
		if website[0] not in default_nodes and website[1] not in default_nodes and website[0] != website[1]:
			tps_edges.append("{};{};Directed;{};{}\n".format(website[0], website[1], website[4], website[6]))

	with open('tps_edges.csv', 'w') as edges_file:
		edges_file.writelines(tps_edges)


# Crea una lista de aristas con las relaciones entre las fps, sin ninguna tp
def firstPartyRelations():
	fps_edges = list(format_edges)

	for website in data:
		if website[0] in default_nodes and website[1] in default_nodes and website[0] != website[1]:
			fps_edges.append("{};{};Directed;{};{}\n".format(website[0], website[1], website[4], website[6]))

	with open('fps_edges.csv', 'w') as edges_file:
		edges_file.writelines(fps_edges)  # guardar en el csv


# Encuentra las fps que tiene una arista con la tp target y las muestra
def findNodesWhitTarget(targets):
	foundNodes = []

	for target in targets:
		print('\n# ----------------------------------------------- #\n')
		print('Default nodes pointing to {}:'.format(target)) 
		for website in data:
			if website[0] in default_nodes and website[1] == target and website[0] not in foundNodes:
				foundNodes.append(website[0])
				print(website[0])
		if len(foundNodes) == 0:
			print('None')
		foundNodes = []
	print('\n# ----------------------------------------------- #')


# ------------------ Variables ------------------ #

file_name = 'popular'

# first parties estudiadas
default_nodes = [
	'google.es',
	'google.com',
	'ucm.es',
	'minijuegos.com',
	'seriesblanco.com',
	'wikipedia.org',
	'twitter.com',
	'youtube.com',
	'github.com',
	'urjc.es',
	'uax.es',
	'yahoo.com',
	'thepiratebay-proxylist.org',
	'pornhub.com',
	'forocoches.com',
	'facebook.com',
	'instagram.com'
]

# Aristas iniciales
format_edges = []
format_edges.append("Source;Target;Type;Cookie;Secure\n")

# Las 3 tps con mas frado de salida
top3OutDegree = ['doubleclick.net', 'google-analytics.com', 'mathtag.com']

# Cargamos el archivo json en el diccionario data
with open('{}.json'.format(file_name), 'r') as data_file:
	data = json.load(data_file)


# ------------------ Main ------------------ #

generateAll()
thirdPartyRelations()
firstPartyRelations()

findNodesWhitTarget(top3OutDegree)

for node in default_nodes:
	generateSource(node)
	generateTarget(node)