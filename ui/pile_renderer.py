"""
Módulo para renderizar pilas de cartas
"""
from utils.constants import PILE_POSITIONS, CARD_OFFSET_FACE_UP, CARD_OFFSET_FACE_DOWN
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
            font=("Arial", 10, "bold"),
            fill="#b19cd9",
            tags=f"pile_label_{pile_index}"
        )
        
        # Calcular si esta pila es la válida para colocar carta
        is_valid_pile = False
        if selected_card and not animating:
            target_pile = selected_card.num_value - 1
            is_valid_pile = (pile_index == target_pile)
        
        # Calcular la altura total de la pila para el área clickeable
        pile_height = 0
        if len(pile) > 0:
            for i, card in enumerate(pile):
                if i > 0:
                    offset = CARD_OFFSET_FACE_UP if pile[i-1].face_up else CARD_OFFSET_FACE_DOWN
                    pile_height += offset
            pile_height += 100  # Altura de la última carta
        else:
            pile_height = 100  # Pila vacía tiene altura de una carta
        
        # Crear un área clickeable MUCHO MÁS GRANDE que cubra toda la pila
        # El área será más ancha y más alta para capturar mejor los clicks
        click_area_width = 90  # Mucho más ancho que la carta (70px)
        click_area_top = y - 80  # Empezar bien arriba
        click_area_bottom = y + pile_height + 20  # Terminar bien abajo
        
        click_area_tag = f"pile_area_{pile_index}"
        
        # Crear varios rectángulos superpuestos para mayor área clickeable
        # Esto ayuda a capturar clicks en diferentes partes
        for i in range(3):  # 3 capas de áreas clickeables
            offset = i * 5
            click_rect = self.canvas.create_rectangle(
                x - click_area_width - offset, click_area_top - offset,
                x + click_area_width + offset, click_area_bottom + offset,
                fill="",
                outline="",
                tags=click_area_tag
            )
        
        if is_valid_pile:
            # Dibujar resaltado verde GRANDE y MUY VISIBLE
            # Resaltado exterior brillante
            self.canvas.create_rectangle(
                x - 65, y - 85,
                x + 65, y + pile_height + 15,
                outline="#10b981",
                width=5,
                tags=f"highlight_{pile_index}"
            )
            
            # Segundo borde para efecto pulsante
            self.canvas.create_rectangle(
                x - 60, y - 80,
                x + 60, y + pile_height + 10,
                outline="#34d399",
                width=3,
                tags=f"highlight_{pile_index}"
            )
            
            # Tercer borde dorado para máximo contraste
            self.canvas.create_rectangle(
                x - 55, y - 75,
                x + 55, y + pile_height + 5,
                outline="#fbbf24",
                width=2,
                tags=f"highlight_{pile_index}"
            )
            
            # Hacer TODAS las capas del área clickeable con el callback
            for i in range(3):
                layer_tag = f"{click_area_tag}_layer{i}"
                # Bind al evento de click
                self.canvas.tag_bind(click_area_tag, "<Button-1>",
                                   lambda e, p=pile_index: on_pile_click_callback(p) if on_pile_click_callback else None)
                
                # Cambiar cursor cuando pasa sobre el área
                self.canvas.tag_bind(click_area_tag, "<Enter>", 
                                   lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(click_area_tag, "<Leave>", 
                                   lambda e: self.canvas.config(cursor=""))
            
            # También hacer el resaltado clickeable
            self.canvas.tag_bind(f"highlight_{pile_index}", "<Button-1>",
                               lambda e, p=pile_index: on_pile_click_callback(p) if on_pile_click_callback else None)
            self.canvas.tag_bind(f"highlight_{pile_index}", "<Enter>",
                               lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(f"highlight_{pile_index}", "<Leave>",
                               lambda e: self.canvas.config(cursor=""))
        
        # Dibujar cada carta de la pila
        card_y = y
        for card_index, card in enumerate(pile):
            # Calcular offset basado en el estado de la carta anterior
            if card_index > 0:
                prev_card = pile[card_index - 1]
                offset = CARD_OFFSET_FACE_UP if prev_card.face_up else CARD_OFFSET_FACE_DOWN
                card_y += offset
            
            is_top = card_index == len(pile) - 1
            
            card_tag = self.card_renderer.draw_card(x, card_y, card, pile_index, card_index, is_top)
            
            # Si es la pila válida, hacer TODAS las cartas clickeables también
            if is_valid_pile:
                self.canvas.tag_bind(card_tag, "<Button-1>",
                                   lambda e, p=pile_index: on_pile_click_callback(p) if on_pile_click_callback else None)
                self.canvas.tag_bind(card_tag, "<Enter>", 
                                   lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(card_tag, "<Leave>", 
                                   lambda e: self.canvas.config(cursor=""))
        
        # Levantar todas las áreas de click al frente si es válida
        if is_valid_pile:
            self.canvas.tag_raise(click_area_tag)
            self.canvas.tag_raise(f"highlight_{pile_index}")