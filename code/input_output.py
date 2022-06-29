import csv
import os
import pandas as pd

from classes.protein import Protein


def input(file):
    """
    Recreates a protein instance from the letters detailed in an
    output file of a certain protein

    Parameters
    ----------
    file : csv_file
        output file for certain protein
    """
    df = pd.read_csv(file)

    # seperate stability score from the letters in output file
    string = ''.join(df["amino"][:-1])

    return Protein(string)


def output(protein: Protein, subdir: str = "/", prefix: str = "output"):
    """
    Writes a protein to a comma-seperated values file at the filename of
    the format `{prefix}_{sha1(protein)}.csv`

    Parameters
    ----------
    protein : Protein
        the protein to save to file
    subdir : str, optional
        the subdirectory to save the file to
    prefix : str, optional
        the file's prefix, by default "output"

    See Also
    --------
    `Protein.to_sha1`: function used to create sha1 hash from the object
    """

    if not isinstance(protein, Protein):
        raise \
            TypeError("protein argument {protein} must be a Protein instance.")

    filename = f"{prefix}_{Protein.to_sha1(protein)}.csv"
    directory = f"{os.getcwd()}/data/{subdir}"

    # create dir if it does not already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # save file if a file with that hash doesn't already exist
    if not os.path.exists(f"{directory}/{filename}"):
        with open(f"{directory}/{filename}", "w") as f:
            print(f"Writing results to {directory}/{filename}")
            writer = csv.writer(f)

            writer.writerow(["index", "amino", "fold"])

            for amino in protein.aminos:
                writer.writerow([amino.index, amino.type, amino.direction])

            writer.writerow(["score", protein.score])

    return
