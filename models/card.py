"""
Módulo que define la clase Card (Carta)
"""

class Card:
    def __init__(self, suit, value, num_value):
        """
        Inicializa una carta
        
        Args:
            suit (str): El palo de la carta (♠, ♥, ♦, ♣)
            value (str): El valor de la carta (A, 2-10, J, Q, K)
            num_value (int): Valor numérico (1-13)
        """
        self.suit = suit
        self.value = value
        self.num_value = num_value
        self.face_up = False
    
    def flip(self):
        """Voltea la carta boca arriba"""
        self.face_up = True
    
    def is_red(self):
        """
        Verifica si la carta es roja
        
        Returns:
            bool: True si es corazón o diamante
        """
        return self.suit in ['♥', '♦']
    
    def __repr__(self):
        """Representación en string de la carta"""
        return f"{self.value}{self.suit}"