"""
Módulo que maneja el estado del juego
"""

class GameState:
    def __init__(self):
        """Inicializa el estado del juego"""
        self.question = ""
        self.piles = []
        self.selected_card = None
        self.selected_pile = None
        self.state = "question"  # question, shuffling, playing, result
        self.animating = False
        self.result = None
    
    def set_question(self, question):
        """
        Establece la pregunta del usuario
        
        Args:
            question (str): La pregunta al oráculo
        """
        self.question = question
    
    def set_piles(self, piles):
        """
        Establece las pilas de cartas
        
        Args:
            piles (list): Lista de pilas con cartas
        """
        self.piles = piles
    
    def select_card(self, card, pile_index):
        """
        Selecciona una carta
        
        Args:
            card (Card): La carta seleccionada
            pile_index (int): Índice de la pila de origen
        """
        self.selected_card = card
        self.selected_pile = pile_index
    
    def deselect_card(self):
        """Deselecciona la carta actual"""
        self.selected_card = None
        self.selected_pile = None
    
    def can_place_card(self, target_pile):
        """
        Verifica si se puede colocar la carta en la pila objetivo
        
        Args:
            target_pile (int): Índice de la pila objetivo
            
        Returns:
            bool: True si se puede colocar
        """
        if not self.selected_card:
            return False
        return target_pile == self.selected_card.num_value - 1
    
    def get_face_down_cards(self, pile_index):
        """
        Retorna las cartas boca abajo de una pila
        
        Args:
            pile_index (int): Índice de la pila
            
        Returns:
            list: Lista de cartas boca abajo
        """
        if pile_index >= len(self.piles):
            return []
        return [card for card in self.piles[pile_index] if not card.face_up]
    
    def check_victory(self):
        """
        Verifica si todas las cartas están boca arriba
        
        Returns:
            bool: True si todas están boca arriba
        """
        for pile in self.piles:
            for card in pile:
                if not card.face_up:
                    return False
        return True