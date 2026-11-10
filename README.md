# TP2 - Casino

Aplicación de casino desarrollada en Python con interfaz gráfica mediante Tkinter. Permite registrar e iniciar sesión, administrar dinero y fichas, consultar el puntaje y jugar a los juegos disponibles.

## 1. Descripción del proyecto

Creamos un casino virtual en el que cada jugador tiene un perfil. Guardamos sus datos en un archivo binario con `pickle` para conservar el dinero, las fichas y el puntaje entre sesiones.

## 2. Integrantes y distribución del trabajo

- **Mishelle Álvarez (E1):** trabajó en el registro y el inicio de sesión (`sesion.py`), el almacenamiento y la administración de jugadores (`datos.py`), y los módulos de ruleta, blackjack, ranking y análisis.

- **Alexandra De Gracia (E2 – `casino.py`):** trabajó en la integración con E1, el menú principal, la ventana de juegos, tragamonedas, dados, la ventana de compra y canje de fichas y la documentación interna.

## 3. Repositorio

https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez.git

## 4. Funcionalidades

- Registrar jugadores e iniciar sesión mediante `username`.

- Mostrar el menú principal con el usuario, dinero, fichas y puntaje.

- Comprar y canjear fichas, validando las cantidades, el saldo y la disponibilidad.

- Guardar y cargar la información de los jugadores mediante `pickle`.

- Acceder a la ventana de juegos desde el menú.

- **Tragamonedas:**

  - Seleccionar el color y la cantidad de fichas para apostar.

  - Animar los tres rodillos mediante `after()` en aproximadamente 1,8 segundos (12 pasos de 150 ms), sin bloquear la ventana y dentro del máximo de 5 segundos.

  - Validar que el jugador tenga suficientes fichas del color elegido antes de girar.

  - Evaluar las combinaciones ganadoras usando el diccionario y liquidar la apuesta.

  - Actualizar las fichas y el puntaje: `+2` al ganar y `−1` al perder.

  - Mostrar los botones **Girar / Jugar otra vez** y **Regresar a juegos**.

- **Dados:**

  - Lanzar dos dados y representar el resultado como una tupla de dos valores.

  - Permitir apuestas de **par**, **impar**, **dobles** y **suma exacta**, de acuerdo con las opciones del juego.

  - Validar que haya fichas suficientes antes de realizar la apuesta.

  - Aplicar los pagos definidos en el diccionario y actualizar fichas y puntaje (`+2` al ganar y `−1` al perder).

  - Mostrar los botones **Lanzar dados** y **Regresar a juegos**.

- Conectar los juegos con la ventana de juegos y permitir regresar a ella mediante **Regresar a juegos**, no al menú principal.

- Guardar los cambios del jugador después de las operaciones y jugadas.

## 5. Estructura del proyecto (archivos)

- **`casino.py`:** Punto de entrada de E2. Integra la sesión, el menú principal, la ventana de juegos, tragamonedas, dados y la administración gráfica de fichas.

- **`datos.py`:** Módulo de E1 para leer, guardar, buscar y actualizar jugadores, dinero, fichas y puntaje usando `pickle`.

- **`sesion.py`:** Módulo de E1 con las ventanas de registro e inicio de sesión.

- **`jugadores`:** Archivo binario donde se guardan los datos persistentes de los jugadores.

- **`ruleta.py`, `blackjack.py`, `ranking.py` y `analisis.py`:** Módulos de E1 que se incorporarán o integrarán al programa.

## 6. Estructuras de datos

### Estructura del jugador

Representamos al jugador con la siguiente estructura:

```python

[(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]

```

- **Posición 0 — tupla:** `username`, `nombre` y `apellido` (cadenas).

- **Posición 1 — lista:** dinero disponible (`float`) y cantidad de fichas por color (`int`).

  - Rojas: `$10`

  - Azules: `$50`

  - Verdes: `$20`

  - Blancas: `$5`

- **Posición 2 — entero:** puntaje acumulado.

### Constantes, matrices y diccionarios principales

`colores`, `matrizRodillos`, `combinacionesGanadoras`, `pagosDados`, `matrizOpcionesDados` y `modulosE1`

- `datos.VALOR_FICHAS`: diccionario con el valor monetario de cada color.

- `colores`: lista con los colores de fichas.

- En `liquidar`, sumamos `2` puntos al ganar y restamos `1` al perder.

- `matrizRodillos`: matriz de 3 rodillos con 5 símbolos disponibles.

- `combinacionesGanadoras`: diccionario de combinaciones ganadoras de tragamonedas y su multiplicador.

- `pagosDados`: diccionario de multiplicadores para las apuestas de dados (`par`, `impar`, `dobles`, `sumaExacta`).

- `matrizOpcionesDados`: matriz que organiza las opciones de apuestas de dados.

- `modulosE1`: diccionario con referencias a las funciones de E1 conectadas desde `casino.py`.

## 7. Decisiones tomadas

- **Descontar la apuesta al iniciar la jugada:** primero retiramos las fichas apostadas y, si el jugador gana, entregamos el pago correspondiente. Así evitamos duplicar el saldo.

- **Mantener el color de ficha seleccionado:** descontamos y pagamos en el mismo color para conservar su valor.

- **Usar `after()` en la animación:** programamos los cambios de los rodillos sin bloquear la ventana de Tkinter.

- **Usar una única ventana raíz `tk.Tk()`:** creamos las ventanas secundarias con `tk.Toplevel()` y mantenemos un solo `mainloop()`.

- **Centralizar la administración de fichas en `datos.py`:** reutilizamos `VALOR_FICHAS`, `comprarFichas()` y `canjearFichas()` en lugar de duplicar la lógica.

- **Guardar el progreso al finalizar las operaciones:** persistimos los cambios de dinero, fichas y puntaje en el archivo `jugadores`.

- **Asignar `$100.00` de dinero inicial:** damos este monto al registrar un jugador nuevo para que pueda comprar fichas y comenzar a jugar.

- **Registro con username:** el nombre de usuario funciona como identificador para buscar al jugador.

## 8. Decisiones descartadas

- No descontar la apuesta al comenzar y pagar únicamente al final, porque podría duplicar el saldo.

- No mezclar fichas de distintos colores ni pagar en un color diferente al apostado.

- En tragamonedas, no permitir cerrar la ventana durante la animación si eso deja una apuesta descontada sin liquidar.

- No crear varias ventanas raíz `Tk()` ni múltiples llamadas a `mainloop()`.

- No duplicar los diccionarios de precios ni la lógica de compra y canje que ya existe en `datos.py`.

- En tragamonedas, usamos el multiplicador de las reglas generales en lugar de los pagos fijos de ejemplo de `$50` y `$20`.

## 9. Inconsistencias del enunciado

- **Dados:** el enunciado no especifica claramente el puntaje por jugada ni si los valores de `DICCIONARIO_APUESTAS_DADOS` son multiplicadores. Conservamos el diccionario indicado (`par: 2`, `impar: 2`, `dobles: 5`, `sumaExacta: 12`) y aplicamos la regla de puntaje de `+2` al ganar y `−1` al perder. El pago `x12` a cualquier suma exacta no considera que las sumas tienen probabilidades diferentes.

- **Tragamonedas:** el ejemplo presenta pagos fijos de `$50` y `$20`, mientras que las reglas generales indican duplicar la apuesta cuando coinciden los tres símbolos. Aplicamos el multiplicador `x2`.

- **Dinero inicial:** el enunciado no define un monto inicial. Establecimos `$100.00` para que un jugador nuevo pueda adquirir fichas desde el comienzo.

## 10. Archivos que genera el programa

- **`jugadores`:** archivo binario que almacena la información de los jugadores con `pickle`.

## 11. Ejecución del programa

### Requisitos

- Python 3.5.1.

- Módulos estándar: `tkinter`, `random`y `pickle`.

- Tener `casino.py`, `datos.py` y `sesion.py` en la misma carpeta, junto con los módulos E1 que estén integrados.

### Comandos de ejecución

`python casino.py` (o `py casino.py` en Windows).

### Flujo general

1 Se abre la ventana de registro e inicio de sesión.

2 El jugador puede registrarse (con `$100.00` iniciales) o iniciar sesión con un usuario existente.

3 Se muestra el menú principal.

4 Desde **Fichas**, puede comprar o canjear fichas; desde **Jugar**, accede a la ventana de juegos.

5 Las compras, los canjes y las jugadas actualizan y guardan los datos del jugador.

6 Al cerrar sesión, guardamos el progreso, limpiamos los datos de la sesión y regresamos a la ventana de inicio de sesión.

## 12. Estado actual

### Funcionalidades implementadas

- Integramos `casino.py` con `datos.py` y `sesion.py`.

- Implementamos el menú principal, la ventana de juegos y la ventana de compra y canje de fichas.

- Implementamos la lógica de tragamonedas y dados descrita en la sección 4.

- Guardamos los datos de los jugadores mediante `pickle`.

- Validamos números enteros con `isdecimal()` y documentamos las funciones.

### Pendiente

- Integrar los módulos de ruleta, blackjack, ranking y análisis de E1.

- Ejecutar y registrar las pruebas antes de documentarlas como realizadas: `python -m py_compile casino.py datos.py sesion.py`; validación de números enteros, cálculo de fichas, apuestas, resultados de dados y combinaciones de tragamonedas; registro, inicio de sesión, compra y canje de fichas, actualización de datos y cierre de sesión.

- Realizar la prueba manual completa de la interfaz gráfica: revisar visualmente la animación durante el giro y comprobar el comportamiento del cierre de ventana (`X`) de tragamonedas mientras se ejecuta la animación.

## 13 Nota sobre el uso de Inteligencia Artificial

La Inteligencia Artificial (IA) se utilizó únicamente para los docstrings (redacción y ajuste del formato de documentación interna pedido en la Condición 12).


**Última actualización:** 10 de noviembre de 2026.
