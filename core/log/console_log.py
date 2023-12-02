class TColors:
    HEADER = '\033[95m'  # purple
    OKBLUE = '\033[94m'  # blue
    OKCYAN = '\033[96m'  # cyan
    OKGREEN = '\033[92m'  # green
    WARNING = '\033[93m'  # yellow
    FAIL = '\033[91m'  # red
    END = '\033[0m'  # white
    BOLD = '\033[1m'  # print thick
    UNDERLINE = '\033[4m'  # underline


def c_log(color, text):
    print(color + text + TColors.END)