import numpy as np
import random

# Simulación de carga de matriz de distancias para gr17 

def obtener_instancia_gr17():
    # matriz 17x17
    size = 17
    matrix = np.random.randint(10, 100, size=(size, size))
    np.fill_diagonal(matrix, 0)
    return matrix

class TSPHibrido:
    def __init__(self, matriz_distancias, pop_size=20, elite_size=5, mutation_rate=0.05, generations=100):
        self.matriz = matriz_distancias
        self.n = len(matriz_distancias)
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def fitness(self, ruta):
        distancia = sum(self.matriz[ruta[i], ruta[i+1]] for i in range(self.n - 1))
        distancia += self.matriz[ruta[-1], ruta[0]]
        return 1 / float(distancia)

    def busqueda_local_2opt(self, ruta):
        """Componente Híbrido: Refinamiento de la ruta"""
        mejor_ruta = ruta[:]
        estancado = False
        while not estancado:
            estancado = True
            for i in range(1, self.n - 2):
                for j in range(i + 1, self.n):
                    nueva_ruta = mejor_ruta[:i] + mejor_ruta[i:j][::-1] + mejor_ruta[j:]
                    if self.fitness(nueva_ruta) > self.fitness(mejor_ruta):
                        mejor_ruta = nueva_ruta
                        estancado = False
        return mejor_ruta

    def ejecutar(self):
        # Población inicial
        poblacion = [random.sample(range(self.n), self.n) for _ in range(self.pop_size)]
        
        for gen in range(self.generations):
            # Evaluación y Selección
            poblacion = sorted(poblacion, key=lambda x: self.fitness(x), reverse=True)
            nueva_poblacion = poblacion[:self.elite_size] # Elitismo
            
            # Hibridación: Aplicar 2-opt a la élite
            nueva_poblacion = [self.busqueda_local_2opt(ind) for ind in nueva_poblacion]
            
            # Cruce y Mutación para completar la población
            while len(nueva_poblacion) < self.pop_size:
                padre1, padre2 = random.sample(poblacion[:10], 2)
                hijo = self.cruce_ordenado(padre1, padre2)
                if random.random() < self.mutation_rate:
                    self.mutar(hijo)
                nueva_poblacion.append(hijo)
            
            poblacion = nueva_poblacion
            if gen % 20 == 0:
                mejor_dist = 1 / self.fitness(poblacion[0])
                print(f"Generación {gen}: Mejor distancia = {mejor_dist:.2f}")
        
        return poblacion[0], 1 / self.fitness(poblacion[0])

    def cruce_ordenado(self, p1, p2):
        start, end = sorted(random.sample(range(self.n), 2))
        hijo = [None] * self.n
        hijo[start:end] = p1[start:end]
        restantes = [item for item in p2 if item not in hijo]
        ptr = 0
        for i in range(self.n):
            if hijo[i] is None:
                hijo[i] = restantes[ptr]
                ptr += 1
        return hijo

    def mutar(self, ind):
        i, j = random.sample(range(self.n), 2)
        ind[i], ind[j] = ind[j], ind[i]

# Ejecución
if __name__ == "__main__":
    matriz = obtener_instancia_gr17()
    solver = TSPHibrido(matriz)
    mejor_ruta, costo = solver.ejecutar()
    print(f"\nResultado Final:")
    print(f"Mejor Ruta: {mejor_ruta}")
    print(f"Costo: {costo}")
