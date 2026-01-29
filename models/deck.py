"""
Módulo que maneja la baraja de cartas
"""
import random
from models.card import Card

class Deck:
    SUITS = ['♠', '♥', '♦', '♣']
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self):
        """Inicializa una baraja vacía"""
        self.cards = []
        self.initialize()
    
    def initialize(self):
        """Crea una baraja completa de 52 cartas"""
        self.cards = []
        for suit in self.SUITS:
            for i, value in enumerate(self.VALUES):
                card = Card(suit, value, i + 1)
                self.cards.append(card)
    
    def shuffle(self):
        """Mezcla la baraja de forma aleatoria"""
        random.shuffle(self.cards)
    
    def distribute_to_piles(self, num_piles=13, cards_per_pile=4):
        """
        Distribuye las cartas en pilas
        
        Args:
            num_piles (int): Número de pilas a crear
            cards_per_pile (int): Cartas por pila
            
        Returns:
            list: Lista de pilas con cartas
        """
        piles = [[] for _ in range(num_piles)]
        
        for i, card in enumerate(self.cards):
            pile_index = i // cards_per_pile
            if pile_index < num_piles:
                piles[pile_index].append(card)
        
        return piles