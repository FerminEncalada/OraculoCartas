"""
Archivo principal del Oráculo de Cartas
Ejecuta este archivo para iniciar el juego
"""
import tkinter as tk
from tkinter import messagebox
import random
from controllers.game_controller import GameController
from ui.pile_renderer import PileRenderer
from ui.card_renderer import CardRenderer
from utils.constants import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, ANIMATION_TIMES, GAME_AREA_WIDTH

class OracleCardGame:
    def __init__(self, root):
        """
        Inicializa la aplicación del juego
        
        Args:
            root: Ventana principal de tkinter
        """
        self.root = root
        self.root.title("Oráculo de Cartas Místico")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS['bg_main'])
        
        # Controlador del juego
        self.controller = GameController()
        
        # Variables de animación
        self.shuffle_iteration = 0
        self.card_positions = []
        
        # Variables de estado del juego
        self.waiting_for_flip = False  # Espera que usuario voltee carta
        self.waiting_for_placement = False  # Espera que usuario coloque carta
        self.current_pile_to_flip = None  # Pila de donde voltear
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame de pregunta inicial
        self.question_frame = tk.Frame(self.root, bg=COLORS['bg_main'])
        self.question_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título con efecto de gradiente simulado
        title_container = tk.Frame(self.question_frame, bg=COLORS['bg_main'])
        title_container.pack(pady=30)
        
        tk.Label(
            title_container,
            text="✨",
            font=("Arial", 40),
            bg=COLORS['bg_main'],
            fg=COLORS['accent_gold']
        ).pack()
        
        tk.Label(
            title_container,
            text="Oráculo de Cartas",
            font=("Arial", 36, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        ).pack()
        
        tk.Label(
            self.question_frame,
            text="Haz tu pregunta al oráculo y las cartas revelarán tu destino",
            font=("Arial", 13),
            bg=COLORS['bg_main'],
            fg=COLORS['text_secondary']
        ).pack(pady=15)
        
        # Frame para el área de texto
        text_container = tk.Frame(self.question_frame, bg=COLORS['bg_secondary'], relief=tk.FLAT)
        text_container.pack(pady=20, padx=40)
        
        self.question_text = tk.Text(
            text_container,
            width=50,
            height=4,
            font=("Arial", 12),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_primary'],
            relief=tk.FLAT,
            padx=15,
            pady=15,
            borderwidth=0
        )
        self.question_text.pack(padx=3, pady=3)
        
        tk.Button(
            self.question_frame,
            text="🔮 Consultar al Oráculo",
            font=("Arial", 14, "bold"),
            bg=COLORS['accent_primary'],
            fg="white",
            activebackground=COLORS['accent_secondary'],
            activeforeground="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            command=self.start_game
        ).pack(pady=20)
        
        # Canvas para el área de juego (izquierda)
        self.game_canvas = tk.Canvas(
            self.root,
            width=GAME_AREA_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS['bg_main'],
            highlightthickness=0
        )
        
        # Canvas para la carta en mano (derecha)
        self.hand_canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH - GAME_AREA_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS['hand_bg'],
            highlightthickness=0
        )
        
        self.pile_renderer = PileRenderer(self.game_canvas)
        self.card_renderer = CardRenderer(self.game_canvas)
        self.hand_card_renderer = CardRenderer(self.hand_canvas)
        
        # Frames para controles y resultado
        self.top_bar_frame = tk.Frame(self.root, bg=COLORS['bg_secondary'], height=70)
        self.instruction_label = None
        self.result_frame = tk.Frame(self.root, bg=COLORS['bg_main'])
    
    def start_game(self):
        """Inicia el juego con la pregunta del usuario"""
        question = self.question_text.get("1.0", tk.END).strip()
        if not question:
            messagebox.showwarning("Advertencia", "Por favor, escribe tu pregunta al oráculo primero")
            return
        
        self.question_frame.place_forget()
        self.controller.state.set_question(question)
        
        # Iniciar animación de mezcla
        self.show_shuffle_animation()
    
    def show_shuffle_animation(self):
        """Muestra la animación de mezcla de cartas"""
        # Limpiar pantalla
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        self.game_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.game_canvas.delete("all")
        
        # Título de mezcla
        self.game_canvas.create_text(
            GAME_AREA_WIDTH // 2, 100,
            text="✨ Mezclando las cartas... ✨",
            font=("Arial", 24, "bold"),
            fill=COLORS['text_primary'],
            tags="shuffle_text"
        )
        
        self.game_canvas.create_text(
            GAME_AREA_WIDTH // 2, 145,
            text="El oráculo está escuchando tu pregunta",
            font=("Arial", 13),
            fill=COLORS['text_secondary'],
            tags="shuffle_text"
        )
        
        # Generar posiciones aleatorias para las cartas
        self.card_positions = []
        for i in range(52):
            x = random.randint(100, GAME_AREA_WIDTH - 100)
            y = random.randint(220, WINDOW_HEIGHT - 120)
            self.card_positions.append((x, y))
        
        # Iniciar animación
        self.shuffle_iteration = 0
        self.animate_shuffle()
    
    def animate_shuffle(self):
        """Anima la mezcla de cartas"""
        if self.shuffle_iteration >= ANIMATION_TIMES['shuffle_iterations']:
            # Terminar animación y distribuir cartas
            self.finish_shuffle()
            return
        
        # Limpiar cartas anteriores
        self.game_canvas.delete("shuffle_card")
        
        # Dibujar cartas en posiciones aleatorias con movimiento
        num_cards_to_show = min(20, 52)
        
        for i in range(num_cards_to_show):
            base_x, base_y = self.card_positions[i]
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            
            x = base_x + offset_x
            y = base_y + offset_y
            
            self.card_renderer.draw_shuffling_card(x, y)
        
        # Mezclar realmente el mazo
        self.controller.deck.riffle_shuffle()
        
        self.shuffle_iteration += 1
        self.root.after(ANIMATION_TIMES['shuffle_interval'], self.animate_shuffle)
    
    def finish_shuffle(self):
        """Finaliza la mezcla y distribuye las cartas"""
        # Realizar mezclas finales
        self.controller.deck.shuffle(iterations=7)
        
        # Distribuir en pilas
        piles = self.controller.deck.distribute_to_piles()
        self.controller.state.set_piles(piles)
        self.controller.state.state = "playing"
        
        # Configurar tablero
        self.root.after(500, self.setup_game_board)
    
    def setup_game_board(self):
        """Configura el tablero de juego"""
        # Limpiar todo
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        self.game_canvas.delete("all")
        self.hand_canvas.delete("all")
        
        # Barra superior
        self.top_bar_frame.pack(side=tk.TOP, fill=tk.X)
        
        for widget in self.top_bar_frame.winfo_children():
            widget.destroy()
        
        # Frame izquierdo para la pregunta
        question_container = tk.Frame(self.top_bar_frame, bg=COLORS['bg_secondary'])
        question_container.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            question_container,
            text="Tu pregunta:",
            font=("Arial", 9, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W)
        
        tk.Label(
            question_container,
            text=self.controller.state.question,
            font=("Arial", 11, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            wraplength=400,
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Frame derecho para controles
        controls_container = tk.Frame(self.top_bar_frame, bg=COLORS['bg_secondary'])
        controls_container.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            controls_container,
            text="Ayuda automática:",
            font=("Arial", 9, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.auto_step_button = tk.Button(
            controls_container,
            text="⚡ Colocar carta",
            font=("Arial", 9, "bold"),
            bg=COLORS['green_highlight'],
            fg="white",
            activebackground=COLORS['green_dark'],
            activeforeground="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            command=self.auto_play_step,
            state=tk.DISABLED
        )
        self.auto_step_button.pack(side=tk.LEFT, padx=3)
        
        self.auto_all_button = tk.Button(
            controls_container,
            text="⚡ Completar todo",
            font=("Arial", 9, "bold"),
            bg=COLORS['accent_primary'],
            fg="white",
            activebackground=COLORS['accent_secondary'],
            activeforeground="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            command=self.auto_play_all,
            state=tk.DISABLED
        )
        self.auto_all_button.pack(side=tk.LEFT, padx=3)
        
        # Canvas del juego (izquierda) y carta en mano (derecha)
        self.game_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.hand_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título en el panel de carta en mano
        self.update_hand_panel()
        
        # Instrucción inicial
        self.show_instruction("Haz clic en el CENTRO para voltear la primera carta")
        
        # Preparar para que usuario voltee primera carta del conjunto 13
        self.waiting_for_flip = True
        self.current_pile_to_flip = 12  # Conjunto 13 = índice 12
        
        self.update_game_display()
    
    def update_hand_panel(self, card=None):
        """Actualiza el panel de la carta en mano"""
        self.hand_canvas.delete("all")
        
        # Título del panel
        self.hand_canvas.create_text(
            (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2, 50,
            text="CARTA EN MANO",
            font=("Arial", 22, "bold"),
            fill=COLORS['text_primary'],
            tags="hand_title"
        )
        
        if card:
            # Dibujar la carta grande
            center_x = (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2
            center_y = WINDOW_HEIGHT // 2
            
            self.hand_card_renderer.draw_large_card(
                center_x, center_y, card,
                label=f"🎴 {card.value}{card.suit}"
            )
        else:
            # No hay carta seleccionada
            self.hand_canvas.create_text(
                (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2, 
                WINDOW_HEIGHT // 2,
                text="Voltea una carta\npara verla aquí",
                font=("Arial", 18),
                fill=COLORS['text_secondary'],
                tags="hand_empty",
                justify=tk.CENTER
            )
            
            self.hand_canvas.create_text(
                (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2, 
                WINDOW_HEIGHT // 2 + 80,
                text="👆",
                font=("Arial", 48),
                fill=COLORS['text_secondary'],
                tags="hand_empty"
            )
    
    def show_instruction(self, text):
        """Muestra una instrucción al usuario"""
        if self.instruction_label:
            self.instruction_label.destroy()
        
        self.instruction_label = tk.Label(
            self.root,
            text=text,
            font=("Arial", 13, "bold"),
            bg=COLORS['accent_secondary'],
            fg="white",
            padx=20,
            pady=10
        )
        self.instruction_label.place(relx=0.5, rely=0.94, anchor="center")
    
    def update_game_display(self):
        """Actualiza la visualización del juego"""
        if self.waiting_for_flip:
            # Usuario debe voltear carta - resaltar pila correspondiente
            self.pile_renderer.draw_all_piles(
                self.controller.state.piles,
                None,
                self.controller.state.animating,
                on_pile_click_callback=self.on_pile_clicked_for_flip
            )
            # Resaltar la pila donde debe voltear
            from utils.constants import PILE_POSITIONS
            x, y = PILE_POSITIONS[self.current_pile_to_flip]
            self.card_renderer.draw_highlight(x, y)
            
            # Hacer el área de highlight clickeable
            self.game_canvas.tag_bind("highlight", "<Button-1>",
                                     lambda e: self.on_pile_clicked_for_flip(self.current_pile_to_flip))
            self.game_canvas.tag_bind("highlight", "<Enter>", 
                                     lambda e: self.game_canvas.config(cursor="hand2"))
            self.game_canvas.tag_bind("highlight", "<Leave>", 
                                     lambda e: self.game_canvas.config(cursor=""))
            
            # No mostrar carta en mano
            self.update_hand_panel(None)
        
        elif self.waiting_for_placement:
            # Usuario debe colocar carta - resaltar pila destino
            self.pile_renderer.draw_all_piles(
                self.controller.state.piles,
                self.controller.state.selected_card,
                self.controller.state.animating,
                on_pile_click_callback=self.on_pile_clicked_for_placement
            )
            
            # Mostrar carta en mano
            if self.controller.state.selected_card:
                self.update_hand_panel(self.controller.state.selected_card)
        else:
            # Estado normal
            self.pile_renderer.draw_all_piles(
                self.controller.state.piles,
                self.controller.state.selected_card,
                self.controller.state.animating,
                on_pile_click_callback=None
            )
            
            # Actualizar panel de mano
            self.update_hand_panel(self.controller.state.selected_card)
    
    def on_pile_clicked_for_flip(self, pile_index):
        """Manejador cuando usuario hace clic para voltear carta"""
        if not self.waiting_for_flip:
            return
        
        if pile_index != self.current_pile_to_flip:
            return
        
        if self.controller.state.animating:
            return
        
        # Voltear la carta
        self.flip_card_at_pile(pile_index)
    
    def flip_card_at_pile(self, pile_index):
        """Voltea la primera carta boca abajo de una pila"""
        # Encontrar primera carta boca abajo
        card_index = None
        for i, card in enumerate(self.controller.state.piles[pile_index]):
            if not card.face_up:
                card_index = i
                break
        
        if card_index is None:
            return
        
        # Voltear
        self.controller.flip_card(pile_index, card_index)
        
        # Ahora esperar que usuario coloque la carta
        self.waiting_for_flip = False
        self.waiting_for_placement = True
        self.current_pile_to_flip = None
        
        # Habilitar botones de ayuda
        self.auto_step_button.config(state=tk.NORMAL)
        self.auto_all_button.config(state=tk.NORMAL)
        
        # Mostrar instrucción
        card = self.controller.state.selected_card
        pile_name = "Centro" if card.num_value - 1 == 12 else f"Pila {card.num_value}"
        self.show_instruction(f"Haz clic en {pile_name} para colocar la carta")
        
        self.update_game_display()
    
    def on_pile_clicked_for_placement(self, pile_index):
        """Manejador cuando usuario hace clic para colocar carta"""
        if not self.waiting_for_placement:
            return
        
        if self.controller.state.animating:
            return
        
        if not self.controller.state.selected_card:
            return
        
        # Verificar que sea la pila correcta
        target_pile = self.controller.state.selected_card.num_value - 1
        if pile_index != target_pile:
            return
        
        # Colocar la carta
        self.place_card(pile_index)
    
    def place_card(self, target_pile):
        """Coloca una carta en la pila objetivo"""
        if self.controller.state.animating:
            return
        
        self.controller.state.animating = True
        self.waiting_for_placement = False
        
        # Deshabilitar botones temporalmente
        self.auto_step_button.config(state=tk.DISABLED)
        self.auto_all_button.config(state=tk.DISABLED)
        
        success = self.controller.place_card(target_pile)
        if not success:
            self.controller.state.animating = False
            return
        
        self.update_game_display()
        
        # Verificar si hay más cartas en esa pila
        if self.controller.check_game_over(target_pile):
            self.show_instruction("¡Juego terminado! Calculando resultado...")
            self.root.after(ANIMATION_TIMES['flip_delay'], self.show_result)
        else:
            # Hay más cartas - usuario debe voltear siguiente
            self.root.after(ANIMATION_TIMES['place_card_delay'], 
                          lambda: self.prepare_next_flip(target_pile))
    
    def prepare_next_flip(self, pile_index):
        """Prepara para que usuario voltee siguiente carta"""
        self.controller.state.animating = False
        self.waiting_for_flip = True
        self.current_pile_to_flip = pile_index
        
        pile_name = "Centro" if pile_index == 12 else f"Pila {pile_index + 1}"
        self.show_instruction(f"Haz clic en {pile_name} para voltear la siguiente carta")
        
        self.update_game_display()
    
    def auto_play_step(self):
        """Ayuda: Coloca automáticamente la carta actual"""
        if self.waiting_for_flip and self.current_pile_to_flip is not None:
            # Voltear automáticamente
            self.flip_card_at_pile(self.current_pile_to_flip)
        elif self.waiting_for_placement and self.controller.state.selected_card:
            # Colocar automáticamente
            target_pile = self.controller.state.selected_card.num_value - 1
            self.place_card(target_pile)
    
    def auto_play_all(self):
        """Completa el juego automáticamente"""
        if self.controller.state.animating:
            return
        
        self.controller.state.animating = True
        self.waiting_for_flip = False
        self.waiting_for_placement = False
        self.auto_step_button.config(state=tk.DISABLED)
        self.auto_all_button.config(state=tk.DISABLED)
        self.show_instruction("Completando automáticamente...")
        
        self.auto_play_recursive()
    
    def auto_play_recursive(self):
        """Juega recursivamente de forma automática"""
        # Si hay carta seleccionada, colocarla
        if self.controller.state.selected_card:
            target_pile = self.controller.state.selected_card.num_value - 1
            self.controller.place_card(target_pile)
            self.update_game_display()
            
            # Verificar fin
            if self.controller.check_game_over(target_pile):
                self.root.after(ANIMATION_TIMES['flip_delay'], self.show_result)
                return
            
            # Voltear siguiente
            next_card_idx = self.controller.get_next_card_to_flip(target_pile)
            if next_card_idx is not None:
                self.controller.flip_card(target_pile, next_card_idx)
                self.root.after(ANIMATION_TIMES['auto_play_delay'], 
                              lambda: (self.update_game_display(), self.auto_play_recursive()))
            else:
                self.controller.state.animating = False
        else:
            # Necesita voltear carta inicial
            if self.current_pile_to_flip is not None:
                self.flip_card_at_pile(self.current_pile_to_flip)
                self.root.after(ANIMATION_TIMES['auto_play_delay'], self.auto_play_recursive)
            else:
                self.controller.state.animating = False
    
    def show_result(self):
        """Muestra el resultado del juego"""
        result = self.controller.get_result()
        success = result == "success"
        
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        self.result_frame.place(relx=0.5, rely=0.5, anchor="center")
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Ícono y título
        icon = "✨" if success else "🌙"
        title = f"{icon} {'¡El Oráculo ha Hablado!' if success else 'El Destino es Incierto'} {icon}"
        
        tk.Label(
            self.result_frame,
            text=title,
            font=("Arial", 30, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        ).pack(pady=30)
        
        # Caja de resultado
        question_box = tk.Frame(self.result_frame, bg=COLORS['bg_secondary'], relief=tk.FLAT)
        question_box.pack(pady=20, padx=50)
        
        tk.Label(
            question_box,
            text="Tu pregunta:",
            font=("Arial", 11, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(pady=(20, 5), padx=30)
        
        tk.Label(
            question_box,
            text=self.controller.state.question,
            font=("Arial", 13, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            wraplength=550
        ).pack(pady=(0, 15), padx=30)
        
        # Resultado
        result_text = "✓ SÍ, se cumplirá" if success else "✗ NO, no se cumplirá"
        result_color = COLORS['green_highlight'] if success else COLORS['red_card']
        
        tk.Label(
            question_box,
            text=result_text,
            font=("Arial", 26, "bold"),
            bg=COLORS['bg_secondary'],
            fg=result_color
        ).pack(pady=20, padx=30)
        
        message = ("Todas las cartas han sido reveladas.\nEl universo conspira a tu favor." if success
                  else "Las cartas permanecen ocultas.\nEl camino aún no está claro.")
        
        tk.Label(
            self.result_frame,
            text=message,
            font=("Arial", 13),
            bg=COLORS['bg_main'],
            fg=COLORS['text_secondary']
        ).pack(pady=15)
        
        tk.Button(
            self.result_frame,
            text="🔄 Consultar Nuevamente",
            font=("Arial", 14, "bold"),
            bg=COLORS['accent_primary'],
            fg="white",
            activebackground=COLORS['accent_secondary'],
            activeforeground="white",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            command=self.reset_game
        ).pack(pady=25)
    
    def reset_game(self):
        """Reinicia el juego"""
        self.controller.reset()
        self.waiting_for_flip = False
        self.waiting_for_placement = False
        self.current_pile_to_flip = None
        
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        self.question_text.delete("1.0", tk.END)
        self.question_frame.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    game = OracleCardGame(root)
    root.mainloop()