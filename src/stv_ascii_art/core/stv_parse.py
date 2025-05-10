# MIT License
# Copyright (c) 2025 星灿长风v


import argparse
from stv_ascii_art.utils.change_text import parse_text


def classify_stv_parse():
    pt = parse_text(check = True)

    parser = argparse.ArgumentParser(description=pt[0])

    parser.add_argument("--input", type=str, help=pt[1])
    parser.add_argument("-o", "--output", type=str, help=pt[2])
    parser.add_argument("-v", "--video", action="store_true", help=pt[3])
    parser.add_argument("-eh", "--enhanced", action="store_true", help=pt[4])
    parser.add_argument("-x", "--export", action="store_true", help=pt[5])
    parser.add_argument("-g", "--gpu", action="store_true", help=pt[6])
    parser.add_argument("-lic", "--license", action="store_true", help=pt[7])
    parser.add_argument("-so", "--solidify", type=str, help=pt[8])
    parser.add_argument("-V", "--version", action='store_true', help=pt[9])
    parser.add_argument("-sl", "--set_language", action="store_true", help=pt[10])
    parser.add_argument("-rs", "--reset_language", action="store_true", help=pt[11])

    args = parser.parse_args()
    return args

class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=30, width=100)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return self._metavar_formatter(action, action.dest)(1)[0]
        else:
            parts = []
            parts.extend(action.option_strings)
            return ", ".join(parts)


def stv_parse():
    pt = parse_text(check=True)
    from stv_ascii.utils.change_text import beautiful_parse_text

    bpt = beautiful_parse_text(check = True)

    parser = argparse.ArgumentParser(
        description=f"\033[1m{pt[0]}\033[0m",
        formatter_class=CustomHelpFormatter,
        add_help=False,
        epilog="Thanks for your support!"
    )

    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                            help=f"\033[1;36m{bpt[0]}\033[0m")

    input_group = parser.add_argument_group(f"\033[1;32m{bpt[1]}\033[0m")
    process_group = parser.add_argument_group(f"\033[1;34m{bpt[2]}\033[0m")
    advanced_group = parser.add_argument_group(f"\033[1;35m{bpt[3]}\033[0m")
    system_group = parser.add_argument_group(f"\033[1;33m{bpt[4]}\033[0m")

    input_group.add_argument("--input", type=str,
                             help=f"\033[96m{pt[1]}\033[0m")
    input_group.add_argument("-o", "--output", type=str,
                             help=f"\033[96m{pt[2]}\033[0m")

    process_group.add_argument("-v", "--video", action="store_true", help=f"\033[95m{pt[3]}\033[0m")
    process_group.add_argument("-eh", "--enhanced", action="store_true", help=f"\033[95m{pt[4]}\033[0m")
    process_group.add_argument("-x", "--export", action="store_true", help=f"\033[95m{pt[5]}\033[0m")

    advanced_group.add_argument("-g", "--gpu", action="store_true",  help=f"\033[93m{pt[6]}\033[0m")
    advanced_group.add_argument("-so", "--solidify", type=str, help=f"\033[93m{pt[8]}\033[0m")

    system_group.add_argument("-lic", "--license", action="store_true",help=f"\033[90m{pt[7]}\033[0m")
    system_group.add_argument("-V", "--version", action='store_true',help=f"\033[90m{pt[9]}\033[0m")
    system_group.add_argument("-sl", "--set_language", action="store_true",help=f"\033[90m{pt[10]}\033[0m")
    system_group.add_argument("-rs", "--reset_language", action="store_true",help=f"\033[90m{pt[11]}\033[0m")

    args = parser.parse_args()
    return args