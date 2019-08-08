#!/usr/bin/env python3

from typing import Dict
from random import randint

class Cell:
    def __init__(
            self,
            # health:int = 1,
            strategy:Dict[int, str] = {0:"death", 1:"still", 2:"reproduce"}
        ):
        # self.health = health
        self.strategy = strategy

    def step(self, eat:int):
        return self.strategy.get(eat, "still")

class Space:
    def __init__(self, number_cells=10, number_eats=200):
        self.number_cells = number_cells
        self.number_eats = number_eats

        self.iteration = 0
        self.avg_live = float(number_cells)

        self.set_up()

    def set_up(self):
        self.cells = [Cell() for _ in range(self.number_cells)]
        self.eats_taken = [list() for _ in range(self.number_eats)]

    def step(self):
        self.eats = [(0, 0, 0, 1, 1, 2, 2, 2)[randint(0, 7)] for _ in range(self.number_eats)]
        for place in self.eats_taken:
            place.clear()

        for cell in self.cells:
            i = 0
            while i < 100:
                place_index = randint(0, len(self.eats_taken) - 1)
                place = self.eats_taken[place_index]
                if len(place) > 2:
                    i += 1
                    continue
                place.append(cell)
                break
            else:
                raise Exception(f"Max iteration {i}")

        for index, place in enumerate(self.eats_taken):
            if len(place) == 1:
                step = place[0].step(self.eats[index])
                if step == "death":
                    place.clear()
                elif step == "reproduce":
                    place.append(Cell())
            if len(place) == 2:
                eat = self.eats[index]
                if eat == 0:
                    place.clear()
                if eat == 1:
                    death = randint(0, 1)
                    place.pop(death)
                    step = place[0].step(eat)
                if eat == 2:
                    step = place[0].step(eat/2)
                    step = place[0].step(eat/2)

        self.cells = list()
        for place in self.eats_taken:
            for cell in place:
                self.cells.append(cell)

        self.avg_live = (self.avg_live * self.iteration + len(self.cells)) / max(self.iteration + 1, 1)
        self.iteration += 1

    def __str__(self):
        return f"[i{self.iteration:3}][avg{self.avg_live:.0f}][cur{len(self.cells)}]{min(len(self.cells), 120)*'-'}>"

if __name__ == "__main__":
    space = Space()

    for i in range(100):
        print(space)
        space.step()
        if not space.cells:
            print("All dead!")
            break