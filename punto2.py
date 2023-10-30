#INTEGRANTES: ESTEBAN ORTEGA Y BRANDO LOPEZ

import tkinter as tk
import random
import string

# Parámetros del algoritmo genético
tamaño_poblacion = 100
tasa_mutacion = 0.05
num_generaciones = 90
objetivo = "HELLO WORLD"
elitismo = True

# Funciones del algoritmo genético

# Genera una cadena aleatoria del mismo tamaño que el objetivo
def cadena_aleatoria():
    return ''.join(random.choice(string.ascii_uppercase + ' ') for _ in range(len(objetivo)))

# Calcula la aptitud de una cadena, que es la cantidad de caracteres en la posición correcta
def calcular_aptitud(cadena):
    return sum(1 for c1, c2 in zip(cadena, objetivo) if c1 == c2)

# Selecciona un individuo de la población basado en su aptitud
def seleccionar_padre(poblacion, aptitudes):
    total_aptitud = sum(aptitudes)
    seleccion = random.uniform(0, total_aptitud)
    suma = 0
    for individuo, aptitud in zip(poblacion, aptitudes):
        suma += aptitud
        if suma >= seleccion:
            return individuo
    return poblacion[-1]

# Cruza dos padres para generar un hijo
def cruzar(padre1, padre2):
    punto = random.randint(0, len(padre1) - 1)
    return padre1[:punto] + padre2[punto:]

# Realiza una mutación en la cadena con una probabilidad tasa_mutacion
def mutar(cadena):
    if random.random() < tasa_mutacion:
        posicion = random.randint(0, len(cadena) - 1)
        caracter = random.choice(string.ascii_uppercase + ' ')
        return cadena[:posicion] + caracter + cadena[posicion+1:]
    return cadena

# Función para actualizar la interfaz gráfica
def actualizar_interfaz(generacion, mejor_aptitud, mejor_cadena):
    generacion_label.config(text=f"Generación {generacion}")
    aptitud_label.config(text=f"Mejor aptitud: {mejor_aptitud}")
    cadena_label.config(text=f"Cadena: {mejor_cadena}")
    ventana.update()

# Función para iniciar el algoritmo genético
def iniciar_algoritmo():
    poblacion = [cadena_aleatoria() for _ in range(tamaño_poblacion)]
    for generacion in range(num_generaciones):
        aptitudes = [calcular_aptitud(individuo) for individuo in poblacion]

        if max(aptitudes) == len(objetivo):
            actualizar_interfaz(generacion, max(aptitudes), poblacion[aptitudes.index(max(aptitudes))])
            print(f"Solución encontrada en la generación {generacion}!")
            break

        actualizar_interfaz(generacion, max(aptitudes), poblacion[aptitudes.index(max(aptitudes))])

        if elitismo:
            elite = [poblacion[aptitudes.index(max(aptitudes))]]
        else:
            elite = []

        nuevos_padres = [seleccionar_padre(poblacion, aptitudes) for _ in range(tamaño_poblacion - len(elite))]

        if len(nuevos_padres) % 2 != 0:
            nuevos_padres.append(random.choice(nuevos_padres))

        poblacion = elite + [mutar(cruzar(nuevos_padres[i], nuevos_padres[i + 1])) for i in range(0, len(nuevos_padres), 2)]
    else:
        print("No se encontró la solución en el número de generaciones definido.")

# Crear una ventana de Tkinter
ventana = tk.Tk()
ventana.title("Algoritmo Genético")
generacion_label = tk.Label(ventana, text="")
aptitud_label = tk.Label(ventana, text="")
cadena_label = tk.Label(ventana, text="")
generacion_label.pack()
aptitud_label.pack()
cadena_label.pack()

# Botón para iniciar el algoritmo
iniciar_button = tk.Button(ventana, text="Iniciar Algoritmo", command=iniciar_algoritmo)
iniciar_button.pack()

ventana.mainloop()
