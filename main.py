# Created with ChatGPT 4.0
# 1st Prompt:  Provide the code for a 15 Puzzle.  The code should be written in Python with a UI of Kivy.
#              The tiles should automatically resize when the window is made bigger or smaller
#              so that they take up all available space. The aim of the game is to move the tiles so that
#              they are in order from 1 to 15 with the blank at the lower right. Clicking on a tile will move it,
#              provided it is adjacent to the blank.
#
# 2nd Prompt: Modify the application so that it begins from a solved state and then shuffle
#              it by randomly moving positions 5000 times.

import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty


class FifteenPuzzle(GridLayout):
    tiles = ListProperty([])

    def __init__(self, **kwargs):
        super(FifteenPuzzle, self).__init__(**kwargs)
        self.setup()
        self.shuffle_tiles(5000)
        self.update_tiles()

    def setup(self):
        self.rows = 4
        self.cols = 4
        self.spacing = 2
        self.tiles = list(range(1, 16)) + [0]

    def shuffle_tiles(self, moves):
        for _ in range(moves):
            index = self.tiles.index(0)
            row, col = divmod(index, self.cols)

            adjacent = []
            for r_offset, c_offset in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_row, new_col = row + r_offset, col + c_offset
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    new_index = new_row * self.cols + new_col
                    adjacent.append(new_index)

            target = random.choice(adjacent)
            self.tiles[index], self.tiles[target] = self.tiles[target], self.tiles[index]

    def update_tiles(self):
        self.clear_widgets()
        for value in self.tiles:
            btn = Button(text=str(value) if value > 0 else '',
                         font_size=24,
                         background_normal='',
                         background_color=(1, 1, 1, 0.3) if value > 0 else (1, 1, 1, 0))
            btn.bind(on_release=self.move_tile)
            self.add_widget(btn)

    def move_tile(self, button):
        if button.text == '':
            return

        index = self.tiles.index(int(button.text))
        row, col = divmod(index, self.cols)

        for r_offset, c_offset in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + r_offset, col + c_offset
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_index = new_row * self.cols + new_col
                if self.tiles[new_index] == 0:
                    self.tiles[index], self.tiles[new_index] = self.tiles[new_index], self.tiles[index]
                    self.update_tiles()
                    break

    def on_size(self, *args):
        Clock.schedule_once(lambda dt: self.update_tiles(), 0.1)


class FifteenPuzzleApp(App):
    def build(self):
        return FifteenPuzzle()


if __name__ == "__main__":
    Window.clearcolor = (0.1, 0.1, 0.1, 1)
    FifteenPuzzleApp().run()
