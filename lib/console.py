import os
import re
import subprocess
from enum import Enum, auto
from lib.keyboard import get_char_input


class ConsoleColor:
    CYAN: str = '\033[96m'
    PURPLE: str = '\033[95m'
    BLUE: str = '\033[94m'
    YELLOW: str = '\033[93m'
    GREEN: str = '\033[92m'
    RED: str = '\033[91m'
    UNDERLINE: str = '\033[4m'
    BOLD: str = '\033[1m'
    ENDC: str = '\033[0m'

    def color(s: str, color_code: str | list[str]) -> str:
        if type(color_code):
            color_codes_str: str = "".join(color_code)
            
            return f"{color_codes_str}{s}{ConsoleColor.ENDC}"
        elif type(color_code):
            return f"{color_code}{s}{ConsoleColor.ENDC}"
        else:
            return s

class Alignment(Enum):
    Left = auto()
    Center = auto()
    Right = auto()

class Console:
    def get_max_columns() -> int:
        tput_cols = subprocess.check_output(['tput', 'cols']).decode().strip()
        cols: int = int(tput_cols)
        
        if cols % 2 != 0:
            cols -= 1

        return cols
    
    def print_aligned(s: str, alignment: Alignment):
        if alignment == Alignment.Left:
            print(s)
            return

        column_count: int = Console.get_max_columns()
        slen: int = len(s)
        COLOR_CODE_PATTERN = r'(\x1B(?:\[([0-9]{1,2}(;[0-9]{1,2})?)m|))'       
        color_occurences: list = re.findall(COLOR_CODE_PATTERN, s)
        total_color_len: int = 0

        for occurence in color_occurences:
            total_color_len += len(occurence[0])

        slen -= total_color_len

        if alignment == Alignment.Center:
            pad_times: int = (column_count - slen) // 2
            pad: str = " " * pad_times
            print(f"{pad}{s}")
            
            return

        if alignment == Alignment.Right:
            pad_times: int = (column_count - slen)
            pad: str = " " * pad_times
            print(f"{pad}{s}")

            return
    
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class Screen:
    def render(lines: list[str], on_key_down: callable):
        rowcount: int = len(lines)
        for line in lines:
            print(f"\r{line}\n", sep="", end="")
        
        _continue, lines = on_key_down(get_char_input(), lines)
        
        if not _continue:
            print(f"\033[{rowcount}A", sep="", end="")
            return
        
        print(f"\033[{rowcount}A", sep="", end="")
        Screen.render(lines, on_key_down)
