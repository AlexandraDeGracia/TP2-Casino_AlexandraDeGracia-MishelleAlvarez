# TP2 - Casino

Casino virtual hecho en Python con Tkinter. Permite crear una cuenta, iniciar sesión, comprar fichas y jugar tragamonedas o dados.

## 1. Integrantes

- **Mishelle Álvarez (E1):** trabajó en la creación de los archivos datos.py y sesion.py.
- **Alexandra De Gracia (E2):** trabajó en casino.py, integró los módulos y desarrolló el menú, la sala de juegos, la tragamonedas, los dados, la ventana de compra y canje de fichas y el cierre de sesión.

## 2. Repositorio

https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez.git

## 3. ¿Qué puede hacer el programa?

- Registrar jugadores e iniciar sesión.
- Mostrar el dinero, las fichas y los puntos de cada jugador.
- Comprar fichas y cambiarlas por dinero.
- Guardar los datos para que el jugador continúe después.
- Jugar tragamonedas o dados desde la sala de juegos.
- Cerrar sesión y volver al inicio.

**Faltaria :** Ruleta y Blackjack (botones de la sala de juegos) y Ranking y Análisis (botones del menú principal). Esos cuatro botones aparecen en el programa, pero solo muestran el aviso de que no están disponibles.

### Tragamonedas

Se elige el color y la cantidad de fichas a apostar. El programa revisa que haya suficientes fichas, anima los rodillos (alrededor de 1.8 segundos) y aplica el pago según la combinación. Ganar suma 2 puntos y perder resta 1.

### Dados

Se puede apostar a par, impar, dobles o suma exacta. Se lanzan dos dados (el resultado se guarda en una tupla) y se calcula el pago según el tipo de apuesta. También suma 2 puntos al ganar y resta 1 al perder.

## 4. Archivos

- casino.py: inicia el programa y conecta las ventanas y los juegos.
- datos.py: registra, busca y actualiza la información de los jugadores, y contiene la lógica de compra y canje de fichas.
- sesion.py: maneja el registro y el inicio de sesión.
- jugadores: archivo binario con las cuentas. Se crea solo la primera vez que el programa necesita guardar datos.

## 5. Datos utilizados

Cada jugador es una lista con tres partes:

1. Una tupla con usuario, nombre y apellido.
2. Una lista con el dinero y las fichas rojas, azules, verdes y blancas.
3. Un entero con el puntaje acumulado.

También se usan listas, matrices, tuplas y diccionarios para los rodillos, las combinaciones ganadoras, las apuestas y los pagos de los dados (pagosDados, pagosSumaExacta). El diccionario modulosE1 tiene cuatro claves (ruleta, blackjack, ranking y analisis) y debe guardar la función que se ejecuta al presionar el botón de cada módulo. Como esos módulos no se entregan en esta versión, está vacío y esos botones muestran el mensaje de "no disponible". Los datos se guardan con pickle.

## 6. Decisiones tomadas

- Cada jugador empieza con **100 dólares**.
- La apuesta se descuenta antes de jugar; si gana, se agrega el premio.
- Se usa el mismo color de ficha para apostar y para cobrar.
- La animación usa after de Tkinter para que la ventana siga respondiendo.
- Hay una sola ventana raíz y las demás pantallas son ventanas secundarias.
- La compra y el canje se dejaron en datos.py para reutilizarlos desde casino.py.
- Los errores en datos.py y sesion.py se devuelven como texto en lugar de usar raise.
- Los multiplicadores de suma exacta varían según la probabilidad de cada suma.

## 7. Decisiones descartadas

- Pagar solo al final sin descontar antes la apuesta, porque el saldo podía duplicarse por un error.
- Mezclar fichas de distintos colores en una apuesta o pagar con un color distinto al apostado.
- Dejar cerrar la tragamonedas mientras los rodillos giran, porque la apuesta ya estaría descontada y la jugada quedaría sin resolver.
- Crear varias ventanas raíz.
- Repetir en casino.py los precios de las fichas o las funciones de compra y canje de datos.py.
- Usar los pagos fijos de 50 y 20 dólares del ejemplo de la tragamonedas, en favor de los multiplicadores de las reglas generales.

## 8. Puntos del enunciado que no estaban definidos o eran inconsistentes

- **Saldo inicial:** el enunciado no lo indica. Se usaron 100 dólares.
- **Puntos en los dados:** el enunciado no define cuántos puntos se suman o restan. Se usó el mismo criterio de la tragamonedas: +2 al ganar y −1 al perder.
- **Suma exacta:** el diccionario del enunciado asigna x12 a toda suma exacta, pero no todas las sumas tienen la misma probabilidad. Se usa la tabla pagosSumaExacta (por ejemplo, x30 para 2 y 12, y x5 para 7). El valor 12 de sumaExacta en pagosDados se conserva pero no se utiliza.

## 9. Validaciones

- Campos vacíos en el registro.
- Nombre de usuario repetido al registrarse y usuario inexistente al iniciar sesión.
- Cantidades que deben ser números enteros.
- Dinero insuficiente al comprar fichas y fichas insuficientes al canjear o apostar.
- Compra o canje con todas las cantidades en cero.
- Suma exacta solo entre 2 y 12.

## 10. Cómo ejecutar

Se necesita Python 3.5.1 o superior y los archivos casino.py, datos.py y sesion.py en la misma carpeta. En una terminal dentro de esa carpeta:

python casino.py

## 11. Estado del proyecto

Están conectados el registro e inicio de sesión, el menú, la compra y el canje de fichas, la tragamonedas, los dados y el cierre de sesión. Ruleta, Blackjack, Ranking y Análisis esta faltando .

## 12. Nota sobre el uso de Inteligencia Artificial

La Inteligencia Artificial (IA) se utilizó únicamente para los docstrings (redacción y ajuste del formato de documentación interna pedido en la Condición 12).

**Última actualización:** 17 de noviembre de 2026.
