import turtle
import time
from multiprocessing import Process
from multiprocessing import Queue
from typing import List, Tuple

from elevator import Elevator



#  Create color choosing squares at the top of screen
colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black", "#F9F9F9"]


class Window:
    WIDTH = 1000
    HEIGHT = 1000

    def __init__(self, /, num_of_people: int, num_of_elevators: int = 1) -> None:
        self.setup()
        self.elevators: List[ElevatorShape] = []
        self.draw_elevators(num_of_elevators)
        self.people: List[PersonShape] = []
        self.draw_people(num_of_people)
        self.draw_agenda()
        self.loop()

    def __call__(self, queue):
        self.queue = queue

    def loop(self):
        while True:
            # self.screen.forward(1)
            time.sleep(0.01)
            # on exit turtle.done()

    def draw_elevators(self, num_of_elevators: int):
        x, y = (-400, -400)
        for _ in range(num_of_elevators):
            elevator = ElevatorShape(x, y, 3)
            x += ElevatorShape.WIDTH  # Move the next elevator to the right
            self.elevators.append(elevator)

    def draw_agenda(self):
        pass

    def draw_people(self, num_of_people: int):
        x, y = (-400, 0)
        for index in range(num_of_people):
            person = PersonShape(x, y, "Josh", colors[index])
            y += 20  # Height of a person
            self.people.append(person)
        new = self.people[0].screen.clone()
        
        new.goto(-390, -390)


    def draw(self):
        pass

    def setup(self) -> None:
        turtle.setup(width=self.WIDTH, height=self.HEIGHT, startx=200, starty=200)
        turtle.title("Elevators")


class Screen:
    def __init__(self) -> None:
        self.queue: Queue = Queue()
        self.window = Window(num_of_elevators=3, num_of_people=2)
        self.draw_process = Process(target=self.window, args=(self.queue,), daemon=True)
        self.draw_process.start()

    def draw(self, elevators: List[Elevator]) -> None:
        pass


class ElevatorShape:
    WIDTH = 100
    FLOOR_HEIGHT = 100

    def __init__(self, x: int, y: int, floors: int) -> None:
        self.floors: int = floors
        self.initial_x = x
        self.initial_y = y
        self.screen = turtle.Turtle()
        self.screen.penup()
        self.screen.goto(x, y)
        self.screen.pendown()
        self.screen.forward(self.WIDTH)
        self.screen.left(90)
        # Draw wall
        for _ in range(self.floors):
            self.screen.forward(self.FLOOR_HEIGHT)
        self.screen.left(90)
        self.screen.forward(self.WIDTH)
        self.screen.left(90)
        # Draw wall
        for _ in range(self.floors):
            self.screen.forward(self.FLOOR_HEIGHT)

        self.draw_elevator()

    def draw_elevator(self):
        # TODO: Make into shapes
        self.elevator = turtle.Shape('compound')
        # https://stackoverflow.com/questions/47144177/how-do-i-move-a-turtle-graphics-drawn-object-using-only-built-in-functions
        self.elevator = turtle.Turtle()
        self.elevator.penup()
        self.elevator.goto(self.initial_x, self.initial_y)
        self.elevator.color("red")
        self.elevator.pendown()
        self.elevator.forward(self.WIDTH)
        self.elevator.left(90)
        self.elevator.forward(self.WIDTH)
        self.elevator.left(90)
        self.elevator.forward(self.WIDTH)
        self.elevator.left(90)
        self.elevator.forward(self.WIDTH)
        self.elevator.left(90)

    def move(self, move_vector: Tuple(int)):
        pass



class PersonShape:
    def __init__(self, x: int, y: int, name: str, color: str) -> None:
        self.name = name
        self.screen = turtle.Turtle(shape="turtle")
        self.screen.color(color)
        self.screen.penup()
        self.screen.goto(x, y)
        self.screen.write(f"       {self.name}")  # Extra spaces to align on the view

class Agenda:
    pass


if __name__ == "__main__":
    screen = Screen()
