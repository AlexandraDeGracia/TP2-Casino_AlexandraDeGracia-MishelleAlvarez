# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.

import tkinter as tk
from tkinter import messagebox
import random
import datos
import sesion

PASOS_ANIMACION = 12
INTERVALO_ANIMACION = 150
CANTIDAD_RODILLOS = 3
CANTIDAD_SIMBOLOS = 5
CARAS_DADO = 6
SUMA_MINIMA_DADOS = 2
SUMA_MAXIMA_DADOS = 12
PUNTOS_POR_GANAR = 2
PUNTOS_POR_PERDER = 1

colores = ["Rojo", "Azul", "Verde", "Blanco"]
llavesColores = ["rojas", "azules", "verdes", "blancas"]

matrizRodillos = [
    ["Cereza", "Limón", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limón", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limón", "Campana", "Estrella", "Siete"]
]

combinacionesGanadoras = {
    ("Cereza", "Cereza", "Cereza"): 2,
    ("Limón", "Limón", "Limón"): 2,
    ("Campana", "Campana", "Campana"): 2,
    ("Estrella", "Estrella", "Estrella"): 2,
    ("Siete", "Siete", "Siete"): 2
}

pagosDados = {"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}

matrizOpcionesDados = [
    ["par", "impar"],
    ["dobles", "sumaExacta"]
]

# [(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntos]
jugador = [("", "", ""), [0.0, 0, 0, 0, 0], 0]
estado = {"raiz": "", "actual": "", "girando": False, "indices": [0, 0, 0]}
widgets = {}

# Datos del jugador
def fichasDe(color):
    """
    Funcionalidad:
        Devuelve cuantas fichas tiene el jugador de un color.
    Entrada:
    - color(str): Nombre del color.
    Salida:
    - cantidad(int): Fichas de ese color, o -1 si el color no existe.
    """
    for posicion in range(len(colores)):
        if colores[posicion] == color:
            return jugador[1][posicion + 1]
    return -1

def valorFicha(color):
    """
    Funcionalidad:
        Devuelve el valor en dolares de una ficha.
    Entrada:
    - color(str): Nombre del color.
    Salida:
    - valor(int): Valor de la ficha, o -1 si el color no existe.
    """
    for posicion in range(len(colores)):
        if colores[posicion] == color:
            llave = llavesColores[posicion]
            return datos.VALOR_FICHAS[llave]
    return -1

def totalFichas():
    """
    Funcionalidad:
        Suma todas las fichas del jugador.
    Entrada:
    - Ninguna.
    Salida:
    - total(int): Total de fichas.
    """
    total = 0
    for color in colores:
        total = total + fichasDe(color)
    return total

def textoSaldo():
    """
    Funcionalidad:
        Arma el texto con las fichas de cada color, el total y los puntos.
    Entrada:
    - Ninguna.
    Salida:
    - texto(str): Texto para mostrar en pantalla.
    """
    texto = ""
    for i in range(len(colores)):
        texto = texto + colores[i] + ": " + str(jugador[1][i + 1]) + "   "
    return texto + "\nTotal: " + str(totalFichas()) + "   Puntos: " + str(jugador[2])

def esEntero(texto):
    """
    Funcionalidad:
        Revisa que el texto tenga solo digitos del 0 al 9.
    Entrada:
    - texto(str): Texto a revisar.
    Salida:
    - valido(bool): True si es un entero sin signo, False si no.
    """
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in "0123456789":
            return False
    return True

def validarApuesta(textoApuesta, color):
    """
    Funcionalidad:
        Revisa que la apuesta sea un entero mayor que cero y que alcancen las fichas.
    Entrada:
    - textoApuesta(str): Texto ingresado por el usuario en el campo de apuesta.
    - color(str): Color de las fichas seleccionadas para apostar.
    Salida:
    - apuesta(int): Cantidad entera valida a apostar, o 0 si la apuesta es invalida.
    """
    textoApuesta = textoApuesta.strip()
    if not esEntero(textoApuesta) or int(textoApuesta) <= 0:
        messagebox.showwarning("Apuesta inválida", "Escribe un número entero mayor que cero")
        return 0
    apuesta = int(textoApuesta)
    if apuesta > fichasDe(color):
        messagebox.showwarning("Fichas insuficientes", "Solo tienes " + str(fichasDe(color)) + " ficha(s) " + color)
        return 0
    return apuesta

def descontarApuesta(apuesta, color):
    """
    Funcionalidad:
        Descuenta las fichas apostadas del color elegido.
    Entrada:
    - apuesta(int): Cantidad de fichas que se descontaran del jugador.
    - color(str): Color de las fichas sobre el cual se realiza el descuento.
    Salida:
    - Ninguna.
    """
    posicion = colores.index(color) + 1
    jugador[1][posicion] = jugador[1][posicion] - apuesta

def liquidar(apuesta, color, gano, multiplicador):
    """
    Funcionalidad:
        Paga las fichas si gano, actualiza los puntos y guarda en el archivo.
    Entrada:
    - apuesta(int): Cantidad de fichas apostadas.
    - color(str): Color de las fichas apostadas.
    - gano(bool): True si el jugador gano la partida, False si perdio.
    - multiplicador(int): Factor aplicado a la apuesta cuando gana.
    Salida:
    - pagoTotal(int): Cantidad de fichas que recibe el jugador.
    """
    pagoTotal = 0
    if gano:
        pagoTotal = apuesta * multiplicador
        posicion = colores.index(color) + 1
        jugador[1][posicion] = jugador[1][posicion] + pagoTotal
        jugador[2] = jugador[2] + PUNTOS_POR_GANAR
    else:
        jugador[2] = jugador[2] - PUNTOS_POR_PERDER
    resultado = datos.guardarCambiosJugador(jugador)
    if type(resultado) == str:
        messagebox.showerror("Error al guardar", resultado)
    return pagoTotal

def mostrarResultadoJuego(apuesta, color, gano, pagoTotal):
    """
    Funcionalidad:
        Muestra el resultado de la jugada y actualiza el saldo en pantalla.
    Entrada:
    - apuesta(int): Cantidad de fichas apostadas.
    - color(str): Color de las fichas apostadas.
    - gano(bool): True si el jugador gano la partida, False si perdio.
    - pagoTotal(int): Total de fichas entregadas como premio.
    Salida:
    - Ninguna.
    """
    if gano:
        widgets["resultado"].config(text="¡Ganó! Recibe " + str(pagoTotal) + " ficha(s) " + color + " (ganancia neta: " + str(pagoTotal - apuesta) + ") y +" + str(PUNTOS_POR_GANAR) + " puntos")
    else:
        widgets["resultado"].config(text="Perdió " + str(apuesta) + " ficha(s) " + color + " y -" + str(PUNTOS_POR_PERDER) + " punto")
    widgets["saldo"].config(text=textoSaldo())

# Ventanas y elementos
def cerrarTodo():
    """
    Funcionalidad:
        Cierra el programa.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    estado["raiz"].destroy()

def nuevaVentana(titulo, tamano, funcionAlCerrar):
    """
    Funcionalidad:
        Cierra la ventana actual y crea una nueva ventana secundaria.
    Entrada:
    - titulo(str): Titulo que se mostrara en la barra de la ventana.
    - tamano(str): Dimensiones de la ventana en formato ancho x alto.
    - funcionAlCerrar(function): Funcion que se ejecuta al presionar la X de cierre.
    Salida:
    - ventana(Toplevel): Nueva ventana secundaria creada.
    """
    if estado["actual"] != "":
        estado["actual"].destroy()
    ventana = tk.Toplevel(estado["raiz"])
    ventana.title(titulo)
    ventana.geometry(tamano)
    ventana.protocol("WM_DELETE_WINDOW", funcionAlCerrar)
    estado["actual"] = ventana
    return ventana

def crearBoton(ventana, texto, funcion):
    """
    Funcionalidad:
        Crea un boton estandar y lo coloca en la ventana indicada.
    Entrada:
    - ventana(Tk o Toplevel): Ventana contenedora donde se ubicara el boton.
    - texto(str): Etiqueta visible del boton.
    - funcion(function o None): Funcion que ejecuta al hacer clic, o None si no tiene accion.
    Salida:
    - Ninguna.
    """
    tk.Button(ventana, text=texto, width=24, command=funcion).pack(pady=4)

def crearSelectorColor(ventana):
    """
    Funcionalidad:
        Crea los cuatro radiobuttons para escoger el color de ficha.
    Entrada:
    - ventana(Tk o Toplevel): Ventana contenedora donde se ubicara el selector de colores.
    Salida:
    - Ninguna.
    """
    widgets["color"] = tk.StringVar(value="Blanco")
    marco = tk.Frame(ventana)
    marco.pack(pady=5)
    for i in range(len(colores)):
        texto = colores[i] + " ($" + str(valorFicha(colores[i])) + ")"
        tk.Radiobutton(marco, text=texto, variable=widgets["color"], value=colores[i]).grid(row=0, column=i)

def crearCampoApuesta(ventana):
    """
    Funcionalidad:
        Crea el campo donde se escribe la apuesta.
    Entrada:
    - ventana(Tk o Toplevel): Ventana contenedora donde se ubicara el campo de apuesta.
    Salida:
    - Ninguna.
    """
    marco = tk.Frame(ventana)
    marco.pack(pady=5)
    tk.Label(marco, text="Fichas a apostar:").grid(row=0, column=0)
    widgets["apuesta"] = tk.Entry(marco, width=8)
    widgets["apuesta"].insert(0, "1")
    widgets["apuesta"].grid(row=0, column=1)

# Sesion y menus
def abrirSesion():
    """
    Funcionalidad:
        Abre la ventana de inicio de sesion.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    ventana = nuevaVentana("Casino - Sesion", "430x440", cerrarTodo)
    sesion.crearVentanaSesion(iniciarSesion, ventana)

def iniciarSesion(registroJugador):
    """
    Funcionalidad:
        Valida y carga el registro del jugador activo y abre el menu principal.
    Entrada:
    - registroJugador(list): Lista con identidad, recursos y puntaje del jugador que inicio sesion.
    Salida:
    - Ninguna.
    """
    global jugador
    if not datos.validarEstructuraJugador(registroJugador):
        messagebox.showerror("Error", "El registro del jugador no es valido")
        return
    jugador = registroJugador
    menuPrincipal()

def cerrarSesion():
    """
    Funcionalidad:
        Pregunta si quiere cerrar sesion y vuelve al login.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    global jugador
    if messagebox.askyesno("Cerrar sesion", "Seguro que quiere cerrar la sesion?"):
        jugador = [("", "", ""), [0.0, 0, 0, 0, 0], 0]
        abrirSesion()

def menuPrincipal():
    """
    Funcionalidad:
        Muestra el menu principal.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    ventana = nuevaVentana("Casino - Menú", "420x380", cerrarTodo)
    tk.Label(ventana, text="CASINO", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(ventana, text="Jugador: " + str(jugador[0][0]) + "   Dinero: $" + str(jugador[1][0])).pack()
    tk.Label(ventana, text=textoSaldo()).pack(pady=5)
    crearBoton(ventana, "Jugar", salaJuegos)
    crearBoton(ventana, "Fichas", ventanaFichas)
    crearBoton(ventana, "Ranking", None)
    crearBoton(ventana, "Análisis", None)
    crearBoton(ventana, "Cerrar sesión", cerrarSesion)

def salaJuegos():
    """
    Funcionalidad:
        Muestra la sala con los botones de cada juego.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    ventana = nuevaVentana("Casino - Juegos", "420x350", menuPrincipal)
    tk.Label(ventana, text="SALA DE JUEGOS", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(ventana, text=textoSaldo()).pack(pady=5)
    crearBoton(ventana, "Ruleta", None)
    crearBoton(ventana, "Tragamonedas", tragamonedas)
    crearBoton(ventana, "Blackjack", None)
    crearBoton(ventana, "Dados", dados)
    crearBoton(ventana, "Volver al menú", menuPrincipal)

# Tragamonedas
def volverDeTragamonedas():
    """
    Funcionalidad:
        Vuelve a la sala solo si los rodillos no estan girando.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    if estado["girando"]:
        messagebox.showinfo("Girando", "Espere a que terminen de girar los rodillos")
    else:
        salaJuegos()

def girarRodillos(paso, apuesta, color):
    """
    Funcionalidad:
        Mueve los rodillos paso a paso y al final revisa si gano.
    Entrada:
    - paso(int): Numero de paso actual de la animacion.
    - apuesta(int): Cantidad de fichas apostadas en el giro.
    - color(str): Color de las fichas apostadas.
    Salida:
    - Ninguna.
    """
    simbolos = []
    for i in range(CANTIDAD_RODILLOS):
        estado["indices"][i] = (estado["indices"][i] + 1) % CANTIDAD_SIMBOLOS
        simbolos.append(matrizRodillos[i][estado["indices"][i]])
    widgets["rodillos"].config(text=simbolos[0] + "  |  " + simbolos[1] + "  |  " + simbolos[2])

    if paso < PASOS_ANIMACION:
        estado["actual"].after(INTERVALO_ANIMACION, girarRodillos, paso + 1, apuesta, color)
        return

    combinacion = (simbolos[0], simbolos[1], simbolos[2])
    multiplicador = 0
    if combinacion in combinacionesGanadoras:
        multiplicador = combinacionesGanadoras[combinacion]
    gano = multiplicador > 0
    pagoTotal = liquidar(apuesta, color, gano, multiplicador)
    mostrarResultadoJuego(apuesta, color, gano, pagoTotal)
    estado["girando"] = False

def iniciarGiro():
    """
    Funcionalidad:
        Revisa la apuesta, descuenta las fichas y empieza a girar.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    if estado["girando"]:
        return
    color = widgets["color"].get()
    apuesta = validarApuesta(widgets["apuesta"].get(), color)
    if apuesta == 0:
        return
    descontarApuesta(apuesta, color)
    widgets["saldo"].config(text=textoSaldo())
    widgets["resultado"].config(text="Girando...")
    for i in range(CANTIDAD_RODILLOS):
        estado["indices"][i] = random.randint(0, CANTIDAD_SIMBOLOS - 1)
    estado["girando"] = True
    girarRodillos(1, apuesta, color)

def tragamonedas():
    """
    Funcionalidad:
        Muestra la pantalla de la tragamonedas.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    estado["girando"] = False
    ventana = nuevaVentana("Casino - Tragamonedas", "520x420", volverDeTragamonedas)
    tk.Label(ventana, text="TRAGAMONEDAS", font=("Arial", 16, "bold")).pack(pady=8)
    widgets["saldo"] = tk.Label(ventana, text=textoSaldo())
    widgets["saldo"].pack()
    widgets["rodillos"] = tk.Label(ventana, text="?  |  ?  |  ?", font=("Arial", 16))
    widgets["rodillos"].pack(pady=10)
    crearSelectorColor(ventana)
    crearCampoApuesta(ventana)
    widgets["resultado"] = tk.Label(ventana, text="Escoja el color, la apuesta y presione Girar")
    widgets["resultado"].pack(pady=8)
    crearBoton(ventana, "Girar / Jugar otra vez", iniciarGiro)
    crearBoton(ventana, "Regresar a juegos", volverDeTragamonedas)

# Dados
def validarSumaExacta(textoSuma):
    """
    Funcionalidad:
        Revisa que la suma exacta sea un entero entre 2 y 12.
    Entrada:
    - textoSuma(str): Texto ingresado por el usuario.
    Salida:
    - suma(int): Número entero válido o 0 si es inválido.
    """
    if not esEntero(textoSuma) or int(textoSuma) < SUMA_MINIMA_DADOS or int(textoSuma) > SUMA_MAXIMA_DADOS:
        messagebox.showwarning("Suma inválida", "Escriba un número entero entre 2 y 12")
        return 0
    return int(textoSuma)

def evaluarApuestaDados(tipo, tiradaDados, suma, sumaObjetivo):
    """
    Funcionalidad:
        Determina si la tirada de dados cumple la apuesta seleccionada.
    Entrada:
    - tipo(str): Modalidad de apuesta ("par", "impar", "dobles" o "sumaExacta").
    - tiradaDados(tuple): Tupla con los valores obtenidos en los dos dados.
    - suma(int): Suma total de ambos dados.
    - sumaObjetivo(int): Valor exacto elegido por el jugador cuando apuesta a "sumaExacta".
    Salida:
    - gano(bool): True si acerto la apuesta, False si perdio.
    """
    if tipo == "par":
        return suma % 2 == 0
    if tipo == "impar":
        return suma % 2 == 1
    if tipo == "dobles":
        return tiradaDados[0] == tiradaDados[1]
    return suma == sumaObjetivo

def lanzarDados():
    """
    Funcionalidad:
        Revisa la apuesta, tira dos dados, liquida el pago y muestra el resultado.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    color = widgets["color"].get()
    apuesta = validarApuesta(widgets["apuesta"].get(), color)
    if apuesta == 0:
        return

    tipo = widgets["tipo"].get()
    sumaObjetivo = 0
    if tipo == "sumaExacta":
        sumaObjetivo = validarSumaExacta(widgets["suma"].get().strip())
        if sumaObjetivo == 0:
            return

    descontarApuesta(apuesta, color)
    tiradaDados = (random.randint(1, CARAS_DADO), random.randint(1, CARAS_DADO))
    suma = tiradaDados[0] + tiradaDados[1]
    gano = evaluarApuestaDados(tipo, tiradaDados, suma, sumaObjetivo)
    multiplicador = pagosDados[tipo]
    pagoTotal = liquidar(apuesta, color, gano, multiplicador)
    widgets["dados"].config(text="Dados: " + str(tiradaDados) + "   Suma: " + str(suma))
    mostrarResultadoJuego(apuesta, color, gano, pagoTotal)

def dados():
    """
    Funcionalidad:
        Muestra la pantalla del juego de dados.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    ventana = nuevaVentana("Casino - Dados", "520x560", salaJuegos)
    tk.Label(ventana, text="JUEGO DE DADOS", font=("Arial", 16, "bold")).pack(pady=8)
    widgets["saldo"] = tk.Label(ventana, text=textoSaldo())
    widgets["saldo"].pack()
    crearSelectorColor(ventana)
    crearCampoApuesta(ventana)

    marcoTipo = tk.LabelFrame(ventana, text="Tipo de apuesta")
    marcoTipo.pack(pady=5)
    widgets["tipo"] = tk.StringVar(value="par")
    for fila in range(2):
        for columna in range(2):
            tipo = matrizOpcionesDados[fila][columna]
            texto = tipo + " (x" + str(pagosDados[tipo]) + ")"
            tk.Radiobutton(marcoTipo, text=texto, variable=widgets["tipo"], value=tipo).grid(row=fila, column=columna, sticky="w", padx=10)

    marcoSuma = tk.Frame(ventana)
    marcoSuma.pack(pady=5)
    tk.Label(marcoSuma, text="Suma exacta (2 al 12):").grid(row=0, column=0)
    widgets["suma"] = tk.Entry(marcoSuma, width=6)
    widgets["suma"].insert(0, "7")
    widgets["suma"].grid(row=0, column=1)

    widgets["dados"] = tk.Label(ventana, text="Dados: (-, -)", font=("Arial", 13, "bold"))
    widgets["dados"].pack(pady=5)
    widgets["resultado"] = tk.Label(ventana, text="Escoja su apuesta y lance los dados")
    widgets["resultado"].pack(pady=5)
    crearBoton(ventana, "Lanzar dados / Jugar otra vez", lanzarDados)
    crearBoton(ventana, "Regresar a juegos", salaJuegos)

# Fichas
def refrescarFichas():
    """
    Funcionalidad:
        Actualiza el dinero disponible, las fichas por color y reinicia los campos.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    widgets["dinero"].config(text="Dinero: $" + str(jugador[1][0]) + "   Total fichas: " + str(totalFichas()))
    for color in colores:
        widgets["tiene"][color].config(text=str(fichasDe(color)))
        widgets["cantidad"][color].delete(0, tk.END)
        widgets["cantidad"][color].insert(0, "0")

def leerCantidadesFichas(esCompra):
    """
    Funcionalidad:
        Lee y valida las cantidades por color, calculando el total y el monto.
    Entrada:
    - esCompra(bool): True si es compra, False si es canje.
    Salida:
    - resultado(dict): Diccionario con cantidades, total y monto, o {} si hay error.
    """
    cantidades = {}
    totalOperacion = 0
    montoTotal = 0
    for i in range(len(colores)):
        color = colores[i]
        texto = widgets["cantidad"][color].get().strip()
        if not esEntero(texto):
            messagebox.showwarning("Cantidad inválida", "Solo números enteros en " + color)
            return {}
        cantidad = int(texto)
        if not esCompra and cantidad > fichasDe(color):
            messagebox.showerror("Fichas insuficientes", "Solo tiene " + str(fichasDe(color)) + " ficha(s) " + color)
            return {}
        cantidades[llavesColores[i]] = cantidad
        totalOperacion = totalOperacion + cantidad
        montoTotal = montoTotal + cantidad * valorFicha(color)
    return {"cantidades": cantidades, "total": totalOperacion, "monto": montoTotal}

def validarOperacionFichas(esCompra, totalOperacion, montoTotal):
    """
    Funcionalidad:
        Valida que la operacion tenga fichas, que alcance el dinero y pide confirmacion.
    Entrada:
    - esCompra(bool): True si la operacion es compra, False si es canje.
    - totalOperacion(int): Cantidad total de fichas a comprar o canjear.
    - montoTotal(int): Monto total en dolares de la operacion.
    Salida:
    - valido(bool): True si es valido y confirmado, False en caso contrario.
    """
    if totalOperacion == 0:
        messagebox.showwarning("Vacío", "Escriba una cantidad mayor que cero en algún color")
        return False
    if esCompra and montoTotal > jugador[1][0]:
        messagebox.showerror("Dinero insuficiente", "Cuesta $" + str(montoTotal) + " y solo tiene $" + str(jugador[1][0]))
        return False
    verbo = "Comprar " if esCompra else "Canjear "
    return messagebox.askyesno("Confirmar", "¿" + verbo + str(totalOperacion) + " ficha(s) por $" + str(montoTotal) + "?")

def operarFichas(esCompra):
    """
    Funcionalidad:
        Hace la compra o el canje de fichas despues de revisar y confirmar.
    Entrada:
    - esCompra(bool): True si es compra, False si es canje.
    Salida:
    - Ninguna.
    """
    lectura = leerCantidadesFichas(esCompra)
    if len(lectura) == 0 or not validarOperacionFichas(esCompra, lectura["total"], lectura["monto"]):
        return
    if esCompra:
        resultado = datos.comprarFichas(jugador, lectura["cantidades"])
    else:
        resultado = datos.canjearFichas(jugador, lectura["cantidades"])
    if type(resultado) == str:
        messagebox.showerror("Error", "No se pudo completar: " + resultado)
    else:
        messagebox.showinfo("Listo", "Operación realizada")
    refrescarFichas()

def comprarFichas():
    """
    Funcionalidad:
        Hace una compra de fichas.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    operarFichas(True)

def canjearFichas():
    """
    Funcionalidad:
        Hace un canje de fichas.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    operarFichas(False)

def ventanaFichas():
    """
    Funcionalidad:
        Muestra la pantalla de compra y canje de fichas.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    ventana = nuevaVentana("Casino - Fichas", "480x420", menuPrincipal)
    tk.Label(ventana, text="COMPRA Y CANJE DE FICHAS", font=("Arial", 14, "bold")).pack(pady=8)
    widgets["dinero"] = tk.Label(ventana, text="")
    widgets["dinero"].pack()

    marcoTabla = tk.Frame(ventana)
    marcoTabla.pack(pady=8)
    titulos = ["Color", "Valor ($)", "Tienes", "Cantidad"]
    for i in range(len(titulos)):
        tk.Label(marcoTabla, text=titulos[i], font=("Arial", 10, "bold"), width=10).grid(row=0, column=i)

    widgets["tiene"] = {}
    widgets["cantidad"] = {}
    for i in range(len(colores)):
        color = colores[i]
        tk.Label(marcoTabla, text=color).grid(row=i + 1, column=0, pady=3)
        tk.Label(marcoTabla, text="$" + str(valorFicha(color))).grid(row=i + 1, column=1)
        widgets["tiene"][color] = tk.Label(marcoTabla, text="")
        widgets["tiene"][color].grid(row=i + 1, column=2)
        widgets["cantidad"][color] = tk.Entry(marcoTabla, width=8, justify="center")
        widgets["cantidad"][color].grid(row=i + 1, column=3)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=8)
    tk.Button(marcoBotones, text="Comprar fichas", width=16, command=comprarFichas).grid(row=0, column=0, padx=8)
    tk.Button(marcoBotones, text="Canjear fichas", width=16, command=canjearFichas).grid(row=0, column=1, padx=8)
    crearBoton(ventana, "Volver al menu", menuPrincipal)
    refrescarFichas()

# Inicio del programa
def iniciar():
    """
    Funcionalidad:
        Crea la ventana raiz escondida, abre el login y arranca el programa.
    Entrada:
    - Ninguna.
    Salida:
    - Ninguna.
    """
    estado["raiz"] = tk.Tk()
    estado["raiz"].withdraw()
    abrirSesion()
    estado["raiz"].mainloop()

if __name__ == "__main__":
    iniciar()
