from InquirerPy.validator import PathValidator
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import os
from pyfiglet import Figlet
from pathlib import Path

from src.combine import combine
from src.concatenate import concatenate

f = Figlet(font='slant')
print(f"""
----------------------------------------------------------
{f.renderText('combinator')}
ADEPT ML © TU Dortmund
----------------------------------------------------------
""")


def main():
    directory_location = inquirer.select(
        message="Where do you want to choose files from?",
        choices=[
            Choice(value=0, name="The 'data' directory in the current directory", enabled=True),
            Choice(value=1, name="A custom directory"),
            Choice(value=None, name="Exit"),
        ],
        default=0,
    ).execute()

    match directory_location:
        case 0:
            p = Path(__file__).parents[1] / "data"
            data_directory = p.resolve()
            print(data_directory)
        case 1:
            data_directory = inquirer.filepath(
                message="Please enter a path:",
                default=os.getcwd(),
                validate=PathValidator(
                    is_dir=True, message="Input is not a directory"),
                only_directories=True,
            ).execute()
        case _:
            print("cancelled")
            return

    available_data = []

    for root, dirs, files in os.walk(data_directory):
        for file in files:
            basename = os.path.basename(file)
            file_name, file_ext = basename.rsplit(".", 1)
            if file_ext == "xls":
                available_data.append(os.path.join(root, file))

    if len(available_data) <= 1:
        print("ERROR the directory was empty or contained only one file")
        return

    selected = inquirer.checkbox(
        message="Please pick the two buildings to be used for concatenation or combination:",
        choices=available_data,
        validate=lambda result: len(result) >= 2,
        invalid_message="should be exactly 2 selected",
        instruction="(select exactly 2 using 'space' on your keyboard)",
    ).execute()

    selected_util_function = inquirer.select(
        message="To you want to concatenate data from the same building or combine it from two different buildings?",
        choices=[
            Choice(value=0, name="Concatenate from same building", enabled=True),
            Choice(value=1, name="Combine from two different buildings"),
            Choice(value=None, name="Exit"),
        ],
        default=0,
    ).execute()
    
    match selected_util_function:
        case 0:
            concatenate(data_directory, selected)
        case 1:
            combine(data_directory, selected)
        case None:
            print("cancelled")
            return

if __name__ == "__main__":
    main()
