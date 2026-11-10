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

colores = ("Rojo", "Azul", "Verde", "Blanco")
llavesColores = ("rojas", "azules", "verdes", "blancas")

matrizRodillos = [
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"]
]

combinacionesGanadoras = {
    ("Cereza", "Cereza", "Cereza"): 2,
    ("Limon", "Limon", "Limon"): 2,
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

ventanaRaiz = ""
ventanaActual = ""
estaGirando = False

# Aqui se conecta E1
modulosE1 = {"ruleta": "", "blackjack": "", "ranking": "", "analisis": ""}


# datos del jugador

def fichasDe(color):
    """
    Funcionalidad:
        Obtiene la cantidad de fichas que posee el jugador de un color determinado.

    Entrada:
        - color(str): Nombre del color de la ficha a consultar.

    Salida:
        - cantidad(int): Cantidad de fichas disponibles de ese color.
    """
    return int(jugador[1][colores.index(color) + 1])


def valorFicha(color):
    """
    Funcionalidad:
        Consulta en el diccionario de datos el valor monetario en dolares de una ficha.

    Entrada:
        - color(str): Nombre del color de la ficha a consultar.

    Salida:
        - valor(int): Valor monetario unitario de la ficha.
    """
    return int(datos.VALOR_FICHAS[llavesColores[colores.index(color)]])


def totalFichas():
    """
    Funcionalidad:
        Calcula la suma total de fichas de todos los colores pertenecientes al jugador.

    Entrada:
        - Ninguna.

    Salida:
        - total(int): Suma total de fichas del jugador.
    """
    total = 0
    for color in colores:
        total += fichasDe(color)
    return total


def textoSaldo():
    """
    Funcionalidad:
        Construye el texto informativo con el desglose de fichas por color, total y puntaje.

    Entrada:
        - Ninguna.

    Salida:
        - texto(str): Cadena formateada para mostrar en las etiquetas de saldo.
    """
    textoFichas = ""
    for posicion in range(4):
        textoFichas += colores[posicion] + ": " + str(jugador[1][posicion + 1]) + "   "
    textoTotal = "Total: " + str(totalFichas()) + "   Puntos: " + str(jugador[2])
    return textoFichas + "\n" + textoTotal


def guardar():
    """
    Funcionalidad:
        Guarda los datos actualizados del jugador en el archivo local de jugadores.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    try:
        datos.guardarCambiosJugador(jugador)
    except Exception as error:
        messagebox.showerror("Error al guardar", str(error))


def validarApuesta(textoApuesta, color):
    """
    Funcionalidad:
        Valida que la cantidad escrita sea un numero entero positivo y que existan fichas suficientes.

    Entrada:
        - textoApuesta(str): Texto ingresado en el campo de apuesta.
        - color(str): Color de ficha seleccionado para la jugada.

    Salida:
        - apuesta(int): Monto entero validado o cero si la entrada es invalida.
    """
    if not textoApuesta.strip().isdecimal() or int(textoApuesta) <= 0:
        messagebox.showwarning("Apuesta invalida", "Escribe un numero entero mayor que cero")
        return 0
    apuesta = int(textoApuesta)
    if apuesta > fichasDe(color):
        messagebox.showwarning("Fichas insuficientes", "Solo tienes " + str(fichasDe(color)) + " ficha(s) " + color)
        return 0
    return apuesta


def liquidar(apuesta, color, gano, multiplicador):
    """
    Funcionalidad:
        Acredita las fichas ganadas, suma o resta puntos y guarda los cambios en el archivo.

    Entrada:
        - apuesta(int): Cantidad de fichas apostadas.
        - color(str): Color de ficha apostada.
        - gano(bool): Indicador booleano de si el jugador gano o perdio.
        - multiplicador(int): Multiplicador de ganancia de la apuesta.

    Salida:
        - resultado(tuple): Tupla con el pago total y la ganancia neta obtenida.
    """
    pagoTotal = 0
    if gano:
        pagoTotal = apuesta * multiplicador
        jugador[1][colores.index(color) + 1] += pagoTotal
        jugador[2] += 2
    else:
        jugador[2] -= 1
    guardar()
    return (pagoTotal, pagoTotal - apuesta)


# ventanas

def cerrarTodo():
    """
    Funcionalidad:
        Finaliza la aplicacion destruyendo la ventana raiz de Tkinter.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaRaiz.destroy()


def nuevaVentana(titulo, tamano, funcionAlCerrar):
    """
    Funcionalidad:
        Destruye la ventana secundaria actual y crea una nueva ventana Toplevel configurada.

    Entrada:
        - titulo(str): Titulo que aparecera en la barra superior.
        - tamano(str): Dimensiones de la ventana en formato ancho por alto.
        - funcionAlCerrar(function): Protocolo a ejecutar al presionar el boton de cerrar.

    Salida:
        - ventanaNueva(Toplevel): Instancia de la nueva ventana secundaria creada.
    """
    global ventanaActual
    if ventanaActual:
        ventanaActual.destroy()
    ventanaNueva = tk.Toplevel(ventanaRaiz)
    ventanaNueva.title(titulo)
    ventanaNueva.geometry(tamano)
    ventanaNueva.protocol("WM_DELETE_WINDOW", funcionAlCerrar)
    ventanaActual = ventanaNueva
    return ventanaNueva


def crearBoton(ventanaPadre, textoBoton, funcionBoton):
    """
    Funcionalidad:
        Crea y empaqueta un boton estandar con texto y comando asignado.

    Entrada:
        - ventanaPadre(Widget): Contenedor donde se agregara el boton.
        - textoBoton(str): Texto visible del boton.
        - funcionBoton(function): Accion que ejecutara el boton al ser presionado.

    Salida:
        - Ninguna.
    """
    tk.Button(ventanaPadre, text=textoBoton, width=24, command=funcionBoton).pack(pady=4)


def crearSelectorColor(ventanaPadre):
    """
    Funcionalidad:
        Crea y coloca los radiobuttons correspondientes a los cuatro colores de ficha.

    Entrada:
        - ventanaPadre(Widget): Contenedor donde se ubicaran las opciones de color.

    Salida:
        - colorElegido(StringVar): Variable de Tkinter que almacena el color seleccionado.
    """
    colorElegido = tk.StringVar(value="Blanco")
    marcoColores = tk.Frame(ventanaPadre)
    marcoColores.pack(pady=5)
    for posicion in range(4):
        textoColor = colores[posicion] + " ($" + str(valorFicha(colores[posicion])) + ")"
        tk.Radiobutton(marcoColores, text=textoColor, variable=colorElegido, value=colores[posicion]).grid(row=0, column=posicion)
    return colorElegido


def crearCampoApuesta(ventanaPadre):
    """
    Funcionalidad:
        Crea la etiqueta y el campo de entrada numerica para indicar la apuesta.

    Entrada:
        - ventanaPadre(Widget): Contenedor donde se ubicara el campo de entrada.

    Salida:
        - campoApuesta(Entry): Entrada de texto configurada con valor inicial de 1.
    """
    marcoApuesta = tk.Frame(ventanaPadre)
    marcoApuesta.pack(pady=5)
    tk.Label(marcoApuesta, text="Fichas a apostar:").grid(row=0, column=0)
    campoApuesta = tk.Entry(marcoApuesta, width=8)
    campoApuesta.insert(0, "1")
    campoApuesta.grid(row=0, column=1)
    return campoApuesta


# sesion y menus

def abrirSesion():
    """
    Funcionalidad:
        Construye la ventana secundaria de inicio de sesion y la conecta con sesion.py.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaSesion = nuevaVentana("Casino - Sesion", "430x440", cerrarTodo)
    sesion.crearVentanaSesion(iniciarSesion, ventanaSesion)


def iniciarSesion(registroJugador):
    """
    Funcionalidad:
        Valida el registro del jugador recibido y abre la ventana del menu principal.

    Entrada:
        - registroJugador(list): Lista con los datos personales, recursos y puntaje del jugador.

    Salida:
        - exito(bool): True si el jugador es valido y se inicio la sesion, False en caso contrario.
    """
    global jugador
    if type(registroJugador) != list or not datos.validarEstructuraJugador(registroJugador):
        messagebox.showerror("Error", "El registro del jugador no es valido")
        return False
    jugador = registroJugador
    menuPrincipal()
    return True


def cerrarSesion():
    """
    Funcionalidad:
        Pide confirmacion al usuario, guarda los datos, limpia la memoria y vuelve al login.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    global jugador
    if messagebox.askyesno("Cerrar sesion", "Seguro que quiere cerrar la sesion?"):
        guardar()
        jugador = [("", "", ""), [0.0, 0, 0, 0, 0], 0]
        abrirSesion()


def abrirE1(nombreModulo):
    """
    Funcionalidad:
        Ejecuta una funcion del modulo E1 o muestra una advertencia si no esta disponible.

    Entrada:
        - nombreModulo(str): Identificador de la funcion solicitada dentro de modulosE1.

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
        Abre el juego de Ruleta implementado en el modulo E1.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("ruleta")


def abrirBlackjack():
    """
    Funcionalidad:
        Abre el juego de Blackjack implementado en el modulo E1.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("blackjack")


def abrirRanking():
    """
    Funcionalidad:
        Abre la pantalla de Ranking implementada en el modulo E1.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("ranking")


def abrirAnalisis():
    """
    Funcionalidad:
        Abre la pantalla de Analisis implementada en el modulo E1.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    abrirE1("analisis")


def menuPrincipal():
    """
    Funcionalidad:
        Construye y muestra la pantalla del menu principal con los datos del jugador y opciones.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaMenu = nuevaVentana("Casino - Menu", "420x380", cerrarTodo)
    tk.Label(ventanaMenu, text="CASINO", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(ventanaMenu, text="Jugador: " + str(jugador[0][0]) + "   Dinero: $" + str(jugador[1][0])).pack()
    tk.Label(ventanaMenu, text=textoSaldo()).pack(pady=5)
    crearBoton(ventanaMenu, "Jugar", salaJuegos)
    crearBoton(ventanaMenu, "Fichas", ventanaFichas)
    crearBoton(ventanaMenu, "Ranking", abrirRanking)
    crearBoton(ventanaMenu, "Analisis", abrirAnalisis)
    crearBoton(ventanaMenu, "Cerrar sesion", cerrarSesion)


def salaJuegos():
    """
    Funcionalidad:
        Construye y muestra la pantalla selectora de juegos con botones para cada opcion.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaSala = nuevaVentana("Casino - Juegos", "420x350", menuPrincipal)
    tk.Label(ventanaSala, text="SALA DE JUEGOS", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(ventanaSala, text=textoSaldo()).pack(pady=5)
    crearBoton(ventanaSala, "Ruleta", abrirRuleta)
    crearBoton(ventanaSala, "Tragamonedas", tragamonedas)
    crearBoton(ventanaSala, "Blackjack", abrirBlackjack)
    crearBoton(ventanaSala, "Dados", dados)
    crearBoton(ventanaSala, "Volver al menu", menuPrincipal)


# tragamonedas

def tragamonedas():
    """
    Funcionalidad:
        Construye y gestiona la interfaz del juego de tragamonedas de tres rodillos.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    global estaGirando
    estaGirando = False
    indicesRodillos = [0, 1, 2]

    def volverASala():
        """
        Funcionalidad:
            Regresa a la sala de juegos asegurando que los rodillos no esten girando.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        if estaGirando:
            messagebox.showinfo("Girando", "Espere a que terminen de girar los rodillos")
        else:
            salaJuegos()

    ventanaTragamonedas = nuevaVentana("Casino - Tragamonedas", "520x420", volverASala)
    tk.Label(ventanaTragamonedas, text="TRAGAMONEDAS", font=("Arial", 16, "bold")).pack(pady=8)
    etiquetaSaldo = tk.Label(ventanaTragamonedas, text=textoSaldo())
    etiquetaSaldo.pack()
    etiquetaRodillos = tk.Label(ventanaTragamonedas, text="?  |  ?  |  ?", font=("Arial", 16))
    etiquetaRodillos.pack(pady=10)
    colorElegido = crearSelectorColor(ventanaTragamonedas)
    campoApuesta = crearCampoApuesta(ventanaTragamonedas)
    etiquetaResultado = tk.Label(ventanaTragamonedas, text="Escoja el color, la apuesta y presione Girar / Jugar otra vez")
    etiquetaResultado.pack(pady=8)

    def girarRodillos(pasoActual, apuesta, color):
        """
        Funcionalidad:
            Realiza la animacion ciclica de los rodillos, comprueba si gano y liquida la apuesta.

        Entrada:
            - pasoActual(int): Numero de paso actual dentro de la animacion.
            - apuesta(int): Cantidad de fichas apostadas.
            - color(str): Color de las fichas en juego.

        Salida:
            - Ninguna.
        """
        global estaGirando
        simbolos = []
        for fila in range(3):
            indicesRodillos[fila] = (indicesRodillos[fila] + 1) % 5
            simbolos.append(matrizRodillos[fila][indicesRodillos[fila]])
        simbolosActuales = tuple(simbolos)
        etiquetaRodillos.config(text="  |  ".join(simbolosActuales))

        if pasoActual < 12:
            ventanaTragamonedas.after(150, girarRodillos, pasoActual + 1, apuesta, color)
            return

        multiplicador = combinacionesGanadoras.get(simbolosActuales, 0)
        gano = multiplicador > 0
        pagoTotal, gananciaNeta = liquidar(apuesta, color, gano, multiplicador)
        if gano:
            etiquetaResultado.config(text="GANASTE! Recibe " + str(pagoTotal) + " ficha(s) " + color + " y +2 puntos")
        else:
            etiquetaResultado.config(text="Perdio " + str(apuesta) + " ficha(s) " + color + " y -1 punto")
        etiquetaSaldo.config(text=textoSaldo())
        estaGirando = False

    def iniciarGiro():
        """
        Funcionalidad:
            Valida la apuesta, descuenta las fichas e inicia el giro animado de los rodillos.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        global estaGirando
        if estaGirando:
            return
        color = colorElegido.get()
        apuesta = validarApuesta(campoApuesta.get(), color)
        if apuesta == 0:
            return
        jugador[1][colores.index(color) + 1] -= apuesta
        etiquetaSaldo.config(text=textoSaldo())
        etiquetaResultado.config(text="Girando...")
        for fila in range(3):
            indicesRodillos[fila] = random.randint(0, 4)
        estaGirando = True
        girarRodillos(1, apuesta, color)

    crearBoton(ventanaTragamonedas, "Girar / Jugar otra vez", iniciarGiro)
    crearBoton(ventanaTragamonedas, "Regresar a juegos", volverASala)


# dados

def dados():
    """
    Funcionalidad:
        Construye y gestiona la interfaz del juego de dados con diversos tipos de apuesta.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaDados = nuevaVentana("Casino - Dados", "520x520", salaJuegos)
    tk.Label(ventanaDados, text="JUEGO DE DADOS", font=("Arial", 16, "bold")).pack(pady=8)
    etiquetaSaldo = tk.Label(ventanaDados, text=textoSaldo())
    etiquetaSaldo.pack()
    colorElegido = crearSelectorColor(ventanaDados)
    campoApuesta = crearCampoApuesta(ventanaDados)

    marcoTipoApuesta = tk.LabelFrame(ventanaDados, text="Tipo de apuesta")
    marcoTipoApuesta.pack(pady=5)
    tipoElegido = tk.StringVar(value="par")
    for fila in range(2):
        for columna in range(2):
            tipoApuesta = matrizOpcionesDados[fila][columna]
            textoOpcion = tipoApuesta + " (x" + str(pagosDados[tipoApuesta]) + ")"
            tk.Radiobutton(marcoTipoApuesta, text=textoOpcion, variable=tipoElegido, value=tipoApuesta).grid(row=fila, column=columna, sticky="w", padx=10)

    marcoSumaExacta = tk.Frame(ventanaDados)
    marcoSumaExacta.pack(pady=5)
    tk.Label(marcoSumaExacta, text="Suma exacta (2 al 12):").grid(row=0, column=0)
    campoSumaExacta = tk.Entry(marcoSumaExacta, width=6)
    campoSumaExacta.insert(0, "7")
    campoSumaExacta.grid(row=0, column=1)

    etiquetaDados = tk.Label(ventanaDados, text="Dados: (-, -)", font=("Arial", 13, "bold"))
    etiquetaDados.pack(pady=5)
    etiquetaResultado = tk.Label(ventanaDados, text="Escoja su apuesta y lance los dados")
    etiquetaResultado.pack(pady=5)

    def lanzarDados():
        """
        Funcionalidad:
            Valida la apuesta, genera la tirada de dos dados, evalua el acierto y liquida el resultado.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        color = colorElegido.get()
        apuesta = validarApuesta(campoApuesta.get(), color)
        if apuesta == 0:
            return

        tipoApuesta = tipoElegido.get()
        textoSuma = campoSumaExacta.get().strip()
        if tipoApuesta == "sumaExacta":
            if not textoSuma.isdecimal() or int(textoSuma) < 2 or int(textoSuma) > 12:
                messagebox.showwarning("Suma invalida", "Escriba un numero entero entre 2 y 12")
                return

        jugador[1][colores.index(color) + 1] -= apuesta
        tiradaDados = (random.randint(1, 6), random.randint(1, 6))
        sumaDados = tiradaDados[0] + tiradaDados[1]

        if tipoApuesta == "sumaExacta":
            gano = sumaDados == int(textoSuma)
        elif tipoApuesta == "par":
            gano = sumaDados % 2 == 0
        elif tipoApuesta == "impar":
            gano = sumaDados % 2 == 1
        else:
            gano = tiradaDados[0] == tiradaDados[1]

        pagoTotal, gananciaNeta = liquidar(apuesta, color, gano, pagosDados[tipoApuesta])
        etiquetaDados.config(text="Dados: " + str(tiradaDados) + "   Suma: " + str(sumaDados))
        if gano:
            etiquetaResultado.config(text="Acerto! Recibe " + str(pagoTotal) + " ficha(s) " + color + " y +2 puntos")
        else:
            etiquetaResultado.config(text="No acerto. Perdio " + str(apuesta) + " ficha(s) " + color + " y -1 punto")
        etiquetaSaldo.config(text=textoSaldo())

    crearBoton(ventanaDados, "Lanzar dados", lanzarDados)
    crearBoton(ventanaDados, "Regresar a juegos", salaJuegos)


# fichas

def ventanaFichas():
    """
    Funcionalidad:
        Construye y gestiona la pantalla para la compra y el canje de fichas del jugador.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    ventanaCompraCanje = nuevaVentana("Casino - Fichas", "480x420", menuPrincipal)
    tk.Label(ventanaCompraCanje, text="COMPRA Y CANJE DE FICHAS", font=("Arial", 14, "bold")).pack(pady=8)
    etiquetaDinero = tk.Label(ventanaCompraCanje, text="")
    etiquetaDinero.pack()

    marcoTabla = tk.Frame(ventanaCompraCanje)
    marcoTabla.pack(pady=8)
    titulosColumnas = ["Color", "Valor ($)", "Tienes", "Cantidad"]
    for columna in range(4):
        tk.Label(marcoTabla, text=titulosColumnas[columna], font=("Arial", 10, "bold"), width=10).grid(row=0, column=columna)

    etiquetasFichasTiene = {}
    camposCantidad = {}
    for posicion in range(4):
        color = colores[posicion]
        tk.Label(marcoTabla, text=color).grid(row=posicion + 1, column=0, pady=3)
        tk.Label(marcoTabla, text="$" + str(valorFicha(color))).grid(row=posicion + 1, column=1)
        etiquetasFichasTiene[color] = tk.Label(marcoTabla, text="")
        etiquetasFichasTiene[color].grid(row=posicion + 1, column=2)
        camposCantidad[color] = tk.Entry(marcoTabla, width=8, justify="center")
        camposCantidad[color].grid(row=posicion + 1, column=3)

    def refrescarPantalla():
        """
        Funcionalidad:
            Actualiza en pantalla el dinero disponible y la cantidad de fichas por color.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        etiquetaDinero.config(text="Dinero: $" + str(jugador[1][0]) + "   Total fichas: " + str(totalFichas()))
        for color in colores:
            etiquetasFichasTiene[color].config(text=str(fichasDe(color)))
            camposCantidad[color].delete(0, tk.END)
            camposCantidad[color].insert(0, "0")

    def operarFichas(esCompra):
        """
        Funcionalidad:
            Procesa y valida la transaccion de compra o canje de fichas solicitando confirmacion.

        Entrada:
            - esCompra(bool): True si corresponde a una compra de fichas, False si es un canje.

        Salida:
            - Ninguna.
        """
        cantidadesPorColor = {}
        totalFichasOperacion = 0
        montoTotal = 0
        for posicion in range(4):
            color = colores[posicion]
            textoCantidad = camposCantidad[color].get().strip()
            if not textoCantidad.isdecimal():
                messagebox.showwarning("Cantidad invalida", "Solo numeros enteros en " + color)
                return
            cantidad = int(textoCantidad)
            if not esCompra and cantidad > fichasDe(color):
                messagebox.showerror("Fichas insuficientes", "Solo tiene " + str(fichasDe(color)) + " ficha(s) " + color)
                return
            cantidadesPorColor[llavesColores[posicion]] = cantidad
            totalFichasOperacion += cantidad
            montoTotal += cantidad * valorFicha(color)

        if totalFichasOperacion == 0:
            messagebox.showwarning("Vacio", "Escriba una cantidad mayor que cero en algun color")
            return
        if esCompra and montoTotal > jugador[1][0]:
            messagebox.showerror("Dinero insuficiente", "Cuesta $" + str(montoTotal) + " y solo tiene $" + str(jugador[1][0]))
            return

        verbo = "Canjear "
        if esCompra:
            verbo = "Comprar "
        if not messagebox.askyesno("Confirmar", verbo + str(totalFichasOperacion) + " ficha(s) por $" + str(montoTotal) + "?"):
            return

        respaldoRecursos = list(jugador[1])
        try:
            if esCompra:
                datos.comprarFichas(jugador, cantidadesPorColor)
            else:
                datos.canjearFichas(jugador, cantidadesPorColor)
            messagebox.showinfo("Listo", "Operacion realizada")
        except Exception as error:
            jugador[1] = respaldoRecursos
            messagebox.showerror("Error", "No se pudo completar: " + str(error))
        refrescarPantalla()

    def comprarFichas():
        """
        Funcionalidad:
            Ejecuta la transaccion de compra de fichas llamando a operarFichas con True.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        operarFichas(True)

    def canjearFichas():
        """
        Funcionalidad:
            Ejecuta la transaccion de canje de fichas llamando a operarFichas con False.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna.
        """
        operarFichas(False)

    marcoBotones = tk.Frame(ventanaCompraCanje)
    marcoBotones.pack(pady=8)
    tk.Button(marcoBotones, text="Comprar fichas", width=16, command=comprarFichas).grid(row=0, column=0, padx=8)
    tk.Button(marcoBotones, text="Canjear fichas", width=16, command=canjearFichas).grid(row=0, column=1, padx=8)
    crearBoton(ventanaCompraCanje, "Volver al menu", menuPrincipal)
    refrescarPantalla()
# inicio
def iniciar():
    """
    Funcionalidad:
        Crea la ventana raiz escondida, abre la sesion y arranca el bucle de eventos.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna.
    """
    global ventanaRaiz
    ventanaRaiz = tk.Tk()
    ventanaRaiz.withdraw()
    abrirSesion()
    ventanaRaiz.mainloop()

iniciar()
