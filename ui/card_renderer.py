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
    
    def draw_card(self, x, y, card, pile_index, card_index, is_top=False):
        """
        Dibuja una carta en el canvas con diseño mejorado
        
        Args:
            x (int): Posición X
            y (int): Posición Y
            card (Card): La carta a dibujar
            pile_index (int): Índice de la pila
            card_index (int): Índice de la carta en la pila
            is_top (bool): Si es la carta superior
            
        Returns:
            str: Tag de la carta dibujada
        """
        half_width = CARD_WIDTH // 2
        half_height = CARD_HEIGHT // 2
        
        # Determinar colores
        if card.face_up:
            # Carta boca arriba - fondo blanco
            fill_color = "white"
            if card.is_red():
                text_color = COLORS['red_card']
                border_color = COLORS['red_card']
            else:
                text_color = "black"
                border_color = "#1f2937"
        else:
            # Carta boca abajo - diseño con gradiente simulado
            fill_color = COLORS['card_back']
            text_color = COLORS['card_back_accent']
            border_color = COLORS['card_back_accent']
        
        # Dibujar sombra suave
        self.canvas.create_rectangle(
            x - half_width + 2, y - half_height + 2,
            x + half_width + 2, y + half_height + 2,
            fill="#666666",
            outline="",
            tags=f"card_{pile_index}_{card_index}"
        )
        
        # Dibujar rectángulo principal de la carta
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
            # Carta boca arriba - mostrar valor y palo
            self.canvas.create_text(
                x, y - 15,
                text=card.value,
                font=("Arial", 16, "bold"),
                fill=text_color,
                tags=f"card_{pile_index}_{card_index}"
            )
            self.canvas.create_text(
                x, y + 18,
                text=card.suit,
                font=("Arial", 26, "bold"),
                fill=text_color,
                tags=f"card_{pile_index}_{card_index}"
            )
        else:
            # Carta boca abajo - diseño decorativo
            # Patrón central
            self.canvas.create_oval(
                x - 22, y - 30,
                x + 22, y + 30,
                outline=text_color,
                width=2,
                tags=f"card_{pile_index}_{card_index}"
            )
            
            # Símbolo decorativo
            self.canvas.create_text(
                x, y,
                text="✨",
                font=("Arial", 24),
                fill=COLORS['accent_gold'],
                tags=f"card_{pile_index}_{card_index}"
            )
        
        return f"card_{pile_index}_{card_index}"
    
    def draw_large_card(self, x, y, card, label=""):
        """
        Dibuja una carta grande (para el panel de carta en mano)
        
        Args:
            x (int): Posición X
            y (int): Posición Y
            card (Card): La carta a dibujar
            label (str): Etiqueta para mostrar arriba de la carta
        """
        # Tamaño grande para mejor visualización
        width = 200
        height = 280
        half_width = width // 2
        half_height = height // 2
        
        # Etiqueta superior
        if label:
            self.canvas.create_text(
                x, y - height // 2 - 40,
                text=label,
                font=("Arial", 18, "bold"),
                fill=COLORS['accent_gold'],
                tags="hand_card"
            )
        
        # Determinar colores
        if card.is_red():
            text_color = COLORS['red_card']
            border_color = COLORS['red_card']
        else:
            text_color = "black"
            border_color = "#1f2937"
        
        # Sombra
        self.canvas.create_rectangle(
            x - half_width + 5, y - half_height + 5,
            x + half_width + 5, y + half_height + 5,
            fill="#666666",
            outline="",
            tags="hand_card"
        )
        
        # Fondo de la carta
        self.canvas.create_rectangle(
            x - half_width, y - half_height,
            x + half_width, y + half_height,
            fill="white",
            outline=border_color,
            width=4,
            tags="hand_card"
        )
        
        # Valor en la esquina superior izquierda
        self.canvas.create_text(
            x - half_width + 25, y - half_height + 30,
            text=card.value,
            font=("Arial", 32, "bold"),
            fill=text_color,
            tags="hand_card"
        )
        
        # Palo central grande
        self.canvas.create_text(
            x, y,
            text=card.suit,
            font=("Arial", 100, "bold"),
            fill=text_color,
            tags="hand_card"
        )
        
        # Valor en la esquina inferior derecha
        self.canvas.create_text(
            x + half_width - 25, y + half_height - 30,
            text=card.value,
            font=("Arial", 32, "bold"),
            fill=text_color,
            tags="hand_card"
        )
        
        # Información adicional
        pile_name = f"Va a la Pila {card.num_value}" if card.num_value != 13 else "Va al Centro"
        self.canvas.create_text(
            x, y + height // 2 + 40,
            text=pile_name,
            font=("Arial", 16, "bold"),
            fill=COLORS['green_highlight'],
            tags="hand_card"
        )
    
    def draw_highlight(self, x, y):
        """
        Dibuja un resaltado alrededor de una pila
        
        Args:
            x (int): Posición X
            y (int): Posición Y
        """
        half_width = CARD_WIDTH // 2
        
        # Resaltado con efecto de brillo
        self.canvas.create_rectangle(
            x - half_width - 12, y - 65,
            x + half_width + 12, y + 65,
            outline=COLORS['green_highlight'],
            width=5,
            tags="highlight"
        )
        
        # Segundo borde para efecto de brillo
        self.canvas.create_rectangle(
            x - half_width - 8, y - 61,
            x + half_width + 8, y + 61,
            outline=COLORS['accent_gold'],
            width=2,
            tags="highlight"
        )
    
    def draw_shuffling_card(self, x, y, rotation=0):
        """
        Dibuja una carta durante la animación de mezcla
        
        Args:
            x (int): Posición X
            y (int): Posición Y
            rotation (int): Ángulo de rotación (no usado pero puede expandirse)
        """
        half_width = CARD_WIDTH // 2
        half_height = CARD_HEIGHT // 2
        
        # Carta simple con reverso
        self.canvas.create_rectangle(
            x - half_width, y - half_height,
            x + half_width, y + half_height,
            fill=COLORS['card_back'],
            outline=COLORS['card_back_accent'],
            width=2,
            tags="shuffle_card"
        )
        
        self.canvas.create_text(
            x, y,
            text="✨",
            font=("Arial", 20),
            fill=COLORS['accent_gold'],
            tags="shuffle_card"
        )