import csv

from colorama import Fore, Style


def get_csv_content_list(csv_path: str) -> list[list]:
    with open(csv_path, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = [row for row in csv_reader]
        return rows


def alert(*args: list) -> None:
    print(Fore.RED)
    print(*args, Style.RESET_ALL)


def success(*args: list) -> None:
    print(Fore.GREEN)
    print(*args, Style.RESET_ALL)


def warning(*args: list) -> None:
    print(Fore.YELLOW)
    print(*args, Style.RESET_ALL)
