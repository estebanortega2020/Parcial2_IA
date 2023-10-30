#INTEGRANTES: ESTEBAN ORTEGA Y BRANDO LOPEZ

import tkinter as tk
import random

class Puzzle:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Puzzle-8")
        
        # Inicializa el tablero con números del 1 al 8 y un espacio en blanco (None), luego lo desordena.
        self.board = list(range(1, 9)) + [None]
        random.shuffle(self.board)
        
        # Crea una lista de botones que representan el tablero.
        self.tiles = []
        for i in range(9):
            tile = tk.Button(self.window, text=str(self.board[i]), width=10, height=5, font=('Helvetica', 16))
            tile.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='nsew')  # Agrega relleno y ajusta a 'nsew'
            tile.configure(bg='lightblue', fg='black')
            self.tiles.append(tile)
        
        # Configura el sistema de gestión de geometría 'grid' para que se expanda y se centre
        for i in range(3):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)
        
        # Asocia la función key_press al evento de presionar teclas
        self.window.bind("<Key>", self.key_press)
        
        # Crea botones para mostrar las heurísticas
        self.manhattan_btn = tk.Button(self.window, text="Manhattan Distance", command=self.show_manhattan_distance, bg='lightgreen', font=('Helvetica', 12))
        self.manhattan_btn.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        
        self.out_of_place_btn = tk.Button(self.window, text="Out of Place", command=self.show_out_of_place, bg='lightgreen', font=('Helvetica', 12))
        self.out_of_place_btn.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')
        
        # Agrega un botón para mostrar la heurística "Ficha en su lugar final"
        self.in_place_btn = tk.Button(self.window, text="Fichas correctas", command=self.show_in_place, bg='lightgreen', font=('Helvetica', 12))
        self.in_place_btn.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')

        
        # Actualiza las etiquetas de las heurísticas
        self.update_heuristics()
        
        # Configura el sistema de gestión de geometría 'grid' para que se expanda y se centre
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        # Inicia el bucle de la interfaz gráfica
        self.window.mainloop()

    def key_press(self, event):
        # Maneja el evento de presionar teclas para mover el espacio en blanco
        index = self.board.index(None)
        if event.keysym == "Up" and index not in [0, 1, 2]:
            self.swap(index, index-3)
        elif event.keysym == "Down" and index not in [6, 7, 8]:
            self.swap(index, index+3)
        elif event.keysym == "Left" and index not in [0, 3, 6]:
            self.swap(index, index-1)
        elif event.keysym == "Right" and index not in [2, 5, 8]:
            self.swap(index, index+1)
        
        # Actualiza las heurísticas
        self.update_heuristics()

    def swap(self, i, j):
        # Intercambia dos valores en el tablero y actualiza los botones correspondientes
        self.board[i], self.board[j] = self.board[j], self.board[i]
        
        if self.board[i] is None:
            self.tiles[i].config(text="", bg='yellow', fg='black')
        else:
            self.tiles[i].config(text=str(self.board[i]), bg='lightblue', fg='black')
        
        if self.board[j] is None:
            self.tiles[j].config(text="", bg='yellow', fg='black')
        else:
            self.tiles[j].config(text=str(self.board[j]), bg='lightblue', fg='black')

    
    def manhattan_distance(self):
        # Calcula la distancia de Manhattan
        distance = 0
        for i in range(1, 9):
            xi, yi = self.index(i)
            xj, yj = (i-1)//3, (i-1)%3
            distance += abs(xi-xj) + abs(yi-yj)
        return distance

    def out_of_place(self):
        # Calcula el número de fichas fuera de lugar
        return sum(i != j for i, j in zip(self.board, list(range(1, 9)) + [None]))

    def index(self, value):
        # Obtiene la posición de un valor en el tablero
        return self.board.index(value)//3, self.board.index(value)%3
    
    def update_heuristics(self):
        # Actualiza las etiquetas de las heurísticas en la interfaz gráfica
        self.manhattan_btn.config(text="Distancia: {}".format(self.manhattan_distance()))
        self.out_of_place_btn.config(text="Fuera de lugar: {}".format(self.out_of_place()))
        self.in_place_btn.config(text="Fichas correctas: {}".format(self.in_place()))
    
    def show_manhattan_distance(self):
        # Muestra la distancia de Manhattan en la consola
        print("Manhattan Distance:", self.manhattan_distance())
    
    def show_out_of_place(self):
        # Muestra el número de fichas fuera de lugar en la consola
        print("Out of Place:", self.out_of_place())
        
    def in_place(self):
        # Calcula cuántas fichas están en su lugar final
        return sum(i == j for i, j in zip(self.board, list(range(1, 9)) + [None]))

    def show_in_place(self):
        # Muestra cuántas fichas están en su lugar final en la consola
        print("Fichas correctas:", self.in_place())
if __name__ == "__main__":
    Puzzle()
