# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis y manejo de datos con pickle.
# E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas, cerrar sesión y documentación interna.

import os
import pickle

NOMBRE_ARCHIVO = "jugadores"
RUTA_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_ARCHIVO)

VALOR_FICHAS = {
    "rojas": 10,
    "azules": 50,
    "verdes": 20,
    "blancas": 5
}

POSICIONES_FICHAS = {
    "rojas": 1,
    "azules": 2,
    "verdes": 3,
    "blancas": 4
}


def validarEstructuraJugador(jugador):
    """
    Funcionalidad:
        Verifica que el registro de un jugador cumpla con la estructura de lista, tupla de identidad, sublista de dinero y fichas no negativas y puntaje entero.
    Entrada:
    - jugador(list): Estructura con los datos personales, recursos y puntaje del jugador.
    Salida:
    - esValido(bool): True si el registro cumple la estructura esperada, False en caso contrario.
    """
    if type(jugador) != list or len(jugador) != 3:
        return False

    datosPersonales = jugador[0]
    recursos = jugador[1]
    puntaje = jugador[2]

    if type(datosPersonales) != tuple or len(datosPersonales) != 3:
        return False

    for dato in datosPersonales:
        if type(dato) != str or not dato.strip():
            return False

    if type(recursos) != list or len(recursos) != 5:
        return False

    dinero = recursos[0]
    if (type(dinero) != int and type(dinero) != float) or dinero < 0:
        return False

    for i in range(1, len(recursos)):
        if type(recursos[i]) != int or recursos[i] < 0:
            return False

    if type(puntaje) != int:
        return False

    return True


def cargarJugadores():
    """
    Funcionalidad:
        Carga y devuelve la lista de jugadores almacenada en el archivo binario con pickle,
        devuelve una lista vacía si el archivo aún no existe o un texto de error si está dañado.
    Entrada:
    - Ninguna.
    Salida:
    - jugadores(list o str): Lista de registros de jugadores, o texto de error si el archivo esta danado.
    """
    try:
        archivo = open(RUTA_ARCHIVO, "rb")
        jugadores = pickle.load(archivo)
        archivo.close()
    except FileNotFoundError:
        return []
    except (EOFError, pickle.UnpicklingError, ValueError, AttributeError):
        return "El archivo de jugadores esta danado."
    except OSError:
        return "Error al leer el archivo de jugadores."

    if type(jugadores) != list:
        return "El archivo de jugadores no tiene un formato valido."

    for jugador in jugadores:
        if not validarEstructuraJugador(jugador):
            return "El archivo contiene un registro de jugador invalido."

    return jugadores


def guardarJugadores(jugadores):
    """
    Funcionalidad:
        Valida y guarda la lista completa de jugadores en formato binario utilizando pickle.
    Entrada:
    - jugadores(list): Lista de registros de jugadores a almacenar.
    Salida:
    - resultado(bool o str): True si guardo los datos, o texto de error si fallo.
    """
    if type(jugadores) != list:
        return "Los jugadores deben almacenarse en una lista."

    for jugador in jugadores:
        if not validarEstructuraJugador(jugador):
            return "No se puede guardar: hay un jugador con datos invalidos."

    try:
        archivo = open(RUTA_ARCHIVO, "wb")
        pickle.dump(jugadores, archivo)
        archivo.close()
        return True
    except OSError:
        return "Error al escribir en el archivo de jugadores."


def buscarIndiceJugador(username, jugadores):
    """
    Funcionalidad:
        Busca la posicion de un jugador por su username sin distinguir mayusculas o minusculas.
    Entrada:
    - username(str): Identificador de usuario a buscar.
    - jugadores(list): Lista de registros de jugadores donde buscar.
    Salida:
    - indice(int): Posicion del jugador en la lista, o -1 si no existe.
    """
    usernameBuscado = username.strip().lower()
    for indice in range(len(jugadores)):
        if jugadores[indice][0][0].lower() == usernameBuscado:
            return indice
    return -1


def buscarJugador(username):
    """
    Funcionalidad:
        Busca un jugador por su username dentro del archivo de jugadores y devuelve su registro.
    Entrada:
    - username(str): Identificador de usuario a buscar.
    Salida:
    - jugador(list, bool o str): Registro encontrado, False si no existe o texto de error si fallo.
    """
    jugadores = cargarJugadores()
    if type(jugadores) == str:
        return jugadores

    indice = buscarIndiceJugador(username, jugadores)
    if indice != -1:
        return jugadores[indice]
    return False


def registrarJugador(username, nombre, apellido):
    """
    Funcionalidad:
        Registra un jugador nuevo con 100.0 dólares iniciales, fichas y puntaje en cero,
        y lo almacena en el archivo jugadores.
    Entrada:
    - username(str): Nombre de usuario único del jugador.
    - nombre(str): Nombre del jugador.
    - apellido(str): Apellido del jugador.
    Salida:
    - resultado(list o str): Registro del nuevo jugador creado y guardado, o texto de error si fallo.
    """
    username = username.strip()
    nombre = nombre.strip()
    apellido = apellido.strip()

    if not username or not nombre or not apellido:
        return "Todos los campos son obligatorios."

    jugadores = cargarJugadores()
    if type(jugadores) == str:
        return jugadores

    if buscarIndiceJugador(username, jugadores) != -1:
        return "Ese username ya esta registrado."
    nuevoJugador = [
        (username, nombre, apellido),
        [100.0, 0, 0, 0, 0],
        0
    ]

    jugadores.append(nuevoJugador)
    resultadoGuardado = guardarJugadores(jugadores)
    if resultadoGuardado is not True:
        return resultadoGuardado
    return nuevoJugador


def calcularMontoFichas(cantidades):
    """
    Funcionalidad:
        Valida que las cantidades de fichas sean enteros no negativos y calcula su monto total.
    Entrada:
    - cantidades(dict): Diccionario con las cantidades de fichas por color.
    Salida:
    - resultado(int o str): Monto total en dolares o mensaje de error si hay cantidades invalidas.
    """
    if type(cantidades) != dict:
        return "Las cantidades deben enviarse en un diccionario."

    montoTotal = 0
    for color in VALOR_FICHAS:
        cantidad = cantidades.get(color, 0)
        if type(cantidad) != int or cantidad < 0:
            return "Las cantidades deben ser enteros no negativos."
        montoTotal += cantidad * VALOR_FICHAS[color]

    if montoTotal == 0:
        return "Debe seleccionar al menos una ficha."
    return montoTotal


def comprarFichas(jugador, cantidades):
    """
    Funcionalidad:
        Valida el dinero disponible, descuenta el costo total de la compra, suma las fichas adquiridas en cada color y guarda los cambios en el archivo jugadores.
    Entrada:
    - jugador(list): Registro del jugador activo.
    - cantidades(dict): Diccionario con las cantidades de fichas a comprar por color.
    Salida:
    - resultado(int o str): Costo total de la compra realizada en dólares, o texto de error si fallo.
    """
    costoTotal = calcularMontoFichas(cantidades)
    if type(costoTotal) == str:
        return costoTotal

    if float(jugador[1][0]) < costoTotal:
        return "El jugador no tiene dinero suficiente."

    recursosAnteriores = [jugador[1][0], jugador[1][1], jugador[1][2], jugador[1][3], jugador[1][4]]
    jugador[1][0] = float(jugador[1][0]) - costoTotal
    for color in POSICIONES_FICHAS:
        posicion = POSICIONES_FICHAS[color]
        jugador[1][posicion] += cantidades.get(color, 0)

    resultadoGuardado = guardarCambiosJugador(jugador)
    if resultadoGuardado is not True:
        jugador[1] = recursosAnteriores
        return resultadoGuardado
    return costoTotal


def canjearFichas(jugador, cantidades):
    """
    Funcionalidad:
        Valida la disponibilidad de fichas por color, resta las fichas canjeadas, suma el dinero correspondiente al saldo del jugador y guarda los cambios en el archivo jugadores.
    Entrada:
    - jugador(list): Registro del jugador activo.
    - cantidades(dict): Diccionario con las cantidades de fichas a canjear por color.
    Salida:
    - resultado(int o str): Monto total de dinero acreditado por el canje en dólares, o texto de error si fallo.
    """
    dineroRecibido = calcularMontoFichas(cantidades)
    if type(dineroRecibido) == str:
        return dineroRecibido

    for color in POSICIONES_FICHAS:
        posicion = POSICIONES_FICHAS[color]
        if cantidades.get(color, 0) > jugador[1][posicion]:
            return "No hay suficientes fichas " + color + "."

    recursosAnteriores = [jugador[1][0], jugador[1][1], jugador[1][2], jugador[1][3], jugador[1][4]]
    for color in POSICIONES_FICHAS:
        posicion = POSICIONES_FICHAS[color]
        jugador[1][posicion] -= cantidades.get(color, 0)

    jugador[1][0] = float(jugador[1][0]) + dineroRecibido
    resultadoGuardado = guardarCambiosJugador(jugador)
    if resultadoGuardado is not True:
        jugador[1] = recursosAnteriores
        return resultadoGuardado
    return dineroRecibido


def guardarCambiosJugador(jugador):
    """
    Funcionalidad:
        Busca al jugador activo por su username dentro del archivo jugadores, reemplaza su registro con los datos actualizados y persiste la lista en disco.
    Entrada:
    - jugador(list): Registro actualizado del jugador activo.
    Salida:
    - resultado(bool o str): True si guardo los cambios, o texto de error si fallo.
    """
    jugadores = cargarJugadores()
    if type(jugadores) == str:
        return jugadores

    indice = buscarIndiceJugador(jugador[0][0], jugadores)
    if indice != -1:
        jugadores[indice] = jugador
        return guardarJugadores(jugadores)

    return "No se encontro el jugador para guardar los cambios."
