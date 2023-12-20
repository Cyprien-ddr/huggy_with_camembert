import sys
from help_message import help_message


def handle_error():
    if len(sys.argv) == 1:
        return
    elif sys.argv[1] == "-h":
        help_message()
        sys.exit(0)
    elif len(sys.argv) != 1:
        print("Dear user, please run the following command:\n$ ./main -h")
        sys.exit(1)
