class InsideBoard:
    """
    Is class representing the inside board of an elevator.
    """


class Door:
    OPEN = "O"
    CLOSED = "C"


class Elevator:
    def __init__(self, lowest_floor: int, highest_floor: int) -> None:
        self.LOWEST_FLOOR = lowest_floor
        self.HIGHEST_FLOOR = highest_floor
        self.door = Door.CLOSED
        self.current_floor = 0  # Starts from ground level

    def _up_1(self):
        if self.door != Door.CLOSED:
            raise ValueError("Cannot move the elevator if the door is not closed")
        if self.current_floor + 1 > self.HIGHEST_FLOOR:
            raise ValueError(f"Can't go higher that the {self.HIGHEST_FLOOR} floor")
        self.current_floor += 1

    def _down_1(self):
        if self.door != Door.CLOSED:
            raise ValueError("Cannot move the elevator if the door is not closed")
        if self.current_floor - 1 < self.LOWEST_FLOOR:
            raise ValueError(f"Can't go lower that the {self.LOWEST_FLOOR} floor")
        self.current_floor -= 1

    def go_up(self, levels: int) -> None:
        pass

    def go_down(self, levels: int) -> None:
        pass

