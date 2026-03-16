import numpy as np
import random

# Función para calcular la distancia de una ruta
def calcular_distancia(ruta, matriz_distancias):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += matriz_distancias[ruta[i]][ruta[i+1]]
    distancia += matriz_distancias[ruta[-1]][ruta[0]] # Regreso al inicio
    return distancia

# Búsqueda Local: 2-opt (El componente híbrido)
def busqueda_local_2opt(ruta, matriz_distancias):
    mejor_ruta = ruta
    mejor_dist = calcular_distancia(ruta, matriz_distancias)
    for i in range(1, len(ruta) - 2):
        for j in range(i + 1, len(ruta)):
            nueva_ruta = ruta[:i] + ruta[i:j][::-1] + ruta[j:]
            nueva_dist = calcular_distancia(nueva_ruta, matriz_distancias)
            if nueva_dist < mejor_dist:
                mejor_dist = nueva_dist
                mejor_ruta = nueva_ruta
    return mejor_ruta

# Estructura del Algoritmo Genético Híbrido
def algoritmo_hibrido(matriz, n_ciudades, pop_size=50, gen=100):
    # 1. Población inicial
    poblacion = [random.sample(range(n_ciudades), n_ciudades) for _ in range(pop_size)]
    
    for g in range(gen):
        # 2. Evaluación
        poblacion = sorted(poblacion, key=lambda x: calcular_distancia(x, matriz))
        
        # 3. Hibridación: Aplicar 2-opt al top 10%
        for i in range(int(pop_size * 0.1)):
            poblacion[i] = busqueda_local_2opt(poblacion[i], matriz)
        
        # 4. Cruce y Mutación (Simplificado para el ejemplo)
        # ... (Implementar OX Crossover y Swap Mutation) ...
        
    return poblacion[0] # El mejor hallado
