#!/usr/bin/python3
from main import main


def handle(question):
    answer = main(question)
    print(answer)
    return answer


if __name__ == "__main__":
    handle(question="Quel est le siret ?")
