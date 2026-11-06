# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

import tkinter as tk
from tkinter import messagebox
import random
import pickle
import datos
import sesion

# CONSTANTES Y DEFINICIONES GLOBALES

PUNTOS_GANAR = 2
PUNTOS_PERDER = -1
MULTIPLICADOR_TRAGAMONEDAS = 2

PASOS_ANIMACION = 15
INTERVALO_ANIMACION_MS = 150

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
    "ventana_sesion": False,
    "ruleta": False,
    "blackjack": False,
    "ranking": False,
    "analisis": False,
    "cerrar_sesion": False,
    "guardar_datos": False
}

# Variables globales para manejar la ventana principal y las ventanas secundarias
ventana_raiz = False
ventana_secundaria = False
mainloop_iniciado = False


# FUNCIONES DE INTEGRACIÓN CON E1 Y ACCESO A DATOS DEL JUGADOR

def conectar_modulo_e1(ventana_sesion_fn=False, ruleta_fn=False, blackjack_fn=False, ranking_fn=False, analisis_fn=False, cerrar_sesion_fn=False, guardar_datos_fn=False):
    """
    Funcionalidad:
        Guarda en el diccionario enlaces_e1 las funciones desarrolladas por E1
        para poder llamarlas desde los botones del menú principal y de los juegos.

    Entrada:
        - ventana_sesion_fn(function): Función de la ventana de sesión de E1.
        - ruleta_fn(function): Función del juego de ruleta de E1.
        - blackjack_fn(function): Función del juego de blackjack de E1.
        - ranking_fn(function): Función de la ventana de ranking de E1.
        - analisis_fn(function): Función de la ventana de análisis de E1.
        - cerrar_sesion_fn(function): Función para cerrar la sesión activa de E1.
        - guardar_datos_fn(function): Función para guardar los cambios del jugador de E1.

    Salida:
        - enlaces_e1(dict): Diccionario actualizado con las funciones conectadas de E1.
    """
    if ventana_sesion_fn:
        enlaces_e1["ventana_sesion"] = ventana_sesion_fn
    if ruleta_fn:
        enlaces_e1["ruleta"] = ruleta_fn
    if blackjack_fn:
        enlaces_e1["blackjack"] = blackjack_fn
    if ranking_fn:
        enlaces_e1["ranking"] = ranking_fn
    if analisis_fn:
        enlaces_e1["analisis"] = analisis_fn
    if cerrar_sesion_fn:
        enlaces_e1["cerrar_sesion"] = cerrar_sesion_fn
    if guardar_datos_fn:
        enlaces_e1["guardar_datos"] = guardar_datos_fn
    return enlaces_e1


def limpiar_jugador_actual():
    """
    Funcionalidad:
        Reinicia en memoria los datos de jugador_actual con valores vacíos y en cero
        para evitar que una nueva sesión herede información del jugador anterior.

    Entrada:
        - Ninguna.

    Salida:
        - jugador_actual(list): Lista global del jugador reiniciada con sus valores vacíos.
    """
    global jugador_actual
    jugador_actual = [
        ("", "", ""),
        [0.0, 0, 0, 0, 0],
        0
    ]
    return jugador_actual


def cargar_desde_estructura_e1(registro_e1):
    """
    Funcionalidad:
        Valida y carga en jugador_actual la lista del jugador recibida desde E1
        [(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje],
        asegurando que el registro sea válido y que los tipos numéricos sean float e int.

    Entrada:
        - registro_e1(list): Lista con los datos personales, recursos y puntaje del jugador activo.

    Salida:
        - es_valido(bool): True si el registro es válido y fue cargado, False en caso contrario.
    """
    global jugador_actual
    if type(registro_e1) != list or not datos.validarEstructuraJugador(registro_e1):
        messagebox.showerror(
            "Error al cargar jugador",
            "El registro del jugador recibido es inválido o está incompleto."
        )
        return False

    datos_personales = registro_e1[0]
    saldos = registro_e1[1]
    puntaje = registro_e1[2]

    registro_e1[0] = (
        str(datos_personales[0]).strip(),
        str(datos_personales[1]).strip(),
        str(datos_personales[2]).strip()
    )

    saldos[0] = float(saldos[0])
    saldos[1] = int(saldos[1])
    saldos[2] = int(saldos[2])
    saldos[3] = int(saldos[3])
    saldos[4] = int(saldos[4])

    registro_e1[2] = int(puntaje)
    jugador_actual = registro_e1
    return True


def iniciar_sesion_e2(registro_e1):
    """
    Funcionalidad:
        Recibe desde la ventana de sesión de E1 el registro del jugador activo,
        verifica que se haya cargado válidamente y abre el menú principal.

    Entrada:
        - registro_e1(list): Lista del jugador recibida desde la ventana de sesión de E1.

    Salida:
        - sesion_iniciada(bool): True si se abrió el menú principal, False si el registro fue rechazado.
    """
    if cargar_desde_estructura_e1(registro_e1):
        menu_principal()
        return True
    return False


def guardar_datos_e1():
    """
    Funcionalidad:
        Guarda los datos del jugador activo pasando jugador_actual a la función
        de persistencia conectada en enlaces_e1['guardar_datos'] y notifica si ocurre algún error.

    Entrada:
        - Ninguna.

    Salida:
        - guardado_exitoso(bool): True si el guardado se completó sin errores, False en caso contrario.
    """
    funcion_guardar = enlaces_e1["guardar_datos"]
    if not funcion_guardar:
        return True

    username = str(jugador_actual[0][0]).strip()
    if username == "":
        messagebox.showerror(
            "Error al guardar datos",
            "No hay un jugador activo válido para guardar."
        )
        return False

    try:
        funcion_guardar(jugador_actual)
        return True
    except (ValueError, TypeError, OSError, pickle.UnpicklingError, EOFError) as error:
        messagebox.showerror(
            "Error al guardar datos",
            "No se pudieron guardar los datos del jugador '" + username + "': " + str(error)
        )
        return False


def abrir_ventana_sesion_e1():
    """
    Funcionalidad:
        Abre la ventana de sesión de E1 dentro de una ventana Toplevel hija
        de la única ventana raíz tk.Tk() y la conecta con iniciar_sesion_e2.

    Entrada:
        - Ninguna.

    Salida:
        - ventana_login(Toplevel): Ventana secundaria con la interfaz de sesión de E1.
    """
    ventana_login = preparar_ventana_e2(
        "Casino - Sesion", "430x440", False, cerrar_aplicacion_completa
    )
    return sesion.crearVentanaSesion(iniciar_sesion_e2, ventana_login)


def cerrar_sesion_e1():
    """
    Funcionalidad:
        Limpia de la memoria los datos del jugador anterior y abre nuevamente
        la ventana de inicio de sesión de E1 sin crear una segunda ventana raíz.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Limpia el jugador activo y abre la ventana de sesión sin retornar un valor.
    """
    limpiar_jugador_actual()
    abrir_ventana_sesion_e1()


conectar_modulo_e1(
    ventana_sesion_fn=abrir_ventana_sesion_e1,
    cerrar_sesion_fn=cerrar_sesion_e1,
    guardar_datos_fn=datos.guardarCambiosJugador
)


def abrir_funcionalidad_e1(nombre_funcion, descripcion):
    """
    Funcionalidad:
        Ejecuta una función del módulo E1 registrada en enlaces_e1 o muestra un mensaje
        informativo si todavía no ha sido conectada.

    Entrada:
        - nombre_funcion(str): Nombre de la llave de la funcionalidad en el diccionario enlaces_e1.
        - descripcion(str): Nombre visible de la opción seleccionada por el jugador.

    Salida:
        - Ninguna: Ejecuta la función conectada de E1 o muestra un aviso informativo sin retornar un valor.
    """
    funcion_e1 = enlaces_e1[nombre_funcion]
    if funcion_e1:
        funcion_e1()
    else:
        messagebox.showwarning(
            "Módulo no disponible",
            "La función '" + descripcion + "' aún no ha sido conectada desde el módulo E1."
        )


# FUNCIONES DE CÁLCULO Y ACTUALIZACIÓN DE SALDOS Y FICHAS

def obtener_llave_color_e1(color_ficha):
    """
    Funcionalidad:
        Convierte el nombre de un color de ficha ('Rojo', 'Azul', 'Verde', 'Blanco')
        a la llave correspondiente del diccionario compartido datos.VALOR_FICHAS ('rojas', 'azules', 'verdes', 'blancas').

    Entrada:
        - color_ficha(str): Nombre del color de ficha en singular.

    Salida:
        - llave_color(str): Llave en plural correspondiente al color en el diccionario de datos.
    """
    if color_ficha == "Rojo":
        return "rojas"
    elif color_ficha == "Azul":
        return "azules"
    elif color_ficha == "Verde":
        return "verdes"
    elif color_ficha == "Blanco":
        return "blancas"
    else:
        return ""


def obtener_valor_ficha(color_ficha):
    """
    Funcionalidad:
        Consulta el valor en dólares de un color de ficha directamente desde el
        diccionario unificado datos.VALOR_FICHAS.

    Entrada:
        - color_ficha(str): Nombre del color de ficha a consultar.

    Salida:
        - valor(int): Valor unitario en dólares de la ficha del color indicado.
    """
    llave = obtener_llave_color_e1(color_ficha)
    return int(datos.VALOR_FICHAS[llave])


def obtener_indice_color(color_ficha):
    """
    Funcionalidad:
        Obtiene la posición que ocupa un color de ficha dentro de la sublista
        jugador_actual[1] ([dinero, rojas, azules, verdes, blancas]).

    Entrada:
        - color_ficha(str): Nombre del color de ficha a consultar.

    Salida:
        - indice(int): Posición numérica del color en la sublista de recursos o -1 si no existe.
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
        Consulta cuántas fichas tiene el jugador en un color específico.

    Entrada:
        - color_ficha(str): Nombre del color de ficha a consultar.

    Salida:
        - cantidad(int): Cantidad de fichas disponibles del color indicado.
    """
    indice = obtener_indice_color(color_ficha)
    return int(jugador_actual[1][indice])


def calcular_total_fichas():
    """
    Funcionalidad:
        Suma la cantidad total de fichas que posee el jugador recorriendo ORDEN_COLORES.

    Entrada:
        - Ninguna.

    Salida:
        - total(int): Suma total de fichas de todos los colores del jugador activo.
    """
    total = 0
    for color in ORDEN_COLORES:
        total = total + obtener_fichas_color(color)
    return total


def calcular_valor_monetario_fichas():
    """
    Funcionalidad:
        Calcula el valor total en dólares de todas las fichas que posee el jugador
        consultando el diccionario compartido datos.VALOR_FICHAS.

    Entrada:
        - Ninguna.

    Salida:
        - valor_total(int): Suma en dólares del valor de todas las fichas del jugador activo.
    """
    valor_total = 0
    for color in ORDEN_COLORES:
        cantidad = obtener_fichas_color(color)
        valor_total = valor_total + (cantidad * obtener_valor_ficha(color))
    return valor_total


def obtener_texto_desglose_fichas():
    """
    Funcionalidad:
        Genera un texto con la cantidad de fichas de cada color y su valor en dólares
        recorriendo ORDEN_COLORES y consultando datos.VALOR_FICHAS.

    Entrada:
        - Ninguna.

    Salida:
        - texto(str): Cadena formateada con la cantidad y el valor en dólares de cada color de ficha.
    """
    nombres_plurales = {
        "Rojo": "Rojas",
        "Azul": "Azules",
        "Verde": "Verdes",
        "Blanco": "Blancas"
    }
    texto = ""
    for i in range(len(ORDEN_COLORES)):
        color = ORDEN_COLORES[i]
        etiqueta = nombres_plurales[color]
        valor = obtener_valor_ficha(color)
        cantidad = obtener_fichas_color(color)
        texto = texto + etiqueta + " ($" + str(valor) + "): " + str(cantidad)
        if i < len(ORDEN_COLORES) - 1:
            texto = texto + "  |  "
    return texto


def modificar_fichas_juego(cambio, color_ficha):
    """
    Funcionalidad:
        Suma o descuenta fichas del color seleccionado directamente sobre la estructura
        jugador_actual[1].

    Entrada:
        - cambio(int): Cantidad de fichas a sumar o descontar en el color seleccionado.
        - color_ficha(str): Color de la ficha sobre el cual se aplica el cambio.

    Salida:
        - total_fichas(int): Cantidad total de fichas del jugador después de aplicar el cambio.
    """
    indice = obtener_indice_color(color_ficha)
    jugador_actual[1][indice] = int(jugador_actual[1][indice]) + int(cambio)
    return calcular_total_fichas()


def liquidar_resultado_apuesta(apuesta, color_ficha, gano, multiplicador):
    """
    Funcionalidad:
        Acredita las fichas ganadas cuando el jugador acierta (apuesta * multiplicador),
        actualiza el puntaje sumando PUNTOS_GANAR o PUNTOS_PERDER y guarda los datos en el archivo jugadores.

    Entrada:
        - apuesta(int): Cantidad de fichas apostadas al inicio de la jugada.
        - color_ficha(str): Color de las fichas apostadas en la jugada.
        - gano(bool): True si el jugador acertó la jugada, False si perdió.
        - multiplicador(int): Multiplicador de premio correspondiente al juego.

    Salida:
        - resultado(tuple): Tupla con el pago total acreditado y la ganancia neta de la jugada.
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

def validar_entero(texto, nombre_campo, permitir_cero=False):
    """
    Funcionalidad:
        Valida que el texto ingresado contenga únicamente dígitos decimales mediante isdecimal()
        y represente un número entero mayor que cero o mayor o igual a cero según permitir_cero.

    Entrada:
        - texto(str): Texto escrito por el usuario en el campo de entrada.
        - nombre_campo(str): Nombre descriptivo del campo para los mensajes de validación.
        - permitir_cero(bool): True si se admite el valor cero, False si debe ser mayor que cero.

    Salida:
        - resultado(tuple): Tupla con el indicador de validez, el número entero convertido y el mensaje de error.
    """
    texto_limpio = str(texto).strip()
    if texto_limpio == "":
        if permitir_cero:
            return (False, 0, "La cantidad para " + nombre_campo + " no puede estar vacía (usa 0 si no deseas elegir).")
        return (False, 0, "El campo '" + nombre_campo + "' no puede estar vacío.")

    if not texto_limpio.isdecimal():
        if permitir_cero:
            return (False, 0, "La cantidad para " + nombre_campo + " debe contener únicamente números enteros.")
        return (False, 0, "En '" + nombre_campo + "' debes ingresar únicamente números enteros positivos.")

    numero = int(texto_limpio)

    if not permitir_cero and numero <= 0:
        return (False, 0, "El valor de '" + nombre_campo + "' debe ser mayor que cero.")

    return (True, numero, "")


def validar_apuesta_por_color(texto_apuesta, color_ficha):
    """
    Funcionalidad:
        Verifica que la cantidad apostada sea un entero positivo y que el jugador tenga
        suficientes fichas del color elegido.

    Entrada:
        - texto_apuesta(str): Cantidad escrita por el jugador en el campo de apuesta.
        - color_ficha(str): Color de ficha seleccionado para realizar la apuesta.

    Salida:
        - resultado(tuple): Tupla con el indicador de validez y la cantidad entera de fichas apostadas.
    """
    es_valido, apuesta, mensaje = validar_entero(texto_apuesta, "fichas a apostar", False)
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
        Avanza en una posición el índice de cada uno de los tres rodillos dentro de
        MATRIZ_RODILLOS, volviendo a 0 al llegar al final de cada fila.

    Entrada:
        - indices_actuales(list): Lista de tres enteros con la columna actual de cada rodillo.

    Salida:
        - simbolos(list): Lista con los tres símbolos correspondientes a las nuevas posiciones.
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
        Revisa si la tupla de tres símbolos finales está en COMBINACIONES_GANADORAS,
        actualiza fichas y puntos y devuelve el mensaje de resultado.

    Entrada:
        - simbolos_finales(tuple): Tupla con los tres símbolos obtenidos al detenerse los rodillos.
        - apuesta(int): Cantidad de fichas apostadas en el giro.
        - color_ficha(str): Color de las fichas apostadas en el giro.

    Salida:
        - resultado(tuple): Tupla con el indicador de victoria, el mensaje del resultado y el color del texto.
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
        Genera dos números aleatorios entre 1 y 6 correspondientes a los dos dados
        y los devuelve en una tupla.

    Entrada:
        - Ninguna.

    Salida:
        - tirada(tuple): Tupla con el valor del primer dado y del segundo dado.
    """
    dado_1 = random.randint(1, 6)
    dado_2 = random.randint(1, 6)
    return (dado_1, dado_2)


def verificar_acierto_dados(resultado_tirada, tipo_apuesta, numero_elegido):
    """
    Funcionalidad:
        Comprueba si los dos dados obtenidos cumplen con el tipo de apuesta elegido.

    Entrada:
        - resultado_tirada(tuple): Tupla con los valores de los dos dados lanzados.
        - tipo_apuesta(str): Modalidad de apuesta ('par', 'impar', 'dobles' o 'sumaExacta').
        - numero_elegido(int): Suma objetivo entre 2 y 12, usada solo en sumaExacta.

    Salida:
        - acierto(bool): True si el lanzamiento cumple la condición de la apuesta, False en caso contrario.
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
        Realiza una jugada de dados descontando la apuesta inicial, lanzando los dos dados,
        verificando si hubo acierto y actualizando las fichas y los puntos.

    Entrada:
        - apuesta(int): Cantidad de fichas apostadas en el lanzamiento.
        - color_ficha(str): Color de las fichas apostadas.
        - tipo_apuesta(str): Modalidad de apuesta elegida por el jugador.
        - numero_elegido(int): Suma elegida entre 2 y 12 cuando es sumaExacta.

    Salida:
        - resultado(tuple): Tupla con la tirada de los dados, su suma, el mensaje y el color del texto.
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
        Calcula el monto total en dólares (float) y la cantidad total de fichas (int)
        a partir de las cantidades seleccionadas por color consultando datos.VALOR_FICHAS.

    Entrada:
        - cantidades(dict): Diccionario con la cantidad de fichas por cada color.

    Salida:
        - totales(tuple): Tupla con el monto total en dólares y la cantidad total de fichas.
    """
    monto_total = 0.0
    total_fichas = 0
    for color in ORDEN_COLORES:
        cantidad = int(cantidades[color])
        monto_total = monto_total + float(cantidad * obtener_valor_ficha(color))
        total_fichas = total_fichas + cantidad
    return (monto_total, total_fichas)


def validar_disponibilidad_canje(cantidades):
    """
    Funcionalidad:
        Verifica que el jugador tenga suficientes fichas de cada color antes de canjearlas.

    Entrada:
        - cantidades(dict): Diccionario con las cantidades de fichas a canjear por cada color.

    Salida:
        - validacion(tuple): Tupla con el indicador booleano de disponibilidad y el mensaje de error.
    """
    for color in ORDEN_COLORES:
        cantidad = cantidades[color]
        poseidas = obtener_fichas_color(color)
        if cantidad > poseidas:
            mensaje = (
                "No puedes canjear " + str(cantidad) + " ficha(s) de color " + color +
                " porque solo posees " + str(poseidas) + "."
            )
            return (False, mensaje)
    return (True, "")


def convertir_cantidades_a_formato_e1(cantidades):
    """
    Funcionalidad:
        Convierte un diccionario de cantidades con llaves ('Rojo', 'Azul', 'Verde', 'Blanco')
        al formato de llaves de datos.VALOR_FICHAS ('rojas', 'azules', 'verdes', 'blancas').

    Entrada:
        - cantidades(dict): Diccionario con las cantidades por color en singular de la ventana de fichas.

    Salida:
        - cantidades_e1(dict): Diccionario con las llaves de colores en plural requeridas por el módulo de datos.
    """
    cantidades_e1 = {}
    for color in ORDEN_COLORES:
        llave_e1 = obtener_llave_color_e1(color)
        cantidades_e1[llave_e1] = int(cantidades[color])
    return cantidades_e1


# FUNCIONES AUXILIARES DE INTERFAZ GRÁFICA (TKINTER)

def crear_titulo_ventana(ventana_padre, texto_titulo, tamano=16, pady=8):
    """
    Funcionalidad:
        Crea y muestra el título principal de una ventana.

    Entrada:
        - ventana_padre(Widget): Ventana donde se colocará el título.
        - texto_titulo(str): Texto que mostrará la etiqueta del título.
        - tamano(int): Tamaño de la fuente del título.
        - pady(int): Espacio vertical exterior de la etiqueta.

    Salida:
        - etiqueta_titulo(Label): Etiqueta de título creada y empaquetada en la ventana.
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
        Crea las etiquetas que muestran el total de fichas, los puntos y el desglose por colores.

    Entrada:
        - ventana_padre(Widget): Ventana donde se colocarán las etiquetas de saldo.

    Salida:
        - etiquetas(tuple): Tupla con la etiqueta de resumen general y la etiqueta de desglose por color.
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
        Actualiza en pantalla el texto de las etiquetas de fichas totales, puntos y colores.

    Entrada:
        - etiqueta_info(Label): Etiqueta que muestra el total de fichas y los puntos.
        - etiqueta_colores(Label): Etiqueta que muestra el desglose de fichas por color.

    Salida:
        - Ninguna: Actualiza el texto de ambas etiquetas sin retornar un valor.
    """
    etiqueta_info.config(
        text="Fichas disponibles: " + str(calcular_total_fichas()) +
             "   |   Puntos: " + str(jugador_actual[2])
    )
    etiqueta_colores.config(text=obtener_texto_desglose_fichas())


def crear_campo_entrada_apuesta(ventana_padre):
    """
    Funcionalidad:
        Crea un cuadro con etiqueta y campo de texto para escribir la cantidad de fichas a apostar.

    Entrada:
        - ventana_padre(Widget): Ventana donde se colocará el campo de entrada de apuesta.

    Salida:
        - campo_apuesta(Entry): Campo de texto creado para ingresar la cantidad de fichas a apostar.
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
        Crea un botón de Tkinter con el estilo visual del casino.

    Entrada:
        - padre(Widget): Contenedor donde se colocará el botón.
        - texto(str): Texto visible dentro del botón.
        - comando(function): Función que se ejecuta al presionar el botón.
        - bg_color(str): Color de fondo del botón.
        - fg_color(str): Color del texto del botón.
        - ancho(int): Ancho del botón en caracteres.
        - fuente(tuple): Tupla con la familia, el tamaño y el estilo de la fuente.
        - pady(int): Espacio vertical exterior del botón.
        - empaquetar(bool): True si se empaqueta con pack, False si se posicionará con grid.

    Salida:
        - boton(Button): Botón estándar creado con la configuración indicada.
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
        Crea el cuadro con botones de opción (Radiobutton) para elegir el color de ficha al apostar,
        consultando el valor en dólares desde datos.VALOR_FICHAS.

    Entrada:
        - ventana_padre(Widget): Ventana donde se colocará el selector de color de ficha.

    Salida:
        - selector(tuple): Tupla con la variable del color seleccionado y la lista de botones de opción.
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

    for columna_color in range(len(ORDEN_COLORES)):
        color = ORDEN_COLORES[columna_color]
        rb_color = tk.Radiobutton(
            marco_color,
            text=color + " ($" + str(obtener_valor_ficha(color)) + ")",
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

    return (color_seleccionado, botones_color)


def crear_etiquetas_rodillos(marco_padre, simbolos_iniciales):
    """
    Funcionalidad:
        Crea las tres etiquetas blancas que muestran los símbolos de los rodillos en la tragamonedas.

    Entrada:
        - marco_padre(Frame): Marco contenedor donde se colocarán los tres rodillos.
        - simbolos_iniciales(list): Lista con los tres símbolos iniciales a mostrar.

    Salida:
        - etiquetas_rodillos(list): Lista con las tres etiquetas gráficas de los rodillos.
    """
    etiquetas = []
    for indice in range(3):
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
    return etiquetas


def crear_tabla_inventario_fichas(ventana_padre):
    """
    Funcionalidad:
        Crea la tabla que muestra cada color de ficha, su valor en dólares desde
        datos.VALOR_FICHAS, cuántas tiene el jugador y el campo de texto para comprar o canjear.

    Entrada:
        - ventana_padre(Widget): Ventana donde se colocará la tabla de inventario de fichas.

    Salida:
        - tabla(tuple): Tupla con el diccionario de etiquetas de inventario y el diccionario de campos de entrada.
    """
    marco_tabla = tk.Frame(ventana_padre, bg="#081c15", bd=2, relief="ridge", padx=10, pady=10)
    marco_tabla.pack(pady=10)

    encabezados = ["Color", "Valor ($)", "Tienes", "Cantidad"]
    for col_idx in range(len(encabezados)):
        tk.Label(
            marco_tabla,
            text=encabezados[col_idx],
            font=("Arial", 10, "bold"),
            bg="#081c15",
            fg="#ffd166",
            width=10
        ).grid(row=0, column=col_idx, pady=4)

    etiquetas_cantidades = {}
    entradas_cantidades = {}

    for i in range(len(ORDEN_COLORES)):
        color = ORDEN_COLORES[i]
        fila = i + 1
        valor_monetario = obtener_valor_ficha(color)
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

    return (etiquetas_cantidades, entradas_cantidades)


# ADMINISTRACIÓN DE VENTANAS TKINTER

def asegurar_ventana_raiz():
    """
    Funcionalidad:
        Asegura que exista una única ventana principal tk.Tk() activa en toda la aplicación.

    Entrada:
        - Ninguna.

    Salida:
        - ventana_raiz(Tk): Instancia raíz principal de Tkinter para la aplicación.
    """
    global ventana_raiz
    if not ventana_raiz:
        ventana_raiz = tk.Tk()
    return ventana_raiz


def cerrar_aplicacion_completa():
    """
    Funcionalidad:
        Cierra la ventana secundaria (si existe) y la ventana raíz de Tkinter para finalizar el programa.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Destruye las ventanas activas y finaliza la aplicación sin retornar un valor.
    """
    global ventana_raiz, ventana_secundaria, mainloop_iniciado
    if ventana_secundaria:
        if ventana_secundaria.winfo_exists():
            ventana_secundaria.destroy()
        ventana_secundaria = False

    if ventana_raiz:
        try:
            ventana_raiz.quit()
        except tk.TclError:
            pass
        if ventana_raiz.winfo_exists():
            ventana_raiz.destroy()
        ventana_raiz = False

    mainloop_iniciado = False


def preparar_ventana_e2(titulo, geometria, es_principal, funcion_retorno):
    """
    Funcionalidad:
        Prepara la ventana que se va a mostrar en pantalla, usando la única ventana raíz tk.Tk()
        para el menú principal y una ventana secundaria tk.Toplevel() para las demás pantallas.

    Entrada:
        - titulo(str): Título que se mostrará en la barra superior de la ventana.
        - geometria(str): Dimensiones de la ventana en formato ancho por alto.
        - es_principal(bool): True si corresponde al menú principal, False si es una ventana secundaria.
        - funcion_retorno(function): Función que se ejecuta al cerrar la ventana con el botón X.

    Salida:
        - ventana(Widget): Ventana configurada y lista para agregar los controles gráficos.
    """
    global ventana_secundaria

    raiz = asegurar_ventana_raiz()

    if ventana_secundaria:
        if ventana_secundaria.winfo_exists():
            ventana_secundaria.destroy()
        ventana_secundaria = False

    if funcion_retorno:
        protocolo_cierre = funcion_retorno
    else:
        protocolo_cierre = cerrar_aplicacion_completa

    if es_principal:
        for hijo in raiz.winfo_children():
            hijo.destroy()
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
        Inicia el mainloop() de la única ventana raíz una sola vez.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Inicia el bucle principal de eventos de Tkinter sin retornar un valor.
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
        Punto de entrada de casino.py: asegura la única ventana raíz tk.Tk(),
        abre la ventana de sesión de E1 (si está conectada) o el menú principal, e inicia el único mainloop().

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Inicializa la ventana raíz, abre la sesión y arranca el bucle principal sin retornar un valor.
    """
    asegurar_ventana_raiz()
    funcion_sesion_e1 = enlaces_e1["ventana_sesion"]
    if funcion_sesion_e1:
        funcion_sesion_e1()
        iniciar_bucle_principal_si_corresponde()
    else:
        menu_principal()


# E2.1. MENÚ PRINCIPAL

def menu_principal():
    """
    Funcionalidad:
        Muestra el menú principal con el username del jugador y los cinco botones
        obligatorios: Jugar, Fichas, Ranking, Análisis y Cerrar sesión.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Construye y muestra la ventana del menú principal sin retornar un valor.
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
            Abre la ventana de Ranking de E1.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Abre la funcionalidad de ranking conectada con E1 sin retornar un valor.
        """
        abrir_funcionalidad_e1("ranking", "Ranking")

    def ir_analisis():
        """
        Funcionalidad:
            Abre la ventana de Análisis de E1.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Abre la funcionalidad de análisis conectada con E1 sin retornar un valor.
        """
        abrir_funcionalidad_e1("analisis", "Análisis")

    def ir_cerrar_sesion():
        """
        Funcionalidad:
            Solicita confirmación al jugador antes de cerrar la sesión; si confirma,
            guarda los datos del jugador, limpia jugador_actual de la memoria y regresa a la ventana de sesión de E1.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Solicita confirmación, guarda los datos y cierra la sesión activa sin retornar un valor.
        """
        confirmacion = messagebox.askyesno(
            "Confirmar cierre de sesión",
            "¿Estás seguro de que deseas cerrar la sesión actual?"
        )
        if not confirmacion:
            return

        guardar_datos_e1()
        funcion_cerrar = enlaces_e1["cerrar_sesion"]
        funcion_sesion = enlaces_e1["ventana_sesion"]
        if funcion_cerrar:
            funcion_cerrar()
        elif funcion_sesion:
            limpiar_jugador_actual()
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
        Muestra la ventana de juegos con los botones Ruleta, Tragamonedas, Blackjack y Dados,
        la cantidad de fichas disponibles y el botón para volver al menú principal.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Construye y muestra la ventana selectora de juegos sin retornar un valor.
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
            Abre el juego de Ruleta de E1.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Abre el juego de ruleta conectado con E1 sin retornar un valor.
        """
        abrir_funcionalidad_e1("ruleta", "Ruleta")

    def abrir_blackjack():
        """
        Funcionalidad:
            Abre el juego de Blackjack de E1.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Abre el juego de blackjack conectado con E1 sin retornar un valor.
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
        Muestra la ventana del juego de tragamonedas de tres rodillos, anima el giro
        recorriendo MATRIZ_RODILLOS y evalúa las combinaciones ganadoras.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Construye y muestra la interfaz gráfica del juego de tragamonedas sin retornar un valor.
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
            Impide que el jugador cierre o salga de la ventana mientras los rodillos están girando.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Verifica si los rodillos están girando antes de volver a la ventana de juegos sin retornar un valor.
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
            Habilita o deshabilita los botones y entradas mientras los rodillos giran.

        Entrada:
            - estado(str): Estado de activación normal o deshabilitado para los controles del juego.

        Salida:
            - Ninguna: Actualiza el estado de los botones y selectores de la ventana sin retornar un valor.
        """
        boton_girar.config(state=estado)
        entrada_apuesta.config(state=estado)
        boton_jugar_otra_vez.config(state=estado)
        boton_volver.config(state=estado)
        for boton in botones_color:
            boton.config(state=estado)

    def finalizar_giro():
        """
        Funcionalidad:
            Detiene el giro, forma la tupla con los tres símbolos finales, evalúa el resultado
            y vuelve a habilitar los botones.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Evalúa la combinación final de los rodillos y actualiza los saldos sin retornar un valor.
        """
        if not ventana.winfo_exists():
            return

        indices = estado_juego["indices"]
        simbolos_finales = (
            MATRIZ_RODILLOS[0][indices[0]],
            MATRIZ_RODILLOS[1][indices[1]],
            MATRIZ_RODILLOS[2][indices[2]]
        )

        for i in range(3):
            etiquetas_rodillos[i].config(text=simbolos_finales[i])

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
            Avanza un paso de animación en los tres rodillos cada INTERVALO_ANIMACION_MS
            milisegundos hasta completar PASOS_ANIMACION pasos.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Ejecuta un paso de la animación secuencial de los rodillos sin retornar un valor.
        """
        if not ventana.winfo_exists():
            return

        if estado_juego["paso"] < PASOS_ANIMACION:
            nuevos_simbolos = avanzar_indices_rodillos(estado_juego["indices"])
            for i in range(3):
                etiquetas_rodillos[i].config(text=nuevos_simbolos[i])

            estado_juego["paso"] = estado_juego["paso"] + 1
            ventana.after(INTERVALO_ANIMACION_MS, animar_rodillos)
        else:
            finalizar_giro()

    def iniciar_giro():
        """
        Funcionalidad:
            Valida la apuesta, descuenta las fichas apostadas e inicia la animación de los rodillos.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Valida la apuesta, descuenta las fichas e inicia la animación de giro sin retornar un valor.
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
            Reinicia el campo de apuesta y el mensaje en pantalla para jugar otra vez.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Restablece el campo de apuesta y los rodillos para una nueva jugada sin retornar un valor.
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
        Muestra la ventana del juego de dados permitiendo elegir color y cantidad de fichas,
        seleccionar el tipo de apuesta desde MATRIZ_OPCIONES_DADOS y lanzar los dos dados.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Construye y muestra la interfaz gráfica del juego de dados sin retornar un valor.
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

    for fila_rb in range(len(MATRIZ_OPCIONES_DADOS)):
        for col_rb in range(len(MATRIZ_OPCIONES_DADOS[fila_rb])):
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
            Valida la apuesta y la suma exacta (si aplica), ejecuta la tirada de dados
            y muestra la tupla obtenida y el resultado en pantalla.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Valida la apuesta, ejecuta el lanzamiento de dados y actualiza la ventana sin retornar un valor.
        """
        color_ficha = color_seleccionado.get()
        es_valida, apuesta = validar_apuesta_por_color(entrada_apuesta.get(), color_ficha)
        if not es_valida:
            return

        tipo = tipo_seleccionado.get()
        numero_elegido = 0

        if tipo == "sumaExacta":
            es_suma_valida, numero_elegido, error_suma = validar_entero(
                entrada_suma_exacta.get(), "Suma exacta", False
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
            Reinicia los textos de resultado para realizar una nueva tirada de dados.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Limpia los campos de entrada y restablece las etiquetas para otro lanzamiento sin retornar un valor.
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
        Muestra la ventana de compra y canje de fichas con la tabla de colores y valores,
        permitiendo comprar fichas con dinero o canjear fichas por dinero mediante las funciones de datos.py.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Construye y muestra la ventana de compra y canje de fichas sin retornar un valor.
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
            Actualiza en pantalla el dinero disponible, las cantidades de fichas por color
            y reinicia las cajas de texto a 0.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Actualiza las etiquetas de dinero y fichas y limpia las entradas sin retornar un valor.
        """
        etiqueta_dinero.config(
            text="Dinero disponible: $" + (jugador_actual[1][0]) +
                 "   |   Total de fichas: " + str(calcular_total_fichas())
        )
        for color in ORDEN_COLORES:
            etiquetas_cantidades[color].config(text=str(obtener_fichas_color(color)))
            entradas_cantidades[color].delete(0, tk.END)
            entradas_cantidades[color].insert(0, "0")

    def leer_cantidades_ingresadas():
        """
        Funcionalidad:
            Lee y valida las cantidades escritas por el jugador en cada color de ficha
            utilizando validar_entero con permitir_cero=True.

        Entrada:
            - Ninguna.

        Salida:
            - cantidades(dict): Diccionario con las cantidades enteras por color o un diccionario vacío si algún valor es inválido.
        """
        seleccion = {}
        for color in ORDEN_COLORES:
            texto = entradas_cantidades[color].get()
            es_valido, numero, mensaje_error = validar_entero(texto, "color " + color, True)
            if not es_valido:
                messagebox.showwarning("Cantidad inválida", mensaje_error)
                return {}
            seleccion[color] = numero
        return seleccion

    def comprar_fichas():
        """
        Funcionalidad:
            Valida la compra de fichas, solicita confirmación al jugador y ejecuta
            la compra y persistencia a través de datos.comprarFichas.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Valida las cantidades, solicita confirmación y ejecuta la compra de fichas sin retornar un valor.
        """
        cantidades = leer_cantidades_ingresadas()
        if not cantidades:
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
            cantidades_e1 = convertir_cantidades_a_formato_e1(cantidades)
            respaldo_recursos = list(jugador_actual[1])
            try:
                datos.comprarFichas(jugador_actual, cantidades_e1)
                refrescar_vista_fichas()
                messagebox.showinfo("Compra exitosa", "Se compraron las fichas correctamente.")
            except (ValueError, TypeError, OSError, pickle.UnpicklingError, EOFError) as error:
                jugador_actual[1] = respaldo_recursos
                refrescar_vista_fichas()
                messagebox.showerror(
                    "Error al guardar la compra",
                    "No se pudo completar y guardar la compra de fichas: " + str(error)
                )

    def canjear_fichas():
        """
        Funcionalidad:
            Valida el canje de fichas, solicita confirmación al jugador y ejecuta
            el canje y persistencia a través de datos.canjearFichas.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Valida las cantidades, solicita confirmación y ejecuta el canje de fichas sin retornar un valor.
        """
        cantidades = leer_cantidades_ingresadas()
        if not cantidades:
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
            cantidades_e1 = convertir_cantidades_a_formato_e1(cantidades)
            respaldo_recursos = list(jugador_actual[1])
            try:
                datos.canjearFichas(jugador_actual, cantidades_e1)
                refrescar_vista_fichas()
                messagebox.showinfo(
                    "Canje exitoso",
                    "Se canjearon las fichas y se sumó $" + str(dinero_recibir) + " a tu dinero disponible."
                )
            except (ValueError, TypeError, OSError, pickle.UnpicklingError, EOFError) as error:
                jugador_actual[1] = respaldo_recursos
                refrescar_vista_fichas()
                messagebox.showerror(
                    "Error al guardar el canje",
                    "No se pudo completar y guardar el canje de fichas: " + str(error)
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
