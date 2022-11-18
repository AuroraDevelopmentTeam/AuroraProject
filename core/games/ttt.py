from typing import List

import nextcord
from nextcord.ext import commands


class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=x)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.x][self.y]
        if state != 0:
            return

        if view.current_player == view.X:
            self.view.board[self.x][self.y] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.view.board[self.x][self.y] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()
        if winner is None:
            best_move = view.find_best_move()
            self.view.board[best_move[0]][best_move[1]] = view.O
            view.current_player = view.X
            content = "It is     now X's turn"

            winner = view.check_board_winner()
            if winner is not None:
                if winner == view.X:
                    content = "X won!"
                elif winner == view.O:
                    content = "O won!"
                else:
                    content = "It's a tie!"

                for child in view.children:
                    child.disabled = True

                view.stop()

        view.clear_items()

        for x in range(3):
            for y in range(3):
                if view.board[x][y] == 0:
                    button = TicTacToeButton(x, y)
                    button.row = x
                    view.add_item(button)
                elif view.board[x][y] == 1:
                    button = TicTacToeButton(x, y)
                    button.label = "O"
                    button.row = x
                    button.style = nextcord.ButtonStyle.success
                    button.disabled = True
                    view.add_item(button)
                elif view.board[x][y] == -1:
                    button = TicTacToeButton(x, y)
                    button.label = "X"
                    button.row = x
                    button.style = nextcord.ButtonStyle.danger
                    button.disabled = True
                    view.add_item(button)
        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(nextcord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    button = TicTacToeButton(x, y)
                    button.row = x
                    self.add_item(button)
                elif self.board[x][y] == 1:
                    button = TicTacToeButton(x, y)
                    button.label = "O"
                    button.row = x
                    button.style = nextcord.ButtonStyle.success
                    button.disabled = True
                    self.add_item(button)
                elif self.board[x][y] == -1:
                    button = TicTacToeButton(x, y)
                    button.label = "X"
                    button.row = x
                    button.style = nextcord.ButtonStyle.danger
                    button.disabled = True
                    self.add_item(button)

    def is_moves_left(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return True
        return False

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    def evaluate(self):
        b = self.board

        # Checking for Rows for X or O victory.
        for row in range(3):
            if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
                if b[row][0] == self.X:
                    return 10
                elif b[row][0] == self.O:
                    return -10

        # Checking for Columns for X or O victory.
        for col in range(3):

            if b[0][col] == b[1][col] and b[1][col] == b[2][col]:

                if b[0][col] == self.O:
                    return 10
                elif b[0][col] == self.X:
                    return -10

        # Checking for Diagonals for X or O victory.
        if b[0][0] == b[1][1] and b[1][1] == b[2][2]:

            if b[0][0] == self.X:
                return 10
            elif b[0][0] == self.O:
                return -10

        if b[0][2] == b[1][1] and b[1][1] == b[2][0]:

            if b[0][2] == self.X:
                return 10
            elif b[0][2] == self.O:
                return -10

        # Else if none of them have won then return 0
        return 0

    def minimax(self, depth, isMax):
        score = self.evaluate()
        if score == 10:
            return score

        if score == -10:
            return score

        if not self.is_moves_left():
            return 0

        if isMax:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.X
                        best = max(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = 0
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.O
                        best = max(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = 0
            return best

    def find_best_move(self):
        global bestVal
        best_val = -1000
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 1
                    move_val = self.minimax(0, False)
                    self.board[i][j] = 0
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val
        return best_move
