import subprocess

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

    def color(s: str, color_code: str) -> str:
        return f"{color_code}{s}{ConsoleColor.ENDC}"

class Console:
    def get_max_columns() -> int:
        tput_cols = subprocess.check_output(['tput', 'cols']).decode().strip()
        
        return tput_cols
