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
    
    def riffle_shuffle(self):
        """
        Mezcla estilo riffle (mezcla americana) - más realista
        Simula como un humano mezclaría las cartas
        """
        # Dividir el mazo aproximadamente por la mitad (con variación)
        mid = len(self.cards) // 2
        variance = random.randint(-3, 3)
        split_point = mid + variance
        
        left_half = self.cards[:split_point]
        right_half = self.cards[split_point:]
        
        # Intercalar las cartas de forma imperfecta
        shuffled = []
        while left_half or right_half:
            # Decidir de qué mitad tomar (con probabilidad variable)
            if left_half and right_half:
                # A veces tomar 1 carta, a veces 2-3
                num_cards = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
                
                if random.random() < 0.5:
                    for _ in range(min(num_cards, len(left_half))):
                        shuffled.append(left_half.pop(0))
                else:
                    for _ in range(min(num_cards, len(right_half))):
                        shuffled.append(right_half.pop(0))
            elif left_half:
                shuffled.extend(left_half)
                left_half = []
            else:
                shuffled.extend(right_half)
                right_half = []
        
        self.cards = shuffled
    
    def shuffle(self, iterations=7):
        """
        Mezcla la baraja múltiples veces como lo haría un humano
        
        Args:
            iterations (int): Número de mezclas riffle a realizar
        """
        for _ in range(iterations):
            self.riffle_shuffle()
    
    def distribute_to_piles(self, num_piles=13, cards_per_pile=4):
        """
        Distribuye las cartas MEZCLADAS en pilas de 4 cartas cada una.
        IMPORTANTE: Las cartas YA están mezcladas, solo se reparten una por una
        en orden, como cuando repartes cartas en la vida real.
        
        Esto significa que:
        - Pila 0 (AS) tendrá 4 cartas ALEATORIAS (pueden ser 5♠, K♥, 3♦, 7♣)
        - Pila 1 (2) tendrá 4 cartas ALEATORIAS
        - etc.
        - Pila 12 (CENTRO/K) tendrá 4 cartas ALEATORIAS
        
        Args:
            num_piles (int): Número de pilas a crear (13)
            cards_per_pile (int): Cartas por pila (4)
            
        Returns:
            list: Lista de 13 pilas con 4 cartas ALEATORIAS cada una
        """
        piles = [[] for _ in range(num_piles)]
        
        # Repartir las cartas UNA POR UNA a cada pila
        # Como cuando repartes cartas: primera carta a pila 0, segunda a pila 1, etc.
        card_index = 0
        
        # Repartir 4 rondas (4 cartas por pila)
        for round_num in range(cards_per_pile):
            # En cada ronda, dar una carta a cada pila
            for pile_index in range(num_piles):
                if card_index < len(self.cards):
                    piles[pile_index].append(self.cards[card_index])
                    card_index += 1
        
        return piles
    
    def get_shuffle_animation_state(self, iteration, total_iterations):
        """
        Obtiene un estado intermedio de la mezcla para animación
        
        Args:
            iteration (int): Iteración actual
            total_iterations (int): Total de iteraciones
            
        Returns:
            list: Estado actual de las cartas
        """
        # Realizar una mezcla parcial
        if iteration > 0:
            self.riffle_shuffle()
        
        return self.cards.copy()