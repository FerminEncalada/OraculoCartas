"""
Controlador principal del juego
"""
from models.deck import Deck
from models.game_state import GameState

class GameController:
    def __init__(self):
        """Inicializa el controlador del juego"""
        self.deck = Deck()
        self.state = GameState()
    
    def start_game(self, question):
        """
        Inicia el juego con una pregunta
        
        Args:
            question (str): La pregunta al oráculo
        """
        self.state.set_question(question)
        self.state.state = "shuffling"
        
        # Mezclar y distribuir
        self.deck.shuffle()
        piles = self.deck.distribute_to_piles()
        self.state.set_piles(piles)
        
        self.state.state = "playing"
    
    def flip_card(self, pile_index, card_index):
        """
        Voltea una carta específica
        
        Args:
            pile_index (int): Índice de la pila
            card_index (int): Índice de la carta en la pila
            
        Returns:
            bool: True si se pudo voltear la carta
        """
        if pile_index >= len(self.state.piles):
            return False
        
        pile = self.state.piles[pile_index]
        if card_index >= len(pile):
            return False
        
        card = pile[card_index]
        if card.face_up:
            return False
        
        card.flip()
        self.state.select_card(card, pile_index)
        return True
    
    def place_card(self, target_pile):
        """
        Coloca la carta seleccionada en la pila objetivo
        
        Args:
            target_pile (int): Índice de la pila objetivo
            
        Returns:
            bool: True si se pudo colocar la carta
        """
        if not self.state.can_place_card(target_pile):
            return False
        
        from_pile = self.state.selected_pile
        card = self.state.selected_card
        
        # Remover de pila original
        self.state.piles[from_pile].pop()
        
        # Agregar a pila objetivo
        self.state.piles[target_pile].append(card)
        
        self.state.deselect_card()
        return True
    
    def get_next_card_to_flip(self, pile_index):
        """
        Retorna el índice de la siguiente carta a voltear en una pila
        
        Args:
            pile_index (int): Índice de la pila
            
        Returns:
            int or None: Índice de la carta o None si no hay más
        """
        if pile_index >= len(self.state.piles):
            return None
        
        pile = self.state.piles[pile_index]
        for i, card in enumerate(pile):
            if not card.face_up:
                return i
        
        return None
    
    def check_game_over(self, last_pile):
        """
        Verifica si el juego terminó
        
        Args:
            last_pile (int): Índice de la última pila donde se colocó una carta
            
        Returns:
            bool: True si el juego terminó
        """
        face_down = self.state.get_face_down_cards(last_pile)
        return len(face_down) == 0
    
    def get_result(self):
        """
        Obtiene el resultado del juego
        
        Returns:
            str: "success" o "failure"
        """
        victory = self.state.check_victory()
        self.state.result = "success" if victory else "failure"
        self.state.state = "result"
        return self.state.result
    
    def reset(self):
        """Reinicia el juego completamente"""
        self.deck.initialize()
        self.state = GameState()