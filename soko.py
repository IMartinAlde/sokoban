# SOKOBAN

JUGADOR = '@'
CAJA = '$'
OBJETIVO = '.'
JUGADOR_OBJETIVO = '+'
CAJA_OBJETIVO = '*'
PARED = '#'
VACIO = ' '

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []
    for i in range(len(desc)):
        lista = list(desc[i])
        grilla.append(lista)
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return(len(grilla[0]),len(grilla))

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c] == CAJA_OBJETIVO or grilla[f][c] == JUGADOR_OBJETIVO

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == CAJA_OBJETIVO

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] == JUGADOR or grilla[f][c] == JUGADOR_OBJETIVO

def hay_vacio(grilla, c, f):
    '''Devuelve True si en la columna y fila (c, f) no hay nada (casillero vacío).'''
    return grilla[f][c] == VACIO

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for i in range(len(grilla)):
        for j in range(len(grilla[0])):
            if grilla[i][j] == OBJETIVO or grilla[i][j] == JUGADOR_OBJETIVO:
                return False
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''

    nueva_grilla = crear_grilla(grilla)

    #Ubica la posición del jugador y sus casilleros adyacentes (vecinos) 
    #en el sentido del movimiento realizado como una tupla (fila, columna):

    for fil in range(len(grilla)): 
        for col in range(len(grilla[0])):
            if grilla[fil][col] == JUGADOR or grilla[fil][col] == JUGADOR_OBJETIVO:
                posicion_jugador = (fil, col)

    posicion_vecino_1 = (posicion_jugador[0] + direccion[1], posicion_jugador[1] + direccion[0])
    posicion_vecino_2 = (posicion_jugador[0] + 2*direccion[1], posicion_jugador[1] + 2*direccion[0])

    #Pido que el segundo casillero vecino pertenezca a la grilla definiendo
    #primero el valor de "condicion", dependiendo del movimiento:

    if direccion[0] == 0:       #Movimiento NORTE-SUR
        condicion = posicion_vecino_2[0]
        maximo = len(grilla)
    else:                       #Movimiento ESTE-OESTE
        condicion = posicion_vecino_2[1]
        maximo = len(grilla[0])

    if 0 > condicion or condicion >= maximo:
        return nueva_grilla

    caracter_jugador = nueva_grilla[posicion_jugador[0]][posicion_jugador[1]]
    caracter_vecino_1 = nueva_grilla[posicion_vecino_1[0]][posicion_vecino_1[1]]
    caracter_vecino_2 = nueva_grilla[posicion_vecino_2[0]][posicion_vecino_2[1]]

    obstaculo_1 = hay_pared(grilla, posicion_vecino_1[1], posicion_vecino_1[0])
    obstaculo_2 = (hay_caja(grilla, posicion_vecino_1[1], posicion_vecino_1[0]) and
                (hay_caja(grilla, posicion_vecino_2[1], posicion_vecino_2[0]) or
                hay_pared(grilla, posicion_vecino_2[1], posicion_vecino_2[0])))

    movimiento_no_valido = obstaculo_1 or obstaculo_2

    if movimiento_no_valido == True:
        return nueva_grilla

    if hay_objetivo(nueva_grilla, posicion_jugador[1], posicion_jugador[0]) == True:
        caracter_jugador = OBJETIVO
    else:
        caracter_jugador = VACIO

    if hay_objetivo(nueva_grilla, posicion_vecino_1[1], posicion_vecino_1[0]) == True:
        caracter_vecino_1 = JUGADOR_OBJETIVO
    else:
        caracter_vecino_1 = JUGADOR

    if hay_caja(nueva_grilla, posicion_vecino_1[1], posicion_vecino_1[0]) == True:
        if hay_objetivo(nueva_grilla, posicion_vecino_2[1], posicion_vecino_2[0]) == True:
            caracter_vecino_2 = CAJA_OBJETIVO
        else:
            caracter_vecino_2 = CAJA

    nueva_grilla[posicion_jugador[0]][posicion_jugador[1]] = caracter_jugador
    nueva_grilla[posicion_vecino_1[0]][posicion_vecino_1[1]] = caracter_vecino_1
    nueva_grilla[posicion_vecino_2[0]][posicion_vecino_2[1]] = caracter_vecino_2
    
    return nueva_grilla