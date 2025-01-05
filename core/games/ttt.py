from typing import List
import typing
import random

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from core.locales.getters import get_msg_from_locale_by_key
from core.embeds import construct_basic_embed
from core.ui.buttons import create_button, ViewAuthorCheck, View
from core.money.updaters import update_user_balance
from core.money.getters import get_user_balance


class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=x)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        bet = self.view.bet
        view: TicTacToe = self.view
        state = view.board[self.x][self.y]
        if state != 0:
            return

        if view.current_player == view.X:
            self.view.board[self.x][self.y] = view.X
            view.current_player = view.O
            content = get_msg_from_locale_by_key(
                interaction.guild.id, "ttt_turn_o"
            )
        else:
            self.view.board[self.x][self.y] = view.O
            view.current_player = view.X
            content = get_msg_from_locale_by_key(
                interaction.guild.id, "ttt_turn_x"
            )

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"X {get_msg_from_locale_by_key(interaction.guild.id, 'win')}"
                await update_user_balance(interaction.guild.id, interaction.user.id, int(bet/2))
            elif winner == view.O:
                content = f"O {get_msg_from_locale_by_key(interaction.guild.id, 'win')}"
                await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
            else:
                content = get_msg_from_locale_by_key(
                    interaction.guild.id, "draw"
                )
                await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet/10))

            for child in view.children:
                child.disabled = True

            view.stop()
        if winner is None:
            bad_move_chance = 10
            randomizer = random.randint(1, 100)
            best_move = view.make_move(is_bad=(bad_move_chance > randomizer))
            self.view.board[best_move[0]][best_move[1]] = view.O
            view.current_player = view.X
            content = get_msg_from_locale_by_key(
                interaction.guild.id, "ttt_turn_x"
            )

            winner = view.check_board_winner()
            if winner is not None:
                if winner == view.X:
                    content = f"X {get_msg_from_locale_by_key(interaction.guild.id, 'win')}"
                    await update_user_balance(interaction.guild.id, interaction.user.id, int(bet / 2))
                elif winner == view.O:
                    content = f"O {get_msg_from_locale_by_key(interaction.guild.id, 'win')}"
                    await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet))
                else:
                    content = get_msg_from_locale_by_key(
                        interaction.guild.id, "draw"
                    )
                    await update_user_balance(interaction.guild.id, interaction.user.id, -int(bet / 10))

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
        requested = get_msg_from_locale_by_key(interaction.guild.id, "requested_by")
        msg = get_msg_from_locale_by_key(interaction.guild.id, "on_balance")
        balance = await get_user_balance(interaction.guild.id, interaction.user.id)
        embed = construct_basic_embed(
            "O | ☓",
            f"{content}",
            f"{requested} {interaction.user}\n{msg} {balance}",
            interaction.user.display_avatar,
            interaction.guild.id,
        )
        await interaction.response.edit_message(embed=embed, view=view)


class TicTacToe(nextcord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, author: typing.Union[nextcord.Member, nextcord.User], bet: typing.Optional[int]):
        self.bet = bet
        self.author = author
        super().__init__()
        self.bet = bet
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

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True

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

    def eval(self):
        winner = self.check_board_winner()
        if winner is not None:
            if winner == self.X:
                return -10
            elif winner == self.O:
                return 10
            else:
                return 0

    def minimax(self, depth, isMax):
        score = self.eval()
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
                        self.board[i][j] = 1
                        best = max(best, self.minimax(depth=depth + 1, isMax=(not isMax)))
                        self.board[i][j] = 0
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = -1
                        best = min(best, self.minimax(depth=depth + 1, isMax=(not isMax)))
                        self.board[i][j] = 0
            return best

    def make_move(self, is_bad: bool) -> tuple:
        if is_bad is True:
            moves = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        moves.append((i, j))

            move = random.choice(moves)
        else:
            move = self.find_best_move()
        return move

    def find_best_move(self) -> tuple:
        bestVal = -1000
        bestMove = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 1
                    moveVal = self.minimax(0, False)
                    self.board[i][j] = 0
                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal

        return bestMove
