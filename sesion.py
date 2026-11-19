# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

import tkinter as tk
from tkinter import messagebox

import datos

camposSesion = {}


def validarRegistro(username, nombre, apellido):
    """
    Funcionalidad:
        Valida que los tres campos del registro (username, nombre y apellido)
        contengan texto y no estén vacíos.

    Entrada:
        - username(str): Nombre de usuario ingresado.
        - nombre(str): Nombre del jugador ingresado.
        - apellido(str): Apellido del jugador ingresado.

    Salida:
        - es_valido(bool): True si los tres campos tienen contenido, False en caso contrario.
    """
    return bool(username.strip() and nombre.strip() and apellido.strip())


def iniciarSesion(username):
    """
    Funcionalidad:
        Busca el jugador por su username en el archivo de jugadores y devuelve su registro si existe.

    Entrada:
        - username(str): Nombre de usuario ingresado para iniciar sesion.

    Salida:
        - resultado(list o str): Registro del jugador encontrado o mensaje de error si fallo.
    """
    if not username.strip():
        return "Escriba su username."

    jugador = datos.buscarJugador(username)
    if not jugador:
        return "No existe un jugador con ese username."

    return jugador


def registrarDesdeFormulario(username, nombre, apellido):
    """
    Funcionalidad:
        Valida los datos ingresados en el formulario y registra al nuevo jugador en el archivo de datos.

    Entrada:
        - username(str): Nombre de usuario unico del jugador.
        - nombre(str): Nombre del jugador.
        - apellido(str): Apellido del jugador.

    Salida:
        - resultado(list o str): Registro del jugador recién creado o mensaje de error si fallo.
    """
    if not validarRegistro(username, nombre, apellido):
        return "Complete username, nombre y apellido."

    return datos.registrarJugador(username, nombre, apellido)


def registrar():
    """
    Funcionalidad:
        Procesa el formulario de registro de un nuevo jugador, muestra un aviso
        al completarse y coloca el username registrado en el campo de inicio de sesion.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Registra al jugador y actualiza los campos de la ventana sin retornar un valor.
    """
    resultado = registrarDesdeFormulario(
        camposSesion["usernameRegistro"].get(),
        camposSesion["nombre"].get(),
        camposSesion["apellido"].get()
    )
    if type(resultado) == str:
        messagebox.showerror("No se pudo registrar", resultado)
        return

    messagebox.showinfo(
        "Registro correcto",
        "Jugador registrado. Ya puede iniciar sesion."
    )
    camposSesion["usernameSesion"].delete(0, tk.END)
    camposSesion["usernameSesion"].insert(0, resultado[0][0])
    camposSesion["usernameRegistro"].delete(0, tk.END)
    camposSesion["nombre"].delete(0, tk.END)
    camposSesion["apellido"].delete(0, tk.END)


def entrar():
    """
    Funcionalidad:
        Valida el username ingresado para iniciar sesion y transfiere el registro
        del jugador a la funcion conectada en alIniciarSesion.

    Entrada:
        - Ninguna.

    Salida:
        - Ninguna: Inicia la sesion del jugador y abre el menu principal sin retornar un valor.
    """
    resultado = iniciarSesion(camposSesion["usernameSesion"].get())
    if type(resultado) == str:
        messagebox.showerror("No se pudo iniciar sesion", resultado)
        return

    jugador = resultado
    alIniciarSesion = camposSesion["alIniciarSesion"]
    ventanaPadre = camposSesion["ventanaPadre"]
    ventana = camposSesion["ventana"]

    if alIniciarSesion:
        if not ventanaPadre:
            ventana.destroy()
        alIniciarSesion(jugador)
    else:
        messagebox.showinfo(
            "Sesion iniciada",
            "Bienvenido, " + jugador[0][1] + " " + jugador[0][2] + "."
        )


def crearVentanaSesion(alIniciarSesion, ventanaPadre):
    """
    Funcionalidad:
        Crea y configura la ventana de registro e inicio de sesión de jugadores,
        reutilizando la ventana recibida en ventanaPadre o creando una ventana propia si se ejecuta de forma independiente.

    Entrada:
        - alIniciarSesion(function): Función que recibe el registro del jugador al iniciar sesión.
        - ventanaPadre(Toplevel): Ventana contenedora donde se construye la interfaz de sesión.

    Salida:
        - ventana(Toplevel): Ventana de sesión configurada con los formularios de registro e ingreso.
    """
    if ventanaPadre:
        ventana = ventanaPadre
    else:
        ventana = tk.Tk()

    camposSesion["alIniciarSesion"] = alIniciarSesion
    camposSesion["ventanaPadre"] = ventanaPadre
    camposSesion["ventana"] = ventana

    ventana.title("Casino - Sesion")
    ventana.geometry("430x440")
    ventana.resizable(False, False)

    titulo = tk.Label(
        ventana, text="CASINO", font=("Arial", 20, "bold")
    )
    titulo.pack(pady=(15, 5))

    subtitulo = tk.Label(
        ventana, text="Registrese o inicie sesion", font=("Arial", 11)
    )
    subtitulo.pack(pady=(0, 12))

    marcoRegistro = tk.LabelFrame(
        ventana, text="Registro de jugador", padx=12, pady=10
    )
    marcoRegistro.pack(fill="x", padx=20, pady=8)

    tk.Label(marcoRegistro, text="Username:").grid(
        row=0, column=0, sticky="w", pady=4
    )
    camposSesion["usernameRegistro"] = tk.Entry(marcoRegistro, width=27)
    camposSesion["usernameRegistro"].grid(row=0, column=1, pady=4)

    tk.Label(marcoRegistro, text="Nombre:").grid(
        row=1, column=0, sticky="w", pady=4
    )
    camposSesion["nombre"] = tk.Entry(marcoRegistro, width=27)
    camposSesion["nombre"].grid(row=1, column=1, pady=4)

    tk.Label(marcoRegistro, text="Apellido:").grid(
        row=2, column=0, sticky="w", pady=4
    )
    camposSesion["apellido"] = tk.Entry(marcoRegistro, width=27)
    camposSesion["apellido"].grid(row=2, column=1, pady=4)

    tk.Button(
        marcoRegistro, text="Registrarse", command=registrar, width=18
    ).grid(row=3, column=0, columnspan=2, pady=(10, 2))

    marcoSesion = tk.LabelFrame(
        ventana, text="Inicio de sesion", padx=12, pady=10
    )
    marcoSesion.pack(fill="x", padx=20, pady=8)

    tk.Label(marcoSesion, text="Username:").grid(
        row=0, column=0, sticky="w", pady=4
    )
    camposSesion["usernameSesion"] = tk.Entry(marcoSesion, width=27)
    camposSesion["usernameSesion"].grid(row=0, column=1, pady=4)

    tk.Button(
        marcoSesion, text="Iniciar sesion", command=entrar, width=18
    ).grid(row=1, column=0, columnspan=2, pady=(10, 2))

    if not ventanaPadre:
        ventana.mainloop()

    return ventana
