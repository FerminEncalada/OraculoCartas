"""
Módulo para renderizar cartas en el canvas
"""
from utils.constants import COLORS, CARD_WIDTH, CARD_HEIGHT

class CardRenderer:
    def __init__(self, canvas):
        """
        Inicializa el renderizador de cartas
        
        Args:
            canvas: Canvas de tkinter donde dibujar
        """
        self.canvas = canvas
    
    def draw_card(self, x, y, card, pile_index, card_index, is_top=False, can_click=False):
        """
        Dibuja una carta en el canvas
        
        Args:
            x (int): Posición X
            y (int): Posición Y
            card (Card): La carta a dibujar
            pile_index (int): Índice de la pila
            card_index (int): Índice de la carta en la pila
            is_top (bool): Si es la carta superior
            can_click (bool): Si se puede hacer click
            
        Returns:
            str: Tag de la carta dibujada
        """
        # Determinar colores
        if card.face_up:
            if card.is_red():
                fill_color = "white"
                text_color = COLORS['red_card']
                border_color = COLORS['red_card']
            else:
                fill_color = "white"
                text_color = "black"
                border_color = "black"
        else:
            fill_color = COLORS['purple_card']
            text_color = COLORS['gold']
            border_color = COLORS['purple_border']
        
        half_width = CARD_WIDTH // 2
        half_height = CARD_HEIGHT // 2
        
        # Dibujar rectángulo de la carta
        card_id = self.canvas.create_rectangle(
            x - half_width, y - half_height,
            x + half_width, y + half_height,
            fill=fill_color,
            outline=border_color,
            width=2,
            tags=f"card_{pile_index}_{card_index}"
        )
        
        # Dibujar contenido de la carta
        if card.face_up:
            # Valor de la carta
            self.canvas.create_text(
                x, y - 15,
                text=card.value,
                font=("Arial", 16, "bold"),
                fill=text_color,
                tags=f"card_{pile_index}_{card_index}"
            )
            # Palo de la carta
            self.canvas.create_text(
                x, y + 15,
                text=card.suit,
                font=("Arial", 24, "bold"),
                fill=text_color,
                tags=f"card_{pile_index}_{card_index}"
            )
        else:
            # Carta boca abajo - mostrar símbolo místico
            self.canvas.create_text(
                x, y,
                text="✨",
                font=("Arial", 28),
                fill=text_color,
                tags=f"card_{pile_index}_{card_index}"
            )
        
        return f"card_{pile_index}_{card_index}"
    
    def draw_highlight(self, x, y):
        """
        Dibuja un resaltado alrededor de una pila
        
        Args:
            x (int): Posición X
            y (int): Posición Y
        """
        half_width = CARD_WIDTH // 2
        self.canvas.create_rectangle(
            x - half_width - 10, y - 60,
            x + half_width + 10, y + 100,
            outline=COLORS['green_highlight'],
            width=4,
            tags="highlight"
        )