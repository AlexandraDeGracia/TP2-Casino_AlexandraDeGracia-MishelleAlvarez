"""
Modulo de interfaz de sesion del casino.
Permite registrar jugadores e iniciar sesion por username.
"""

import tkinter as tk
from tkinter import messagebox

import datos


def validarRegistro(username, nombre, apellido):
    """Valida que los tres campos del registro esten completos."""
    return bool(username.strip() and nombre.strip() and apellido.strip())


def iniciarSesion(username):
    """Busca el jugador y devuelve su registro si existe."""
    if not username.strip():
        raise ValueError("Escriba su username.")

    jugador = datos.buscarJugador(username)
    if jugador is None:
        raise ValueError("No existe un jugador con ese username.")

    return jugador


def registrarDesdeFormulario(username, nombre, apellido):
    """Valida y registra los datos recibidos desde la ventana."""
    if not validarRegistro(username, nombre, apellido):
        raise ValueError("Complete username, nombre y apellido.")

    return datos.registrarJugador(username, nombre, apellido)


def crearVentanaSesion(alIniciarSesion=None):
    """
    Crea la ventana de registro e inicio de sesion.

    alIniciarSesion: funcion opcional que recibe el jugador seleccionado.
    Se utiliza para conectar esta ventana con el menu principal del equipo.
    """
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
        except (ValueError, OSError) as error:
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
        try:
            jugador = iniciarSesion(entradaUsernameSesion.get())

            if alIniciarSesion is not None:
                ventana.destroy()
                alIniciarSesion(jugador)
            else:
                messagebox.showinfo(
                    "Sesion iniciada",
                    "Bienvenido, " + jugador[0][1] + " " + jugador[0][2] + "."
                )
        except (ValueError, OSError) as error:
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

    ventana.mainloop()
