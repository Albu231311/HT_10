import sys

INF = float('inf')

def leer_grafo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    ciudades = set()
    aristas = {}
    
    for linea in lineas:
        datos = linea.strip().split()
        ciudad1, ciudad2 = datos[0], datos[1]
        tiempos = list(map(int, datos[2:]))
        
        ciudades.add(ciudad1)
        ciudades.add(ciudad2)
        
        if ciudad1 not in aristas:
            aristas[ciudad1] = {}
        if ciudad2 not in aristas:
            aristas[ciudad2] = {}
        
        aristas[ciudad1][ciudad2] = tiempos
        aristas[ciudad2][ciudad1] = tiempos  # Asumiendo un grafo no dirigido
    
    return list(ciudades), aristas

def inicializar_matrices(ciudades, aristas, condicion_climatica=0):
    n = len(ciudades)
    dist = [[INF] * n for _ in range(n)]
    siguiente_ciudad = [[None] * n for _ in range(n)]
    
    indice_ciudad = {ciudad: idx for idx, ciudad in enumerate(ciudades)}
    
    for i in range(n):
        dist[i][i] = 0
    
    for ciudad1 in aristas:
        for ciudad2 in aristas[ciudad1]:
            i, j = indice_ciudad[ciudad1], indice_ciudad[ciudad2]
            dist[i][j] = aristas[ciudad1][ciudad2][condicion_climatica]
            siguiente_ciudad[i][j] = ciudad2
    
    return dist, siguiente_ciudad, indice_ciudad

def floyd_warshall(dist, siguiente_ciudad, n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    siguiente_ciudad[i][j] = siguiente_ciudad[i][k]

def construir_camino(siguiente_ciudad, indice_ciudad, inicio, fin):
    if siguiente_ciudad[indice_ciudad[inicio]][indice_ciudad[fin]] is None:
        return None
    
    camino = [inicio]
    while inicio != fin:
        inicio = siguiente_ciudad[indice_ciudad[inicio]][indice_ciudad[fin]]
        camino.append(inicio)
    
    return camino

def encontrar_centro_grafo(dist, ciudades):
    excentricidad = [max(fila) for fila in dist]
    min_excentricidad = min(excentricidad)
    centro = ciudades[excentricidad.index(min_excentricidad)]
    return centro