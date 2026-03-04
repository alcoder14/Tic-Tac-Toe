import tkinter as tk

class TicTacToe:
    def __init__(self, root):
        """
        Inicializacija igre: ustvarimo glavno okno, stanje igre, gumb in label za status.
        """
        self.root = root
        self.root.title("Tic Tac Toe - Minimax AI")

        # Igralna tabla: 9 praznih polj
        self.board = [""] * 9

        # Seznam gumbov za grafični prikaz
        self.buttons = []

        # Ali je igra končana
        self.game_over = False

        # Label zgoraj, ki prikazuje status igre
        self.status_label = tk.Label(root, text="Tvoja poteza (X)", font=("Arial", 16))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Ustvarimo igralno mrežo 3x3
        self.create_board()

        # Gumb za reset igre, vedno spodaj
        self.reset_button = tk.Button(root, text="Nova igra", font=("Arial", 14), command=self.reset_game)
        self.reset_button.grid(row=5, column=0, columnspan=3, pady=10)

    def create_board(self):
        """
        Ustvari 3x3 mrežo gumbov za igro Tic Tac Toe.
        Vsak gumb kliče player_move ob kliku.
        """
        for i in range(9):
            button = tk.Button(
                self.root,
                text="",                 # začetno prazno
                font=("Arial", 32),      # velik font za X in O
                width=5,
                height=2,
                command=lambda i=i: self.player_move(i)  # lambda ohrani indeks i
            )
            # Postavimo gumbe v mrežo
            # Začetek v vrstici 1, ker je vrstica 0 status label
            button.grid(row=(i // 3) + 1, column=i % 3)
            self.buttons.append(button)

    def player_move(self, index):
        """
        Funkcija, ki se sproži ob potezi igralca (X).
        - Posodobi stanje table.
        - Preveri zmago ali neodločeno.
        - Če igra ni končana, sproži potezo AI.
        """
        if self.board[index] == "" and not self.game_over:
            # Nastavimo X na tabelo in gumb
            self.board[index] = "X"
            self.buttons[index].config(text="X")

            # Preverimo, če je igralec zmagal
            if self.check_winner("X"):
                self.end_game("Zmagal si!")
                return
            # Preverimo, če je neodločeno
            elif "" not in self.board:
                self.end_game("Neodločeno!")
                return

            # AI razmišlja
            self.status_label.config(text="AI razmišlja...")
            self.set_buttons_state("disabled")  # onemogočimo klikanje med razmišljanjem
            self.root.after(500, self.ai_move)  # majhen zamik, da se status label prikaže

    def ai_move(self):
        """
        Funkcija za AI potezo (O) z Minimax algoritmom.
        Izbere optimalno potezo in posodobi tablo.
        """
        best_score = float("-inf")
        best_move = None

        # Preiščemo vse možne poteze AI
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)  # preverimo vrednost poteze
                self.board[i] = ""  # povrnemo stanje
                if score > best_score:
                    best_score = score
                    best_move = i

        # Postavimo optimalno potezo
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O")

        # Preverimo, ali je AI zmagal ali je neodločeno
        if self.check_winner("O"):
            self.end_game("AI je zmagal!")
        elif "" not in self.board:
            self.end_game("Neodločeno!")
        else:
            # Nadaljujemo z igralčevo potezo
            self.status_label.config(text="Tvoja poteza (X)")
            self.set_buttons_state("normal")

    def minimax(self, board, depth, is_maximizing):
        """
        Minimax algoritm za AI.
        - is_maximizing=True: AI poskuša maksimizirati rezultat
        - is_maximizing=False: igralec poskuša minimizirati AI rezultat
        Vrednosti: +1 = AI zmaga, -1 = igralec zmaga, 0 = neodločeno
        """
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if "" not in board:
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        """
        Preveri, če je določen igralec zmagal.
        - player: "X" ali "O"
        """
        win_positions = [
            [0,1,2], [3,4,5], [6,7,8],  # vrstice
            [0,3,6], [1,4,7], [2,5,8],  # stolpci
            [0,4,8], [2,4,6]            # diagonale
        ]
        for pos in win_positions:
            if all(self.board[i] == player for i in pos):
                return True
        return False

    def end_game(self, message):
        """
        Zaključi igro:
        - Prikaže sporočilo v status label
        - Onemogoči gumbke (mreža)
        """
        self.status_label.config(text=message)
        self.game_over = True
        self.set_buttons_state("disabled")

    def reset_game(self):
        """
        Ponastavi igro na začetno stanje:
        - Prazna tabla
        - Omogočeni gumbi
        - Status label nastavi na začetni tekst
        """
        self.board = [""] * 9
        self.game_over = False
        self.status_label.config(text="Tvoja poteza (X)")
        for i, button in enumerate(self.buttons):
            button.config(text="", state="normal")

    def set_buttons_state(self, state):
        """
        Nastavi stanje gumbov na 'normal' ali 'disabled'
        - Blokira samo prazna polja, da ne prekrijejo že postavljenih X/O
        """
        for button in self.buttons:
            if button["text"] == "":
                button.config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()