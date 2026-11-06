# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

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
    """
    Funcionalidad:
        Obtiene la ruta absoluta del archivo binario donde se almacenan los jugadores.

    Entrada:
        - Ninguna.

    Salida:
        - ruta(str): Ruta completa del archivo binario jugadores en el directorio del proyecto.
    """
    carpetaActual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpetaActual, NOMBRE_ARCHIVO)


def validarEstructuraJugador(jugador):
    """
    Funcionalidad:
        Verifica que el registro de un jugador cumpla con la estructura de lista, tupla de identidad,
        sublista de dinero y fichas no negativas y puntaje entero.

    Entrada:
        - jugador(list): Estructura con los datos personales, recursos y puntaje del jugador.

    Salida:
        - es_valido(bool): True si el registro cumple la estructura esperada, False en caso contrario.
    """
    if not isinstance(jugador, list) or len(jugador) != 3:
        return False

    datosPersonales, recursos, puntaje = jugador

    if not isinstance(datosPersonales, tuple) or len(datosPersonales) != 3:
        return False

    for dato in datosPersonales:
        if not isinstance(dato, str) or not dato.strip():
            return False

    if not isinstance(recursos, list) or len(recursos) != 5:
        return False

    dinero = recursos[0]
    if not isinstance(dinero, (int, float)) or isinstance(dinero, bool) or dinero < 0:
        return False

    for ficha in recursos[1:]:
        if not isinstance(ficha, int) or isinstance(ficha, bool) or ficha < 0:
            return False

    if not isinstance(puntaje, int) or isinstance(puntaje, bool):
        return False

    return True


def validarArchivoJugadores():
    """
    Funcionalidad:
        Comprueba que el archivo binario de jugadores exista, no esté vacío y contenga
        una lista válida de jugadores con usernames únicos.

    Entrada:
        - Ninguna.

    Salida:
        - resultado(tuple): Tupla con el indicador booleano de validez y el mensaje descriptivo del estado.
    """
    ruta = obtenerRutaArchivo()

    if not os.path.exists(ruta):
        return False, "El archivo de jugadores no existe."

    if os.path.getsize(ruta) == 0:
        return False, "El archivo de jugadores esta vacio."

    try:
        archivo = open(ruta, "rb")
        try:
            jugadores = pickle.load(archivo)
        finally:
            archivo.close()
    except (OSError, pickle.UnpicklingError, EOFError):
        return False, "El archivo de jugadores esta danado o no tiene formato pickle valido."

    if not isinstance(jugadores, list):
        return False, "El contenido del archivo debe ser una lista de jugadores."

    usernames = set()
    for jugador in jugadores:
        if not validarEstructuraJugador(jugador):
            return False, "Uno de los jugadores guardados no tiene la estructura correcta."

        username = jugador[0][0].strip().lower()
        if username in usernames:
            return False, "Existen usernames repetidos en el archivo."
        usernames.add(username)

    return True, "Archivo de jugadores valido."


def cargarJugadores():
    """
    Funcionalidad:
        Carga y devuelve la lista de jugadores almacenada en el archivo binario con pickle,
        o crea una lista vacía si el archivo aún no existe.

    Entrada:
        - Ninguna.

    Salida:
        - jugadores(list): Lista de registros de jugadores almacenados en el archivo.
    """
    ruta = obtenerRutaArchivo()

    if not os.path.exists(ruta):
        guardarJugadores([])
        return []

    if os.path.getsize(ruta) == 0:
        return []

    archivo = open(ruta, "rb")
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
    """
    Funcionalidad:
        Valida y guarda la lista completa de jugadores en formato binario utilizando pickle.

    Entrada:
        - jugadores(list): Lista de registros de jugadores a almacenar.

    Salida:
        - Ninguna: Actualiza el archivo binario jugadores en disco sin retornar un valor.
    """
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
    """
    Funcionalidad:
        Busca un jugador por su username dentro de la lista de jugadores y devuelve su registro.

    Entrada:
        - username(str): Identificador de usuario a buscar.
        - jugadores(list): Lista de jugadores donde realizar la búsqueda.

    Salida:
        - jugador(list): Registro del jugador encontrado o None si no existe.
    """
    if jugadores is None:
        jugadores = cargarJugadores()

    usernameBuscado = username.strip().lower()

    for jugador in jugadores:
        if jugador[0][0].lower() == usernameBuscado:
            return jugador

    return None


def registrarJugador(username, nombre, apellido):
    """
    Funcionalidad:
        Registra un jugador nuevo con un saldo inicial de 100.0 dólares, fichas y puntaje iniciales en cero,
        y lo almacena en el archivo jugadores.

    Entrada:
        - username(str): Nombre de usuario único del jugador.
        - nombre(str): Nombre del jugador.
        - apellido(str): Apellido del jugador.

    Salida:
        - nuevoJugador(list): Registro del nuevo jugador creado y guardado en el archivo.
    """
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
        [100.0, 0, 0, 0, 0],
        0
    ]

    jugadores.append(nuevoJugador)
    guardarJugadores(jugadores)
    return nuevoJugador


def consultarDinero(jugador):
    """
    Funcionalidad:
        Consulta y devuelve el dinero disponible del jugador.

    Entrada:
        - jugador(list): Registro del jugador a consultar.

    Salida:
        - dinero(float): Dinero disponible del jugador en dólares.
    """
    return float(jugador[1][0])


def consultarFichas(jugador):
    """
    Funcionalidad:
        Consulta y devuelve un diccionario con la cantidad de fichas por color del jugador.

    Entrada:
        - jugador(list): Registro del jugador a consultar.

    Salida:
        - fichas(dict): Diccionario con las cantidades de fichas rojas, azules, verdes y blancas.
    """
    return {
        "rojas": jugador[1][1],
        "azules": jugador[1][2],
        "verdes": jugador[1][3],
        "blancas": jugador[1][4]
    }


def comprarFichas(jugador, cantidades):
    """
    Funcionalidad:
        Valida el dinero disponible, descuenta el costo total de la compra,
        suma las fichas adquiridas en cada color y guarda los cambios en el archivo jugadores.

    Entrada:
        - jugador(list): Registro del jugador activo.
        - cantidades(dict): Diccionario con las cantidades de fichas a comprar por color.

    Salida:
        - costoTotal(int): Costo total de la compra realizada en dólares.
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
    """
    Funcionalidad:
        Valida la disponibilidad de fichas por color, resta las fichas canjeadas,
        suma el dinero correspondiente al saldo del jugador y guarda los cambios en el archivo jugadores.

    Entrada:
        - jugador(list): Registro del jugador activo.
        - cantidades(dict): Diccionario con las cantidades de fichas a canjear por color.

    Salida:
        - dineroRecibido(int): Monto total de dinero acreditado por el canje en dólares.
    """
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
    """
    Funcionalidad:
        Suma o resta una cantidad entera de puntos al puntaje general del jugador
        y guarda los cambios en el archivo jugadores.

    Entrada:
        - jugador(list): Registro del jugador activo.
        - cantidad(int): Cantidad de puntos a sumar o restar.

    Salida:
        - puntaje(int): Puntaje actualizado del jugador.
    """
    if not isinstance(cantidad, int):
        raise TypeError("La variacion del puntaje debe ser un entero.")

    jugador[2] += cantidad
    guardarCambiosJugador(jugador)
    return jugador[2]


def guardarCambiosJugador(jugador):
    """
    Funcionalidad:
        Busca al jugador activo por su username dentro del archivo jugadores,
        reemplaza su registro con los datos actualizados y persiste la lista en disco.

    Entrada:
        - jugador(list): Registro actualizado del jugador activo.

    Salida:
        - Ninguna: Actualiza el registro del jugador en el archivo jugadores sin retornar un valor.
    """
    jugadores = cargarJugadores()
    username = jugador[0][0]

    for indice, jugadorGuardado in enumerate(jugadores):
        if jugadorGuardado[0][0].lower() == username.lower():
            jugadores[indice] = jugador
            guardarJugadores(jugadores)
            return

    raise ValueError("No se encontro el jugador para guardar los cambios.")
