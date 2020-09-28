import time
from typing import List

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from elevator import Controller
from elevator import Elevator
from elevator import Person


bottom_toolbar = HTML(
    'Running elevator program, type <b><style bg="ansired">exit</style></b> to quit the program!'
)
session = PromptSession()


class Program:
    def __init__(self, controller: Controller, people: List[Person]) -> None:
        self.lift_controller: Controller = controller
        self.people: List[Person] = people
        self.waiting_for_elevator: List[Person] = people

    def report_status(self) -> None:
        """Prints out the status of the program"""

        def names(people) -> List[str]:
            return [person.name for person in people]

        for elevator in self.lift_controller.elevators.values():
            print(f"The elevator is at {elevator.floor} floor.")
            print(f"People in the elevator {names(elevator.people)}")
        print(f"People waiting for a lift {names(self.waiting_for_elevator)}")

    def add_person_to_lift(self, elevator: Elevator,person: Person) -> None:
        """
        Moves a person into a lift. 

        TODO: Provide better abstractions for adding and removing people.
        """
        if not elevator.door.is_open:
            elevator.open_door()
        elevator.people.append(person)
        self.waiting_for_elevator.remove(person)
        print(f"{person.name} has entered the lift at {elevator.floor} floor")

    def remove_person_to_lift(self, elevator: Elevator, person: Person) -> None:
        """
        Removes people from a lift. 

        TODO: Provide better abstractions removing people from a lift.
        """
        if not elevator.door.is_open:
            elevator.open_door()
        elevator.people.remove(person)

        # If there are not people in the lift, it is not moving nowhere
        if not elevator.people:
            elevator.moving_to = None
        print(f"{person.name} has left the lift at {elevator.floor} floor")

    def next(self) -> None:
        """
        Method triggering an action driven progression through a scenario.
        """
        # Remove people leaving at current floors
        for elevator in self.lift_controller.elevators.values():
            for person in elevator.people_leaving:
                return self.remove_person_to_lift(elevator, person)

        for person in self.waiting_for_elevator:
            # Move people waiting into lifts if there is a lift at their floor
            if elevator := self.lift_controller.elevator_at(person.enter_floor):
                return self.add_person_to_lift(elevator, person)
            else:
                # For people waiting on the lift calls the elevator
                on_its_way = self.lift_controller.call_elevator(person.enter_floor)
                if on_its_way:
                    return print(f"An elevator for {person.name} is on its way!")

        # Action elevators
        self.lift_controller.move_elevators()


    def handle_input(self, answer: str) -> None:
        """
        A method that handles the input and therefore program progress 
        """
        answer = answer.lower()
        if answer in ["", "next"]:
            self.next()
        elif answer in ["new"]:
            self.enter_a_person()
        elif answer in ["s", "status"]:
            self.report_status()
        else:
            print(f"No action for '{answer}'")

    def enter_a_person(self) -> None:
        """
        On being called takes input and adds a person to the waiting people
        """
        name = session.prompt("> ", bottom_toolbar=HTML("Enter a person's name"))
        enter_floor = session.prompt(
            "> ", bottom_toolbar=HTML("The floor they called the elevator")
        )
        exit_floor = session.prompt(
            "> ", bottom_toolbar=HTML("The floor they need to exit")
        )
        self.people.append(Person(name, enter_floor, exit_floor))


scenario_1 = Program(
    controller=Controller(),
    people=[
        Person("John", 0, 3),
        Person("Jack", 0, 4),
        Person("Jackson", 2, -1),
        Person("Janet", 2, 3),
    ],
)
scenario_1.lift_controller.add_elevator(Elevator(-1, 4))


# Scenario at which the first person is not at the ground floor
scenario_2 = Program(
    controller=Controller(),
    people=[
        Person("John", 1, 3),
        Person("Jack", 0, -2),
        Person("Jackson", 2, -1),
        Person("Janet", 2, 3),
    ],
)
scenario_2.lift_controller.add_elevator(Elevator(-3, 5))

# Scenario with multiple lifts
scenario_3 = Program(
    controller=Controller(),
    people=[
        Person("John", 1, 3),
        Person("Jack", 0, -2),
        Person("Jackson", 2, -1),
        Person("Janet", 2, 3),
        Person("Joe", -3, 5),
        Person("Jonathan", -1, 6),
    ],
)
scenario_3.lift_controller.add_elevator(Elevator(-3, 5))
scenario_3.lift_controller.add_elevator(Elevator(-1, 6))


if __name__ == "__main__":
    program = scenario_3

    while True:
        answer = session.prompt("> ", bottom_toolbar=bottom_toolbar)
        if answer == "exit":
            break
        try:
            program.handle_input(answer=answer)
        except ValueError as error:
            print(error)

        # Avoid cooking CPU
        time.sleep(0.01)

