# TP2 - Casino

Casino virtual hecho en Python con Tkinter. Permite crear una cuenta, iniciar sesión, comprar y canjear fichas, y jugar tragamonedas o dados.

## 1. Integrantes

- **Mishelle Álvarez (E1):** trabajó en la creación de los archivos datos.py y sesion.py.
- **Alexandra De Gracia (E2):** trabajó en casino.py, integró los módulos y desarrolló el menú, la sala de juegos, la tragamonedas, los dados, la ventana de compra y canje de fichas y el cierre de sesión.

## 2. Repositorio

https://github.com/AlexandraDeGracia/TP2-Casino_AlexandraDeGracia-MishelleAlvarez.git

## 3. ¿Qué puede hacer el programa?

- Registrar jugadores e iniciar sesión.
- Mostrar el dinero, las fichas y los puntos de cada jugador.
- Comprar fichas (Rojo: $10, Azul: $50, Verde: $20, Blanco: $5) y canjearlas por dinero.
- Guardar los datos para que el jugador continúe después.
- Jugar tragamonedas o dados desde la sala de juegos.
- Cerrar sesión y volver al inicio.

**No se incluyen en esta versión:** Ruleta y Blackjack (botones de la sala de juegos) y Ranking y Análisis (botones del menú principal). Esos cuatro botones aparecen en el programa, pero quedan pendientes de implementar y no ejecutan ninguna acción al hacer clic.

### Tragamonedas

Se elige el color y la cantidad de fichas a apostar. El programa revisa que haya suficientes fichas, anima los rodillos (PASOS_ANIMACION = 12 pasos cada INTERVALO_ANIMACION = 150 ms, menos de 2 segundos) y aplica el pago según la combinación. Si coinciden los tres símbolos, duplica las fichas apostadas (x2 en el mismo color) y suma 2 puntos (PUNTOS_POR_GANAR); si no coinciden, pierde las fichas apostadas y resta 1 punto (PUNTOS_POR_PERDER).

### Dados

Se puede apostar a par, impar, dobles o sumaExacta (entre 2 y 12). Se lanzan dos dados (el resultado se guarda en la tupla tiradaDados) y se evalúa la apuesta. Si acierta, multiplica las fichas apostadas del mismo color según pagosDados (x2 en par e impar, x5 en dobles y x12 en sumaExacta) y suma 2 puntos (PUNTOS_POR_GANAR). Si falla, pierde las fichas apostadas y resta 1 punto (PUNTOS_POR_PERDER).

## 4. Archivos

- casino.py: inicia el programa y conecta las ventanas, los juegos y la ventana de fichas.
- datos.py: registra, busca y actualiza la información de los jugadores, y contiene la lógica de compra y canje de fichas.
- sesion.py: maneja el registro y el inicio de sesión.
- jugadores: archivo binario con las cuentas. Se crea solo la primera vez que se guardan datos.

## 5. Datos utilizados

Cada jugador es una lista con tres partes:

1. Una tupla con (username, nombre, apellido).
2. Una lista con [dinero, rojas, azules, verdes, blancas].
3. Un entero con el puntaje acumulado.

También se usan estas estructuras:
- Listas y matrices para los colores de fichas, los rodillos (matrizRodillos) y las opciones de dados (matrizOpcionesDados).
- Tuplas para las combinaciones de la tragamonedas y los dos dados de cada tirada (tiradaDados).
- Diccionarios para premios (combinacionesGanadoras, pagosDados), precios y posiciones de fichas (VALOR_FICHAS, POSICIONES_FICHAS), y controles de pantalla (estado, widgets, camposSesion).
- Constantes para la animación, límites de dados y puntos al ganar o perder.
- pickle para guardar y leer las cuentas en binario.

## 6. Decisiones tomadas

- Cada jugador empieza con 100 dólares.
- La apuesta se descuenta antes de jugar: si gana, en tragamonedas duplica sus fichas (x2) y en dados multiplica según pagosDados (x2, x2, x5 o x12), sumando 2 puntos en ambos juegos; si pierde, resta 1 punto.
- La tragamonedas anima los rodillos juntos usando after de Tkinter para que la ventana no se congele.
- Solo hay una ventana raíz y cada pantalla nueva se abre en una ventana secundaria (Toplevel).
- La lógica de compra y canje vive en datos.py para reutilizarla desde casino.py.
- Los errores en datos.py y sesion.py se devuelven como texto en lugar de usar raise.
- El diccionario pagosDados (2, 2, 5 y 12) se usa como multiplicador de fichas al acertar en dados, aplicando +2 puntos al ganar y -1 punto al perder igual que en la tragamonedas.
- Se definieron los símbolos Cereza, Limón, Campana, Estrella y Siete para los rodillos.
- El progreso del jugador se guarda automáticamente después de cada jugada, compra o canje.
- Se unificó en mostrarResultadoJuego (junto con liquidar) la forma de pagar y mostrar el resultado de la tragamonedas y los dados para evitar código repetido.

## 7. Decisiones descartadas

- Pagar solo al final sin descontar antes la apuesta, porque un error o giro repetido podría duplicar el saldo.
- Mezclar fichas de distintos colores en una jugada o pagar en otro color, para no alterar el valor real de lo apostado.
- Dejar cerrar o salir de la tragamonedas mientras gira, ya que la apuesta estaría descontada y la partida quedaría a medias.
- Crear varias ventanas principales (Tk) para prevenir fallos con los controles y el bucle de Tkinter.
- Repetir en casino.py los precios o la lógica de compra y canje, aprovechando directamente las funciones de datos.py.
- Usar los pagos fijos de 50 y 20 fichas del ejemplo, siguiendo en su lugar la regla general de duplicar las fichas (x2).

## 8. Puntos del enunciado que no estaban definidos o eran inconsistentes

- **Saldo inicial:** el enunciado no indica un monto de inicio, así que cada cuenta nueva arranca con 100 dólares.
- **Puntos en los dados:** el enunciado no aclara cuántos puntos sumar o restar en dados, por lo que se aplicó la misma regla de la tragamonedas (+2 al ganar y -1 al perder), dejando pagosDados (2, 2, 5 y 12) como multiplicador de fichas.
- **Suma exacta:** se mantuvo el multiplicador x12 de pagosDados para cualquier suma exacta, aunque no todas tengan la misma probabilidad.
- **Pagos de la tragamonedas:** el texto pide duplicar las fichas, mientras el ejemplo muestra pagos de 50 y 20. Se siguió el texto aplicando x2 en todas las combinaciones.
- **Símbolos de la tragamonedas:** el enunciado solo da dos ejemplos (diamante y campana) para los 5 símbolos, así que se usaron Cereza, Limón, Campana, Estrella y Siete.

## 9. Validaciones

- Datos vacíos al registrarse o al iniciar sesión.
- Usuarios repetidos al registrarse y cuentas inexistentes al entrar.
- Solo enteros (sin letras, decimales ni signos) en fichas y apuestas.
- Apuestas mayores que cero y dentro de las fichas disponibles de ese color.
- Bloqueo para no girar de nuevo ni cerrar la tragamonedas mientras gira.
- Falta de dinero al comprar o de fichas al canjear.
- Compras o canjes con todas las cantidades en cero.
- Confirmación previa al comprar, canjear o cerrar sesión.
- Suma exacta en dados entre 2 y 12 (solo cuando se elige sumaExacta).
- Archivo jugadores dañado o inválido: muestra error y protege los datos sin sobrescribirlos.

## 10. Cómo ejecutar

Se necesita Python 3.5.1 o superior (solo biblioteca estándar: tkinter, random, pickle) y los archivos casino.py, datos.py y sesion.py en la misma carpeta. En una terminal dentro de esa carpeta:

python casino.py

## 11. Estado del proyecto

Están conectados el registro e inicio de sesión, el menú, la compra y el canje de fichas, la tragamonedas, los dados y el cierre de sesión. Ruleta, Blackjack, Ranking y Análisis no se incluyen en esta versión.

## 12. Nota sobre el uso de Inteligencia Artificial

La Inteligencia Artificial (IA) se utilizó únicamente para los docstrings (redacción y ajuste del formato de documentación interna pedido en la Condición 12).

**Última actualización:** 20 de noviembre de 2026.
