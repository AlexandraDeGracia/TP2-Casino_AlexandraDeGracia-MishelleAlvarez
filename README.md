# TP2-Casino_AlexandraDeGracia-MishelleAlvarez

## 1. Nombre del proyecto
TP2 - Casino

## 2. Enlace del repositorio
https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez

## 3. Integrantes
- Mishelle Álvarez (E1)
- Alexandra De Gracia (E2)

## 4. División del trabajo

Nos dividimos las partes del proyecto siguiendo las entregas de E1 y E2:

- **E1 – Mishelle Álvarez:** Se encargó de la ventana de inicio de sesión y registro (`sesion.py`: `crearVentanaSesion`, `iniciarSesion`, `registrarDesdeFormulario`, `validarRegistro`), todo el manejo del archivo binario con `pickle` (`datos.py`: `obtenerRutaArchivo`, `validarEstructuraJugador`, `validarArchivoJugadores`, `cargarJugadores`, `guardarJugadores`, `buscarJugador`, `registrarJugador`, `guardarCambiosJugador`, `consultarDinero`, `consultarFichas`, `comprarFichas`, `canjearFichas`, `actualizarPuntaje`), y los módulos de ruleta (`ruleta`), blackjack (`blackjack`), ranking (`ranking`) y análisis (`analisis`).
- **E2 – Alexandra De Gracia (`casino.py`):** Se encargó de unir el arranque del programa con la sesión de E1 (`iniciar_aplicacion`, `conectar_modulo_e1`, `limpiar_jugador_actual`, `cargar_desde_estructura_e1`, `iniciar_sesion_e2`, `guardar_datos_e1`, `abrir_ventana_sesion_e1`, `cerrar_sesion_e1`, `abrir_funcionalidad_e1`), el menú principal (`menu_principal`), la ventana de juegos (`ventana_juegos`), el juego de tragamonedas (`tragamonedas`), el juego de dados (`dados`), la ventana para comprar y canjear fichas (`ventana_fichas`) y la revisión de la documentación interna.

---

## 5. Estructuras de datos

### 5.1. Estructura principal del jugador (`jugador_actual`)
Tanto en `casino.py` como en `datos.py` y `sesion.py` trabajamos con la misma lista para representar al jugador que tiene la sesión abierta y guardarlo en el archivo `jugadores`:

```python
[(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]
```

#### Cómo está armada la lista en el código:
- **Posición `0` — `(username, nombre, apellido)` (`tuple`):**
  - `username` (`str`): usuario único del jugador (`jugador_actual[0][0]`).
  - `nombre` (`str`): nombre del jugador (`jugador_actual[0][1]`).
  - `apellido` (`str`): apellido del jugador (`jugador_actual[0][2]`).
- **Posición `1` — `[dinero, rojas, azules, verdes, blancas]` (`list` con un `float` y cuatro `int`):**
  - Índice `0` — `dinero` (`float`): dinero disponible en dólares (`jugador_actual[1][0]`).
  - Índice `1` — `rojas` (`int`): fichas rojas de `$10` (`jugador_actual[1][1]`).
  - Índice `2` — `azules` (`int`): fichas azules de `$50` (`jugador_actual[1][2]`).
  - Índice `3` — `verdes` (`int`): fichas verdes de `$20` (`jugador_actual[1][3]`).
  - Índice `4` — `blancas` (`int`): fichas blancas de `$5` (`jugador_actual[1][4]`).
- **Posición `2` — `puntaje` (`int`):** puntos acumulados por el jugador en las partidas (`jugador_actual[2]`).

Para leer y actualizar las fichas según el color elegido sin tener listas repetidas, usamos en `casino.py` las funciones `obtener_indice_color(color_ficha)` (que devuelve del `1` al `4` según el color, o `-1` si no existe), `obtener_fichas_color(color_ficha)`, `obtener_llave_color_e1(color_ficha)` y `obtener_valor_ficha(color_ficha)`.

### 5.2. Constantes, matrices y diccionarios en `datos.py` y `casino.py`
- **En `datos.py`:**
  - `NOMBRE_ARCHIVO` (`str`): `"jugadores"` (nombre del archivo binario donde guardamos los jugadores con `pickle`).
  - `VALOR_FICHAS` (`dict`): `{"rojas": 10, "azules": 50, "verdes": 20, "blancas": 5}` (diccionario con el precio en dólares de cada color de ficha).
- **En `casino.py`:**
  - `ORDEN_COLORES` (`list`): `["Rojo", "Azul", "Verde", "Blanco"]`.
  - `PUNTOS_GANAR` (`int`): `2` (puntos que se suman al ganar una partida).
  - `PUNTOS_PERDER` (`int`): `-1` (puntos que se restan al perder).
  - `MULTIPLICADOR_TRAGAMONEDAS` (`int`): `2` (paga el doble cuando salen tres símbolos iguales).
  - `PASOS_ANIMACION` (`int`): `15` (cantidad de cambios que hacen los rodillos antes de detenerse).
  - `INTERVALO_ANIMACION_MS` (`int`): `150` (milisegundos entre cada cambio del giro).
  - `MATRIZ_RODILLOS` (`list` de 3 `list`): matriz de `3x5` con los cinco símbolos de cada rodillo (`"Cereza"`, `"Limon"`, `"Campana"`, `"Estrella"`, `"Siete"`).
  - `COMBINACIONES_GANADORAS` (`dict`): diccionario que usa tuplas de 3 símbolos iguales como llaves y les asigna el multiplicador `2`.
  - `DICCIONARIO_APUESTAS_DADOS` (`dict`): `{"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}`.
  - `MATRIZ_OPCIONES_DADOS` (`list` de 2 `list`): matriz de `2x2` `[["par", "impar"], ["dobles", "sumaExacta"]]` para acomodar los botones en la ventana de dados.
  - `enlaces_e1` (`dict`): diccionario donde guardamos las referencias a las funciones de E1 al iniciar el programa con `conectar_modulo_e1()`.

---

## 6. Decisiones tomadas, opciones descartadas e inconsistencias del enunciado (Condición 11)

Durante el desarrollo encontramos algunos detalles que no estaban del todo claros o tenían diferencias en el enunciado. Siguiendo la **Condición 11**, aquí explicamos qué encontramos y cómo decidimos resolverlo:

### 6.1. Inconsistencias del enunciado (Condición 11)

1. **Dados (puntaje y ventaja matemática del `x12` en suma exacta a `7`):**
   - **Problema encontrado:** En la parte de dados, el enunciado no dice cuántos puntos se ganan o se pierden por jugada, ni aclara si los números del diccionario `{"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}` son multiplicadores. Además, pagar `x12` por igual para cualquier suma exacta entre `2` y `12` no coincide con las probabilidades reales de dos dados: sacar un `7` tiene `6/36` (`1/6`) de probabilidad, por lo que pagar `x12` le da ventaja al jugador con una esperanza matemática de `2` por apuesta (`(6/36) × 12 = 2`, es decir, gana `+1` en promedio por jugada), mientras que sacar `2` o `12` solo tiene `1/36` de probabilidad (esperanza de `12/36 = 1/3`).
   - **Cómo lo resolvimos (decisión consciente):** Como decisión consciente del diseño, preferimos dejar el diccionario tal cual viene en el enunciado (`{"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}`) usando esos valores como multiplicadores directos (incluyendo el `x12` cuando se apuesta al `7`) para no cambiar la estructura pedida. Para el puntaje, aplicamos la misma regla del resto del casino: `+2` puntos al ganar y `-1` punto al perder.

2. **Tragamonedas (ejemplo con pagos de 50 y 20 vs. duplicar las fichas):**
   - **Problema encontrado:** El ejemplo del enunciado menciona pagos fijos de `50` y `20`, pero la explicación de las reglas dice que al sacar tres símbolos iguales se duplican las fichas apostadas.
   - **Cómo lo resolvimos:** Nos guiamos por la regla general y usamos el multiplicador `2` (`MULTIPLICADOR_TRAGAMONEDAS = 2`) en `COMBINACIONES_GANADORAS` para duplicar la apuesta cuando los tres rodillos coinciden, descartando los pagos fijos de `50` y `20`.

3. **Dinero inicial al registrar un jugador nuevo:**
   - **Problema encontrado:** El enunciado no indica explícitamente con cuánto dinero debe empezar un jugador recién registrado y tampoco pide una ventana para recargar o depositar dinero.
   - **Qué pasaba si empezaba en `$0.00`:** Si un usuario nuevo se creaba con `[0.0, 0, 0, 0, 0]`, entraba al casino con `$0.00` y `0` fichas. Como la ficha más barata (la blanca) cuesta `$5`, el jugador quedaba bloqueado desde el inicio sin poder comprar fichas en `ventana_fichas()` ni apostar en ningún juego.
   - **Cómo lo resolvimos:** Definimos un dinero inicial de `$100.00` (`[100.0, 0, 0, 0, 0]`) en la función `registrarJugador()` de `datos.py`. Elegimos `$100.00` porque se ajusta bien a los precios de las fichas (`$5`, `$10`, `$20` y `$50`) y a la apuesta mínima de `1` ficha, permitiendo que cualquier usuario recién registrado pueda comprar fichas de todos los colores (por ejemplo, hasta `2` azules, `5` verdes, `10` rojas o `20` blancas) y probar los juegos de inmediato.

### 6.2. Otras decisiones que tomamos en el código

1. **Descuento de fichas al apostar:**
   - **Lo que hicimos:** Descontar las fichas apenas inicia la jugada (`modificar_fichas_juego(-apuesta, color_ficha)`) y, si el jugador gana, entregarle `apuesta * multiplicador` en `liquidar_resultado_apuesta()`.
   - **Lo que descartamos:** No descontar la apuesta al principio y sumar `apuesta * multiplicador` al final, porque eso le regalaba al jugador las fichas que había puesto en la mesa.
2. **Apuestas respetando el color de ficha:**
   - **Lo que hicimos:** Agregar un selector de color (`Rojo`, `Azul`, `Verde`, `Blanco`) en los juegos para que la apuesta se descuente y se pague en ese mismo color dentro de `jugador_actual[1]`.
   - **Lo que descartamos:** Restar fichas mezclando colores o pagar siempre con fichas blancas, porque eso cambiaba el valor en dólares que tenía el jugador.
3. **Animación de los rodillos y bloqueo de la ventana en Tragamonedas:**
   - **Lo que hicimos:** Mover cada rodillo por índice dentro de `MATRIZ_RODILLOS` durante `15` pasos de `150` ms (`2.25` segundos en total) usando `after()`. Mientras los rodillos están girando, se deshabilitan los botones y también se bloquea el cierre con la `X` de la ventana (`WM_DELETE_WINDOW`).
   - **Lo que descartamos:** Dejar que el usuario cierre la ventana en pleno giro, porque ya se le habían descontado las fichas y la jugada quedaba a medias sin sumar ni restar puntos.
4. **Manejo de ventanas en Tkinter:**
   - **Lo que hicimos:** Mantener una sola ventana raíz `tk.Tk()` (`asegurar_ventana_raiz()`) y abrir las demás pantallas como `tk.Toplevel()` (`preparar_ventana_e2()`, incluyendo el login de `sesion.py`), con un único `mainloop()`.
   - **Lo que descartamos:** Crear varios `tk.Tk()` o llamar a `mainloop()` en cada módulo, ya que eso daba problemas al cambiar entre la sesión y el menú principal.
5. **Validación de números enteros con `isdecimal()`:**
   - **Lo que hicimos:** Unificar la revisión de campos numéricos en `validar_entero(texto, nombre_campo, permitir_cero=False)` usando `isdecimal()` en vez de `isdigit()`.
   - **Lo que descartamos:** Usar `isdigit()` o tener dos funciones casi iguales con `try/except`, porque `isdigit()` acepta caracteres como `"²"` que luego fallan al hacer `int("²")`.
6. **Unificación de la compra y canje de fichas con `datos.py`:**
   - **Lo que hicimos:** En lugar de tener dos diccionarios de precios distintos, `casino.py` consulta directamente `datos.VALOR_FICHAS`, y cuando el jugador confirma una compra o un canje en `ventana_fichas()`, se llaman las funciones `datos.comprarFichas()` y `datos.canjearFichas()`, las cuales actualizan los saldos y guardan en el archivo `jugadores`.
   - **Lo que descartamos:** Mantener un diccionario `valores_fichas` repetido y funciones separadas (`aplicar_compra_fichas` y `aplicar_canje_fichas`) que no guardaban en el archivo de E1.
7. **Guardado de cambios y limpieza al cerrar sesión:**
   - **Lo que hicimos:** Al iniciar sesión se comprueba con `datos.validarEstructuraJugador()` que el registro esté completo antes de abrir el menú. Al terminar cada jugada o cerrar sesión se guarda el progreso con `datos.guardarCambiosJugador(jugador_actual)`. Si falla el guardado, se avisa con un mensaje de error en vez de decir que todo salió bien. Al cerrar sesión, `limpiar_jugador_actual()` deja `jugador_actual` en blanco antes de volver al login.
   - **Lo que descartamos:** Dejar los datos del usuario anterior cargados en `jugador_actual` al salir de la sesión.

---

## 7. Avances por integrante y funciones del proyecto

### 7.1. Parte de E1 (Mishelle Álvarez – `sesion.py` y `datos.py`)

#### Lo que ya está implementado en `sesion.py` y `datos.py`:
- **`sesion.crearVentanaSesion(alIniciarSesion=False, ventanaPadre=False)`:** Arma la ventana para registrarse o iniciar sesión con el `username`. Recibe `ventanaPadre` desde `casino.py` para abrirse dentro del mismo flujo de Tkinter y, cuando el jugador entra, llama a `casino.iniciar_sesion_e2(jugador)`.
- **`sesion.iniciarSesion(username)`:** Revisa que el campo no esté vacío y busca al jugador en el archivo con `datos.buscarJugador(username)`.
- **`sesion.registrarDesdeFormulario(username, nombre, apellido)` y `sesion.validarRegistro(username, nombre, apellido)`:** Comprueban que los tres datos estén escritos y crean al jugador con `datos.registrarJugador()`.
- **`datos.obtenerRutaArchivo()`, `datos.validarEstructuraJugador(jugador)` y `datos.validarArchivoJugadores()`:** Se encargan de ubicar el archivo `jugadores` y revisar que los datos guardados no estén corruptos ni incompletos.
- **`datos.cargarJugadores()` y `datos.guardarJugadores(jugadores)`:** Leen y guardan la lista de jugadores en binario con `pickle`.
- **`datos.buscarJugador(username, jugadores=None)` y `datos.registrarJugador(username, nombre, apellido)`:** Buscan un usuario existente o registran uno nuevo dándole `$100.00` de dinero inicial (`[100.0, 0, 0, 0, 0]`) y `0` puntos.
- **`datos.guardarCambiosJugador(jugador)`:** Actualiza los datos del jugador activo dentro del archivo `jugadores`.
- **`datos.comprarFichas(jugador, cantidades)` y `datos.canjearFichas(jugador, cantidades)`:** Calculan el total con `datos.VALOR_FICHAS`, actualizan el dinero y las fichas del jugador y guardan los cambios en el archivo.
- **`datos.consultarDinero(jugador)`, `datos.consultarFichas(jugador)` y `datos.actualizarPuntaje(jugador, cantidad)`:** Funciones de apoyo para consultar saldos y modificar el puntaje.

#### Módulos de E1 que faltan por subir:
- **`ruleta`**, **`blackjack`**, **`ranking`** y **`analisis`**. Mientras se terminan de integrar, los botones en `casino.py` usan `abrir_funcionalidad_e1()` para avisar si el módulo aún no está conectado.

### 7.2. Parte de E2 (Alexandra De Gracia – `casino.py`)
- **`iniciar_aplicacion()`:** Punto de arranque del programa. Crea la ventana raíz, abre el login de E1 y pone a correr el `mainloop()`.
- **`menu_principal()`:** Muestra el `username` del jugador, su dinero disponible (`$0.00`), el total de fichas, sus puntos y cuántas fichas tiene de cada color. Incluye los botones `"Jugar"`, `"Fichas"`, `"Ranking"`, `"Análisis"` y `"Cerrar sesión"` (que pide confirmación, guarda los datos y limpia la sesión).
- **`ventana_juegos()`:** Muestra las fichas disponibles del jugador (`calcular_total_fichas()`), el valor total en dólares de sus fichas (`calcular_valor_monetario_fichas()`), el detalle por color con su precio (`Rojas ($10)`, `Azules ($50)`, `Verdes ($20)`, `Blancas ($5)`), los puntos acumulados, los botones hacia los cuatro juegos (`Ruleta`, `Tragamonedas`, `Blackjack` y `Dados`) y el botón `"Volver al menú principal"`.
- **`ventana_fichas()`:** Permite comprar y canjear fichas viendo en pantalla el dinero disponible (`$0.00`) y una tabla con la cantidad actual y el valor de cada color. Valida que no se ingresen letras ni símbolos inválidos, que no se haga una operación en cero, que alcance el dinero al comprar y que alcancen las fichas al canjear. Antes de aplicar el cambio pide confirmación con `messagebox.askyesno` y guarda todo en el archivo `jugadores`.
- **`tragamonedas()` (Entrada 3):** Corresponde a la **Entrada 3 del Drive: tragamonedas**:
  - **Matriz de rodillos y diccionario de combinaciones:** Usa `MATRIZ_RODILLOS` (`3x5` con `"Cereza"`, `"Limon"`, `"Campana"`, `"Estrella"` y `"Siete"`) y `COMBINACIONES_GANADORAS` (tuplas de 3 símbolos iguales con multiplicador `x2`).
  - **Ventana de tragamonedas y selección de fichas a apostar:** Construye la interfaz gráfica con los tres rodillos, el panel de saldo, el selector de color de ficha (`crear_selector_color_ficha()`), el campo de entrada de apuesta (`crear_campo_entrada_apuesta()`) y la validación por color (`validar_apuesta_por_color()`).
  - **Giro de rodillos y evaluación del resultado:** Al presionar `"Girar"`, descuenta las fichas apostadas, recorre los rodillos durante `15` pasos con `after()` (`iniciar_giro()`, `animar_rodillos()`, `avanzar_indices_rodillos()`), evalúa si los tres símbolos finales coinciden (`finalizar_giro()`, `evaluar_resultado_tragamonedas()`), actualiza fichas y puntos (`liquidar_resultado_apuesta()`) y guarda en el archivo `jugadores`.
- **`dados()`:** Permite apostar por color de ficha a `"par"`, `"impar"`, `"dobles"` o `"sumaExacta"` (validando que la suma elegida esté entre `2` y `12`), lanza los dos dados con `random.randint(1, 6)`, muestra el resultado y actualiza fichas y puntaje.

---

## 8. Estado actual del proyecto

### Implementado
- **En `casino.py` (E2 – Alexandra De Gracia):**
  - Conexión completa con `datos.py` y `sesion.py` usando una sola ventana raíz `tk.Tk()`.
  - `menu_principal()`, `ventana_juegos()`, `ventana_fichas()`, `tragamonedas()` y `dados()`.
  - Entrada 3 completa: matriz de rodillos, diccionario de combinaciones, ventana de tragamonedas, apuesta con fichas y giro de rodillos.
  - Validación de enteros con `isdecimal()` en `validar_entero()` y docstrings de las `62` funciones ajustados al formato de la Condición 12 (`- nombre(tipo): Descripción.`, `- Ninguna.` y `- Ninguna: ...`).
- **En `datos.py` y `sesion.py` (E1 – Mishelle Álvarez):**
  - Guardado y lectura en `pickle`, registro con `$100.00` de dinero inicial (`[100.0, 0, 0, 0, 0]`), inicio de sesión conectado al menú principal, compra y canje con `VALOR_FICHAS`, y docstrings de las `13` funciones de `datos.py` y las `6` funciones de `sesion.py` en el formato de la Condición 12.

### Probado
- **Verificado mediante compilación:**
  - Los tres archivos (`casino.py`, `datos.py` y `sesion.py`) compilan sin errores con `python -m py_compile`.
  - Se revisó mediante análisis sintáctico (`ast`) que las `81` funciones del proyecto tengan su docstring completo con `Funcionalidad:`, `Entrada:` y `Salida:` en líneas separadas y con el formato `- nombre(tipo): Descripción.` (o `- Ninguna.` / `- Ninguna: ...` cuando no reciben parámetros o no retornan valor).
- **Verificado mediante prueba de lógica:**
  - Prueba de `validar_entero()` con entradas válidas (`"123"`, `"0"` cuando se permite cero, `"１２３"`) e inválidas (`"0"` en apuestas, `"-5"`, `"12.5"`, `"abc"`, `""` y `"²"`, confirmando que `isdecimal()` rechaza `"²"`).
  - Pruebas de cálculo de fichas, validación de apuestas por color, resultados de dados y combinaciones de tragamonedas.
- **Verificado mediante integración:**
  - Registro de un jugador nuevo en `datos.registrarJugador()` verificando que inicia con `$100.00` (`[100.0, 0, 0, 0, 0]`), inicio de sesión hacia `menu_principal()`, y rechazo de registros incompletos o con formato inválido.
  - Compra y canje de fichas guardando en el archivo `jugadores`, actualización de puntaje y fichas después de jugar en dados y tragamonedas, y limpieza de `jugador_actual` al cerrar sesión para que otro usuario pueda entrar sin que se mezclen los datos.

### Pendiente
- Subir e integrar los cuatro módulos restantes de **E1 (Mishelle Álvarez)**: `ruleta`, `blackjack`, `ranking` y `analisis`.
- Verificación manual de la interfaz gráfica ejecutando `python casino.py` con un jugador de prueba (abrir manualmente cada ventana, comprobar visualmente la animación de los rodillos de tragamonedas y el bloqueo del botón `X` durante el giro).

---

## 9. Instrucciones para ejecutar el programa

- **Versión de Python:** Python 3.5.1 o superior.
- **Archivos necesarios:** `casino.py`, `datos.py` y `sesion.py` en la misma carpeta.
- **Librerías:** Solo librerías estándar de Python (`tkinter`, `random`, `pickle` y `os`).
- **Cómo iniciarlo:**
  ```bash
  python casino.py
  ```
- **Resumen de cómo funciona al abrirlo:**
  1. Al correr `python casino.py`, se abre la ventana de sesión (`sesion.py`).
  2. Ahí se puede registrar un jugador nuevo (que empieza con `$100.00` de dinero disponible) o escribir el `username` de uno ya registrado y darle a `"Iniciar sesion"`.
  3. Al iniciar sesión se abre el `menu_principal()`, desde donde se puede entrar a `"Fichas"` (`ventana_fichas()`) para comprar fichas con los `$100.00` iniciales o canjearlas por dinero, y a `"Jugar"` (`ventana_juegos()`) para entrar a `Tragamonedas` o `Dados`.
  4. Cada compra, canje o jugada guarda automáticamente los cambios del jugador en el archivo binario `jugadores`.
  5. Al presionar `"Cerrar sesión"` y confirmar que `"Sí"`, se guardan los datos, se limpia la estructura en memoria y vuelve a salir la ventana de inicio de sesión.

---

## 10. Organización de archivos y notas del equipo

### 10.1. Archivos del repositorio y seguimiento Scrum
- `casino.py`: archivo principal desde donde se corre el programa (`python casino.py`). Contiene toda la parte de **E2 (Alexandra De Gracia)**: integración general, menú principal, ventana de juegos, tragamonedas, dados y ventana gráfica de compra y canje de fichas.
- `datos.py`: módulo de **E1 (Mishelle Álvarez)** que maneja el archivo binario `jugadores` con `pickle`, el diccionario `VALOR_FICHAS` y las funciones que actualizan el dinero, las fichas y el puntaje en disco.
- `sesion.py`: módulo de **E1 (Mishelle Álvarez)** con la interfaz de registro e inicio de sesión por `username`.
- **Seguimiento Scrum:** El seguimiento Scrum de las etapas del proyecto y las evidencias (incluyendo la **Entrada 3 del Drive: tragamonedas**) se encuentran registrados en la carpeta compartida de Google Drive del equipo.

### 10.2. Relación entre E1 y E2 en el manejo de fichas
La interfaz gráfica de `ventana_fichas()`, la tabla de inventario, los cuadros de confirmación y las validaciones de lo que escribe el usuario pertenecen a **E2 (`casino.py`)**, mientras que `datos.py` (**E1**) aporta el diccionario `VALOR_FICHAS` y las funciones `comprarFichas`, `canjearFichas` y `guardarCambiosJugador` para que todo quede guardado en el archivo `jugadores`.

### 10.3. Nota sobre el uso de Inteligencia Artificial
La Inteligencia Artificial (IA) se utilizó únicamente para los docstrings (redacción y ajuste del formato de documentación interna pedido en la Condición 12).
