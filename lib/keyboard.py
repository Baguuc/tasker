import struct
import os


codes_names = {
  59: "f1",
  60: "f2",
  61: "f3",
  62: "f4",
  63: "f5",
  64: "f6",
  65: "f7",
  66: "f8",
  67: "f9",
  68: "f10",
  87: "f11",
  88: "f12",
  41: "`",
  2: "1",
  3: "2",
  4: "3",
  5: "4",
  6: "5",
  7: "6",
  8: "7",
  9: "8",
  10: "9",
  11: "0",
  12: "-",
  13: "=",
  15: "tab",
  16: "q",
  17: "w",
  18: "e",
  19: "r",
  20: "t",
  21: "y",
  22: "u",
  23: "i",
  24: "o",
  25: "p",
  26: "[",
  27: "]",
  30: "a",
  31: "s",
  32: "d",
  33: "f",
  34: "g",
  35: "h",
  36: "j",
  37: "k",
  38: "l",
  39: ";",
  40: "'",
  44: "z",
  45: "x",
  46: "c",
  47: "v",
  48: "b",
  49: "n",
  50: "m",
  51: ",",
  52: ".",
  53: "/",
  1: "esc",
  28: "enter",
  14: "backspace",
  69: "num lock",
  110: "insert",
  102: "home",
  104: "page up",
  109: "page down",
  107: "end",
  111: "delete",
  58: "caps lock",
  57: "space",
  29: "ctrl",
  97: "ctrl right",
  42: "shift",
  54: "shift right",
  56: "alt",
  100: "alt right",
  200: "arrow up",
  208: "arrow down",
  203: "arrow left",
  205: "arrow right",
  219: "meta",
  199: "home",
  207: "end",
  210: "insert",
  211: "delete",
  227: "fn",
  184: "right alt",
  183: "prtsc",
  157: "right control",
  201: "pgup",
  209: "pgdn",
}

names_codes = {
  "f1": 59,
  "f2": 60,
  "f3": 61,
  "f4": 62,
  "f5": 63,
  "f6": 64,
  "f7": 65,
  "f8": 66,
  "f9": 67,
  "f10": 68,
  "f11": 87,
  "f12": 88,
  "`": 41,
  "1": 2,
  "2": 3,
  "3": 4,
  "4": 5,
  "5": 6,
  "6": 7,
  "7": 8,
  "8": 9,
  "9": 10,
  "0": 11,
  "-": 12,
  "=": 13,
  "tab": 15,
  "q": 16,
  "w": 17,
  "e": 18,
  "r": 19,
  "t": 20,
  "y": 21,
  "u": 22,
  "i": 23,
  "o": 24,
  "p": 25,
  "[": 26,
  "]": 27,
  "a": 30,
  "s": 31,
  "d": 32,
  "f": 33,
  "g": 34,
  "h": 35,
  "j": 36,
  "k": 37,
  "l": 38,
  ";": 39,
  "'": 40,
  "z": 44,
  "x": 45,
  "c": 46,
  "v": 47,
  "b": 48,
  "n": 49,
  "m": 50,
  ",": 51,
  ".": 52,
  "/": 53,
  "esc": 1,
  "enter": 28,
  "backspace": 14,
  "num lock": 69,
  "insert": 110,
  "home": 102,
  "page up": 104,
  "page down": 109,
  "end": 107,
  "delete": 111,
  "caps lock": 58,
  "space": 57,
  "ctrl": 29,
  "ctrl right": 97,
  "shift": 42,
  "shift right": 54,
  "alt": 56,
  "alt right": 100,
  "arrow up": 200,
  "arrow down": 208,
  "arrow left": 203,
  "arrow right": 205,
  "meta": 219,
  "home": 199,
  "end": 207,
  "insert": 210,
  "delete": 211,
  "fn": 227,
  "right alt": 184,
  "prtsc": 183,
  "right control": 157,
  "pgup": 201,
  "pgdn": 209,
}


def get_keyboard_event_file() -> str: 
    cmd: str = r'egrep -i "keyboard.+\/dev" /var/log/Xorg.0.log'
    output: str = os.popen(cmd).read()
    lines: list[str] = output.split("\n")

    split: list[str] = lines[0].split("/")
    event_file_name: str = split[-1][:-1]
    event_file_path: str = f"/dev/input/{event_file_name}"

    return event_file_path


def get_char_input_raw_code(double=False) -> int:
    FORMAT: str = "llHHI"
    EVENT_SIZE: int = struct.calcsize(FORMAT)

    def read() -> str:
        with open(get_keyboard_event_file(), "rb") as f:
            event = f.read(EVENT_SIZE)
            (tv_sec, tv_usec, _type, code, value) = struct.unpack(FORMAT, event)
        
        return value
    
    if double:
        key1: int = read()
        key2: int = read()

        if key1 == key2:
            return key1
        
        return None
    
    return read()

def get_char_input_raw(double=False) -> str:
    code: int|None = get_char_input_raw_code(double=double)

    if code == None:
        return None

    key_char: str = codes_names[code]
    
    return key_char


def get_char_input(double=False) -> str:
    return get_char_input_raw(double=double)
