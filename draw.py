from multiprocessing import Process
from multiprocessing import Queue
from typing import List

from elevator import Elevator

class Screen: 
    def __init__(self) -> None:
        self.queue = Queue()

    def draw(self, elevators: List[Elevator]) -> None:
        pass