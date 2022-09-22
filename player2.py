from gameboard import BoardClass

class server:


    def __init__(self):
        self.Server_window = None
        self.run_server()


    def run_server(self):
        self.Server_window = BoardClass(title='Player2')
        self.Server_window.link_to_client_server = self
        self.Server_window.master.mainloop()


    def WhetherContinue(self):
        self.P1_response = self.Server_window.conn.recv(1024).decode()
        if self.P1_response == "Play Again":
            self.Server_window.playagain()
        else:
            self.Server_window.CannotMove()
            self.Server_window.computeStats()
            self.Server_window.Gameover()


    def game_started(self):
        self.Server_window.resetGameBoard()
        self.Server_window.updateGameBoard()
        self.Server_window.updateGamesPlayed()
        self.Server_window.over = False

    def P1_turn(self):
        self.Server_window.TurnLabel.config(text= f"{self.Server_window.other}'s Turn")
        self.Server_window.master.update()
        self.Server_window.CannotMove()
        self.P1_move = self.Server_window.conn.recv(1024).decode()
        self.Server_window.last_player = self.Server_window.other
        self.Server_window.othermove(int(self.P1_move))


    def P2_turn(self):
        self.Server_window.TurnLabel.config(text= "Your Turn")
        self.Server_window.master.update()
        self.Server_window.last_player = self.Server_window.own
        self.Server_window.CanMove()
        self.Server_window.CannotClick()


if __name__ == "__main__":
    server()
