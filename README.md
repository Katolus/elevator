# Elevator

Elevator simulator written in Python.
In order to learn how to progress through this program, go to the [how-to](./docs/HowTo.md) document.

## Requirements

- Python 3.8.5

## Prerequisites

- You will need to install `virtualenv` if yet not present in your packages. Command: `pip install virtualenv`.
- Install dependencies by running.

```
virtualenv venv
venv/bin/pip install -r requirements.txt
```

## How to run the program?

- Run `venv/bin/python run.py` in the root directory

## How to run tests?

- Run `./venv/bin/python -m pytest` in the root directory

## In the pipeline

- Enhance test coverage
- Enhance error types (better type chosen, custom types)
- Add integration tests for the program itself
- More scenarios
- Find a better way to progress through program time
- More / better input commands
- Provide better, better abstractions for actions like `self.elevator.people.remove(person)`
- Provide more user friendly running scripts

## Learnings

- Learned some new parts of python vocabularies like 'OrderedDict'
- Got a better understanding of abstractions
- Putting more effort into planing before starting to code pays back
- Considered a controller class from the start would be a better and more efficient way of progress
