import pandas as pd

from classes.protein import Protein


def input(file):
    df = pd.read_csv(file)

    # seperate stability score from the letters in output file
    string = ''.join(df["amino"][:-1])

    return Protein(string)
