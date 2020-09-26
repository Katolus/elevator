from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML


bottom_toolbar = HTML('Running elevator program, type <b><style bg="ansired">exit</style></b> to quit the program!')
session = PromptSession()


if __name__ == "__main__":
    answer = session.prompt("> ", bottom_toolbar=bottom_toolbar)
    if answer == 'exit':
        pass
        # break
    print('You said', answer)