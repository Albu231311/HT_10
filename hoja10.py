import sys

# Definir una constante para representar el infinito
INF = float('inf')

def leer_grafo(nombre_archivo):
    # Leer el archivo y almacenar los datos en un conjunto de ciudades y un diccionario de aristas
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    ciudades = set()  # Conjunto para almacenar los nombres de las ciudades
    aristas = {}  # Diccionario para almacenar los tiempos de viaje entre ciudades
    
    for linea in lineas:
        # Separar los datos de cada línea y convertir los tiempos a enteros
        datos = linea.strip().split()
        ciudad1, ciudad2 = datos[0], datos[1]
        tiempos = list(map(int, datos[2:]))
        
        # Agregar las ciudades al conjunto
        ciudades.add(ciudad1)
        ciudades.add(ciudad2)
        
        # Inicializar las entradas en el diccionario de aristas si no existen
        if ciudad1 not in aristas:
            aristas[ciudad1] = {}
        if ciudad2 not in aristas:
            aristas[ciudad2] = {}
        
        # Asignar los tiempos de viaje a las aristas en ambas direcciones
        aristas[ciudad1][ciudad2] = tiempos
        aristas[ciudad2][ciudad1] = tiempos  # Asumiendo un grafo no dirigido
    
    # Retornar la lista de ciudades y el diccionario de aristas
    return list(ciudades), aristas

def inicializar_matrices(ciudades, aristas, condicion_climatica=0):
    # Inicializar las matrices de distancia y siguiente ciudad
    n = len(ciudades)
    dist = [[INF] * n for _ in range(n)]  # Matriz de distancias
    siguiente_ciudad = [[None] * n for _ in range(n)]  # Matriz de siguiente ciudad
    
    # Crear un diccionario para mapear los nombres de las ciudades a sus índices
    indice_ciudad = {ciudad: idx for idx, ciudad in enumerate(ciudades)}
    
    # La distancia de una ciudad a sí misma es 0
    for i in range(n):
        dist[i][i] = 0
    
    # Llenar la matriz de distancias con los tiempos de viaje proporcionados
    for ciudad1 in aristas:
        for ciudad2 in aristas[ciudad1]:
            i, j = indice_ciudad[ciudad1], indice_ciudad[ciudad2]
            dist[i][j] = aristas[ciudad1][ciudad2][condicion_climatica]
            siguiente_ciudad[i][j] = ciudad2
    
    # Retornar las matrices y el diccionario de índices de ciudades
    return dist, siguiente_ciudad, indice_ciudad

    # Implementar el algoritmo de Floyd-Warshall para encontrar las rutas más cortas
def floyd_warshall(dist, siguiente_ciudad, n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    siguiente_ciudad[i][j] = siguiente_ciudad[i][k]

    # Construir el camino más corto entre dos ciudades utilizando la matriz de siguiente ciudad
def construir_camino(siguiente_ciudad, indice_ciudad, inicio, fin):
    if siguiente_ciudad[indice_ciudad[inicio]][indice_ciudad[fin]] is None:
        return None
    
    camino = [inicio]
    while inicio != fin:
        inicio = siguiente_ciudad[indice_ciudad[inicio]][indice_ciudad[fin]]
        camino.append(inicio)
    
    return camino

# Encontrar el centro del grafo calculando la excentricidad de cada ciudad
def encontrar_centro_grafo(dist, ciudades):
    excentricidad = [max(fila) for fila in dist]
    min_excentricidad = min(excentricidad)
    centro = ciudades[excentricidad.index(min_excentricidad)]
    return centro

# Actualizar el grafo con nuevos tiempos de viaje entre dos ciudades
def actualizar_grafo(dist, siguiente_ciudad, indice_ciudad, ciudad1, ciudad2, tiempos, condicion_climatica):
    i, j = indice_ciudad[ciudad1], indice_ciudad[ciudad2]
    dist[i][j] = tiempos[condicion_climatica]
    dist[j][i] = tiempos[condicion_climatica]
    siguiente_ciudad[i][j] = ciudad2
    siguiente_ciudad[j][i] = ciudad1
    
# Imprimir una matriz de distancias o siguiente ciudad
def imprimir_matriz(matriz):
    for fila in matriz:
        print(" ".join(map(str, fila)))

def main():
    nombre_archivo = 'logistica.txt'
    ciudades, aristas = leer_grafo(nombre_archivo)
    condicion_climatica = 0
    
    dist, siguiente_ciudad, indice_ciudad = inicializar_matrices(ciudades, aristas, condicion_climatica)
    floyd_warshall(dist, siguiente_ciudad, len(ciudades))
    
    while True:
        # Mostrar el menú de opciones al usuario
        print("\nMenú:")
        print("1. Encontrar la ruta más corta entre dos ciudades")
        print("2. Encontrar el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Salir")
        
        # Solicitar al usuario que ingrese una opción del menú
        opcion = input("Ingrese su opción: ")
        
        
        # Opción 1: Encontrar la ruta más corta entre dos ciudades

        if opcion == '1':
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            camino = construir_camino(siguiente_ciudad, indice_ciudad, origen, destino)
            if camino:
            # Si se encontró un camino, mostrar la ruta y el tiempo total de viaje
                print(f"La ruta más corta de {origen} a {destino} es: {' -> '.join(camino)}")
                print(f"Tiempo total de viaje: {dist[indice_ciudad[origen]][indice_ciudad[destino]]}")
            else:
                print("No se encontró ruta.")
        
        elif opcion == '2':
            # Opción 2: Encontrar el centro del grafo
            centro = encontrar_centro_grafo(dist, ciudades)
            print(f"El centro del grafo es: {centro}")
        
        elif opcion == '3':
            # Opción 3: Modificar el grafo
            print("Opciones de modificación:")
            print("a. Interrumpir tráfico entre ciudades")
            print("b. Establecer una nueva conexión")
            print("c. Establecer condición climática entre ciudades")
            # Solicitar al usuario que ingrese una sub-opción de modificación
            sub_opcion = input("Ingrese su opción: ")
            
            if sub_opcion == 'a':
                # Sub-opción a: Interrumpir tráfico entre ciudades
                ciudad1 = input("Ingrese la primera ciudad: ")
                ciudad2 = input("Ingrese la segunda ciudad: ")
                actualizar_grafo(dist, siguiente_ciudad, indice_ciudad, ciudad1, ciudad2, [INF, INF, INF, INF], condicion_climatica)
                floyd_warshall(dist, siguiente_ciudad, len(ciudades))
                print("Interrupción de tráfico actualizada.")
            
            elif sub_opcion == 'b':
                # Sub-opción b: Establecer una nueva conexión
                ciudad1 = input("Ingrese la primera ciudad: ")
                ciudad2 = input("Ingrese la segunda ciudad: ")
                tiempos = list(map(int, input("Ingrese los tiempos de viaje (normal, lluvia, nieve, tormenta) separados por espacio: ").split()))
                actualizar_grafo(dist, siguiente_ciudad, indice_ciudad, ciudad1, ciudad2, tiempos, condicion_climatica)
                floyd_warshall(dist, siguiente_ciudad, len(ciudades))
                print("Nueva conexión establecida.")
            
            elif sub_opcion == 'c':
                # Sub-opción c: Establecer condición climática entre ciudades
                ciudad1 = input("Ingrese la primera ciudad: ")
                ciudad2 = input("Ingrese la segunda ciudad: ")
                # Pedir la condición climática a establecer
                condicion_climatica = int(input("Ingrese la condición climática (0: normal, 1: lluvia, 2: nieve, 3: tormenta): "))
                 # Actualizar el grafo con los tiempos de viaje bajo la nueva condición climática
                actualizar_grafo(dist, siguiente_ciudad, indice_ciudad, ciudad1, ciudad2, aristas[ciudad1][ciudad2], condicion_climatica)
                floyd_warshall(dist, siguiente_ciudad, len(ciudades))
                print("Condición climática actualizada.")
        
        elif opcion == '4':
            # Opción 4: Salir del programa
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
