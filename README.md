# TP2-Casino_AlexandraDeGracia-MishelleAlvarez

## 1. Nombre del proyecto
TP2 - Casino

## 2. Enlace del repositorio
https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez

## 3. Integrantes
- Mishelle Álvarez (E1)
- Alexandra De Gracia (E2)

## 4. División del trabajo

- **E1 – Mishelle Álvarez:** Ventana de sesión (`ventana_sesion`), ruleta (`ruleta`), blackjack (`blackjack`), ranking (`ranking`), análisis (`analisis`), cerrar sesión (`cerrar_sesion`) y manejo y almacenamiento de datos con `pickle` (`guardar_datos`).
- **E2 – Alexandra De Gracia:** Punto de arranque e integración (`iniciar_aplicacion`), menú principal (`menu_principal`), ventana de juegos (`ventana_juegos`), tragamonedas (`tragamonedas`), dados (`dados`), ventana de fichas (`ventana_fichas`) y documentación interna.

---

## 5. Estructuras de datos

### 5.1. Estructura principal compartida entre E1 y E2 (`jugador_actual`)
El registro del jugador activo en `casino.py` trabaja directamente sobre la estructura posicional establecida por el enunciado para la integración entre E1 y E2 y su persistencia en archivo:

```python
[(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]
```

#### Tipos de datos reales en el código:
- **Posición `0` — `(username, nombre, apellido)` (`tuple`):**
  - `username` (`str`): identificador único de usuario del jugador (`jugador_actual[0][0]`).
  - `nombre` (`str`): nombre del jugador (`jugador_actual[0][1]`).
  - `apellido` (`str`): apellido del jugador (`jugador_actual[0][2]`).
- **Posición `1` — `[dinero, rojas, azules, verdes, blancas]` (`list` con un `float` y cuatro `int`):**
  - Índice `0` — `dinero` (`float`): dinero disponible del jugador en dólares (`jugador_actual[1][0]`).
  - Índice `1` — `rojas` (`int`): cantidad de fichas rojas de `$10` (`jugador_actual[1][1]`).
  - Índice `2` — `azules` (`int`): cantidad de fichas azules de `$50` (`jugador_actual[1][2]`).
  - Índice `3` — `verdes` (`int`): cantidad de fichas verdes de `$20` (`jugador_actual[1][3]`).
  - Índice `4` — `blancas` (`int`): cantidad de fichas blancas de `$5` (`jugador_actual[1][4]`).
- **Posición `2` — `puntaje` (`int`):** puntaje entero acumulado por el jugador en los juegos del casino (`jugador_actual[2]`).

Para consultar y modificar las fichas por color directamente sobre `jugador_actual[1]` sin duplicar estructuras de datos, se utilizan las funciones auxiliares `obtener_indice_color(color_ficha)` (que devuelve los índices `1` a `4` según el color, o `-1` si no existe) y `obtener_fichas_color(color_ficha)`.

### 5.2. Constantes y estructuras auxiliares en `casino.py`
- `valores_fichas` (`dict`): `{"Rojo": 10, "Azul": 50, "Verde": 20, "Blanco": 5}`.
- `ORDEN_COLORES` (`list`): `["Rojo", "Azul", "Verde", "Blanco"]`.
- `PUNTOS_GANAR` (`int`): `2` (puntos otorgados por victoria).
- `PUNTOS_PERDER` (`int`): `-1` (puntos descontados por derrota).
- `MULTIPLICADOR_TRAGAMONEDAS` (`int`): `2` (multiplicador de pago al obtener tres símbolos iguales en tragamonedas).
- `PASOS_ANIMACION` (`int`): `15` (cantidad de pasos de animación en los rodillos de tragamonedas).
- `INTERVALO_ANIMACION_MS` (`int`): `150` (intervalo en milisegundos entre cada paso de animación).
- `MATRIZ_RODILLOS` (`list` de 3 `list`): matriz de 3 filas por 5 símbolos (`"Cereza"`, `"Limon"`, `"Campana"`, `"Estrella"`, `"Siete"`).
- `COMBINACIONES_GANADORAS` (`dict`): diccionario que asocia cada tupla de 3 símbolos iguales con `MULTIPLICADOR_TRAGAMONEDAS` (`2`).
- `DICCIONARIO_APUESTAS_DADOS` (`dict`): `{"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}`.
- `MATRIZ_OPCIONES_DADOS` (`list` de 2 `list`): matriz de 2x2 `[["par", "impar"], ["dobles", "sumaExacta"]]` para posicionar los botones de opción en `dados()`.
- `enlaces_e1` (`dict`): diccionario de referencias para conectar las funciones de E1 (`ventana_sesion`, `ruleta`, `blackjack`, `ranking`, `analisis`, `cerrar_sesion`, `guardar_datos`) mediante `conectar_modulo_e1()`.

---

## 6. Decisiones tomadas y descartadas e inconsistencias del enunciado (Condición 11)

A continuación se documentan las inconsistencias identificadas en el enunciado conforme a la **Condición 11** de las especificaciones, así como las decisiones técnicas adoptadas en el desarrollo del proyecto:

### 6.1. Inconsistencias del enunciado y resolución conforme a la Condición 11

1. **Dados (puntos, diccionario de premios y probabilidades de suma exacta):**
   - **Problema o inconsistencia encontrada:** El enunciado no especifica una regla de asignación de puntos para el juego de dados ni define expresamente si los valores del diccionario de ejemplo `{"par": 2, "impar": 2, "dobles": 5, "sumaExacta": 12}` corresponden a multiplicadores de pago. Asimismo, aplicar un multiplicador único `x12` para cualquier suma exacta entre `2` y `12` no representa una distribución proporcional a la probabilidad real con dos dados (por ejemplo, obtener una suma de `7` tiene `6/36` combinaciones posibles, mientras que obtener `2` o `12` tiene únicamente `1/36`).
   - **Solución adoptada:** El equipo detectó la inconsistencia y, siguiendo la Condición 11, documenta el problema y la solución adoptada: utilizar los valores `2`, `2`, `5` y `12` como multiplicadores directos de la apuesta en `DICCIONARIO_APUESTAS_DADOS`, y asignar `+2` puntos (`PUNTOS_GANAR`) al ganar y `-1` punto (`PUNTOS_PERDER`) al perder para mantener total uniformidad con el sistema general de puntaje del casino.

2. **Tragamonedas (ejemplo de pagos de 50 y 20 frente a duplicar fichas):**
   - **Problema o inconsistencia encontrada:** El ejemplo incluido en el enunciado muestra pagos fijos de `50` y `20`, mientras que la regla general del texto descriptivo indica que al obtener tres símbolos iguales se duplican las fichas apostadas.
   - **Solución adoptada:** El equipo detectó la inconsistencia y, siguiendo la Condición 11, documenta el problema y la solución adoptada: utilizar el multiplicador `2` (`MULTIPLICADOR_TRAGAMONEDAS = 2`) en `COMBINACIONES_GANADORAS` para duplicar la apuesta realizada cuando los tres rodillos coinciden, descartando los valores fijos `50` y `20` del ejemplo.

### 6.2. Decisiones técnicas de diseño

1. **Sistema de apuestas y descuentos de fichas:**
   - **Elegida:** Descontar las fichas apostadas al iniciar la jugada (`modificar_fichas_juego(-apuesta, color_ficha)`) y, en caso de ganar, acreditar el pago completo `apuesta * multiplicador` (`liquidar_resultado_apuesta`).
   - **Descartada:** No descontar la apuesta antes de jugar y sumar `apuesta * multiplicador` al ganar, ya que duplicaba indebidamente las fichas apostadas.
2. **Apuestas por color de ficha:**
   - **Elegida:** Permitir seleccionar el color de ficha (`Rojo`, `Azul`, `Verde`, `Blanco`) antes de apostar y liquidar tanto descuentos como ganancias sobre ese mismo color directamente en `jugador_actual[1]`.
   - **Descartada:** Descontar mezclando colores y acreditar siempre fichas blancas, ya que alteraba el valor monetario del inventario del jugador.
3. **Animación por índices y bloqueo de cierre en Tragamonedas:**
   - **Elegida:** Recorrer secuencialmente por índice cada fila de `MATRIZ_RODILLOS` durante `15` pasos (`PASOS_ANIMACION`) de `150` ms (`INTERVALO_ANIMACION_MS`) (`2.25` segundos en total) con `after()`, bloqueando los botones y el cierre de la ventana mediante la `X` (`WM_DELETE_WINDOW`) mientras `estado_juego["girando"]` está activo.
   - **Descartada:** Permitir cerrar la ventana con la `X` en mitad del giro, lo cual interrumpía la partida cuando la apuesta ya había sido descontada sin procesar el resultado ni los puntos.
4. **Administración de ventanas Tkinter y disposición de controles:**
   - **Elegida:** Utilizar una única instancia raíz `tk.Tk()` mediante `asegurar_ventana_raiz()` y ventanas secundarias `tk.Toplevel()` mediante `preparar_ventana_e2()`, organizando los controles con espaciado compacto y, en `dados()`, una cuadrícula 2x2 (`MATRIZ_OPCIONES_DADOS`) para las opciones de apuesta, con ventanas de `550x620` (`dados`) y `540x580` (`tragamonedas`).
   - **Descartada:** Crear múltiples instancias de `tk.Tk()` o múltiples llamadas a `mainloop()`.
5. **Integración modular entre E1 y `casino.py` (módulo de E2):**
   - **Elegida:** Mantener en `casino.py` exclusivamente las funcionalidades de E2 operando directamente sobre la lista `jugador_actual` y conectar las funciones de E1 mediante el diccionario `enlaces_e1` y la función `conectar_modulo_e1()`.
   - **Descartada:** Mantener dos estructuras de datos separadas para el mismo jugador o crear múltiples ventanas raíz `tk.Tk()` entre E1 y E2.

---

## 7. Documentación de módulos del proyecto (E1 y E2) y persistencia de archivos

### 7.1. Módulos y funciones correspondientes a E1 (Mishelle Álvarez)
Puntos de enlace previstos para las funciones de E1 según el enunciado y el contrato `enlaces_e1`:
- **`ventana_sesion()`:** Ventana de inicio de sesión y registro de jugadores (sin uso de contraseñas, conforme al enunciado). Una vez seleccionado o registrado el jugador activo, transfiere su lista de datos a `iniciar_sesion_e2(registro_jugador)`.
  - Detalle de implementación interna: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`ruleta()`:** Juego de ruleta correspondiente a E1, invocado desde `ventana_juegos()` mediante `abrir_funcionalidad_e1("ruleta", "Ruleta")`.
  - Detalle de implementación interna: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`blackjack()`:** Juego de blackjack correspondiente a E1, invocado desde `ventana_juegos()` mediante `abrir_funcionalidad_e1("blackjack", "Blackjack")`.
  - Detalle de implementación interna: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`ranking()`:** Módulo de ranking correspondiente a E1, invocado desde `menu_principal()` mediante `abrir_funcionalidad_e1("ranking", "Ranking")`.
  - Detalle de implementación interna y archivo HTML: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`analisis()`:** Módulo de análisis correspondiente a E1, invocado desde `menu_principal()` mediante `abrir_funcionalidad_e1("analisis", "Análisis")`.
  - Detalle de implementación interna y archivo CSV: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`cerrar_sesion()`:** Función de cierre de sesión correspondiente a E1, invocada desde `menu_principal()` tras ejecutar `guardar_datos_e1()`.
  - Detalle de implementación interna: `[Pendiente de completar por E1 (Mishelle Álvarez)]`
- **`guardar_datos()`:** Función de persistencia en `pickle` correspondiente a E1, invocada mediante `guardar_datos_e1()`.
  - Detalle de implementación interna y nombre del archivo `pickle`: `[Pendiente de completar por E1 (Mishelle Álvarez)]`

### 7.2. Módulos y funciones correspondientes a E2 (Alexandra De Gracia – `casino.py`)
- **`iniciar_aplicacion()`:** Punto de entrada en `casino.py`. Asegura la única ventana raíz `tk.Tk()` e inicia el flujo de la aplicación por `ventana_sesion()` (si el módulo de E1 está conectado) o abre `menu_principal()` en modo de prueba de E2.
- **`menu_principal()`:** Ventana principal del casino con información del jugador activo y botones de acceso a `ventana_juegos()`, `ventana_fichas()`, `ranking()`, `analisis()` y cierre de sesión.
- **`ventana_juegos()`:** Menú selector de los cuatro juegos del casino (`ruleta`, `blackjack`, `tragamonedas`, `dados`), mostrando el total de fichas (`calcular_total_fichas()`), su valor en dólares (`calcular_valor_monetario_fichas()`) y el desglose por color (`obtener_texto_desglose_fichas()`).
- **`tragamonedas()`:** Juego de tragamonedas apoyado en las funciones `validar_apuesta_por_color()`, `modificar_fichas_juego()`, `avanzar_indices_rodillos()`, `evaluar_resultado_tragamonedas()` y `liquidar_resultado_apuesta()`.
- **`dados()`:** Juego de dados apoyado en las funciones `validar_apuesta_por_color()`, `validar_entero_positivo()`, `ejecutar_jugada_dados()`, `modificar_fichas_juego()`, `generar_tirada_dados()`, `verificar_acierto_dados()` y `liquidar_resultado_apuesta()`.
- **`ventana_fichas()`:** Ventana de compra y canje de fichas apoyada en las funciones `validar_entero_no_negativo()`, `calcular_totales_operacion_fichas()`, `validar_disponibilidad_canje()`, `aplicar_compra_fichas()` y `aplicar_canje_fichas()`.
- **Funciones de acceso y cálculo de fichas:** `obtener_indice_color()`, `obtener_fichas_color()`, `calcular_total_fichas()`, `calcular_valor_monetario_fichas()` y `obtener_texto_desglose_fichas()`.
- **Funciones de administración de ventanas Tkinter:** `asegurar_ventana_raiz()`, `preparar_ventana_e2()`, `cerrar_aplicacion_completa()`, `iniciar_bucle_principal_si_corresponde()`, `crear_titulo_ventana()`, `crear_panel_saldo_juego()`, `actualizar_panel_saldo_juego()`, `crear_campo_entrada_apuesta()`, `crear_boton_estandar()`, `crear_selector_color_ficha()`, `crear_etiquetas_rodillos()` y `crear_tabla_inventario_fichas()`.
- **Funciones de integración con E1:** `conectar_modulo_e1()`, `cargar_desde_estructura_e1()`, `iniciar_sesion_e2()`, `guardar_datos_e1()` y `abrir_funcionalidad_e1()`.

---

## 8. Estado de implementación

### Implementado
- **En `casino.py` (E2 – Alexandra De Gracia):**
  - `iniciar_aplicacion()`
  - `menu_principal()`
  - `ventana_juegos()`
  - `tragamonedas()` (`avanzar_indices_rodillos`, `evaluar_resultado_tragamonedas`, `modificar_fichas_juego`, `liquidar_resultado_apuesta`, `validar_apuesta_por_color`)
  - `dados()` (`ejecutar_jugada_dados`, `generar_tirada_dados`, `verificar_acierto_dados`, `modificar_fichas_juego`, `liquidar_resultado_apuesta`, `validar_apuesta_por_color`)
  - `ventana_fichas()` (`calcular_totales_operacion_fichas`, `validar_disponibilidad_canje`, `aplicar_compra_fichas`, `aplicar_canje_fichas`, `validar_entero_no_negativo`)
  - Funciones de acceso y cálculo de fichas (`obtener_indice_color`, `obtener_fichas_color`, `calcular_total_fichas`, `calcular_valor_monetario_fichas`, `obtener_texto_desglose_fichas`) y de integración con E1 (`conectar_modulo_e1`, `cargar_desde_estructura_e1`, `iniciar_sesion_e2`, `guardar_datos_e1`, `abrir_funcionalidad_e1`).

### Probado
- Compilación y verificación estática de sintaxis de `casino.py` mediante `py_compile` sin errores.
- Revisión del formato de docstrings (`Funcionalidad`, `Entrada`, `Salida`) en las funciones de `casino.py`.

### Pendiente
- Pruebas interactivas en la interfaz gráfica con un jugador de prueba (apuestas en tragamonedas y dados, compra y canje de fichas, validaciones de campos y respuesta `"Sí"` / `"No"` en los cuadros de confirmación).
- Integración en el repositorio con el módulo desarrollado por **E1 (Mishelle Álvarez)**: `ventana_sesion`, `ruleta`, `blackjack`, `ranking`, `analisis`, `cerrar_sesion` y `guardar_datos`.
- Pruebas integradas del flujo completo del proyecto (E1 + E2).

---

## 9. Instrucciones para ejecutar el programa

- **Versión de Python compatible:** Python 3.5.1 o superior.
- **Archivo de E2:** `casino.py`
- **Dependencias necesarias:** Librerías estándar de Python (`tkinter` y `random`).
- **Comando para ejecutar actualmente E2 (modo de prueba mientras se integra E1):**
  ```bash
  python casino.py
  ```
  > **Nota:** Actualmente, ejecutar `python casino.py` inicia únicamente el módulo de E2 abriendo `menu_principal()` en modo de prueba, dado que la integración con el módulo de E1 aún se encuentra pendiente.
- **Flujo de arranque e integración E1/E2 (previsto y pendiente de integración con E1):**
  1. *(Pendiente de integración)* Vincular el módulo de E1 con `casino.py` (módulo de E2) registrando las funciones de E1 mediante `casino.conectar_modulo_e1(...)`.
  2. *(Pendiente de integración)* Compartir una única ventana raíz `tk.Tk()` administrada por `casino.asegurar_ventana_raiz()` e iniciar la ejecución desde `ventana_sesion()` de E1.
  3. *(Pendiente de integración)* Al iniciar la sesión de un jugador en `ventana_sesion()`, invocar `casino.iniciar_sesion_e2(registro_jugador)` pasando la estructura `[(username, nombre, apellido), [dinero, rojas, azules, verdes, blancas], puntaje]` para cargarla en `jugador_actual` y abrir `menu_principal()`.
