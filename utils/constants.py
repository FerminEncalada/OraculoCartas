"""
Constantes del juego
"""

# Colores del tema
COLORS = {
    'bg_main': '#1a0b2e',
    'bg_secondary': '#2d1b4e',
    'purple_light': '#e0b0ff',
    'purple_mid': '#b19cd9',
    'purple_dark': '#7b2cbf',
    'purple_active': '#9d4edd',
    'purple_card': '#5b21b6',
    'purple_border': '#7c3aed',
    'red_card': '#dc2626',
    'green_highlight': '#10b981',
    'green_dark': '#059669',
    'blue_button': '#3b82f6',
    'blue_active': '#2563eb',
    'gold': '#fbbf24'
}

# Posiciones de las pilas en el canvas (x, y)
# Organizadas en cuadrado con sentido horario + centro
# Esquema:
#   0   1   2   3
# 11            4
# 10     12     5
#  9            6
#   8   7   6   5

PILE_POSITIONS = [
    (250, 180),   # 0 - esquina superior izquierda
    (450, 180),   # 1 - superior izquierda-centro
    (650, 180),   # 2 - superior derecha-centro
    (850, 180),   # 3 - esquina superior derecha
    (850, 350),   # 4 - derecha superior
    (850, 520),   # 5 - derecha inferior
    (850, 690),   # 6 - esquina inferior derecha
    (650, 690),   # 7 - inferior derecha-centro
    (450, 690),   # 8 - inferior izquierda-centro
    (250, 690),   # 9 - esquina inferior izquierda
    (250, 520),   # 10 - izquierda inferior
    (250, 350),   # 11 - izquierda superior
    (550, 435)    # 12 - centro (pila 13)
]

# Dimensiones de las cartas y ventana
CARD_WIDTH = 80
CARD_HEIGHT = 110
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 900

# Tiempos de animación en milisegundos
ANIMATION_TIMES = {
    'shuffle_wait': 2000,      # Tiempo de espera al mezclar
    'flip_delay': 400,         # Tiempo antes de voltear carta
    'auto_play_delay': 500,    # Tiempo entre movimientos automáticos
    'place_card_delay': 300    # Tiempo al colocar carta
}