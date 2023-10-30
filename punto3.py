#INTEGRANTES: ESTEBAN ORTEGA Y BRANDO LOPEZ

import random
import math
import tkinter as tk
from tkinter import ttk

# Datos de ejemplo para las conferencias
conferencias = [
    {"nombre": "Conferencia 1", "duracion": 4, "horarioPreferido": "Mañana", "asientosDisponibles": 100},
    {"nombre": "Conferencia 2", "duracion": 4, "horarioPreferido": "Tarde", "asientosDisponibles": 80},
    {"nombre": "Conferencia 3", "duracion": 4, "horarioPreferido": "Noche", "asientosDisponibles": 120},
    {"nombre": "Conferencia 4", "duracion": 4, "horarioPreferido": "Noche", "asientosDisponibles": 50},
    # Agrega datos para las otras conferencias
]

# Datos de ejemplo para las salas de conferencias y horarios
salas = ["Sala 1", "Sala 2", "Sala 3"]
horarios = ["Mañana", "Tarde", "Noche"]

# Inicializa un diccionario para llevar un registro de los asientos disponibles en cada sala
asientos_disponibles = {sala: 0 for sala in salas}

# Función para calcular la asistencia total de una programación
def calcular_asistencia_total(programacion):
    asistencia_total = 0
    for conferencia in programacion:
        asistencia_total += conferencia["asistentes"]
    return asistencia_total

# Función para generar una programación aleatoria
def generar_programacion_aleatoria(conferencias, salas, horarios):
    programacion = []
    for conferencia in conferencias:
        sala = random.choice(salas)
        horario = random.choice(horarios)
        asistentes = random.randint(0, conferencia["asientosDisponibles"])
        programacion.append({"conferencia": conferencia, "sala": sala, "horario": horario, "asistentes": asistentes})
        # Actualiza la cantidad de asientos disponibles en la sala
        asientos_disponibles[sala] += asistentes
    return programacion

# Restaura la cantidad de asientos disponibles en cada sala
def restaurar_asientos_disponibles(programacion):
    for conferencia in programacion:
        sala = conferencia["sala"]
        asistentes = conferencia["asistentes"]
        asientos_disponibles[sala] -= asistentes

# Función para aplicar el algoritmo de recocido simulado
def recocido_simulado(conferencias, salas, horarios, temperatura_inicial, enfriamiento):
    programacion_actual = generar_programacion_aleatoria(conferencias, salas, horarios)
    asistencia_actual = calcular_asistencia_total(programacion_actual)

    mejor_programacion = list(programacion_actual)
    mejor_asistencia = asistencia_actual

    temperatura = temperatura_inicial

    while temperatura > 1:
        i, j = random.sample(range(len(conferencias)), 2)
        programacion_actual[i]["horario"], programacion_actual[j]["horario"] = (
            programacion_actual[j]["horario"],
            programacion_actual[i]["horario"],
        )

        nueva_asistencia = calcular_asistencia_total(programacion_actual)
        diferencia = nueva_asistencia - asistencia_actual

        if diferencia > 0 or random.random() < math.exp(diferencia / temperatura):
            asistencia_actual = nueva_asistencia
            if asistencia_actual > mejor_asistencia:
                mejor_programacion = list(programacion_actual)
                mejor_asistencia = asistencia_actual
        else:
            programacion_actual[i]["horario"], programacion_actual[j]["horario"] = (
                programacion_actual[j]["horario"],
                programacion_actual[i]["horario"],
            )

        temperatura *= enfriamiento

    return mejor_programacion

# Función para mostrar la programación en una tabla en la interfaz gráfica
def mostrar_programacion(programacion):
    # Borra la tabla existente
    for i in tabla.get_children():
        tabla.delete(i)

    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12))  # Cambiar el tamaño de fuente
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  # Cabeceras en negrita

    # Definir tags para personalizar los colores de filas
    tabla.tag_configure('evenrow', background='#F2F2F2')
    tabla.tag_configure('oddrow', background='#E0E0E0')

    row_count = 0
    for conferencia in programacion:
        row_tags = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        tabla.insert('', 'end', values=[
            conferencia['conferencia']['nombre'],
            conferencia['sala'],
            conferencia['horario'],
            conferencia['conferencia']['duracion'],  # Mostrar la duración de la conferencia en horas
            conferencia['asistentes']
        ], tags=(row_tags,))
        row_count += 1
    
    # Mostrar la duración total en horas
    asistencia_total_label.config(text=f"Asistencia total óptima: {calcular_asistencia_total(programacion)}")

# Función para ejecutar el algoritmo de recocido simulado
def ejecutar_recocido_simulado():
    temperatura_inicial = 1000
    enfriamiento = 0.98
    programacion_optima = recocido_simulado(conferencias, salas, horarios, temperatura_inicial, enfriamiento)
    mostrar_programacion(programacion_optima)

# Crear una ventana de Tkinter
ventana = tk.Tk()
ventana.title("Planificador de Conferencias")

# Etiqueta para mostrar la asistencia total
asistencia_total_label = tk.Label(ventana, text="")
asistencia_total_label.pack()

# Crear una tabla para mostrar la programación
tabla = ttk.Treeview(ventana, columns=("Conferencia", "Sala", "Horario", "Duración (horas)", "Asistentes"))
tabla.heading("#1", text="Conferencia")
tabla.heading("#2", text="Sala")
tabla.heading("#3", text="Horario")
tabla.heading("#4", text="Duración (horas)")
tabla.heading("#5", text="Asistentes")
tabla.column("#1", anchor="center")  # Centrar el contenido de la columna 1
tabla.column("#2", anchor="center")  # Centrar el contenido de la columna 2
tabla.column("#3", anchor="center")  # Centrar el contenido de la columna 3
tabla.column("#4", anchor="center")  # Centrar el contenido de la columna 4
tabla.column("#5", anchor="center")  # Centrar el contenido de la columna 5
tabla.pack()

# Crear un botón para ejecutar el algoritmo
boton_ejecutar = tk.Button(ventana, text="Ejecutar Recocido Simulado", command=ejecutar_recocido_simulado)
boton_ejecutar.pack()

# Mostrar la ventana de Tkinter
ventana.mainloop()
