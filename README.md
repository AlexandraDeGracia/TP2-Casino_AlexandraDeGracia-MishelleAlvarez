# TP2 - Casino

Este proyecto es un casino virtual hecho en Python con una interfaz gráfica en Tkinter. Cada persona puede registrarse, iniciar sesión, comprar y canjear fichas, ir acumulando puntos y probar suerte en los juegos disponibles.

## 1. De qué trata el proyecto

La idea fue armar un casino donde cada jugador tenga su propio perfil. Todo lo que le pasa en el juego (su dinero, sus fichas y su puntaje) se guarda en un archivo binario con pickle, así que cuando vuelve a entrar encuentra todo tal como lo dejó.

## 2. Quiénes lo hicimos y qué le tocó a cada una

- **Mishelle Álvarez (E1):** se encargó del registro y del inicio de sesión (sesion.py), de guardar y administrar a los jugadores (datos.py) y de los módulos de ruleta, blackjack, ranking y análisis.

- **Alexandra De Gracia (E2, casino.py):** se encargó de unir todo con lo de E1, del menú principal, de la ventana de juegos, de la tragamonedas, de los dados, de la ventana donde se compran y canjean fichas y de la documentación interna.

## 3. Repositorio

https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez.git

## 4. Qué puede hacer el programa

- Registrar jugadores e iniciar sesión usando solo el nombre de usuario.

- Mostrar un menú principal con el usuario, el dinero, las fichas de cada color y el puntaje.

- Comprar y canjear fichas, revisando que las cantidades sean válidas y que alcance el dinero o las fichas.

- Guardar y cargar la información de cada jugador con pickle.

- Entrar a la sala de juegos desde el menú. Ahí también aparecen los botones de Ruleta y Blackjack, pero por ahora avisan que todavía no están conectados, porque son módulos de E1 que falta integrar.

- **Tragamonedas:**

  - Se elige el color de las fichas y cuántas se quieren apostar.

  - Antes de girar se revisa que el jugador tenga suficientes fichas de ese color.

  - Los tres rodillos giran con una animación.

  - Al terminar, el programa busca la combinación que salió entre las combinaciones ganadoras. Si coincide, las fichas se duplican.

  - El puntaje sube 2 puntos al ganar y baja 1 al perder.

  - Aparecen los botones Girar / Jugar otra vez y Regresar a juegos.

- **Dados:**

  - Se lanzan dos dados y la tirada se guarda como una tupla con los dos valores, tal como se pide.

  - Se puede apostar a par, impar, dobles o suma exacta.

  - También se revisa que haya fichas suficientes antes de apostar.

  - El pago sale de los multiplicadores definidos para cada tipo de apuesta, y el puntaje funciona igual que en la tragamonedas: 2 puntos si gana, 1 menos si pierde.

  - Aparecen los botones Lanzar dados / Jugar otra vez y Regresar a juegos, así que se puede volver a tirar sin salir de la ventana.

- Los dos juegos están conectados a la sala de juegos, y el botón Regresar a juegos lleva de vuelta a esa sala, no al menú principal.

- Después de cada compra, canje o jugada, los cambios del jugador se guardan.

## 5. Archivos del proyecto

- **casino.py:** es el archivo principal, el que se ejecuta. Junta la sesión, el menú, la sala de juegos, la tragamonedas, los dados y la pantalla de fichas.

- **datos.py:** módulo de E1 que lee, guarda, busca y actualiza a los jugadores, su dinero, sus fichas y su puntaje con pickle.

- **sesion.py:** módulo de E1 con las ventanas de registro e inicio de sesión.

- **ruleta.py, blackjack.py, ranking.py y analisis.py:** módulos de E1 que todavía falta incorporar al programa.

## 6. Cómo organizamos los datos

### El jugador

Cada jugador es una lista con tres partes:

- **Primera parte, una tupla:** el nombre de usuario, el nombre y el apellido.

- **Segunda parte, una lista:** primero el dinero disponible (con decimales) y después la cantidad de fichas de cada color, en este orden: rojas, azules, verdes y blancas. Cada ficha tiene su valor: las rojas valen 10 dólares, las azules 50, las verdes 20 y las blancas 5.

- **Tercera parte, un número entero:** el puntaje acumulado.

### Listas, matrices y diccionarios

- La lista de colores de fichas.

- La matriz de rodillos de la tragamonedas, con tres filas (una por rodillo) y cinco símbolos en cada una.

- El diccionario de combinaciones ganadoras de la tragamonedas, donde cada combinación de tres símbolos tiene su multiplicador.

- El diccionario de pagos de los dados, con los multiplicadores de par, impar, dobles y suma exacta.

- La matriz de opciones de los dados, que ordena los cuatro tipos de apuesta en dos filas y dos columnas.

- El diccionario de módulos de E1, donde se van conectando las funciones de ruleta, blackjack, ranking y análisis.

- El diccionario con los valores de las fichas, que vive en datos.py.

- Un diccionario de estado, que guarda la ventana principal, la ventana que está abierta, si la tragamonedas está girando y la posición de los rodillos.

- Un diccionario de widgets, que guarda las etiquetas, los campos de texto y las opciones de la ventana que estamos usando en ese momento.


## 7. Decisiones que tomamos

- **Descontar la apuesta apenas empieza la jugada:** primero se retiran las fichas apostadas y, si el jugador gana, se le paga. Así evitamos que el saldo se duplique por error.

- **Respetar el color de la ficha apostada:** se descuenta y se paga siempre en el mismo color, para que el valor no cambie.

- **Animar la tragamonedas con after:** así los rodillos se mueven sin trabar la ventana de Tkinter.

- **Tener una sola ventana raíz:** las demás ventanas son secundarias y hay un único bucle principal.

- **Dejar la compra y el canje de fichas en datos.py:** reutilizamos esa lógica en lugar de repetirla en casino.py.

- **Guardar el progreso al terminar cada operación:** el dinero, las fichas y el puntaje se escriben en el archivo de jugadores.

- **Dar 100 dólares al registrarse:** el enunciado no dice con cuánto empieza un jugador nuevo, así que elegimos ese monto para que pueda comprar fichas y empezar a jugar.

- **Identificar al jugador por su nombre de usuario:** con eso lo buscamos y lo cargamos.


## 8. Cosas que descartamos

- Pagar solamente al final sin descontar antes la apuesta, porque podría duplicar el saldo.

- Mezclar fichas de distintos colores o pagar en un color diferente al apostado.

- Dejar cerrar la ventana de la tragamonedas mientras gira, porque la apuesta quedaría descontada sin resolverse.

- Crear varias ventanas raíz o varios bucles principales.

- Repetir los precios de las fichas o la lógica de compra y canje que ya existe en datos.py.

- Usar los pagos fijos de 50 y 20 dólares del ejemplo de la tragamonedas, en lugar del multiplicador de las reglas generales.


## 9. Cómo ejecutarlo

### Qué se necesita

- Python 3.5.1.

- Tener casino.py, datos.py y sesion.py en la misma carpeta, junto con los módulos de E1 que ya estén integrados.

### Cómo se corre

Se abre una terminal en la carpeta del proyecto y se ejecuta el archivo casino.py con Python.

### Así funciona por dentro

1. Se abre la ventana de registro e inicio de sesión.

2. La persona se registra (empieza con 100 dólares) o entra con un usuario que ya existe.

3. Aparece el menú principal.

4. En Fichas puede comprar o canjear, y en Jugar entra a la sala de juegos.

5. Cada compra, canje o jugada actualiza y guarda sus datos.

6. Al cerrar sesión se guarda el progreso, se limpian los datos de la sesión y se vuelve a la ventana de inicio.

## 12. Cómo vamos

### Lo que ya está listo

- Unimos casino.py con datos.py y sesion.py.

- Hicimos el menú principal, la sala de juegos y la ventana de compra y canje de fichas.

- Programamos la tragamonedas y los dados como se describe en la sección 4, usando el diccionario de combinaciones ganadoras y la tupla para la tirada de los dados.

- Agregamos el botón Lanzar dados / Jugar otra vez en la ventana de dados.

- Validamos los números enteros con isdigit y documentamos todas las funciones.

- Guardamos los datos de los jugadores con pickle.

### Lo que falta

- Integrar los módulos de ruleta, blackjack, ranking y análisis de E1.

- Ronda 1 de pruebas cruzadas: probar sesión, ruleta y blackjack de E1 (Mishelle).

- **jugadores:** un archivo binario donde se guarda la información de todos los jugadores con pickle.

- Hacer las pruebas y anotar los resultados antes de decir que se hicieron: revisar que casino.py, datos.py y sesion.py compilen sin errores; probar la validación de números enteros, el conteo de fichas, las apuestas, los resultados de los dados y las combinaciones de la tragamonedas; y probar el registro, el inicio de sesión, la compra y el canje de fichas, la actualización de datos y el cierre de sesión.

- Hacer una prueba manual completa de la interfaz: ver con nuestros propios ojos la animación del giro y comprobar qué pasa si se cierra la ventana de la tragamonedas con la X mientras está girando.

## 13 Nota sobre el uso de Inteligencia Artificial

La Inteligencia Artificial (IA) se utilizó únicamente para los docstrings (redacción y ajuste del formato de documentación interna pedido en la Condición 12).


**Última actualización:** 11 de noviembre de 2026.
