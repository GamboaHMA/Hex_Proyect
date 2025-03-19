filas = 3
columnas = 3

# Crear una matriz vacía
matriz = []

# Contador para los valores ascendentes
contador = 1

# Llenar la matriz con valores en orden ascendente
for i in range(filas):
    fila = []
    for j in range(columnas):
        fila.append(contador)
        contador += 1
    matriz.append(fila)

# Imprimir la matriz
for i in range(3):
    for j in range(3):
        print(matriz[i][j])