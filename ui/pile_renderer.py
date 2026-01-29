"""
Módulo para renderizar pilas de cartas
"""
from utils.constants import PILE_POSITIONS
from ui.card_renderer import CardRenderer

class PileRenderer:
    def __init__(self, canvas):
        """
        Inicializa el renderizador de pilas
        
        Args:
            canvas: Canvas de tkinter donde dibujar
        """
        self.canvas = canvas
        self.card_renderer = CardRenderer(canvas)
    
    def draw_all_piles(self, piles, selected_card=None, animating=False, on_pile_click_callback=None):
        """
        Dibuja todas las pilas en el canvas
        
        Args:
            piles (list): Lista de pilas con cartas
            selected_card (Card): Carta actualmente seleccionada
            animating (bool): Si hay una animación en curso
            on_pile_click_callback: Función a llamar cuando se hace clic en una pila
        """
        self.canvas.delete("all")
        
        for pile_index, pile in enumerate(piles):
            self.draw_pile(pile_index, pile, selected_card, animating, on_pile_click_callback)
    
    def draw_pile(self, pile_index, pile, selected_card=None, animating=False, on_pile_click_callback=None):
        """
        Dibuja una pila individual
        
        Args:
            pile_index (int): Índice de la pila
            pile (list): Lista de cartas en la pila
            selected_card (Card): Carta seleccionada
            animating (bool): Si hay animación en curso
            on_pile_click_callback: Función callback para clicks
        """
        x, y = PILE_POSITIONS[pile_index]
        
        # Dibujar etiqueta de la pila ENCIMA de las cartas
        label_text = "Centro" if pile_index == 12 else f"Pila {pile_index + 1}"
        self.canvas.create_text(
            x, y - 70,
            text=label_text,
            font=("Arial", 11, "bold"),
            fill="#b19cd9",
            tags=f"pile_label_{pile_index}"
        )
        
        # Calcular si esta pila es la válida para colocar carta
        is_valid_pile = False
        if selected_card and not animating:
            target_pile = selected_card.num_value - 1
            is_valid_pile = (pile_index == target_pile)
        
        # Dibujar rectángulo de área de la pila (invisible pero clickeable)
        if is_valid_pile:
            # Dibujar resaltado verde
            self.canvas.create_rectangle(
                x - 50, y - 65,
                x + 50, y + 65,
                outline="#10b981",
                width=4,
                tags=f"pile_area_{pile_index}"
            )
            
            # Hacer toda el área clickeable
            self.canvas.tag_bind(f"pile_area_{pile_index}", "<Button-1>",
                               lambda e, p=pile_index: on_pile_click_callback(p) if on_pile_click_callback else None)
        
        # Dibujar cada carta de la pila
        for card_index, card in enumerate(pile):
            # Las cartas boca arriba se separan un poco más
            offset = card_index * (15 if card.face_up else 2)
            card_y = y + offset
            
            is_top = card_index == len(pile) - 1
            
            card_tag = self.card_renderer.draw_card(x, card_y, card, pile_index, card_index, is_top)
            
            # Si es la pila válida, hacer las cartas clickeables también
            if is_valid_pile:
                self.canvas.tag_bind(card_tag, "<Button-1>",
                                   lambda e, p=pile_index: on_pile_click_callback(p) if on_pile_click_callback else None)