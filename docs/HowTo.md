# How to run the program?

The program works by firing up an event loop in the command line. The event loop will capture input from a user. 

In order to progress through defined scenarios start up the program (having installed the dependencies) by running `venv/bin/python run.py` and progress by entering ''(ENTER) in the command line while the script is running.

To change scenarios, pick a different value from the 3 presented scenarios at the beginning of the script or add your own into the `run.py` script. 


## Additional parameters

One can pass the `--draw` argument into the script to active a drawing option that will draw the current state of a program as it progresses. 


**Supported input**

- `''`/`'next'` - will progress the program in 'elevator-time'
- `'s'`/`'status'` - will print out the status about the program, including lifts and people waiting on lifts
- `'new'` - will add a new person into the waiting list, to support adding people in middle of program execution
- `'exit'` - will exit the loop of the program