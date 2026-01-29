"""
Archivo principal del Oráculo de Cartas
Ejecuta este archivo para iniciar el juego
"""
import tkinter as tk
from tkinter import messagebox
from controllers.game_controller import GameController
from ui.pile_renderer import PileRenderer
from utils.constants import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, ANIMATION_TIMES

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
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame de pregunta inicial
        self.question_frame = tk.Frame(self.root, bg=COLORS['bg_main'])
        self.question_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            self.question_frame,
            text="✨ Oráculo de Cartas ✨",
            font=("Arial", 32, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['purple_light']
        ).pack(pady=20)
        
        tk.Label(
            self.question_frame,
            text="Haz tu pregunta al oráculo y las cartas revelarán tu destino...",
            font=("Arial", 14),
            bg=COLORS['bg_main'],
            fg=COLORS['purple_mid']
        ).pack(pady=10)
        
        self.question_text = tk.Text(
            self.question_frame,
            width=50,
            height=4,
            font=("Arial", 12),
            bg=COLORS['bg_secondary'],
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.question_text.pack(pady=20)
        
        tk.Button(
            self.question_frame,
            text="🔮 Consultar al Oráculo",
            font=("Arial", 14, "bold"),
            bg=COLORS['purple_dark'],
            fg="white",
            activebackground=COLORS['purple_active'],
            activeforeground="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_game
        ).pack(pady=10)
        
        # Canvas para el juego
        self.game_canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS['bg_main'],
            highlightthickness=0
        )
        
        self.pile_renderer = PileRenderer(self.game_canvas)
        
        # Frames para controles y pregunta
        self.top_bar_frame = tk.Frame(self.root, bg=COLORS['bg_secondary'], height=60)
        self.result_frame = tk.Frame(self.root, bg=COLORS['bg_main'])
    
    def start_game(self):
        """Inicia el juego con la pregunta del usuario"""
        question = self.question_text.get("1.0", tk.END).strip()
        if not question:
            messagebox.showwarning("Advertencia", "Por favor, escribe tu pregunta al oráculo primero")
            return
        
        self.question_frame.place_forget()
        self.show_shuffling_message()
        
        self.root.after(ANIMATION_TIMES['shuffle_wait'], lambda: self.shuffle_and_distribute(question))
    
    def show_shuffling_message(self):
        """Muestra mensaje de mezclado"""
        shuffle_label = tk.Label(
            self.root,
            text="✨ Mezclando las cartas... ✨\nEl oráculo está escuchando tu pregunta",
            font=("Arial", 24, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['purple_light']
        )
        shuffle_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
    
    def shuffle_and_distribute(self, question):
        """
        Mezcla y distribuye las cartas
        
        Args:
            question (str): La pregunta del usuario
        """
        self.controller.start_game(question)
        self.setup_game_board()
        self.root.after(ANIMATION_TIMES['flip_delay'], lambda: self.auto_flip_first_card())
    
    def auto_flip_first_card(self):
        """Voltea automáticamente la primera carta del centro"""
        self.controller.flip_card(12, 0)
        self.update_game_display()
    
    def setup_game_board(self):
        """Configura el tablero de juego"""
        # Limpiar todo
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        # Barra superior con pregunta y controles
        self.top_bar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Limpiar barra
        for widget in self.top_bar_frame.winfo_children():
            widget.destroy()
        
        # Frame izquierdo para la pregunta
        question_container = tk.Frame(self.top_bar_frame, bg=COLORS['bg_secondary'])
        question_container.pack(side=tk.LEFT, padx=15, pady=10)
        
        tk.Label(
            question_container,
            text="Tu pregunta:",
            font=("Arial", 9),
            bg=COLORS['bg_secondary'],
            fg=COLORS['purple_mid']
        ).pack(anchor=tk.W)
        
        tk.Label(
            question_container,
            text=self.controller.state.question,
            font=("Arial", 10, "bold"),
            bg=COLORS['bg_secondary'],
            fg="white",
            wraplength=400,
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Frame derecho para controles
        controls_container = tk.Frame(self.top_bar_frame, bg=COLORS['bg_secondary'])
        controls_container.pack(side=tk.RIGHT, padx=15, pady=10)
        
        tk.Label(
            controls_container,
            text="Ayuda:",
            font=("Arial", 9, "bold"),
            bg=COLORS['bg_secondary'],
            fg=COLORS['purple_mid']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.auto_step_button = tk.Button(
            controls_container,
            text="⚡ Colocar carta",
            font=("Arial", 9, "bold"),
            bg=COLORS['green_highlight'],
            fg="white",
            activebackground=COLORS['green_dark'],
            activeforeground="white",
            padx=12,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.auto_play_step
        )
        self.auto_step_button.pack(side=tk.LEFT, padx=3)
        
        self.auto_all_button = tk.Button(
            controls_container,
            text="⚡ Completar todo",
            font=("Arial", 9, "bold"),
            bg=COLORS['blue_button'],
            fg="white",
            activebackground=COLORS['blue_active'],
            activeforeground="white",
            padx=12,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.auto_play_all
        )
        self.auto_all_button.pack(side=tk.LEFT, padx=3)
        
        # Canvas del juego
        self.game_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.update_game_display()
    
    def update_game_display(self):
        """Actualiza la visualización del juego"""
        self.pile_renderer.draw_all_piles(
            self.controller.state.piles,
            self.controller.state.selected_card,
            self.controller.state.animating,
            on_pile_click_callback=self.on_pile_clicked
        )
    
    def on_pile_clicked(self, pile_index):
        """
        Manejador cuando el usuario hace clic en una pila
        
        Args:
            pile_index (int): Índice de la pila clickeada
        """
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
        """
        Coloca una carta en la pila objetivo
        
        Args:
            target_pile (int): Índice de la pila objetivo
        """
        if self.controller.state.animating:
            return
        
        self.controller.state.animating = True
        
        success = self.controller.place_card(target_pile)
        if not success:
            self.controller.state.animating = False
            return
        
        self.update_game_display()
        
        # Verificar si hay más cartas
        if self.controller.check_game_over(target_pile):
            self.root.after(ANIMATION_TIMES['flip_delay'], self.show_result)
        else:
            next_card_idx = self.controller.get_next_card_to_flip(target_pile)
            if next_card_idx is not None:
                self.root.after(ANIMATION_TIMES['place_card_delay'], 
                              lambda: self.flip_and_continue(target_pile, next_card_idx))
            else:
                self.controller.state.animating = False
    
    def flip_and_continue(self, pile_index, card_index):
        """
        Voltea carta y continúa el juego
        
        Args:
            pile_index (int): Índice de la pila
            card_index (int): Índice de la carta
        """
        self.controller.flip_card(pile_index, card_index)
        self.controller.state.animating = False
        self.update_game_display()
    
    def auto_play_step(self):
        """Juega automáticamente un paso"""
        if not self.controller.state.selected_card or self.controller.state.animating:
            return
        
        target_pile = self.controller.state.selected_card.num_value - 1
        self.place_card(target_pile)
    
    def auto_play_all(self):
        """Completa el juego automáticamente"""
        if not self.controller.state.selected_card or self.controller.state.animating:
            return
        
        self.controller.state.animating = True
        self.auto_play_recursive()
    
    def auto_play_recursive(self):
        """Juega recursivamente de forma automática"""
        if not self.controller.state.selected_card:
            self.controller.state.animating = False
            return
        
        target_pile = self.controller.state.selected_card.num_value - 1
        self.controller.place_card(target_pile)
        self.update_game_display()
        
        if self.controller.check_game_over(target_pile):
            self.root.after(ANIMATION_TIMES['flip_delay'], self.show_result)
        else:
            next_card_idx = self.controller.get_next_card_to_flip(target_pile)
            if next_card_idx is not None:
                self.controller.flip_card(target_pile, next_card_idx)
                self.root.after(ANIMATION_TIMES['auto_play_delay'], 
                              lambda: (self.update_game_display(), self.auto_play_recursive()))
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
        
        title = "✨ ¡El Oráculo ha Hablado! ✨" if success else "🌙 El Destino es Incierto 🌙"
        tk.Label(
            self.result_frame,
            text=title,
            font=("Arial", 28, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['purple_light']
        ).pack(pady=20)
        
        question_box = tk.Frame(self.result_frame, bg=COLORS['bg_secondary'])
        question_box.pack(pady=20, padx=40)
        
        tk.Label(
            question_box,
            text="Tu pregunta:",
            font=("Arial", 11),
            bg=COLORS['bg_secondary'],
            fg=COLORS['purple_mid']
        ).pack(pady=(10, 5), padx=20)
        
        tk.Label(
            question_box,
            text=self.controller.state.question,
            font=("Arial", 13, "bold"),
            bg=COLORS['bg_secondary'],
            fg="white",
            wraplength=500
        ).pack(pady=(0, 10), padx=20)
        
        result_text = "✓ SÍ, se cumplirá" if success else "✗ NO, no se cumplirá"
        result_color = COLORS['green_highlight'] if success else COLORS['red_card']
        
        tk.Label(
            question_box,
            text=result_text,
            font=("Arial", 24, "bold"),
            bg=COLORS['bg_secondary'],
            fg=result_color
        ).pack(pady=15, padx=20)
        
        message = ("Todas las cartas han sido reveladas.\nEl universo conspira a tu favor." if success
                  else "Las cartas permanecen ocultas.\nEl camino aún no está claro.")
        
        tk.Label(
            self.result_frame,
            text=message,
            font=("Arial", 13),
            bg=COLORS['bg_main'],
            fg=COLORS['purple_mid']
        ).pack(pady=10)
        
        tk.Button(
            self.result_frame,
            text="🔄 Consultar Nuevamente",
            font=("Arial", 14, "bold"),
            bg=COLORS['purple_dark'],
            fg="white",
            activebackground=COLORS['purple_active'],
            activeforeground="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.reset_game
        ).pack(pady=20)
    
    def reset_game(self):
        """Reinicia el juego"""
        self.controller.reset()
        
        for widget in self.root.winfo_children():
            widget.place_forget()
            widget.pack_forget()
        
        self.question_text.delete("1.0", tk.END)
        self.question_frame.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    game = OracleCardGame(root)
    root.mainloop()