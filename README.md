# SOC
Trabajo de la asignatura Análisis de Redes Sociales del grupo 5

El objetivo de este proyecto es, utilizando la extensión de firefox "lightbeam", encontrar las third parties que tienen acceso a la información de los usuarios y analizar los efectos que esto puede tener. 


### Instrucciones de uso:

1. Guardar en una carpeta los archivos lightbeam2gephi.py y popular.json y en otra los archivos cookies.py y librelab.json.
2. Abrir estas carpetas en una terminal.
3. Ejecutar el código fuente con el intérprete de python 3Ñ
  ```python
  python3 lightbeam2gephi.py
  python3 cookies.py
  ```


### Para importar los archivos en gephi:
* Si el grafo utiliza archivos de nodos y aristas importar primero nodos y después aristas
* Si no importar aristas directamente


### Para visualizar en gephi
Hemos usado varios tipos de visualizaciones, el más genérico es:
* Nodos:
  * Color: Utilizando la propiedad firstParty, amarillo si es FP, azul si es TP.
  * Tamaño: Utilizando la propiedad grado, ranking entre 30 y 100.
* Aristas:
  * Color: Utilizando propiedad cookie, rojo si true verde si false. (Color del nodo en grafos de librelab)
* Distribución: Force Atlas 2
  * Escalado: 130. (variar para conseguir la visualización apropiada)
  * Disadir Hubs: Marcado.
  * Evitar solapamiento: Marcado.
