# Module imports
import matplotlib.pyplot as plot
from matplotlib.path import Path
import matplotlib.patches as patches
import pandas as pd
import os
from typing import Any, Callable, Union

# Local imports
from classes.protein import Protein
from classes.amino import Amino
from algorithms.random_protein import fold_randomly


def visualize_protein(prot: Protein, save_fig=False):
    """Visualizes a protein in matplotlib.

    Parameters
    ----------
    prot : Protein
        the protein instance to visualize

    See Also
    --------
    .. _Path tutorial:
        https://matplotlib.org/stable/tutorials/advanced/path_tutorial.html

    To Do
    -----
    - Center figure `example https://stackoverflow.com/a/4718438`
    - Add H-bonds and score
`    """

    points = [(0.0, 0.0)]
    circles = []
    bonds, processed = [], []
    codes = [Path.MOVETO]
    min_x = max_x = min_y = max_y = 0

    for amino in prot.aminos:
        x, y = points[len(points)-1]

        # creëer cirkel
        amino_circle = plot.Circle(
            (x, y),
            .10,
            color="{}".format("red" if amino.type == "H" else "blue")
        )
        circles.append(amino_circle)

        # teken geen lijn als we bij de laatste amino zijn
        if(len(circles) == len(prot)):
            break

        # zoek het volgende punt om een lijn naar te tekenen
        x, y = Amino.get_coordinates_at(amino, amino.direction)
        min_x, max_x = min(x, min_x), max(x, max_x)
        min_y, max_y = min(y, min_y), max(y, max_y)

        # voeg de lijn toe aan de lijst
        points.append((x, y))
        codes.append(Path.LINETO)

    # sluit het pad af
    points.append((0.0, 0.0))
    codes.append(Path.STOP)

    # loop door the bonden
    for b in prot.calculate_bonds(prot.aminos):
        if b not in processed:
            # maak een stippellijn aan
            path = Path(
                [
                    (b.origin.x, b.origin.y),
                    (b.target.x, b.target.y),
                    (0.0, 0.0)
                ],
                [
                    Path.MOVETO,
                    Path.LINETO,
                    Path.STOP
                ]
            )
            bonds.append(path)
            processed.append(b)

    # voeg de lijntekening toe
    path = Path(points, codes)
    fig, ax = plot.subplots()
    patch = patches.PathPatch(path, facecolor="none", lw=2)
    ax.add_patch(patch)

    # voeg de bonden toe
    for b in bonds:
        bond_patch = patches.PathPatch(b, facecolor="none", lw=1, ls="--")
        ax.add_patch(bond_patch)

    # voeg de cirkels toe
    for circle in circles:
        ax.add_patch(circle)

    # zet de x en y axis
    ax.set_xlim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)
    ax.set_ylim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)

    # voeg legende en titel toe
    # zie:
    #   https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
    legend = [
        patches.Patch(color="red", label="Hydrofoob"),
        patches.Patch(color="blue", label="Polair"),
        patches.Patch(color="none", label=f"Stabiliteit: {prot.score}")
    ]

    ax.legend(handles=legend)
    fig.suptitle(prot.types)

    # sla op in output als de vlag is meegegeven
    if save_fig:
        if not os.path.exists("data/"):
            os.makedirs("data/")
        plot.savefig(fname=f"{os.path.abspath('data/')}/{prot.types}.png")

    # laat het figuur zien
    plot.show()


def visualize_scores(
        prot_str: str,
        algorithm: Callable[[Union[str, Protein]], Any]
        ) -> None:
    """Assesses average performance of an algorithm and visualizes the results

    Parameters
    ----------
    prot_str : str
        string representing the protein to test the algorithm with
    algorithm : Callable[[Union[str, Protein]], Any]
        the algorithm to test


    Notes
    --------
    See: `Datagy <https://datagy.io/python-count-occurrences-in-list/#Use_Pandas_to_Count_Number_of_Occurrences_in_a_Python_List>`_
    for example of counting occurances with pandas, which goes nicely with
    matplotlib
    """
    scores = []
    for i in range(0, iter):
        prot = Protein(prot_str)
        algorithm(prot)
        scores.append(prot.score)

    score_freq = pd.Series(scores).value_counts()
    ax = score_freq.plot.barh(x="frequency", y="scores")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Score")
    ax.set_title(
        f"Distribution of scores for '{prot.types}' "\
        f"at {iter} iterations"
    )
    plot.show()


if __name__ == "__main__":
    prot1 = Protein("HHPHPPPPH", [1, 2, -1, -1, 2, 2, 1, -2, 0])
    print(prot1.score)
    visualize_protein(prot1)
    visualize_scores("HHPHHHPH", fold_randomly)
