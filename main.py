import soko
import gamelib
import pila


PARED = '#'
VACIO = ' '

MOVIMIENTOS = {'NORTE':(0, -1), 'SUR':(0, 1), 'ESTE':(1, 0), 'OESTE':(-1, 0)}


def cargar_controles():
    """A partir de un archivo .txt que contiene los comandos básicos
    del juego, genera un diccionario con <clave>:<valor>, donde <clave>
    es la tecla del teclado presionada y <valor> es la acción a realizar"""
    with open('teclas.txt') as teclas:
        acciones = {}
        for linea in teclas:
            if linea != '\n':
                aux = linea.rstrip('\n').split(' = ')
                acciones[aux[0]] = aux[1]
    return acciones


def cargar_niveles():
    """
    A partir de un archivo .txt que contiene los niveles, genera un
    diccionario con <clave>:<valor>, en donde <clave> es el número de nivel y 
    >valor> es el nivel en formato lista de cadena de caracteres
    """
    with open('niveles.txt') as niveles:
        numero_nivel = 1
        nivel = []
        total_niveles = {}
        for linea in niveles:
            if linea[0] in (VACIO, PARED):
                nivel.append(linea.rstrip('\n'))
            if linea == '\n':
                longitud = 0
                for item in nivel:
                    if len(item) > longitud:
                        longitud = len(item)
                for i in range(len(nivel)):
                    while len(nivel[i]) < longitud:
                        nivel[i] += ' '
                total_niveles[numero_nivel] = nivel
                nivel = []
                numero_nivel += 1
        total_niveles[numero_nivel] = nivel
    return total_niveles


def cargar_grilla(nivel_numero, total_niveles):
	"""
    Carga la grilla correspondiente al nivel 'nivel_numero'
    """
	if nivel_numero in total_niveles:
		nivel = total_niveles[nivel_numero]
		grilla = soko.crear_grilla(nivel)
	return grilla


def mostrar_juego(grilla):
    """
    Muestra en la ventana del juego la interfaz gráfica
    """
    mult = 64
    acciones = cargar_controles()
    long_horizontal = mult*len(grilla[0])
    long_vertical = mult*len(grilla)
    gamelib.resize(long_horizontal, long_vertical)
    for i in range(soko.dimensiones(grilla)[1]):
        for j in range(soko.dimensiones(grilla)[0]):
            gamelib.draw_image('img/ground.gif', mult*j, mult*i)
            if soko.hay_jugador(grilla, j, i) == True:
                gamelib.draw_image('img/player.gif', mult*j, mult*i)
            if soko.hay_caja(grilla, j, i) == True:
                gamelib.draw_image('img/box.gif', mult*j, mult*i)
            if soko.hay_pared(grilla, j, i) == True:
                gamelib.draw_image('img/wall.gif', mult*j, mult*i)
            if soko.hay_objetivo(grilla, j, i) == True:
                gamelib.draw_image('img/goal.gif', mult*j, mult*i)
    for tecla in acciones:
        if acciones[tecla] == 'REINICIAR':
            gamelib.draw_text(f'{tecla}: Reiniciar nivel', 375, 15, fill = 'black', size = 10, anchor = 'e')
        if acciones[tecla] == 'DESHACER':
            gamelib.draw_text(f'{tecla} : Deshacer movimiento', 375, 30, fill = 'black', size = 10, anchor = 'e')
        if acciones[tecla] == 'PISTA':
            gamelib.draw_text(f'{tecla} : Pista', 375, 45, fill = 'black', size = 10, anchor = 'e')


def niveles_superados():
    """
    Muestra un mensaje en pantalla cuando todos los niveles hayan sido superados
    """
    gamelib.resize(1000, 300)
    gamelib.draw_text('HAZ SUPERADO TODOS LOS NIVELES', 500, 100, fill = 'white', size = 30)
    gamelib.draw_text('¡¡¡FELICITACIONES!!!', 500, 200, fill = 'white', size = 30)

def estado_inmutable(estado):
    estado_inmut = []
    for i in estado:
        estado_inmut.append(tuple(i))
    estado_inmut = tuple(estado_inmut)
    return estado_inmut

def buscar_solucion(estado):
    visitados = set()
    movimientos_solucion = pila.Pila()
    return backtrack(estado, visitados, movimientos_solucion)


def backtrack(estado, visitados, movimientos_solucion):
    """
    Busca una posible solución al estado de juego actual. Esta solución no siempre
    será la óptima.
    """
    visitados.add(estado_inmutable(estado))
    if soko.juego_ganado(estado) == True:
        return True, movimientos_solucion
    for i in MOVIMIENTOS:
        nuevo_estado = soko.mover(estado, MOVIMIENTOS[i])
        if estado_inmutable(nuevo_estado) in visitados:
            continue
        solucion, acciones = backtrack(nuevo_estado, visitados, movimientos_solucion)
        if solucion is True:
            movimientos_solucion.apilar(i)
            return True, movimientos_solucion
    return False, None


def main():
    # Inicializar el estado del juego
    
    acciones = cargar_controles()
    total_niveles = cargar_niveles()
    pila_grillas = pila.Pila()
    nivel_numero = 1
    grilla = cargar_grilla(nivel_numero, total_niveles)
    pedido_pista = False
    mensaje = ''

    while gamelib.is_alive():
        gamelib.draw_begin()
        if nivel_numero in total_niveles:
            mostrar_juego(grilla)
        else:
            niveles_superados()
        if pedido_pista is True:
            gamelib.draw_text(f'{mensaje}', 60, 20, fill = 'white', size = 10)
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada

        if tecla in acciones:
            for direccion in MOVIMIENTOS:
                if acciones[tecla] == direccion:
                    pila_grillas.apilar(grilla)
                    grilla = soko.mover(grilla, MOVIMIENTOS[direccion])
            if acciones[tecla] == 'REINICIAR':
                grilla = cargar_grilla(nivel_numero, total_niveles)
                pila_grillas = pila.Pila()
            if acciones[tecla] == 'DESHACER':
                if not pila_grillas.esta_vacia():
                    grilla = pila_grillas.desapilar()
                else:
                    continue
            if acciones[tecla] == 'PISTA':
                if pedido_pista is False:
                    mensaje = 'Pensando pista...'
                    condicion_pista, movimientos_pista = buscar_solucion(grilla)
                    if condicion_pista is True:
                        mensaje = 'Pista encontrada.'
                    else:
                        mensaje = 'No hay solución.'
                    pedido_pista = True
                else:
                    if not movimientos_pista.esta_vacia():
                        mov_pista = movimientos_pista.desapilar()
                        grilla = soko.mover(grilla, MOVIMIENTOS[mov_pista])
                    else:
                        continue
                pila_grillas.apilar(grilla)        
            if acciones[tecla] != 'PISTA':
                pedido_pista = False
            if acciones[tecla] == 'SALIR':
                return 

        if soko.juego_ganado(grilla) == True:
            nivel_numero += 1
            grilla = cargar_grilla(nivel_numero, total_niveles)
            pila_grillas = pila.Pila()
            pedido_pista = False

gamelib.init(main)