# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

import tkinter as tk
from tkinter import messagebox
import random

# CONSTANTES Y DEFINICIONES GLOBALES

PUNTOS_GANAR = 2
PUNTOS_PERDER = -1
MULTIPLICADOR_TRAGAMONEDAS = 2

PASOS_ANIMACION = 15
INTERVALO_ANIMACION_MS = 150

# Diccionario que relaciona cada color de ficha con su valor en dólares
valores_fichas = {
    "Rojo": 10,
    "Azul": 50,
    "Verde": 20,
    "Blanco": 5
}

# Orden de colores que coincide con las posiciones 1, 2, 3 y 4 de la sublista de dinero y fichas
ORDEN_COLORES = ["Rojo", "Azul", "Verde", "Blanco"]

# Matriz de 3 filas por 5 columnas con los símbolos de los tres rodillos de la tragamonedas
MATRIZ_RODILLOS = [
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"],
    ["Cereza", "Limon", "Campana", "Estrella", "Siete"]
]

# Diccionario de combinaciones ganadoras en tragamonedas usando tuplas como llaves
COMBINACIONES_GANADORAS = {
    ("Cereza", "Cereza", "Cereza"): MULTIPLICADOR_TRAGAMONEDAS,
    ("Limon", "Limon", "Limon"): MULTIPLICADOR_TRAGAMONEDAS,
    ("Campana", "Campana", "Campana"): MULTIPLICADOR_TRAGAMONEDAS,
    ("Estrella", "Estrella", "Estrella"): MULTIPLICADOR_TRAGAMONEDAS,
    ("Siete", "Siete", "Siete"): MULTIPLICADOR_TRAGAMONEDAS
}

# Diccionario con los tipos de apuesta en dados y sus multiplicadores
DICCIONARIO_APUESTAS_DADOS = {
    "par": 2,
    "impar": 2,
    "dobles": 5,
    "sumaExacta": 12
}

# Matriz de 2x2 para organizar los botones de opción de apuesta en el juego de dados
MATRIZ_OPCIONES_DADOS = [
    ["par", "impar"],
    ["dobles", "sumaExacta"]
]

# Estructura principal del jugador compartida con E1:
# [(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]
jugador_actual = [
    ("", "", ""),
    [0.0, 0, 0, 0, 0],
    0
]

# Diccionario para guardar las funciones de E1 cuando se conecten
enlaces_e1 = {
    "ventana_sesion": None,
    "ruleta": None,
    "blackjack": None,
    "ranking": None,
    "analisis": None,
    "cerrar_sesion": None,
    "guardar_datos": None
}

# Variables globales para manejar la ventana principal y las ventanas secundarias
ventana_raiz = None
ventana_secundaria = None
mainloop_iniciado = False


# FUNCIONES DE INTEGRACIÓN CON E1 Y ACCESO A DATOS DEL JUGADOR

def conectar_modulo_e1(ventana_sesion_fn=None, ruleta_fn=None, blackjack_fn=None, ranking_fn=None, analisis_fn=None, cerrar_sesion_fn=None, guardar_datos_fn=None):
    """
    Funcionalidad:
    Guardar en el diccionario enlaces_e1 las funciones desarrolladas por E1
    para poder llamarlas desde los botones del menú principal y de los juegos.

    Entrada:
    - ventana_sesion_fn(function): función ventana_sesion de E1.
    - ruleta_fn(function): función ruleta de E1.
    - blackjack_fn(function): función blackjack de E1.
    - ranking_fn(function): función ranking de E1.
    - analisis_fn(function): función analisis de E1.
    - cerrar_sesion_fn(function): función cerrar_sesion de E1.
    - guardar_datos_fn(function): función guardar_datos de E1.

    Salida:
    - enlaces_e1(dict): diccionario actualizado con las funciones conectadas.
    """
    if ventana_sesion_fn != None:
        enlaces_e1["ventana_sesion"] = ventana_sesion_fn
    if ruleta_fn != None:
        enlaces_e1["ruleta"] = ruleta_fn
    if blackjack_fn != None:
        enlaces_e1["blackjack"] = blackjack_fn
    if ranking_fn != None:
        enlaces_e1["ranking"] = ranking_fn
    if analisis_fn != None:
        enlaces_e1["analisis"] = analisis_fn
    if cerrar_sesion_fn != None:
        enlaces_e1["cerrar_sesion"] = cerrar_sesion_fn
    if guardar_datos_fn != None:
        enlaces_e1["guardar_datos"] = guardar_datos_fn
    return enlaces_e1


def cargar_desde_estructura_e1(registro_e1):
    """
    Funcionalidad:
    Cargar en jugador_actual la lista del jugador recibida desde E1
    [(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje],
    asegurando que el dinero sea float y las fichas y el puntaje sean int.

    Entrada:
    - registro_e1(list): lista con los datos del jugador activo.

    Salida:
    - Ninguna.
    """
    global jugador_actual
    if type(registro_e1) != list or len(registro_e1) < 3:
        return

    datos_personales = registro_e1[0]
    saldos = registro_e1[1]
    puntaje = registro_e1[2]

    if type(datos_personales) == tuple and len(datos_personales) >= 3:
        registro_e1[0] = (
            str(datos_personales[0]),
            str(datos_personales[1]),
            str(datos_personales[2])
        )

    if type(saldos) == list and len(saldos) >= 5:
        saldos[0] = float(saldos[0])
        saldos[1] = int(saldos[1])
        saldos[2] = int(saldos[2])
        saldos[3] = int(saldos[3])
        saldos[4] = int(saldos[4])

    registro_e1[2] = int(puntaje)
    jugador_actual = registro_e1


def iniciar_sesion_e2(registro_e1):
    """
    Funcionalidad:
    Recibir desde la ventana de sesión de E1 el registro del jugador activo
    y abrir el menú principal.

    Entrada:
    - registro_e1(list): lista del jugador recibido desde la sesión de E1.

    Salida:
    - Ninguna.
    """
    cargar_desde_estructura_e1(registro_e1)
    menu_principal()


def guardar_datos_e1():
    """
    Funcionalidad:
    Llamar a la función guardar_datos de E1 si ya se encuentra conectada.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    funcion_guardar = enlaces_e1["guardar_datos"]
    if funcion_guardar != None:
        funcion_guardar()


def abrir_funcionalidad_e1(nombre_funcion, descripcion):
    """
    Funcionalidad:
    Ejecutar una función del módulo E1 registrada en enlaces_e1 o mostrar un mensaje
    informativo si todavía no ha sido conectada.

    Entrada:
    - nombre_funcion(str): nombre de la llave en enlaces_e1 ('ruleta', 'blackjack', 'ranking', 'analisis').
    - descripcion(str): nombre visible de la opción seleccionada.

    Salida:
    - Ninguna.
    """
    funcion_e1 = enlaces_e1[nombre_funcion]
    if funcion_e1 != None:
        funcion_e1()
    else:
        messagebox.showwarning(
            "Módulo no disponible",
            "La función '" + descripcion + "' aún no ha sido conectada desde el módulo E1."
        )


# FUNCIONES DE CÁLCULO Y ACTUALIZACIÓN DE SALDOS Y FICHAS

def obtener_indice_color(color_ficha):
    """
    Funcionalidad:
    Obtener la posición que ocupa un color de ficha dentro de la sublista
    jugador_actual[1] ([dinero, rojas, azules, verdes, blancas]).

    Entrada:
    - color_ficha(str): nombre del color ('Rojo', 'Azul', 'Verde' o 'Blanco').

    Salida:
    - indice(int): índice numérico (1 para Rojo, 2 para Azul, 3 para Verde, 4 para Blanco, o -1 si no existe).
    """
    if color_ficha == "Rojo":
        return 1
    elif color_ficha == "Azul":
        return 2
    elif color_ficha == "Verde":
        return 3
    elif color_ficha == "Blanco":
        return 4
    else:
        return -1


def obtener_fichas_color(color_ficha):
    """
    Funcionalidad:
    Consultar cuántas fichas tiene el jugador en un color específico.

    Entrada:
    - color_ficha(str): nombre del color ('Rojo', 'Azul', 'Verde' o 'Blanco').

    Salida:
    - cantidad(int): cantidad de fichas disponibles de ese color.
    """
    indice = obtener_indice_color(color_ficha)
    return int(jugador_actual[1][indice])


def calcular_total_fichas():
    """
    Funcionalidad:
    Sumar la cantidad total de fichas que posee el jugador recorriendo ORDEN_COLORES.

    Entrada:
    - Ninguna.

    Salida:
    - total(int): suma total de fichas del jugador.
    """
    total = 0
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        total = total + obtener_fichas_color(color)
        i = i + 1
    return total


def calcular_valor_monetario_fichas():
    """
    Funcionalidad:
    Calcular el valor total en dólares de todas las fichas que posee el jugador.

    Entrada:
    - Ninguna.

    Salida:
    - valor_total(int): suma en dólares del valor de las fichas del jugador.
    """
    valor_total = 0
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        cantidad = obtener_fichas_color(color)
        valor_total = valor_total + (cantidad * valores_fichas[color])
        i = i + 1
    return valor_total


def obtener_texto_desglose_fichas():
    """
    Funcionalidad:
    Generar un texto con la cantidad de fichas de cada color y su valor en dólares
    recorriendo ORDEN_COLORES con un ciclo while y usando valores_fichas.

    Entrada:
    - Ninguna.

    Salida:
    - texto(str): cadena con el desglose de fichas Rojas, Azules, Verdes y Blancas.
    """
    nombres_plurales = {
        "Rojo": "Rojas",
        "Azul": "Azules",
        "Verde": "Verdes",
        "Blanco": "Blancas"
    }
    texto = ""
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        etiqueta = nombres_plurales[color]
        valor = valores_fichas[color]
        cantidad = obtener_fichas_color(color)
        texto = texto + etiqueta + " ($" + str(valor) + "): " + str(cantidad)
        if i < len(ORDEN_COLORES) - 1:
            texto = texto + "  |  "
        i = i + 1
    return texto


def modificar_fichas_juego(cambio, color_ficha):
    """
    Funcionalidad:
    Sumar o descontar fichas del color seleccionado directamente sobre la estructura
    jugador_actual[1].

    Entrada:
    - cambio(int): cantidad de fichas a sumar (positivo) o descontar (negativo).
    - color_ficha(str): color de la ficha ('Rojo', 'Azul', 'Verde' o 'Blanco').

    Salida:
    - total_actualizado(int): cantidad total de fichas del jugador luego del cambio.
    """
    indice = obtener_indice_color(color_ficha)
    jugador_actual[1][indice] = int(jugador_actual[1][indice]) + int(cambio)
    return calcular_total_fichas()


def liquidar_resultado_apuesta(apuesta, color_ficha, gano, multiplicador):
    """
    Funcionalidad:
    Acreditar las fichas ganadas cuando el jugador acierta (apuesta * multiplicador),
    actualizar el puntaje sumando PUNTOS_GANAR o PUNTOS_PERDER y guardar los datos.

    Entrada:
    - apuesta(int): cantidad de fichas apostadas al inicio de la jugada.
    - color_ficha(str): color de las fichas apostadas.
    - gano(bool): True si el jugador ganó la jugada, False si perdió.
    - multiplicador(int): multiplicador de premio según el juego.

    Salida:
    - resultado_liquidacion(tuple): tupla (pago_total, ganancia_neta).
    """
    if gano:
        pago_total = apuesta * multiplicador
        ganancia_neta = pago_total - apuesta
        modificar_fichas_juego(pago_total, color_ficha)
        jugador_actual[2] = int(jugador_actual[2]) + PUNTOS_GANAR
    else:
        pago_total = 0
        ganancia_neta = -apuesta
        jugador_actual[2] = int(jugador_actual[2]) + PUNTOS_PERDER

    guardar_datos_e1()
    return (pago_total, ganancia_neta)


# FUNCIONES AUXILIARES DE VALIDACIÓN

def validar_entero_positivo(texto, nombre_campo):
    """
    Funcionalidad:
    Validar que el texto ingresado contenga solo dígitos y sea un entero mayor que cero.

    Entrada:
    - texto(str): texto escrito por el usuario en el campo de entrada.
    - nombre_campo(str): nombre del campo para mostrar en el mensaje de error.

    Salida:
    - resultado(tuple): tupla (es_valido(bool), numero(int), mensaje_error(str)).
    """
    texto_limpio = str(texto).strip()
    if texto_limpio == "":
        return (False, 0, "El campo '" + nombre_campo + "' no puede estar vacío.")

    if not texto_limpio.isdigit():
        return (False, 0, "En '" + nombre_campo + "' debes ingresar únicamente números enteros positivos.")

    try:
        numero = int(texto_limpio)
    except ValueError:
        return (False, 0, "En '" + nombre_campo + "' debes ingresar un número entero válido.")

    if numero <= 0:
        return (False, 0, "El valor de '" + nombre_campo + "' debe ser mayor que cero.")

    return (True, numero, "")


def validar_entero_no_negativo(texto, nombre_campo):
    """
    Funcionalidad:
    Validar que el texto ingresado contenga solo dígitos y sea un entero mayor o igual a cero.

    Entrada:
    - texto(str): texto escrito por el usuario.
    - nombre_campo(str): nombre del campo que se está validando.

    Salida:
    - resultado(tuple): tupla (es_valido(bool), numero(int), mensaje_error(str)).
    """
    texto_limpio = str(texto).strip()
    if texto_limpio == "":
        return (False, 0, "La cantidad para " + nombre_campo + " no puede estar vacía (usa 0 si no deseas elegir).")

    if not texto_limpio.isdigit():
        return (False, 0, "La cantidad para " + nombre_campo + " debe contener únicamente números enteros.")

    try:
        numero = int(texto_limpio)
    except ValueError:
        return (False, 0, "La cantidad para " + nombre_campo + " debe ser un número entero válido.")

    return (True, numero, "")


def validar_apuesta_por_color(texto_apuesta, color_ficha):
    """
    Funcionalidad:
    Verificar que la cantidad apostada sea un entero positivo y que el jugador tenga
    suficientes fichas del color elegido.

    Entrada:
    - texto_apuesta(str): cantidad escrita en el campo de apuesta.
    - color_ficha(str): color de ficha seleccionado.

    Salida:
    - resultado(tuple): tupla (es_valida(bool), cantidad(int)).
    """
    es_valido, apuesta, mensaje = validar_entero_positivo(texto_apuesta, "fichas a apostar")
    if not es_valido:
        messagebox.showwarning("Apuesta inválida", mensaje)
        return (False, 0)

    disponibles_color = obtener_fichas_color(color_ficha)
    if apuesta > disponibles_color:
        messagebox.showwarning(
            "Fichas insuficientes",
            "Intentas apostar " + str(apuesta) + " ficha(s) de color " + color_ficha +
            ", pero solo tienes " + str(disponibles_color) + " disponible(s) de ese color."
        )
        return (False, 0)

    return (True, apuesta)


# LÓGICA DE JUEGOS Y OPERACIONES DE FICHAS

def avanzar_indices_rodillos(indices_actuales):
    """
    Funcionalidad:
    Avanzar en una posición el índice de cada uno de los tres rodillos dentro de
    MATRIZ_RODILLOS, volviendo a 0 al llegar al final de cada fila.

    Entrada:
    - indices_actuales(list): lista de tres enteros con la columna actual de cada rodillo.

    Salida:
    - simbolos(list): lista con los tres símbolos correspondientes a las nuevas posiciones.
    """
    simbolos = []
    fila = 0
    while fila < 3:
        siguiente_columna = indices_actuales[fila] + 1
        if siguiente_columna >= len(MATRIZ_RODILLOS[fila]):
            siguiente_columna = 0
        indices_actuales[fila] = siguiente_columna
        simbolos.append(MATRIZ_RODILLOS[fila][siguiente_columna])
        fila = fila + 1
    return simbolos


def evaluar_resultado_tragamonedas(simbolos_finales, apuesta, color_ficha):
    """
    Funcionalidad:
    Revisar si la tupla de tres símbolos finales está en COMBINACIONES_GANADORAS,
    actualizar fichas y puntos y devolver el mensaje de resultado.

    Entrada:
    - simbolos_finales(tuple): tupla con los tres símbolos obtenidos al detenerse los rodillos.
    - apuesta(int): cantidad de fichas apostadas.
    - color_ficha(str): color de las fichas apostadas.

    Salida:
    - resultado(tuple): tupla (gano(bool), mensaje(str), color_texto(str)).
    """
    if simbolos_finales in COMBINACIONES_GANADORAS:
        multiplicador = COMBINACIONES_GANADORAS[simbolos_finales]
        pago_total, ganancia_neta = liquidar_resultado_apuesta(
            apuesta, color_ficha, True, multiplicador
        )
        mensaje = (
            "¡GANASTE! Salió " + simbolos_finales[0] + " en los 3 rodillos.\n" +
            "Recibes un pago de " + str(pago_total) + " ficha(s) " + color_ficha +
            " (ganancia neta: +" + str(ganancia_neta) + ") y sumaste +" + str(PUNTOS_GANAR) + " puntos."
        )
        return (True, mensaje, "#80ed99")
    else:
        liquidar_resultado_apuesta(apuesta, color_ficha, False, 0)
        mensaje = (
            "Perdiste la jugada (" + simbolos_finales[0] + " - " +
            simbolos_finales[1] + " - " + simbolos_finales[2] + ").\n" +
            "Perdiste las " + str(apuesta) + " ficha(s) " + color_ficha +
            " apostadas y se restó " + str(abs(PUNTOS_PERDER)) + " punto."
        )
        return (False, mensaje, "#ffadad")


def generar_tirada_dados():
    """
    Funcionalidad:
    Generar dos números aleatorios entre 1 y 6 correspondientes a los dos dados
    y devolverlos en una tupla.

    Entrada:
    - Ninguna.

    Salida:
    - resultado_tirada(tuple): tupla (dado_1(int), dado_2(int)).
    """
    dado_1 = random.randint(1, 6)
    dado_2 = random.randint(1, 6)
    return (dado_1, dado_2)


def verificar_acierto_dados(resultado_tirada, tipo_apuesta, numero_elegido):
    """
    Funcionalidad:
    Comprobar si los dos dados obtenidos cumplen con el tipo de apuesta elegido.

    Entrada:
    - resultado_tirada(tuple): tupla (dado_1, dado_2) con los valores obtenidos.
    - tipo_apuesta(str): tipo de apuesta ('par', 'impar', 'dobles' o 'sumaExacta').
    - numero_elegido(int): número del 2 al 12 elegido cuando la apuesta es 'sumaExacta'.

    Salida:
    - acierto(bool): True si acertó la apuesta, False en caso contrario.
    """
    suma_dados = resultado_tirada[0] + resultado_tirada[1]
    if tipo_apuesta == "sumaExacta":
        return suma_dados == numero_elegido
    elif tipo_apuesta == "par":
        return (suma_dados % 2) == 0
    elif tipo_apuesta == "impar":
        return (suma_dados % 2) != 0
    elif tipo_apuesta == "dobles":
        return resultado_tirada[0] == resultado_tirada[1]
    else:
        return False


def ejecutar_jugada_dados(apuesta, color_ficha, tipo_apuesta, numero_elegido):
    """
    Funcionalidad:
    Realizar una jugada de dados descontando la apuesta inicial, lanzando los dos dados,
    verificando si hubo acierto y actualizando las fichas y los puntos.

    Entrada:
    - apuesta(int): cantidad de fichas apostadas.
    - color_ficha(str): color de ficha seleccionado.
    - tipo_apuesta(str): tipo de apuesta ('par', 'impar', 'dobles', 'sumaExacta').
    - numero_elegido(int): número elegido para suma exacta (2 a 12).

    Salida:
    - resumen(tuple): tupla (resultado_tirada(tuple), suma_dados(int), mensaje(str), color_texto(str)).
    """
    modificar_fichas_juego(-apuesta, color_ficha)
    resultado_tirada = generar_tirada_dados()
    suma_dados = resultado_tirada[0] + resultado_tirada[1]
    gano = verificar_acierto_dados(resultado_tirada, tipo_apuesta, numero_elegido)
    multiplicador = DICCIONARIO_APUESTAS_DADOS[tipo_apuesta]

    pago_total, ganancia_neta = liquidar_resultado_apuesta(
        apuesta, color_ficha, gano, multiplicador
    )

    if gano:
        mensaje = (
            "¡Acertaste en '" + tipo_apuesta + "' (x" + str(multiplicador) + ")! " +
            "Recibes un pago de " + str(pago_total) + " ficha(s) " + color_ficha +
            " (ganancia neta: +" + str(ganancia_neta) + ") y +" + str(PUNTOS_GANAR) + " puntos."
        )
        color_texto = "#80ed99"
    else:
        mensaje = (
            "No acertaste en '" + tipo_apuesta + "'. Perdiste las " + str(apuesta) +
            " ficha(s) " + color_ficha + " apostadas y se restó " + str(abs(PUNTOS_PERDER)) + " punto."
        )
        color_texto = "#ffadad"

    return (resultado_tirada, suma_dados, mensaje, color_texto)


def calcular_totales_operacion_fichas(cantidades):
    """
    Funcionalidad:
    Calcular el monto total en dólares (float) y la cantidad total de fichas (int)
    a partir de las cantidades seleccionadas por color.

    Entrada:
    - cantidades(dict): diccionario con la cantidad entera elegida para cada color.

    Salida:
    - totales(tuple): tupla (monto_total(float), total_fichas(int)).
    """
    monto_total = 0.0
    total_fichas = 0
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        cantidad = int(cantidades[color])
        monto_total = monto_total + float(cantidad * valores_fichas[color])
        total_fichas = total_fichas + cantidad
        i = i + 1
    return (monto_total, total_fichas)


def validar_disponibilidad_canje(cantidades):
    """
    Funcionalidad:
    Verificar que el jugador tenga suficientes fichas de cada color antes de canjearlas.

    Entrada:
    - cantidades(dict): diccionario con las fichas a canjear por cada color.

    Salida:
    - validacion(tuple): tupla (es_valido(bool), mensaje_error(str)).
    """
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        cantidad = cantidades[color]
        poseidas = obtener_fichas_color(color)
        if cantidad > poseidas:
            mensaje = (
                "No puedes canjear " + str(cantidad) + " ficha(s) de color " + color +
                " porque solo posees " + str(poseidas) + "."
            )
            return (False, mensaje)
        i = i + 1
    return (True, "")


def aplicar_compra_fichas(cantidades, costo_total):
    """
    Funcionalidad:
    Restar el costo total del dinero del jugador (manteniendo float), sumar las fichas
    compradas en cada color y guardar los datos.

    Entrada:
    - cantidades(dict): fichas compradas de cada color.
    - costo_total(float): costo total en dólares.

    Salida:
    - Ninguna.
    """
    jugador_actual[1][0] = float(jugador_actual[1][0] - float(costo_total))
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        indice = obtener_indice_color(color)
        jugador_actual[1][indice] = int(jugador_actual[1][indice]) + int(cantidades[color])
        i = i + 1
    guardar_datos_e1()


def aplicar_canje_fichas(cantidades, dinero_recibir):
    """
    Funcionalidad:
    Sumar el dinero recibido al saldo del jugador (manteniendo float), restar las fichas
    canjeadas en cada color y guardar los datos.

    Entrada:
    - cantidades(dict): fichas canjeadas de cada color.
    - dinero_recibir(float): dinero en dólares acreditado al jugador.

    Salida:
    - Ninguna.
    """
    jugador_actual[1][0] = float(jugador_actual[1][0] + float(dinero_recibir))
    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        indice = obtener_indice_color(color)
        jugador_actual[1][indice] = int(jugador_actual[1][indice]) - int(cantidades[color])
        i = i + 1
    guardar_datos_e1()


# FUNCIONES AUXILIARES DE INTERFAZ GRÁFICA (TKINTER)

def crear_titulo_ventana(ventana_padre, texto_titulo, tamano=16, pady=8):
    """
    Funcionalidad:
    Crear y mostrar el título principal de una ventana.

    Entrada:
    - ventana_padre(tk.Misc): ventana donde se colocará el título.
    - texto_titulo(str): texto del título.
    - tamano(int): tamaño de la letra.
    - pady(int): espacio vertical.

    Salida:
    - etiqueta_titulo(tk.Label): etiqueta creada.
    """
    etiqueta_titulo = tk.Label(
        ventana_padre,
        text=texto_titulo,
        font=("Arial", tamano, "bold"),
        bg="#1b4332",
        fg="#ffd166"
    )
    etiqueta_titulo.pack(pady=pady)
    return etiqueta_titulo


def crear_panel_saldo_juego(ventana_padre):
    """
    Funcionalidad:
    Crear las etiquetas que muestran el total de fichas, los puntos y el desglose por colores.

    Entrada:
    - ventana_padre(tk.Misc): ventana donde se colocarán las etiquetas.

    Salida:
    - etiquetas_saldo(tuple): tupla (etiqueta_info(tk.Label), etiqueta_colores(tk.Label)).
    """
    etiqueta_info = tk.Label(
        ventana_padre,
        text="Fichas disponibles: " + str(calcular_total_fichas()) +
             "   |   Puntos: " + str(jugador_actual[2]),
        font=("Arial", 11, "bold"),
        bg="#1b4332",
        fg="white"
    )
    etiqueta_info.pack(pady=2)

    etiqueta_colores = tk.Label(
        ventana_padre,
        text=obtener_texto_desglose_fichas(),
        font=("Arial", 9),
        bg="#1b4332",
        fg="#b7e4c7"
    )
    etiqueta_colores.pack(pady=2)

    return (etiqueta_info, etiqueta_colores)


def actualizar_panel_saldo_juego(etiqueta_info, etiqueta_colores):
    """
    Funcionalidad:
    Actualizar en pantalla el texto de las etiquetas de fichas totales, puntos y colores.

    Entrada:
    - etiqueta_info(tk.Label): etiqueta de fichas totales y puntos.
    - etiqueta_colores(tk.Label): etiqueta de desglose por color.

    Salida:
    - Ninguna.
    """
    etiqueta_info.config(
        text="Fichas disponibles: " + str(calcular_total_fichas()) +
             "   |   Puntos: " + str(jugador_actual[2])
    )
    etiqueta_colores.config(text=obtener_texto_desglose_fichas())


def crear_campo_entrada_apuesta(ventana_padre):
    """
    Funcionalidad:
    Crear un cuadro con etiqueta y campo de texto para escribir la cantidad de fichas a apostar.

    Entrada:
    - ventana_padre(tk.Misc): ventana donde se colocará el campo de apuesta.

    Salida:
    - entrada_apuesta(tk.Entry): campo de texto creado.
    """
    marco_apuesta = tk.Frame(ventana_padre, bg="#1b4332")
    marco_apuesta.pack(pady=4)

    tk.Label(
        marco_apuesta,
        text="Cantidad de fichas a apostar:",
        font=("Arial", 11),
        bg="#1b4332",
        fg="white"
    ).grid(row=0, column=0, padx=5, pady=2)

    entrada_apuesta = tk.Entry(marco_apuesta, font=("Arial", 11), width=10)
    entrada_apuesta.grid(row=0, column=1, padx=5, pady=2)
    entrada_apuesta.insert(0, "1")
    return entrada_apuesta


def crear_boton_estandar(padre, texto, comando, bg_color, fg_color="black", ancho=22, fuente=("Arial", 11, "bold"), pady=6, empaquetar=True):
    """
    Funcionalidad:
    Crear un botón de Tkinter con el estilo visual del casino.

    Entrada:
    - padre(tk.Widget): contenedor donde se colocará el botón.
    - texto(str): texto del botón.
    - comando(function): función que se ejecuta al hacer clic.
    - bg_color(str): color de fondo.
    - fg_color(str): color del texto.
    - ancho(int): ancho del botón.
    - fuente(tuple): fuente del botón.
    - pady(int): espacio vertical.
    - empaquetar(bool): True si se usa pack(), False si se colocará con grid().

    Salida:
    - boton(tk.Button): botón creado.
    """
    boton = tk.Button(
        padre,
        text=texto,
        font=fuente,
        width=ancho,
        bg=bg_color,
        fg=fg_color,
        command=comando
    )
    if empaquetar:
        boton.pack(pady=pady)
    return boton


def crear_selector_color_ficha(ventana_padre):
    """
    Funcionalidad:
    Crear el cuadro con botones de opción (Radiobutton) para elegir el color de ficha al apostar.

    Entrada:
    - ventana_padre(tk.Misc): ventana donde se colocará el selector.

    Salida:
    - resultado(tuple): tupla (color_seleccionado(tk.StringVar), botones_color(list)).
    """
    marco_color = tk.LabelFrame(
        ventana_padre,
        text="Color de ficha para apostar",
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#ffd166",
        padx=8,
        pady=3
    )
    marco_color.pack(pady=4)

    color_seleccionado = tk.StringVar(value="Blanco")
    botones_color = []

    columna_color = 0
    while columna_color < len(ORDEN_COLORES):
        color = ORDEN_COLORES[columna_color]
        rb_color = tk.Radiobutton(
            marco_color,
            text=color + " ($" + str(valores_fichas[color]) + ")",
            variable=color_seleccionado,
            value=color,
            font=("Arial", 9, "bold"),
            bg="#1b4332",
            fg="white",
            selectcolor="#081c15",
            activebackground="#1b4332",
            activeforeground="white"
        )
        rb_color.grid(row=0, column=columna_color, padx=6, pady=2)
        botones_color.append(rb_color)
        columna_color = columna_color + 1

    return (color_seleccionado, botones_color)


def crear_etiquetas_rodillos(marco_padre, simbolos_iniciales):
    """
    Funcionalidad:
    Crear las tres etiquetas blancas que muestran los símbolos de los rodillos en la tragamonedas.

    Entrada:
    - marco_padre(tk.Frame): marco donde se colocarán los tres rodillos.
    - simbolos_iniciales(list): lista con los tres símbolos iniciales.

    Salida:
    - etiquetas(list): lista con las tres etiquetas creadas.
    """
    etiquetas = []
    indice = 0
    while indice < 3:
        etiqueta = tk.Label(
            marco_padre,
            text=simbolos_iniciales[indice],
            font=("Arial", 13, "bold"),
            width=10,
            height=3,
            bg="white",
            fg="black",
            relief="solid",
            bd=2
        )
        etiqueta.grid(row=0, column=indice, padx=8, pady=8)
        etiquetas.append(etiqueta)
        indice = indice + 1
    return etiquetas


def crear_tabla_inventario_fichas(ventana_padre):
    """
    Funcionalidad:
    Crear la tabla que muestra cada color de ficha, su valor en dólares, cuántas tiene
    el jugador y el campo de texto para ingresar la cantidad a comprar o canjear.

    Entrada:
    - ventana_padre(tk.Misc): ventana donde se colocará la tabla.

    Salida:
    - controles_tabla(tuple): tupla (etiquetas_cantidades(dict), entradas_cantidades(dict)).
    """
    marco_tabla = tk.Frame(ventana_padre, bg="#081c15", bd=2, relief="ridge", padx=10, pady=10)
    marco_tabla.pack(pady=10)

    encabezados = ["Color", "Valor ($)", "Tienes", "Cantidad"]
    col_idx = 0
    while col_idx < len(encabezados):
        tk.Label(
            marco_tabla,
            text=encabezados[col_idx],
            font=("Arial", 10, "bold"),
            bg="#081c15",
            fg="#ffd166",
            width=10
        ).grid(row=0, column=col_idx, pady=4)
        col_idx = col_idx + 1

    etiquetas_cantidades = {}
    entradas_cantidades = {}

    i = 0
    while i < len(ORDEN_COLORES):
        color = ORDEN_COLORES[i]
        fila = i + 1
        valor_monetario = valores_fichas[color]
        cantidad_poseida = obtener_fichas_color(color)

        tk.Label(
            marco_tabla,
            text=color,
            font=("Arial", 10, "bold"),
            bg="#081c15",
            fg="white"
        ).grid(row=fila, column=0, pady=5)

        tk.Label(
            marco_tabla,
            text="$" + str(valor_monetario),
            font=("Arial", 10),
            bg="#081c15",
            fg="white"
        ).grid(row=fila, column=1, pady=5)

        lbl_cant = tk.Label(
            marco_tabla,
            text=str(cantidad_poseida),
            font=("Arial", 10, "bold"),
            bg="#081c15",
            fg="#80ed99"
        )
        lbl_cant.grid(row=fila, column=2, pady=5)
        etiquetas_cantidades[color] = lbl_cant

        entrada = tk.Entry(marco_tabla, font=("Arial", 10), width=8, justify="center")
        entrada.insert(0, "0")
        entrada.grid(row=fila, column=3, pady=5, padx=5)
        entradas_cantidades[color] = entrada

        i = i + 1

    return (etiquetas_cantidades, entradas_cantidades)


# ADMINISTRACIÓN DE VENTANAS TKINTER

def asegurar_ventana_raiz():
    """
    Funcionalidad:
    Asegurar que exista una única ventana principal tk.Tk() activa en la aplicación.

    Entrada:
    - Ninguna.

    Salida:
    - ventana_raiz(tk.Tk): ventana raíz principal.
    """
    global ventana_raiz
    if ventana_raiz == None:
        ventana_raiz = tk.Tk()
    return ventana_raiz


def cerrar_aplicacion_completa():
    """
    Funcionalidad:
    Cerrar la ventana secundaria (si existe) y la ventana raíz de Tkinter para finalizar el programa.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    global ventana_raiz, ventana_secundaria, mainloop_iniciado
    if ventana_secundaria != None:
        if ventana_secundaria.winfo_exists():
            ventana_secundaria.destroy()
        ventana_secundaria = None

    if ventana_raiz != None:
        if ventana_raiz.winfo_exists():
            ventana_raiz.destroy()
        ventana_raiz = None

    mainloop_iniciado = False


def preparar_ventana_e2(titulo, geometria, es_principal, funcion_retorno):
    """
    Funcionalidad:
    Preparar la ventana que se va a mostrar en pantalla, usando la ventana raíz tk.Tk()
    para el menú principal y una ventana secundaria tk.Toplevel() para las demás pantallas.

    Entrada:
    - titulo(str): título de la ventana.
    - geometria(str): tamaño de la ventana en formato 'ANCHOxALTO'.
    - es_principal(bool): True si es el menú principal, False si es una ventana secundaria.
    - funcion_retorno(function): función que se ejecuta al cerrar la ventana con la X.

    Salida:
    - ventana(tk.Misc): ventana lista para colocarle los controles.
    """
    global ventana_secundaria

    raiz = asegurar_ventana_raiz()

    if ventana_secundaria != None:
        if ventana_secundaria.winfo_exists():
            ventana_secundaria.destroy()
        ventana_secundaria = None

    if funcion_retorno != None:
        protocolo_cierre = funcion_retorno
    else:
        protocolo_cierre = cerrar_aplicacion_completa

    if es_principal:
        hijos = raiz.winfo_children()
        i = 0
        while i < len(hijos):
            hijos[i].destroy()
            i = i + 1
        raiz.deiconify()
        raiz.title(titulo)
        raiz.geometry(geometria)
        raiz.config(bg="#1b4332")
        raiz.protocol("WM_DELETE_WINDOW", protocolo_cierre)
        return raiz
    else:
        raiz.withdraw()
        secundaria = tk.Toplevel(raiz)
        secundaria.title(titulo)
        secundaria.geometry(geometria)
        secundaria.config(bg="#1b4332")
        secundaria.protocol("WM_DELETE_WINDOW", protocolo_cierre)
        ventana_secundaria = secundaria
        return secundaria


def iniciar_bucle_principal_si_corresponde():
    """
    Funcionalidad:
    Iniciar el mainloop() de la ventana raíz una sola vez.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    global mainloop_iniciado
    raiz = asegurar_ventana_raiz()
    if not mainloop_iniciado:
        mainloop_iniciado = True
        raiz.mainloop()
        mainloop_iniciado = False


def iniciar_aplicacion():
    """
    Funcionalidad:
    Punto de entrada de casino.py (módulo de E2): crea la ventana raíz y abre
    ventana_sesion() si el módulo de E1 fue conectado, o abre menu_principal() en modo de prueba.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    asegurar_ventana_raiz()
    funcion_sesion_e1 = enlaces_e1["ventana_sesion"]
    if funcion_sesion_e1 != None:
        funcion_sesion_e1()
        iniciar_bucle_principal_si_corresponde()
    else:
        menu_principal()


# E2.1. MENÚ PRINCIPAL

def menu_principal():
    """
    Funcionalidad:
    Mostrar el menú principal con el username del jugador y los cinco botones
    obligatorios: Jugar, Fichas, Ranking, Análisis y Cerrar sesión.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    ventana = preparar_ventana_e2("Casino - Menú Principal", "460x460", True, cerrar_aplicacion_completa)

    crear_titulo_ventana(ventana, "CASINO UNIVERSITARIO", tamano=16, pady=15)

    etiqueta_usuario = tk.Label(
        ventana,
        text="Jugador activo: " + str(jugador_actual[0][0]),
        font=("Arial", 12, "bold"),
        bg="#1b4332",
        fg="white"
    )
    etiqueta_usuario.pack(pady=4)

    etiqueta_resumen = tk.Label(
        ventana,
        text="Dinero: $" + str(jugador_actual[1][0]) +
             "   |   Fichas totales: " + str(calcular_total_fichas()) +
             "   |   Puntos: " + str(jugador_actual[2]),
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#d8f3dc"
    )
    etiqueta_resumen.pack(pady=4)

    etiqueta_desglose = tk.Label(
        ventana,
        text=obtener_texto_desglose_fichas(),
        font=("Arial", 9),
        bg="#1b4332",
        fg="#b7e4c7"
    )
    etiqueta_desglose.pack(pady=6)

    def ir_ranking():
        """
        Funcionalidad:
        Abrir la ventana de Ranking de E1.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        abrir_funcionalidad_e1("ranking", "Ranking")

    def ir_analisis():
        """
        Funcionalidad:
        Abrir la ventana de Análisis de E1.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        abrir_funcionalidad_e1("analisis", "Análisis")

    def ir_cerrar_sesion():
        """
        Funcionalidad:
        Guardar los datos del jugador y volver a la ventana de sesión de E1;
        si E1 aún no está conectado, mostrar un aviso sin cerrar la aplicación.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        guardar_datos_e1()
        funcion_cerrar = enlaces_e1["cerrar_sesion"]
        funcion_sesion = enlaces_e1["ventana_sesion"]
        if funcion_cerrar != None:
            funcion_cerrar()
        elif funcion_sesion != None:
            funcion_sesion()
        else:
            messagebox.showwarning(
                "Módulo no disponible",
                "La función 'Cerrar sesión' aún no ha sido conectada desde el módulo E1."
            )

    crear_boton_estandar(ventana, "Jugar", ventana_juegos, "#ffd166")
    crear_boton_estandar(ventana, "Fichas", ventana_fichas, "#ffd166")
    crear_boton_estandar(ventana, "Ranking", ir_ranking, "#f8f9fa", fuente=("Arial", 11))
    crear_boton_estandar(ventana, "Análisis", ir_analisis, "#f8f9fa", fuente=("Arial", 11))
    crear_boton_estandar(ventana, "Cerrar sesión", ir_cerrar_sesion, "#ef476f", fg_color="white", pady=12)

    iniciar_bucle_principal_si_corresponde()


# E2.2. VENTANA DE JUEGOS

def ventana_juegos():
    """
    Funcionalidad:
    Mostrar la ventana de juegos con los botones Ruleta, Tragamonedas, Blackjack y Dados,
    la cantidad de fichas disponibles y el botón para volver al menú principal.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    ventana = preparar_ventana_e2("Casino - Ventana de Juegos", "460x450", False, menu_principal)

    crear_titulo_ventana(ventana, "SALA DE JUEGOS", tamano=16, pady=15)

    etiqueta_fichas = tk.Label(
        ventana,
        text="Fichas disponibles: " + str(calcular_total_fichas()) +
             "  (Valor: $" + str(calcular_valor_monetario_fichas()) + ")",
        font=("Arial", 12, "bold"),
        bg="#1b4332",
        fg="white"
    )
    etiqueta_fichas.pack(pady=4)

    etiqueta_colores = tk.Label(
        ventana,
        text=obtener_texto_desglose_fichas(),
        font=("Arial", 9),
        bg="#1b4332",
        fg="#b7e4c7"
    )
    etiqueta_colores.pack(pady=4)

    etiqueta_puntos = tk.Label(
        ventana,
        text="Puntos acumulados: " + str(jugador_actual[2]),
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#d8f3dc"
    )
    etiqueta_puntos.pack(pady=5)

    def abrir_ruleta():
        """
        Funcionalidad:
        Abrir el juego de Ruleta de E1.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        abrir_funcionalidad_e1("ruleta", "Ruleta")

    def abrir_blackjack():
        """
        Funcionalidad:
        Abrir el juego de Blackjack de E1.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        abrir_funcionalidad_e1("blackjack", "Blackjack")

    crear_boton_estandar(ventana, "Ruleta", abrir_ruleta, "#f8f9fa", fuente=("Arial", 11))
    crear_boton_estandar(ventana, "Tragamonedas", tragamonedas, "#ffd166")
    crear_boton_estandar(ventana, "Blackjack", abrir_blackjack, "#f8f9fa", fuente=("Arial", 11))
    crear_boton_estandar(ventana, "Dados", dados, "#ffd166")
    crear_boton_estandar(
        ventana, "Volver al menú principal", menu_principal, "#adb5bd",
        fuente=("Arial", 10, "bold"), pady=16
    )


# E2.3. TRAGAMONEDAS

def tragamonedas():
    """
    Funcionalidad:
    Mostrar la ventana del juego de tragamonedas de tres rodillos, animar el giro
    recorriendo MATRIZ_RODILLOS y evaluar las combinaciones ganadoras.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    estado_juego = {
        "girando": False,
        "indices": [0, 1, 2],
        "paso": 0,
        "apuesta": 0,
        "color": "Blanco"
    }

    def intentar_salir_tragamonedas():
        """
        Funcionalidad:
        Impedir que el jugador cierre o salga de la ventana mientras los rodillos están girando.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        if estado_juego["girando"]:
            messagebox.showinfo(
                "Giro en curso",
                "No puedes cerrar ni salir mientras los rodillos están girando. Espera a que termine la jugada."
            )
            return
        ventana_juegos()

    ventana = preparar_ventana_e2("Casino - Tragamonedas", "540x580", False, intentar_salir_tragamonedas)

    crear_titulo_ventana(ventana, "JUEGO DE TRAGAMONEDAS", tamano=16, pady=8)
    etiqueta_info, etiqueta_colores = crear_panel_saldo_juego(ventana)

    marco_rodillos = tk.Frame(ventana, bg="#081c15", bd=3, relief="ridge")
    marco_rodillos.pack(pady=8, padx=10)

    simbolos_iniciales = [
        MATRIZ_RODILLOS[0][estado_juego["indices"][0]],
        MATRIZ_RODILLOS[1][estado_juego["indices"][1]],
        MATRIZ_RODILLOS[2][estado_juego["indices"][2]]
    ]
    etiquetas_rodillos = crear_etiquetas_rodillos(marco_rodillos, simbolos_iniciales)

    color_seleccionado, botones_color = crear_selector_color_ficha(ventana)
    entrada_apuesta = crear_campo_entrada_apuesta(ventana)

    etiqueta_resultado = tk.Label(
        ventana,
        text="Selecciona el color de ficha, ingresa tu apuesta y presiona Girar.",
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#ffd166",
        wraplength=480,
        height=2
    )
    etiqueta_resultado.pack(pady=6)

    def cambiar_estado_controles(estado):
        """
        Funcionalidad:
        Habilitar o deshabilitar los botones y entradas mientras los rodillos giran.

        Entrada:
        - estado(str): 'normal' o 'disabled'.

        Salida:
        - Ninguna.
        """
        boton_girar.config(state=estado)
        entrada_apuesta.config(state=estado)
        boton_jugar_otra_vez.config(state=estado)
        boton_volver.config(state=estado)
        i = 0
        while i < len(botones_color):
            botones_color[i].config(state=estado)
            i = i + 1

    def finalizar_giro():
        """
        Funcionalidad:
        Detener el giro, formar la tupla con los tres símbolos finales, evaluar el resultado
        y volver a habilitar los botones.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        if not ventana.winfo_exists():
            return

        indices = estado_juego["indices"]
        simbolos_finales = (
            MATRIZ_RODILLOS[0][indices[0]],
            MATRIZ_RODILLOS[1][indices[1]],
            MATRIZ_RODILLOS[2][indices[2]]
        )

        i = 0
        while i < 3:
            etiquetas_rodillos[i].config(text=simbolos_finales[i])
            i = i + 1

        _, mensaje, color_texto = evaluar_resultado_tragamonedas(
            simbolos_finales, estado_juego["apuesta"], estado_juego["color"]
        )
        etiqueta_resultado.config(text=mensaje, fg=color_texto)

        actualizar_panel_saldo_juego(etiqueta_info, etiqueta_colores)
        estado_juego["girando"] = False
        cambiar_estado_controles("normal")

    def animar_rodillos():
        """
        Funcionalidad:
        Avanzar un paso de animación en los tres rodillos cada INTERVALO_ANIMACION_MS
        milisegundos hasta completar PASOS_ANIMACION pasos.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        if not ventana.winfo_exists():
            return

        if estado_juego["paso"] < PASOS_ANIMACION:
            nuevos_simbolos = avanzar_indices_rodillos(estado_juego["indices"])
            i = 0
            while i < 3:
                etiquetas_rodillos[i].config(text=nuevos_simbolos[i])
                i = i + 1

            estado_juego["paso"] = estado_juego["paso"] + 1
            ventana.after(INTERVALO_ANIMACION_MS, animar_rodillos)
        else:
            finalizar_giro()

    def iniciar_giro():
        """
        Funcionalidad:
        Validar la apuesta, descontar las fichas apostadas e iniciar la animación de los rodillos.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        if estado_juego["girando"]:
            return

        color_ficha = color_seleccionado.get()
        es_valida, apuesta = validar_apuesta_por_color(entrada_apuesta.get(), color_ficha)
        if not es_valida:
            return

        modificar_fichas_juego(-apuesta, color_ficha)
        actualizar_panel_saldo_juego(etiqueta_info, etiqueta_colores)

        estado_juego["indices"] = [
            random.randint(0, len(MATRIZ_RODILLOS[0]) - 1),
            random.randint(0, len(MATRIZ_RODILLOS[1]) - 1),
            random.randint(0, len(MATRIZ_RODILLOS[2]) - 1)
        ]
        estado_juego["paso"] = 0
        estado_juego["apuesta"] = apuesta
        estado_juego["color"] = color_ficha
        estado_juego["girando"] = True

        cambiar_estado_controles("disabled")
        etiqueta_resultado.config(text="Girando los rodillos...", fg="#ffd166")

        animar_rodillos()

    def preparar_nuevo_juego():
        """
        Funcionalidad:
        Reiniciar el campo de apuesta y el mensaje en pantalla para jugar otra vez.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        if estado_juego["girando"]:
            return
        entrada_apuesta.delete(0, tk.END)
        entrada_apuesta.insert(0, "1")
        etiqueta_resultado.config(
            text="Listo para volver a jugar. Elige color, apuesta y presiona Girar.",
            fg="#ffd166"
        )

    boton_girar = crear_boton_estandar(
        ventana, "Girar", iniciar_giro, "#ffd166",
        ancho=18, fuente=("Arial", 12, "bold"), pady=4
    )
    boton_jugar_otra_vez = crear_boton_estandar(
        ventana, "Volver a jugar", preparar_nuevo_juego, "#f8f9fa",
        ancho=22, fuente=("Arial", 10), pady=3
    )
    boton_volver = crear_boton_estandar(
        ventana, "Regresar a ventana de juegos", intentar_salir_tragamonedas, "#adb5bd",
        ancho=24, fuente=("Arial", 10, "bold"), pady=4
    )


# E2.4. DADOS

def dados():
    """
    Funcionalidad:
    Mostrar la ventana del juego de dados permitiendo elegir color y cantidad de fichas,
    seleccionar el tipo de apuesta desde MATRIZ_OPCIONES_DADOS y lanzar los dos dados.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    ventana = preparar_ventana_e2("Casino - Juego de Dados", "550x620", False, ventana_juegos)

    etiquetas_tipos = {
        "par": "Par (pago x2)",
        "impar": "Impar (pago x2)",
        "dobles": "Dobles (pago x5)",
        "sumaExacta": "Suma exacta (pago x12)"
    }

    crear_titulo_ventana(ventana, "JUEGO DE DADOS", tamano=16, pady=6)
    etiqueta_info, etiqueta_colores = crear_panel_saldo_juego(ventana)

    color_seleccionado, _ = crear_selector_color_ficha(ventana)
    entrada_apuesta = crear_campo_entrada_apuesta(ventana)

    marco_tipo = tk.LabelFrame(
        ventana,
        text="Selecciona el tipo de apuesta",
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#ffd166",
        padx=10,
        pady=4
    )
    marco_tipo.pack(pady=4)

    tipo_seleccionado = tk.StringVar(value="par")

    fila_rb = 0
    while fila_rb < len(MATRIZ_OPCIONES_DADOS):
        col_rb = 0
        while col_rb < len(MATRIZ_OPCIONES_DADOS[fila_rb]):
            clave_tipo = MATRIZ_OPCIONES_DADOS[fila_rb][col_rb]
            rb = tk.Radiobutton(
                marco_tipo,
                text=etiquetas_tipos[clave_tipo],
                variable=tipo_seleccionado,
                value=clave_tipo,
                font=("Arial", 10),
                bg="#1b4332",
                fg="white",
                selectcolor="#081c15",
                activebackground="#1b4332",
                activeforeground="white"
            )
            rb.grid(row=fila_rb, column=col_rb, sticky="w", padx=12, pady=2)
            col_rb = col_rb + 1
        fila_rb = fila_rb + 1

    marco_suma = tk.Frame(ventana, bg="#1b4332")
    marco_suma.pack(pady=3)

    tk.Label(
        marco_suma,
        text="Número para Suma exacta (2 al 12):",
        font=("Arial", 10),
        bg="#1b4332",
        fg="white"
    ).grid(row=0, column=0, padx=5)

    entrada_suma_exacta = tk.Entry(marco_suma, font=("Arial", 10), width=6)
    entrada_suma_exacta.grid(row=0, column=1, padx=5)
    entrada_suma_exacta.insert(0, "7")

    etiqueta_dados = tk.Label(
        ventana,
        text="Resultado tirada (tupla): (-, -)",
        font=("Arial", 13, "bold"),
        bg="#081c15",
        fg="white",
        width=32,
        pady=6
    )
    etiqueta_dados.pack(pady=5)

    etiqueta_resultado = tk.Label(
        ventana,
        text="Elige tu apuesta y presiona Lanzar dados.",
        font=("Arial", 10, "bold"),
        bg="#1b4332",
        fg="#ffd166",
        wraplength=480,
        height=2
    )
    etiqueta_resultado.pack(pady=4)

    def lanzar_dados():
        """
        Funcionalidad:
        Validar la apuesta y la suma exacta (si aplica), ejecutar la tirada de dados
        y mostrar la tupla obtenida y el resultado en pantalla.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        color_ficha = color_seleccionado.get()
        es_valida, apuesta = validar_apuesta_por_color(entrada_apuesta.get(), color_ficha)
        if not es_valida:
            return

        tipo = tipo_seleccionado.get()
        numero_elegido = 0

        if tipo == "sumaExacta":
            es_suma_valida, numero_elegido, error_suma = validar_entero_positivo(
                entrada_suma_exacta.get(), "Suma exacta"
            )
            if not es_suma_valida:
                messagebox.showwarning("Suma inválida", error_suma)
                return
            if numero_elegido < 2 or numero_elegido > 12:
                messagebox.showwarning("Suma inválida", "La suma de dos dados debe estar entre 2 y 12.")
                return

        resultado_tirada, suma_dados, mensaje, color_texto = ejecutar_jugada_dados(
            apuesta, color_ficha, tipo, numero_elegido
        )

        etiqueta_dados.config(
            text="Resultado tirada: " + str(resultado_tirada) + "  (Suma: " + str(suma_dados) + ")"
        )
        etiqueta_resultado.config(text=mensaje, fg=color_texto)
        actualizar_panel_saldo_juego(etiqueta_info, etiqueta_colores)

    def jugar_nuevamente():
        """
        Funcionalidad:
        Reiniciar los textos de resultado para realizar una nueva tirada de dados.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        etiqueta_dados.config(text="Resultado tirada (tupla): (-, -)")
        etiqueta_resultado.config(
            text="Listo para otra tirada. Elige tu apuesta y presiona Lanzar dados.",
            fg="#ffd166"
        )

    crear_boton_estandar(
        ventana, "Lanzar dados", lanzar_dados, "#ffd166",
        ancho=20, fuente=("Arial", 11, "bold"), pady=3
    )
    crear_boton_estandar(
        ventana, "Jugar nuevamente", jugar_nuevamente, "#f8f9fa",
        ancho=20, fuente=("Arial", 10), pady=3
    )
    crear_boton_estandar(
        ventana, "Regresar a ventana de juegos", ventana_juegos, "#adb5bd",
        ancho=24, fuente=("Arial", 10, "bold"), pady=4
    )


# E2.5. VENTANA DE FICHAS

def ventana_fichas():
    """
    Funcionalidad:
    Mostrar la ventana de compra y canje de fichas con la tabla de colores y valores,
    permitiendo comprar fichas con dinero o canjear fichas por dinero.

    Entrada:
    - Ninguna.

    Salida:
    - Ninguna.
    """
    ventana = preparar_ventana_e2("Casino - Administración de Fichas", "550x530", False, menu_principal)

    crear_titulo_ventana(ventana, "COMPRA Y CANJE DE FICHAS", tamano=15, pady=10)

    etiqueta_dinero = tk.Label(
        ventana,
        text="Dinero disponible: $" + str(jugador_actual[1][0]) +
             "   |   Total de fichas: " + str(calcular_total_fichas()),
        font=("Arial", 12, "bold"),
        bg="#1b4332",
        fg="white"
    )
    etiqueta_dinero.pack(pady=5)

    etiquetas_cantidades, entradas_cantidades = crear_tabla_inventario_fichas(ventana)

    def refrescar_vista_fichas():
        """
        Funcionalidad:
        Actualizar en pantalla el dinero disponible, las cantidades de fichas por color
        y reiniciar las cajas de texto a 0.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        etiqueta_dinero.config(
            text="Dinero disponible: $" + str(jugador_actual[1][0]) +
                 "   |   Total de fichas: " + str(calcular_total_fichas())
        )
        i = 0
        while i < len(ORDEN_COLORES):
            color = ORDEN_COLORES[i]
            etiquetas_cantidades[color].config(text=str(obtener_fichas_color(color)))
            entradas_cantidades[color].delete(0, tk.END)
            entradas_cantidades[color].insert(0, "0")
            i = i + 1

    def leer_cantidades_ingresadas():
        """
        Funcionalidad:
        Leer y validar las cantidades escritas por el jugador en cada color de ficha.

        Entrada:
        - Ninguna.

        Salida:
        - seleccion(dict): diccionario con las cantidades por color, o None si hubo un dato inválido.
        """
        seleccion = {}
        i = 0
        while i < len(ORDEN_COLORES):
            color = ORDEN_COLORES[i]
            texto = entradas_cantidades[color].get()
            es_valido, numero, mensaje_error = validar_entero_no_negativo(texto, "color " + color)
            if not es_valido:
                messagebox.showwarning("Cantidad inválida", mensaje_error)
                return None
            seleccion[color] = numero
            i = i + 1
        return seleccion

    def comprar_fichas():
        """
        Funcionalidad:
        Validar la compra de fichas, pedir confirmación al jugador y descontar el dinero
        sumando las fichas compradas.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        cantidades = leer_cantidades_ingresadas()
        if cantidades == None:
            return

        costo_total, total_fichas_compra = calcular_totales_operacion_fichas(cantidades)

        if total_fichas_compra <= 0:
            messagebox.showwarning("Compra vacía", "Debes ingresar una cantidad mayor que cero en al menos un color.")
            return

        if costo_total > jugador_actual[1][0]:
            messagebox.showerror(
                "Dinero insuficiente",
                "El costo total es de $" + str(costo_total) +
                " pero solo tienes $" + str(jugador_actual[1][0]) + " disponibles."
            )
            return

        confirmacion = messagebox.askyesno(
            "Confirmar compra de fichas",
            "¿Confirmas la compra de " + str(total_fichas_compra) +
            " ficha(s) por un costo total de $" + str(costo_total) + "?"
        )

        if confirmacion:
            aplicar_compra_fichas(cantidades, costo_total)
            refrescar_vista_fichas()
            messagebox.showinfo("Compra exitosa", "Se compraron las fichas correctamente.")

    def canjear_fichas():
        """
        Funcionalidad:
        Validar el canje de fichas, pedir confirmación al jugador y sumar el dinero
        descontando las fichas canjeadas.

        Entrada:
        - Ninguna.

        Salida:
        - Ninguna.
        """
        cantidades = leer_cantidades_ingresadas()
        if cantidades == None:
            return

        es_valido, error_canje = validar_disponibilidad_canje(cantidades)
        if not es_valido:
            messagebox.showerror("Fichas insuficientes", error_canje)
            return

        dinero_recibir, total_fichas_canje = calcular_totales_operacion_fichas(cantidades)

        if total_fichas_canje <= 0:
            messagebox.showwarning("Canje vacío", "Debes ingresar una cantidad mayor que cero en al menos un color.")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar canje de fichas",
            "¿Confirmas el canje de " + str(total_fichas_canje) +
            " ficha(s) para recibir $" + str(dinero_recibir) + "?"
        )

        if confirmacion:
            aplicar_canje_fichas(cantidades, dinero_recibir)
            refrescar_vista_fichas()
            messagebox.showinfo(
                "Canje exitoso",
                "Se canjearon las fichas y se sumó $" + str(dinero_recibir) + " a tu dinero disponible."
            )

    marco_botones = tk.Frame(ventana, bg="#1b4332")
    marco_botones.pack(pady=10)

    boton_comprar = crear_boton_estandar(
        marco_botones, "Comprar fichas", comprar_fichas, "#ffd166",
        ancho=16, fuente=("Arial", 11, "bold"), empaquetar=False
    )
    boton_comprar.grid(row=0, column=0, padx=8, pady=5)

    boton_canjear = crear_boton_estandar(
        marco_botones, "Canjear fichas", canjear_fichas, "#80ed99",
        ancho=16, fuente=("Arial", 11, "bold"), empaquetar=False
    )
    boton_canjear.grid(row=0, column=1, padx=8, pady=5)

    crear_boton_estandar(
        ventana, "Volver al menú principal", menu_principal, "#adb5bd",
        ancho=24, fuente=("Arial", 10, "bold"), pady=10
    )


if __name__ == "__main__":
    iniciar_aplicacion()
