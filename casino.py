# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

import tkinter as tk
from tkinter import messagebox
import random
import datos
import sesion

colores = ["Rojo", "Azul", "Verde", "Blanco"]
llavesColores = ["rojas", "azules", "verdes", "blancas"]

# Matriz de rodillos: cada fila es un rodillo
matrizRodillos = [
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"]
]

# Diccionario de combinaciones ganadoras: la llave es una tupla con los 3 simbolos
# y el valor es el multiplicador (las fichas se duplican)
combinacionesGanadoras = {
    ("Cereza", "Cereza", "Cereza"): 2,
    ("Limon", "Limon", "Limon"): 2,
    ("Campana", "Campana", "Campana"): 2,
    ("Estrella", "Estrella", "Estrella"): 2,
    ("Siete", "Siete", "Siete"): 2
}

# Diccionario de pagos de los dados
pagosDados = {"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}

# Matriz con las opciones de apuesta de los dados
matrizOpcionesDados = [
    ["par", "impar"],
    ["dobles", "sumaExacta"]
]

# [(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntos]
jugador = [("", "", ""), [0.0, 0, 0, 0, 0], 0]

# Estado del programa:
# raiz = ventana principal, actual = ventana abierta, girando = si la tragamonedas gira
# indices = posicion actual de cada rodillo
estado = {"raiz": "", "actual": "", "girando": False, "indices": [0, 0, 0]}

# Aqui se guardan los objetos de la ventana que se esta usando (etiquetas, campos, etc.)
widgets = {}

# Aqui se conecta E1
modulosE1 = {"ruleta": "", "blackjack": "", "ranking": "", "analisis": ""}



# Datos del jugador
def fichasDe(color):
    """
    Funcionalidad:
        Devuelve cuantas fichas tiene el jugador de un color.

    Entrada:
        - color(str): Nombre del color.

    Salida:
        - cantidad(int): Fichas de ese color.
    """
    posicion = colores.index(color)
    return int(jugador[1][posicion + 1])


def valorFicha(color):
    """
    Funcionalidad:
        Devuelve el valor en dolares de una ficha.

    Entrada:
        - color(str): Nombre del color.

    Salida:
        - valor(int): Valor de la ficha.
    """
    posicion = colores.index(color)
    return int(datos.VALOR_FICHAS[llavesColores[posicion]])


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
    for i in range(4):
        texto = texto + colores[i] + ": " + str(jugador[1][i + 1]) + "   "
    texto = texto + "\nTotal: " + str(totalFichas()) + "   Puntos: " + str(jugador[2])
    return texto


def guardar():
    """
    Funcionalidad:
        Guarda los datos del jugador en el archivo.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    try:
        datos.guardarCambiosJugador(jugador)
    except Exception as error:
        messagebox.showerror("Error al guardar", str(error))

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
        - textoApuesta(str): Lo que escribio el usuario.
        - color(str): Color de ficha elegido.

    Salida:
        - apuesta(int): La apuesta o 0 si es invalida.
    """
    textoApuesta = textoApuesta.strip()
    if not esEntero(textoApuesta):
        messagebox.showwarning("Apuesta invalida", "Escribe un numero entero mayor que cero")
        return 0
    apuesta = int(textoApuesta)
    if apuesta <= 0:
        messagebox.showwarning("Apuesta invalida", "Escribe un numero entero mayor que cero")
        return 0
    if apuesta > fichasDe(color):
        messagebox.showwarning("Fichas insuficientes", "Solo tienes " + str(fichasDe(color)) + " ficha(s) " + color)
        return 0
    return apuesta


def liquidar(apuesta, color, gano, multiplicador):
    """
    Funcionalidad:
        Paga las fichas si gano, cambia los puntos y guarda.
        El pago incluye la apuesta devuelta (la apuesta ya fue descontada).

    Entrada:
        - apuesta(int): Fichas apostadas.
        - color(str): Color apostado.
        - gano(bool): True si gano, False si perdio.
        - multiplicador(int): Veces la apuesta que recibe si gana.

    Salida:
        - pagoTotal(int): Fichas que recibe el jugador.
    """
    pagoTotal = 0
    if gano:
        pagoTotal = apuesta * multiplicador
        jugador[1][colores.index(color) + 1] = jugador[1][colores.index(color) + 1] + pagoTotal
        jugador[2] = jugador[2] + 2
    else:
        jugador[2] = jugador[2] - 1
    guardar()
    return pagoTotal


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
        Cierra la ventana actual y crea una nueva.

    Entrada:
        - titulo(str): Titulo de la ventana.
        - tamano(str): Tamano, por ejemplo "400x300".
        - funcionAlCerrar(function): Funcion que se ejecuta al cerrar con la X.

    Salida:
        - ventana(Toplevel): La ventana nueva.
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
        Crea un boton y lo coloca en la ventana.

    Entrada:
        - ventana(Widget): Donde va el boton.
        - texto(str): Texto del boton.
        - funcion(function): Funcion que ejecuta el boton.

    Salida:
        - Ninguna.
    """
    tk.Button(ventana, text=texto, width=24, command=funcion).pack(pady=4)


def crearSelectorColor(ventana):
    """
    Funcionalidad:
        Crea los cuatro radiobuttons para escoger el color de ficha.

    Entrada:
        - ventana(Widget): Donde van los radiobuttons.

    Salida:
        - Ninguna (la variable queda en widgets["color"]).
    """
    widgets["color"] = tk.StringVar(value="Blanco")
    marco = tk.Frame(ventana)
    marco.pack(pady=5)
    for i in range(4):
        texto = colores[i] + " ($" + str(valorFicha(colores[i])) + ")"
        tk.Radiobutton(marco, text=texto, variable=widgets["color"], value=colores[i]).grid(row=0, column=i)


def crearCampoApuesta(ventana):
    """
    Funcionalidad:
        Crea el campo donde se escribe la apuesta.

    Entrada:
        - ventana(Widget): Donde va el campo.

    Salida:
        - Ninguna (el campo queda en widgets["apuesta"]).
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
        Revisa el registro del jugador y abre el menu principal.

    Entrada:
        - registroJugador(list): Datos del jugador.

    Salida:
        - exito(bool): True si todo salio bien, False si no.
    """
    if type(registroJugador) != list:
        messagebox.showerror("Error", "El registro del jugador no es valido")
        return False
    if not datos.validarEstructuraJugador(registroJugador):
        messagebox.showerror("Error", "El registro del jugador no es valido")
        return False
    jugador[:] = registroJugador
    menuPrincipal()
    return True


def cerrarSesion():
    """
    Funcionalidad:
        Pregunta si quiere cerrar sesion, guarda y vuelve al login.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    if messagebox.askyesno("Cerrar sesion", "Seguro que quiere cerrar la sesion?"):
        guardar()
        jugador[:] = [("", "", ""), [0.0, 0, 0, 0, 0], 0]
        abrirSesion()


def abrirE1(nombreModulo):
    """
    Funcionalidad:
        Abre una pantalla de E1 o avisa si todavia no esta conectada.

    Entrada:
        - nombreModulo(str): Nombre dentro del diccionario modulosE1.

    Salida:
        - Ninguna.
    """
    if modulosE1[nombreModulo] == "":
        messagebox.showwarning("No disponible", "'" + nombreModulo + "' todavia no esta conectado")
    else:
        modulosE1[nombreModulo]()


def abrirRuleta():
    """
    Funcionalidad:
        Abre la ruleta (E1).

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("ruleta")


def abrirBlackjack():
    """
    Funcionalidad:
        Abre el blackjack (E1).

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("blackjack")


def abrirRanking():
    """
    Funcionalidad:
        Abre el ranking (E1).

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("ranking")


def abrirAnalisis():
    """
    Funcionalidad:
        Abre el analisis (E1).

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("analisis")


def menuPrincipal():
    """
    Funcionalidad:
        Muestra el menu principal.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventana = nuevaVentana("Casino - Menu", "420x380", cerrarTodo)
    tk.Label(ventana, text="CASINO", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(ventana, text="Jugador: " + str(jugador[0][0]) + "   Dinero: $" + str(jugador[1][0])).pack()
    tk.Label(ventana, text=textoSaldo()).pack(pady=5)
    crearBoton(ventana, "Jugar", salaJuegos)
    crearBoton(ventana, "Fichas", ventanaFichas)
    crearBoton(ventana, "Ranking", abrirRanking)
    crearBoton(ventana, "Analisis", abrirAnalisis)
    crearBoton(ventana, "Cerrar sesion", cerrarSesion)


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
    crearBoton(ventana, "Ruleta", abrirRuleta)
    crearBoton(ventana, "Tragamonedas", tragamonedas)
    crearBoton(ventana, "Blackjack", abrirBlackjack)
    crearBoton(ventana, "Dados", dados)
    crearBoton(ventana, "Volver al menu", menuPrincipal)


# Tragamonedas
def volverDeTragamonedas():
    """
    Funcionalidad:
        Vuelve a la sala, pero solo si los rodillos no estan girando.

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
        - paso(int): Numero de paso de la animacion.
        - apuesta(int): Fichas apostadas.
        - color(str): Color de las fichas.

    Salida:
        - Ninguna.
    """
    simbolos = []
    for i in range(3):
        estado["indices"][i] = (estado["indices"][i] + 1) % 5
        simbolos.append(matrizRodillos[i][estado["indices"][i]])
    widgets["rodillos"].config(text=simbolos[0] + "  |  " + simbolos[1] + "  |  " + simbolos[2])

    if paso < 12:
        estado["actual"].after(150, girarRodillos, paso + 1, apuesta, color)
        return

    # Se busca la combinacion en el diccionario (si no esta, no gano)
    combinacion = (simbolos[0], simbolos[1], simbolos[2])
    multiplicador = 0
    if combinacion in combinacionesGanadoras:
        multiplicador = combinacionesGanadoras[combinacion]

    gano = False
    if multiplicador > 0:
        gano = True

    pagoTotal = liquidar(apuesta, color, gano, multiplicador)
    if gano:
        widgets["resultado"].config(text="GANASTE! Recibe " + str(pagoTotal) + " ficha(s) " + color + " (ganancia neta: " + str(pagoTotal - apuesta) + ") y +2 puntos")
    else:
        widgets["resultado"].config(text="Perdio " + str(apuesta) + " ficha(s) " + color + " y -1 punto")
    widgets["saldo"].config(text=textoSaldo())
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
    posicion = colores.index(color) + 1
    jugador[1][posicion] = jugador[1][posicion] - apuesta
    widgets["saldo"].config(text=textoSaldo())
    widgets["resultado"].config(text="Girando...")
    for i in range(3):
        estado["indices"][i] = random.randint(0, 4)
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
def lanzarDados():
    """
    Funcionalidad:
        Revisa la apuesta, tira dos dados y dice si gano.

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
    textoSuma = widgets["suma"].get().strip()
    multiplicador = 0
    if tipo == "sumaExacta":
        if not esEntero(textoSuma):
            messagebox.showwarning("Suma invalida", "Escriba un numero entero entre 2 y 12")
            return
        if int(textoSuma) < 2 or int(textoSuma) > 12:
            messagebox.showwarning("Suma invalida", "Escriba un numero entero entre 2 y 12")
            return
        multiplicador = pagosSumaExacta[int(textoSuma)]
    else:
        multiplicador = pagosDados[tipo]

    posicion = colores.index(color) + 1
    jugador[1][posicion] = jugador[1][posicion] - apuesta

    # La tirada es una tupla con los valores de los 2 dados
    tiradaDados = (random.randint(1, 6), random.randint(1, 6))
    suma = tiradaDados[0] + tiradaDados[1]

    gano = False
    if tipo == "par":
        if suma % 2 == 0:
            gano = True
    elif tipo == "impar":
        if suma % 2 == 1:
            gano = True
    elif tipo == "dobles":
        if tiradaDados[0] == tiradaDados[1]:
            gano = True
    elif tipo == "sumaExacta":
        if suma == int(textoSuma):
            gano = True

    pagoTotal = liquidar(apuesta, color, gano, multiplicador)
    widgets["dados"].config(text="Dados: " + str(tiradaDados) + "   Suma: " + str(suma))
    if gano:
        widgets["resultado"].config(text="Acerto! Recibe " + str(pagoTotal) + " ficha(s) " + color + " (ganancia neta: " + str(pagoTotal - apuesta) + ") y +2 puntos")
    else:
        widgets["resultado"].config(text="No acerto. Perdio " + str(apuesta) + " ficha(s) " + color + " y -1 punto")
    widgets["saldo"].config(text=textoSaldo())


def actualizarCampoSuma():
    """
    Funcionalidad:
        Muestra el campo de suma exacta solo si ese tipo de apuesta esta elegido.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    if widgets["tipo"].get() == "sumaExacta":
        widgets["marcoSuma"].pack(pady=5, before=widgets["dados"])
    else:
        widgets["marcoSuma"].pack_forget()


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
            if tipo == "sumaExacta":
                texto = tipo + " (x" + str(min(pagosSumaExacta.values())) + " a x" + str(max(pagosSumaExacta.values())) + ")"
            else:
                texto = tipo + " (x" + str(pagosDados[tipo]) + ")"
            tk.Radiobutton(marcoTipo, text=texto, variable=widgets["tipo"], value=tipo, command=actualizarCampoSuma).grid(row=fila, column=columna, sticky="w", padx=10)

    # Este marco no se muestra hasta que se elige sumaExacta
    widgets["marcoSuma"] = tk.Frame(ventana)
    tk.Label(widgets["marcoSuma"], text="Suma exacta (2 al 12):").grid(row=0, column=0)
    widgets["suma"] = tk.Entry(widgets["marcoSuma"], width=6)
    widgets["suma"].insert(0, "7")
    widgets["suma"].grid(row=0, column=1)
    textoPagos = "Pagos: "
    for suma in range(2, 13):
        textoPagos = textoPagos + str(suma) + "=x" + str(pagosSumaExacta[suma]) + "  "
    tk.Label(widgets["marcoSuma"], text=textoPagos, font=("Arial", 8), wraplength=480).grid(row=1, column=0, columnspan=2)

    widgets["dados"] = tk.Label(ventana, text="Dados: (-, -)", font=("Arial", 13, "bold"))
    widgets["dados"].pack(pady=5)
    widgets["resultado"] = tk.Label(ventana, text="Escoja su apuesta y lance los dados")
    widgets["resultado"].pack(pady=5)
    crearBoton(ventana, "Lanzar dados / Jugar otra vez", lanzarDados)
    crearBoton(ventana, "Regresar a juegos", salaJuegos)

# Fichas
def operarFichas(esCompra):
    """
    Funcionalidad:
        Hace la compra o el canje de fichas despues de revisar y confirmar.

    Entrada:
        - esCompra(bool): True si es compra, False si es canje.

    Salida:
        - Ninguna.
    """
    cantidades = {}
    totalOperacion = 0
    montoTotal = 0
    for i in range(4):
        color = colores[i]
        texto = widgets["cantidad"][color].get().strip()
        if not esEntero(texto):
            messagebox.showwarning("Cantidad invalida", "Solo numeros enteros en " + color)
            return
        cantidad = int(texto)
        if not esCompra and cantidad > fichasDe(color):
            messagebox.showerror("Fichas insuficientes", "Solo tiene " + str(fichasDe(color)) + " ficha(s) " + color)
            return
        cantidades[llavesColores[i]] = cantidad
        totalOperacion = totalOperacion + cantidad
        montoTotal = montoTotal + cantidad * valorFicha(color)

    if totalOperacion == 0:
        messagebox.showwarning("Vacio", "Escriba una cantidad mayor que cero en algun color")
        return
    if esCompra and montoTotal > jugador[1][0]:
        messagebox.showerror("Dinero insuficiente", "Cuesta $" + str(montoTotal) + " y solo tiene $" + str(jugador[1][0]))
        return

    if esCompra:
        verbo = "Comprar "
    else:
        verbo = "Canjear "
    if not messagebox.askyesno("Confirmar", verbo + str(totalOperacion) + " ficha(s) por $" + str(montoTotal) + "?"):
        return

    respaldo = list(jugador[1])
    try:
        if esCompra:
            datos.comprarFichas(jugador, cantidades)
        else:
            datos.canjearFichas(jugador, cantidades)
        messagebox.showinfo("Listo", "Operacion realizada")
    except Exception as error:
        jugador[1] = respaldo
        messagebox.showerror("Error", "No se pudo completar: " + str(error))
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
    for i in range(4):
        tk.Label(marcoTabla, text=titulos[i], font=("Arial", 10, "bold"), width=10).grid(row=0, column=i)

    widgets["tiene"] = {}
    widgets["cantidad"] = {}
    for i in range(4):
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


iniciar()