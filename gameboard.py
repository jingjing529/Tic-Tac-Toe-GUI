import tkinter as tk
import socket
from tkinter import messagebox

class BoardClass:


    def __init__(self, title: str = '', other: str ='', last_player: str = "", num_win: int = 0, num_tie: int = 0, num_loss: int = 0, total: int = 0) -> None:
        self.title = title
        self.other = other
        self.last_player = last_player
        self.num_win = num_win
        self.num_tie = num_tie
        self.num_loss = num_loss
        self.total = total
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.link_to_client_server = None
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        self.CreateWindow()

        self.user = tk.StringVar()
        self.host = tk.StringVar()
        self.port = tk.StringVar()

        self.create_host_info()
        self.create_port_info()
        self.create_connect_button()

        self.resetGameBoard()
        self.place_board()
        self.CannotMove()


    def CreateWindow(self) -> None:
        """Create tkinter window."""
        self.master = tk.Tk()
        self.master.title(self.title)
        self.master.geometry('430x480')
        self.master.resizable(1, 1)


    def create_host_info(self) -> None:
        """Create host label and entry."""
        self.HostLabel = tk.Label(self.master, text='Host:')
        self.HostLabel.grid(row=0,column=0)
        self.HostEntry = tk.Entry(self.master, textvariable=self.host)
        self.HostEntry.grid(row=0,column=1)


    def create_port_info(self) -> None:
        """Create port label and entry."""
        self.PortLabel = tk.Label(self.master, text='Port:')
        self.PortLabel.grid(row=1,column=0)
        self.PortEntry = tk.Entry(self.master, textvariable=self.port)
        self.PortEntry.grid(row=1,column=1)


    def create_connect_button(self) -> None:
        """Create connect button."""
        self.connect_button = tk.Button(self.master, text='Connect', command=lambda: self.click_connect())
        self.connect_button.grid(row=1,column=2)


    def click_connect(self) -> None:
        """Handle connect when clicked the button."""
        if self.title == 'Player1':
            try:
                self.socket.connect((self.HostEntry.get(), int(self.PortEntry.get())))
                self.connect_button.destroy()
                self.create_user_info()
                self.create_submit_button()
            except:
                self.bad_connection()
        else:
            self.socket.bind((self.HostEntry.get(), int(self.PortEntry.get())))
            self.socket.listen(1)
            self.conn, self.addr = self.socket.accept()
            self.connect_button.destroy()
            self.create_user_info()
            self.WaitForClient()
            self.recv_other_user_info()
            self.create_submit_button()


    def bad_connection(self) -> None:
        """Ask if the player want to try again when meet bad connection."""
        self.ClientResponse = messagebox.askyesno(title='Bad Connection',
                             message="Connection cannot be made, do you want to try again?")
        if self.ClientResponse == True:
            pass
        else:
            self.master.destroy()

    def create_user_info(self) -> None:
        """Create username label and entry."""
        self.UserLabel = tk.Label(self.master, text='Your Name:')
        self.UserLabel.grid(row=2, column=0)
        self.UserEntry = tk.Entry(self.master, textvariable=self.user)
        self.UserEntry.grid(row=2, column=1)

    def create_submit_button(self) -> None:
        """Create submit button."""
        self.submit_button = tk.Button(self.master, text='Submit', command=lambda: self.click_submit())
        self.submit_button.grid(row=3, column=0)


    def recv_other_user_info(self) -> None:
        """Recieve other player's username."""
        if self.title == 'Player1':
            self.other = self.socket.recv(1024).decode()
        else:
            self.other = self.conn.recv(1024).decode()


    def click_submit(self) -> None:
        """Handle submit when clicked the button."""
        self.own = self.UserEntry.get()
        if not self.own.isalnum():
            self.invalid_name()
        else:
            if self.title == 'Player1':
                self.socket.sendall(self.own.encode())
                self.recv_other_user_info()
            else:
                self.conn.sendall(self.own.encode())
            self.submit_button.destroy()
            self.Turn_Display()
            self.link_to_client_server.game_started()
            self.link_to_client_server.P1_turn()


    def invalid_name(self) -> None:
        """Show error when name is invalid."""
        messagebox.showerror(title = 'Username Invalid', message = "Error: Please enter an alphanumeric username with no special characters")


    def place_board(self) -> None:
        """Place all the button on the board."""
        self.row_index = 5
        self.column_index = 0
        self.button_1 = tk.Button(self.master, text=self.board[0], width=12, height=6,
                                  command=lambda: self.move(0))

        self.button_2 = tk.Button(self.master, text=self.board[1], width=12, height=6,
                                  command=lambda: self.move(1))

        self.button_3 = tk.Button(self.master, text=self.board[2], width=12, height=6,
                                  command=lambda: self.move(2))

        self.button_4 = tk.Button(self.master, text=self.board[3], width=12, height=6,
                                  command=lambda: self.move(3))

        self.button_5 = tk.Button(self.master, text=self.board[4], width=12, height=6,
                                  command=lambda: self.move(4))

        self.button_6 = tk.Button(self.master, text=self.board[5], width=12, height=6,
                                  command=lambda: self.move(5))
        self.button_7 = tk.Button(self.master, text=self.board[6], width=12, height=6,
                                  command=lambda: self.move(6))
        self.button_8 = tk.Button(self.master, text=self.board[7], width=12, height=6,
                                  command=lambda: self.move(7))
        self.button_9 = tk.Button(self.master, text=self.board[8], width=12, height=6,
                                  command=lambda: self.move(8))

        self.all_buttons = [self.button_1, self.button_2, self.button_3, self.button_4, self.button_5, self.button_6, self.button_7, self.button_8, self.button_9]

        for value in range(9):
            if value != 0 and value % 3 == 0:
                self.row_index += 1
                self.column_index = 0
            self.all_buttons[value].grid(row=self.row_index, column=self.column_index)
            self.column_index += 1


    def resetGameBoard(self) -> None:
        """Clear all the moves from game board."""
        for i in range(len(self.board)):
            self.board[i] = ' '


    def CanMove(self) -> None:
        """Enable the buttons when own turn."""
        for button in self.all_buttons:
            button['state'] = 'normal'


    def CannotMove(self) -> None:
        """Enable the buttons when other's turn."""
        for button in self.all_buttons:
            button['state'] = 'disabled'


    def updateGamesPlayed(self) -> None:
        """Keep track how many games have started."""
        self.total += 1


    def move(self, which_clicked) -> None:
        """Handle clicked board button."""
        if self.board.count(' ') % 2 == 0 and self.board[which_clicked] == ' ':
            self.board[which_clicked] = 'O'
        elif self.board.count(' ') % 2 == 1 and self.board[which_clicked] == ' ':
            self.board[which_clicked] = 'X'
        self.all_buttons[which_clicked]["state"] = "disabled"
        self.updateGameBoard()
        if self.title == 'Player1':
            self.socket.sendall(str(which_clicked).encode())
        else:
            self.conn.sendall(str(which_clicked).encode())
        self.master.update()
        self.check_if_over()


    def CannotClick(self) -> None:
        """Disable the button clicked."""
        for button in self.all_buttons:
            if button['text'] != ' ':
                button['state'] = 'disabled'


    def othermove(self, which_clicked) -> None:
        """Place other's move on the board."""
        if self.board.count(' ') % 2 == 0 and self.board[which_clicked] == ' ':
            self.board[which_clicked] = 'O'
        elif self.board.count(' ') % 2 == 1 and self.board[which_clicked] == ' ':
            self.board[which_clicked] = 'X'
        self.all_buttons[which_clicked]["state"] = "disabled"
        self.updateGameBoard()
        self.master.update()
        self.check_if_over()


    def updateGameBoard(self) -> None:
        """Update the game board with the player's move."""
        for index, text_b in enumerate(self.board):
            self.all_buttons[index].config(text=text_b)


    def check_if_over(self) -> None:
        """Check if the game is over."""
        if self.isWinner() or self.boardIsFull():
            self.link_to_client_server.WhetherContinue()
        else:
            if (self.last_player == self.own and self.title == "Player1") or (self.last_player != self.own and self.title != "Player1"):
                self.link_to_client_server.P2_turn()
            elif (self.last_player == self.own and self.title != "Player1") or (self.last_player != self.own and self.title == "Player1"):
                self.link_to_client_server.P1_turn()


    def WaitForClient(self) -> None:
        """Tell server to wait for client inputting the name."""
        messagebox.showinfo(title='waiting...', message = "Connection succeeded!\nPlease wait for player1 to input username")


    def Turn_Display(self) -> None:
        """Display whose turn it is."""
        self.TurnLabel = tk.Label(self.master, text= ' ')
        self.TurnLabel.grid(row=3, column=0)


    def Continue_or_not(self) -> None:
        """Ask client if continue."""
        self.response = messagebox.askyesno(title = 'Game Over', message=f"Hi {self.own}, this game has finished, do you want to play again?")
        if self.response == True:
            self.link_to_client_server.game_started()
            self.socket.sendall("Play Again".encode())
            self.link_to_client_server.P1_turn()
        else:
            self.socket.sendall("Fun Times".encode())
            self.CannotMove()
            self.computeStats()
            self.Gameover()


    def isWinner(self) -> bool:
        """Check if the latest move resulted in a win and update the wins and losses count."""
        if self.board[0] == self.board[1] == self.board[2] != ' ' or self.board[3] == self.board[4] == self.board[
            5] != ' ' or \
                self.board[6] == self.board[7] == self.board[8] != ' ':
            # check if the horizontal line has the same elements
            if self.last_player == self.other:
                # if the game ends at the other player's side, result in a loss
                self.num_loss += 1
                self.loss_result()
            else:
                # if the game ends at current player's side, result in a win
                self.num_win += 1
                self.win_result()
            return True
        elif self.board[0] == self.board[3] == self.board[6] != ' ' or self.board[1] == self.board[4] == self.board[
            7] != ' ' or \
                self.board[2] == self.board[5] == self.board[8] != ' ':
            # check if the vertical line has the same elements
            if self.last_player == self.other:
                # check if the game ends at the other player's side, if so, result in a loss
                self.num_loss += 1
                self.loss_result()
            else:
                # if the game ends at current player's side, result in a win
                self.num_win += 1
                self.win_result()
            return True
        elif self.board[0] == self.board[4] == self.board[8] != ' ' or self.board[2] == self.board[4] == self.board[
            6] != ' ':
            # check if the diagonal line has the same elements
            if self.last_player == self.other:
                # check if the game ends at the other player's side, if so, result in a loss
                self.num_loss += 1
                self.loss_result()
            else:
                # if the game ends at current player's side, result in a win
                self.num_win += 1
                self.win_result()
            return True
        else:
            return False


    def loss_result(self) -> None:
        """Show loss result."""
        messagebox.showinfo(title='you lost', message=f"Game over!\nSorry {self.own} but you lost")


    def win_result(self) -> None:
        """Show win result."""
        messagebox.showinfo(title = "You Won", message = f"Game over!\nCongratulations {self.own} you won")


    def boardIsFull(self) -> bool:
        """Check if the board is full (I.e. no more moves to make - tie) and update the ties count."""
        full = True
        for element in self.board:
            if element == ' ':
                full = False
        if full == True:
            self.num_tie += 1
            messagebox.showinfo(title="Tie", message="Game over!\nIt's a tie")
        return full


    def playagain(self) -> None:
        """Tell P2 to play again and game restart when P2 click ok in messagebox."""
        messagebox.showinfo(title='Play Again', message= f"{self.other} wants to play again")
        self.link_to_client_server.game_started()
        self.link_to_client_server.P1_turn()


    def computeStats(self) -> None:
        """Prints the following each on a new line:
        Print:
            the players' username
            the username of the last person to make a move
            the number of games
            the number of wins
            the number of losses
            the number of ties

        """
        messagebox.showinfo(title='Stats',
                            message=f'User name: {self.own}\nthe other player: {self.other}\nlast player: {self.last_player}\nGames total: {self.total}\nGames won: {self.num_win}\nGames lost: {self.num_loss}\nGames tied: {self.num_tie}')


    def Gameover(self) -> None:
        """Game over and close socket."""
        if self.title == 'Player1':
            self.socket.close()
        else:
            self.conn.close()
