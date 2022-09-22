from gameboard import BoardClass

class client:


    def __init__(self):
        self.Client_window = None
        self.run_client()

    def run_client(self):
        self.Client_window = BoardClass(title='Player1')
        self.Client_window.link_to_client_server = self
        self.Client_window.master.mainloop()

    def game_started(self):
        self.Client_window.resetGameBoard()
        self.Client_window.updateGameBoard()
        self.Client_window.updateGamesPlayed()
        self.Client_window.over = False

    def P1_turn(self):
        self.Client_window.TurnLabel.config(text= "Your Turn")
        self.Client_window.master.update()
        self.Client_window.last_player = self.Client_window.own
        self.Client_window.CanMove()
        self.Client_window.CannotClick()

    def P2_turn(self):
        self.Client_window.TurnLabel.config(text=f"{self.Client_window.other}'s Turn")
        self.Client_window.master.update()
        self.Client_window.CannotMove()
        self.P2_move = self.Client_window.socket.recv(1024).decode()
        self.Client_window.last_player = self.Client_window.other
        self.Client_window.othermove(int(self.P2_move))


    def WhetherContinue(self):
        self.Client_window.Continue_or_not()


if __name__ == "__main__":
    client()
