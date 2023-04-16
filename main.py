import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.label import Label


class FifteenPuzzle(GridLayout):
    tiles = ListProperty([])
    moves = NumericProperty(0)

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
                    self.moves += 1
                    self.update_tiles()
                    self.check_game_over()
                    break

    def check_game_over(self):
        if self.tiles == list(range(1, 16)) + [0]:
            self.clear_widgets()
            label = Label(text=f"You won using {self.moves} moves!", font_size=24)
            self.add_widget(label)

    def on_size(self, *args):
        Clock.schedule_once(lambda dt: self.update_tiles(), 0.1)


class FifteenPuzzleApp(App):
    def build(self):
        return FifteenPuzzle()


if __name__ == "__main__":
    Window.clearcolor = (0.1, 0.1, 0.1, 1)
    FifteenPuzzleApp().run()
