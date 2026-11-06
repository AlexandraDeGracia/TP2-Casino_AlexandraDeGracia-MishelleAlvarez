# Proyecto: TP2 - Casino
# Integrantes: Mishelle Álvarez y Alexandra De Gracia
# Descripción general: Aplicación de casino con interfaz gráfica en Python usando tkinter.
# División de responsabilidades:
# - E1 (Mishelle Álvarez): Ventana de sesión, ruleta, blackjack, ranking, análisis, cerrar sesión y manejo de datos con pickle.
# - E2 (Alexandra De Gracia): Menú principal, ventana de juegos, tragamonedas, dados, ventana de fichas y documentación interna.

import pickle
import tkinter as tk
from tkinter import messagebox

import datos


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
        - username(str): Nombre de usuario ingresado para iniciar sesión.

    Salida:
        - jugador(list): Registro del jugador encontrado en el archivo jugadores.
    """
    if not username.strip():
        raise ValueError("Escriba su username.")

    jugador = datos.buscarJugador(username)
    if not jugador:
        raise ValueError("No existe un jugador con ese username.")

    return jugador


def registrarDesdeFormulario(username, nombre, apellido):
    """
    Funcionalidad:
        Valida los datos ingresados en el formulario y registra al nuevo jugador en el archivo de datos.

    Entrada:
        - username(str): Nombre de usuario único del jugador.
        - nombre(str): Nombre del jugador.
        - apellido(str): Apellido del jugador.

    Salida:
        - jugador(list): Registro del jugador recién creado en el archivo jugadores.
    """
    if not validarRegistro(username, nombre, apellido):
        raise ValueError("Complete username, nombre y apellido.")

    return datos.registrarJugador(username, nombre, apellido)


def crearVentanaSesion(alIniciarSesion=False, ventanaPadre=False):
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
    entradaUsernameRegistro = tk.Entry(marcoRegistro, width=27)
    entradaUsernameRegistro.grid(row=0, column=1, pady=4)

    tk.Label(marcoRegistro, text="Nombre:").grid(
        row=1, column=0, sticky="w", pady=4
    )
    entradaNombre = tk.Entry(marcoRegistro, width=27)
    entradaNombre.grid(row=1, column=1, pady=4)

    tk.Label(marcoRegistro, text="Apellido:").grid(
        row=2, column=0, sticky="w", pady=4
    )
    entradaApellido = tk.Entry(marcoRegistro, width=27)
    entradaApellido.grid(row=2, column=1, pady=4)

    def registrar():
        """
        Funcionalidad:
            Procesa el formulario de registro de un nuevo jugador, muestra un aviso
            al completarse y coloca el username registrado en el campo de inicio de sesión.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Registra al jugador y actualiza los campos de la ventana sin retornar un valor.
        """
        try:
            jugador = registrarDesdeFormulario(
                entradaUsernameRegistro.get(),
                entradaNombre.get(),
                entradaApellido.get()
            )
            messagebox.showinfo(
                "Registro correcto",
                "Jugador registrado. Ya puede iniciar sesion."
            )
            entradaUsernameSesion.delete(0, tk.END)
            entradaUsernameSesion.insert(0, jugador[0][0])
            entradaUsernameRegistro.delete(0, tk.END)
            entradaNombre.delete(0, tk.END)
            entradaApellido.delete(0, tk.END)
        except (ValueError, OSError, pickle.UnpicklingError, EOFError) as error:
            messagebox.showerror("No se pudo registrar", str(error))

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
    entradaUsernameSesion = tk.Entry(marcoSesion, width=27)
    entradaUsernameSesion.grid(row=0, column=1, pady=4)

    def entrar():
        """
        Funcionalidad:
            Valida el username ingresado para iniciar sesión y transfiere el registro
            del jugador a la función conectada en alIniciarSesion.

        Entrada:
            - Ninguna.

        Salida:
            - Ninguna: Inicia la sesión del jugador y abre el menú principal sin retornar un valor.
        """
        try:
            jugador = iniciarSesion(entradaUsernameSesion.get())

            if alIniciarSesion:
                if not ventanaPadre:
                    ventana.destroy()
                alIniciarSesion(jugador)
            else:
                messagebox.showinfo(
                    "Sesion iniciada",
                    "Bienvenido, " + jugador[0][1] + " " + jugador[0][2] + "."
                )
        except (ValueError, OSError, pickle.UnpicklingError, EOFError) as error:
            messagebox.showerror("No se pudo iniciar sesion", str(error))

    tk.Button(
        marcoSesion, text="Iniciar sesion", command=entrar, width=18
    ).grid(row=1, column=0, columnspan=2, pady=(10, 2))

    tk.Label(
        ventana,
        text="Los datos se guardan localmente en el archivo jugadores.",
        font=("Arial", 8),
        fg="gray"
    ).pack(pady=8)

    if not ventanaPadre:
        ventana.mainloop()

    return ventana
