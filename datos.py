"""
Modulo de datos del casino.

Responsabilidades:
- Guardar y cargar jugadores mediante pickle.
- Consultar y modificar dinero, fichas y puntaje.
- Validar el archivo de jugadores.

Estructura de cada jugador:
[(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]
"""

import os
import pickle

NOMBRE_ARCHIVO = "jugadores"

VALOR_FICHAS = {
    "rojas": 10,
    "azules": 50,
    "verdes": 20,
    "blancas": 5
}


def obtenerRutaArchivo():
    """Devuelve la ruta del archivo jugadores, junto a este modulo."""
    carpetaActual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpetaActual, NOMBRE_ARCHIVO)


def validarEstructuraJugador(jugador):
    """Comprueba que un registro tenga la estructura solicitada."""
    if not isinstance(jugador, (list, tuple)) or len(jugador) != 3:
        return False

    datosPersonales = jugador[0]
    recursos = jugador[1]
    puntaje = jugador[2]

    if not isinstance(datosPersonales, (list, tuple)) or len(datosPersonales) != 3:
        return False
    if not isinstance(recursos, (list, tuple)) or len(recursos) != 5:
        return False
    if not isinstance(puntaje, int):
        return False

    if not all(isinstance(valor, str) and valor.strip()
               for valor in datosPersonales):
        return False

    try:
        if float(recursos[0]) < 0:
            return False
        for cantidad in recursos[1:]:
            if not isinstance(cantidad, int) or cantidad < 0:
                return False
    except (TypeError, ValueError):
        return False

    return True


def validarArchivoJugadores():
    """
    Indica si el archivo existe, contiene datos y su contenido es valido.
    Un archivo inexistente o vacio se considera una lista sin jugadores.
    """
    rutaArchivo = obtenerRutaArchivo()

    if not os.path.exists(rutaArchivo):
        return False

    if os.path.getsize(rutaArchivo) == 0:
        return False

    try:
        jugadores = cargarJugadores()
    except (pickle.UnpicklingError, EOFError, OSError, ValueError):
        return False

    return isinstance(jugadores, list) and all(
        validarEstructuraJugador(jugador) for jugador in jugadores
    )


def cargarJugadores():
    """Carga y devuelve la lista de jugadores. Si no existe, devuelve []."""
    rutaArchivo = obtenerRutaArchivo()

    if not os.path.exists(rutaArchivo) or os.path.getsize(rutaArchivo) == 0:
        return []

    archivo = open(rutaArchivo, "rb")
    try:
        jugadores = pickle.load(archivo)
    finally:
        archivo.close()

    if not isinstance(jugadores, list):
        raise ValueError("El archivo de jugadores no contiene una lista.")

    for jugador in jugadores:
        if not validarEstructuraJugador(jugador):
            raise ValueError("El archivo contiene un registro de jugador invalido.")

    return jugadores


def guardarJugadores(jugadores):
    """Guarda la lista de jugadores en formato binario usando pickle."""
    if not isinstance(jugadores, list):
        raise TypeError("Los jugadores deben almacenarse en una lista.")

    for jugador in jugadores:
        if not validarEstructuraJugador(jugador):
            raise ValueError("No se puede guardar: hay un jugador con datos invalidos.")

    archivo = open(obtenerRutaArchivo(), "wb")
    try:
        pickle.dump(jugadores, archivo, pickle.HIGHEST_PROTOCOL)
    finally:
        archivo.close()


def buscarJugador(username, jugadores=None):
    """Busca un jugador por username y devuelve su registro o None."""
    if jugadores is None:
        jugadores = cargarJugadores()

    usernameBuscado = username.strip().lower()

    for jugador in jugadores:
        if jugador[0][0].lower() == usernameBuscado:
            return jugador

    return None


def registrarJugador(username, nombre, apellido):
    """Registra un jugador nuevo con dinero, fichas y puntaje iniciales."""
    username = username.strip()
    nombre = nombre.strip()
    apellido = apellido.strip()

    if not username or not nombre or not apellido:
        raise ValueError("Todos los campos son obligatorios.")

    jugadores = cargarJugadores()

    if buscarJugador(username, jugadores) is not None:
        raise ValueError("Ese username ya esta registrado.")

    nuevoJugador = [
        (username, nombre, apellido),
        [0.0, 0, 0, 0, 0],
        0
    ]

    jugadores.append(nuevoJugador)
    guardarJugadores(jugadores)
    return nuevoJugador


def consultarDinero(jugador):
    """Devuelve el dinero disponible del jugador."""
    return float(jugador[1][0])


def consultarFichas(jugador):
    """Devuelve un diccionario con las cantidades de fichas del jugador."""
    return {
        "rojas": jugador[1][1],
        "azules": jugador[1][2],
        "verdes": jugador[1][3],
        "blancas": jugador[1][4]
    }


def comprarFichas(jugador, cantidades):
    """
    Compra fichas. cantidades es un diccionario, por ejemplo:
    {"rojas": 2, "azules": 1, "verdes": 0, "blancas": 3}
    """
    costoTotal = 0

    for color in VALOR_FICHAS:
        cantidad = cantidades.get(color, 0)
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Las cantidades deben ser enteros no negativos.")
        costoTotal += cantidad * VALOR_FICHAS[color]

    if consultarDinero(jugador) < costoTotal:
        raise ValueError("El jugador no tiene dinero suficiente.")

    jugador[1][0] = float(jugador[1][0]) - costoTotal
    posiciones = {"rojas": 1, "azules": 2, "verdes": 3, "blancas": 4}

    for color, posicion in posiciones.items():
        jugador[1][posicion] += cantidades.get(color, 0)

    guardarCambiosJugador(jugador)
    return costoTotal


def canjearFichas(jugador, cantidades):
    """Canjea fichas por dinero y devuelve el dinero recibido."""
    dineroRecibido = 0
    posiciones = {"rojas": 1, "azules": 2, "verdes": 3, "blancas": 4}

    for color, posicion in posiciones.items():
        cantidad = cantidades.get(color, 0)
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Las cantidades deben ser enteros no negativos.")
        if cantidad > jugador[1][posicion]:
            raise ValueError("No hay suficientes fichas " + color + ".")

        dineroRecibido += cantidad * VALOR_FICHAS[color]

    for color, posicion in posiciones.items():
        jugador[1][posicion] -= cantidades.get(color, 0)

    jugador[1][0] = float(jugador[1][0]) + dineroRecibido
    guardarCambiosJugador(jugador)
    return dineroRecibido


def actualizarPuntaje(jugador, cantidad):
    """Suma o resta puntos al puntaje general del jugador."""
    if not isinstance(cantidad, int):
        raise TypeError("La variacion del puntaje debe ser un entero.")

    jugador[2] += cantidad
    guardarCambiosJugador(jugador)
    return jugador[2]


def guardarCambiosJugador(jugador):
    """Actualiza en el archivo el registro del jugador modificado."""
    jugadores = cargarJugadores()
    username = jugador[0][0]

    for indice, jugadorGuardado in enumerate(jugadores):
        if jugadorGuardado[0][0].lower() == username.lower():
            jugadores[indice] = jugador
            guardarJugadores(jugadores)
            return

    raise ValueError("No se encontro el jugador para guardar los cambios.")
