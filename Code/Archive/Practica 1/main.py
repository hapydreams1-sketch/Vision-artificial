import math
import random
from math import sqrt
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sep = 1e-9
clases=[((0,10-sep),(0,10-sep)),
        ((10,20-sep),(10,20-sep)),
        ((20,30-sep),(20,30-sep)),
        ((30,40-sep),(30,40-sep)),
        ((40,50-sep),(40,50-sep)),
        ((50,60-sep),(50,60-sep))]

class Punto():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clasificado = False

    def definir_clase(self, clases, distancia_minima=25):
        lista_distancias = []
        for clase in clases:
            centroide_x, centroide_y = clase.centroide
            distancia = sqrt((self.x - centroide_x) ** 2 + (self.y - centroide_y) ** 2)
            lista_distancias.append(distancia)

        min_distancia = min(lista_distancias)
        if min_distancia > distancia_minima:
            return None
        if lista_distancias.count(min_distancia) > 1:
            return "Empate"
        else:
            return lista_distancias.index(min_distancia)

class Clase():
    def __init__(self, intervalo_x, intervalo_y, num_elementos=8):
        self.intervalo_x = intervalo_x
        self.intervalo_y = intervalo_y
        self.elementos = []
        self.no_elementos = 0
        self.inicializar_elementos(num_elementos)
        self.calcular_centroide()

    def inicializar_elementos(self, num_elementos=8):
        while self.no_elementos < num_elementos:
            duplicado = False
            x = random.uniform(self.intervalo_x[0], self.intervalo_x[1])
            y = random.uniform(self.intervalo_y[0], self.intervalo_y[1])
            # Se itera hasta que se generen los n elementos únicos, evitando duplicados
            for elemento in self.elementos:
                if math.isclose(elemento.x, x, abs_tol=sep) and math.isclose(elemento.y, y, abs_tol=sep):
                    duplicado = True
                    break
            if not duplicado:
                self.elementos.append(Punto(x, y))
                self.no_elementos += 1

    def calcular_centroide(self):
        sum_x = sum([elemento.x for elemento in self.elementos])
        sum_y = sum([elemento.y for elemento in self.elementos])
        self.centroide = (sum_x / self.no_elementos, sum_y / self.no_elementos)

    def anadir_elemento(self, elemento):
        self.elementos.append(elemento)
        self.no_elementos += 1

class Interfaz(ttk.Window):
    # * Metodos para la construccion de la interfaz
    def __init__(self):
        self.clases = []
        self.punto_sin_clase = None
        self.distancia_minima_clasificacion = 25
        self.minimo_puntos_clase = 8
        
        super().__init__(themename="superhero")
        self.title("Practica 1")
        self.geometry("600x400")
        self._configurar_frames()
        self._iniciar_grafica()

    def _configurar_frames(self):
        self.columnconfigure(0, weight=3, minsize=400)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_matplotib = ttk.Frame(self)
        self.frame_matplotib.grid(row=0, column=0, sticky="nsew")
        self.frame_matplotib.columnconfigure(0, weight=1)
        self.frame_matplotib.rowconfigure(0, weight=1)

        self.frame_controles_usuario = ttk.Frame(self)
        self.frame_controles_usuario.grid(row=0, column=1, sticky="nsew")
        self.frame_controles_usuario.columnconfigure(0, weight=1)

        self._configurar_controles_usuario()

    def _configurar_controles_usuario(self):
        titulo_frame = ttk.Label(self.frame_controles_usuario, text="Controles de usuario", font=("Arial", 16))
        titulo_frame.grid(row=0, column=0, pady=10)
        
        self.marco_clases = ttk.Labelframe(self.frame_controles_usuario, text="Clases")
        self.marco_clases.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.marco_clases.columnconfigure(0, weight=1)

        titulo_instrucciones = ttk.Label(self.marco_clases, text="Elige dos de las siguientes opciones para trabajar con las clases")
        titulo_instrucciones.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.boton_crear_clases = ttk.Button(self.marco_clases, text="Crear clases", command= lambda: self._crear_clases())
        self.boton_crear_clases.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.boton_reiniciar_clases = ttk.Button(self.marco_clases, text="Reiniciar clases")
        self.boton_reiniciar_clases.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.marco_puntos = ttk.Labelframe(self.frame_controles_usuario, text="Puntos sin clase")
        self.marco_puntos.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.marco_puntos.columnconfigure(0, weight=1)

        titulo_instrucciones_puntos = ttk.Label(self.marco_puntos, text="Agrega nuevos puntos sin clase a la gráfica")
        titulo_instrucciones_puntos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.boton_agregar_punto = ttk.Button(self.marco_puntos, text="Agregar nuevo punto", command= self._agregar_nuevo_punto)
        self.boton_agregar_punto.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.boton_clasificar_punto = ttk.Button(self.marco_puntos, text="Clasificar punto", command= self._clasificar_punto)
        self.boton_clasificar_punto.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def _iniciar_grafica(self):
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figura.add_subplot(111)
        
        self.ax.set_title("Clasificación de Puntos")
        self.ax.set_xlabel("Eje X")
        self.ax.set_ylabel("Eje Y")
        self.ax.grid(True, linestyle='--', alpha=0.6)        
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 60)

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_matplotib)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # * Metodos de funcionalidad de los botones
    def _crear_clases(self):
        if len(self.clases) == 0:
            self.clases = [Clase(intervalo_x, intervalo_y, self.minimo_puntos_clase) for intervalo_x, intervalo_y in clases]
            valido = self.verificar_traslape_clases()
            if not valido:
                self.clases = []
                return
            self.actualizar_grafica()
        else:
            Messagebox.show_warning("Las clases ya han sido creadas. Reinicia las clases para crear nuevas.", title="Advertencia")

    def _pedir_valor_punto(self, coordenada):
        valor = None
        valor = Querybox.get_float(f"Ingrese la coordenada {coordenada} del nuevo punto", 
                                title=f"Agregar coordenada {coordenada} de punto",
                                initialvalue=0.0, minvalue= 0.0, maxvalue=60)
        
        if valor is None:
            Messagebox.show_error(f"Valor de {coordenada} no ingresado", "Operación cancelada")
            return None
        
        try: valor = float(valor); return valor
        except (ValueError):
            Messagebox.show_error(f"Valor de {coordenada} no válido", "Operación cancelada")
            return None

    def _agregar_nuevo_punto(self):
        if len(self.clases) == 0:
            Messagebox.show_warning("No se han creado las clases. Crea las clases antes de agregar un nuevo punto sin clase.", title="Advertencia")
            return

        valor_x = None
        valor_y = None

        if self.punto_sin_clase != None:
            respuesta = Messagebox.yesno("Ya existe un punto sin clase en la gráfica. ¿Deseas reemplazarlo?", "Punto sin clase existente")
            if respuesta in ["No", None]: return
        
        valor_x = self._pedir_valor_punto("X")
        if valor_x is None: return
        valor_y = self._pedir_valor_punto("Y")
        if valor_y is None: return

        for clase in self.clases:
            for elemento in clase.elementos:
                if math.isclose(elemento.x, valor_x, abs_tol=sep) and math.isclose(elemento.y, valor_y, abs_tol=sep):
                    Messagebox.show_error("El punto ingresado ya pertenece a una clase. Intente con otro punto.", "Punto duplicado")
                    return
        
        self.punto_sin_clase= Punto(valor_x, valor_y)
        self.actualizar_grafica()

    def _clasificar_punto(self):
        if len(self.clases) == 0:
            Messagebox.show_warning("No se han creado las clases. Crea las clases antes de clasificar un punto sin clase.", title="Advertencia")
            return

        if self.punto_sin_clase is None:
            Messagebox.show_warning("No hay ningún punto sin clase para clasificar. Agrega un nuevo punto primero.", title="Advertencia")
            return
        
        indice_clase = self.punto_sin_clase.definir_clase(self.clases, self.distancia_minima_clasificacion)
        if indice_clase not in [None, "Empate"]:
            self.clases[indice_clase].anadir_elemento(self.punto_sin_clase)
            self.clases[indice_clase].calcular_centroide()
            self.punto_sin_clase.clasificado = True
            self.punto_sin_clase = None
            self.actualizar_grafica()
            Messagebox.show_info(f"El punto ha sido clasificado en la Clase {indice_clase + 1}.", title="Punto clasificado")
        if indice_clase == "Empate":
            Messagebox.show_info("El punto se encuentra a la misma distancia de dos o más clases, por lo que no se pudo clasificar.", title="Empate en clasificación")
        if indice_clase is None:
            Messagebox.show_info("El punto no se pudo clasificar en ninguna clase existente debido a que la distancia de este a los centros de las clases es mayor a 5.", title="Punto no clasificado")

    def actualizar_grafica(self):
        self.ax.clear()

        self.ax.set_title("Clasificación de Puntos")
        self.ax.set_xlabel("Eje X")
        self.ax.set_ylabel("Eje Y")
        self.ax.grid(True, linestyle='--', alpha=0.6)

        if len(self.clases) == 0:
            self.ax.set_xlim(0, 60)
            self.ax.set_ylim(0, 60)

        colores = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

        if len(self.clases) > 0:
            for i, clase in enumerate(self.clases):
                color_clase = colores[i]
                puntos_x = [punto.x for punto in clase.elementos if not punto.clasificado]
                puntos_y = [punto.y for punto in clase.elementos if not punto.clasificado]

                puntos_x_clasificados = [punto.x for punto in clase.elementos if punto.clasificado]
                puntos_y_clasificados = [punto.y for punto in clase.elementos if punto.clasificado]

                
                self.ax.scatter(puntos_x, puntos_y, color=color_clase, label=f'Clase {i+1}', s=30)
                self.ax.scatter(puntos_x_clasificados, puntos_y_clasificados, color=color_clase, marker='o',s=80, edgecolor='black', zorder=4)

                coordenada_x_centroide, coordenada_y_centroide = clase.centroide
                self.ax.scatter(coordenada_x_centroide, coordenada_y_centroide, color=color_clase, marker='X', s=120, edgecolor='black', zorder=5)

        if self.punto_sin_clase is not None:
            self.ax.scatter(self.punto_sin_clase.x, self.punto_sin_clase.y, color='black', marker='*', s=200, label='Punto sin clasificar', zorder=6)

        if len(self.clases) > 0:
            self.ax.legend(loc='upper right', fontsize='small')
        self.canvas.draw()

    #* Metodo chequeo de traslape entre clases
    def verificar_traslape_clases(self):
        for i in range(len(self.clases)):
            for j in range(i + 1, len(self.clases)):
                clase_base = self.clases[i]
                clase_hermana = self.clases[j]

                # Para que no haya traslape, el intervalo x de una clase debe ser completamente menor o mayor que el intervalo x de la otra clase, 
                # y lo mismo para el intervalo y. Si esto no se cumple, entonces hay traslape.
                if (clase_base.intervalo_x[0] < clase_hermana.intervalo_x[1] and
                    clase_base.intervalo_x[1] > clase_hermana.intervalo_x[0] and
                    clase_base.intervalo_y[0] < clase_hermana.intervalo_y[1] and 
                    clase_base.intervalo_y[1] > clase_hermana.intervalo_y[0]):
                    Messagebox.show_warning(f"Las clases {i+1} y {j+1} se traslapan. Considera ajustar los intervalos del programa para evitar traslapes.",
                                        title="Traslape de clases")
                    return False
        return True

if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()