# Module imports
import matplotlib.pyplot as plot
from matplotlib.path import Path
import matplotlib.patches as patches
from mimetypes import guess_type
import pandas as pd
import os
from typing import Any, Callable, Union

# Local imports
from classes.protein import Protein
from classes.amino import Amino


def visualize_protein(
            prot: Protein,
            save_fig: bool = False,
            save_fig_dir: Union[str, bytes] = "data/",
            save_fig_filename: Union[str, bytes] = ""
        ):
    """Visualizes a protein in matplotlib.

    Parameters
    ----------
    prot : Protein
        the protein instance to visualize
    save_fig: bool, optional
        whether to save the figure to a file
    save_fig_dir : Union[str, bytes], optional
        the path to save the figure to, if the save_fig flag is set,
        by default 'data/' in the current working directory
    save_fig_filename : Union[str, bytes]
        the filename to save the figure to, if the save_fig flag is set,
        by default it is set to a string of amino types of the given protein,
        followed by a sha1 hash of the given protein instance (using hash()),
        followed by the file extension '.png'

    See Also
    --------
    .. `Path tutorial
        <https://matplotlib.org/stable/tutorials/advanced/path_tutorial.html>`

    To Do
    -----
    - Center figure `example <https://stackoverflow.com/a/4718438>`
`    """

    points = [(0.0, 0.0)]
    circles = []
    bonds, processed = [], []
    codes = [Path.MOVETO]
    min_x = max_x = min_y = max_y = 0

    for amino in prot.aminos:
        x, y = points[len(points)-1]

        # creëer cirkel
        color =\
            "orange" if amino.type == "H" else "#50C878" if amino.type == "C" \
            else "#0096FF"

        amino_circle = plot.Circle((x, y), .15, color=f"{color}")
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

    # voeg de labels toe
    for amino, circle in zip(prot.aminos, circles):
        x, y = circle.center
        ax.text(
            x,
            y,
            f"{amino.type}{amino.index}",
            ha="center",
            va="center",
            color="#FFF5EE",
            fontsize=8)

    # zet de x en y axis
    ax.set_xlim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)
    ax.set_ylim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)

    # voeg legende en titel toe
    # zie:
    #   https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
    legend = [
        patches.Patch(color="orange", label="Hydrofoob"),
        patches.Patch(color="#0096FF", label="Polair"),
        patches.Patch(color="none", label=f"Stabiliteit: {prot.score}")
    ]
    if "C" in prot.types:
        score = legend.pop()
        legend.append(patches.Patch(color="#50C878", label="Cysteine"))
        legend.append(score)

    ax.legend(handles=legend)
    fig.suptitle(prot.types)

    # sla op in output als de vlag is meegegeven
    if save_fig:
        cwd = os.getcwd()

        # create path if needed
        # see https://stackoverflow.com/a/44319629/8571352
        path =\
            str(save_fig_dir, "utf-8") if type(save_fig_dir) == bytes \
            else save_fig_dir if save_fig_dir else "data/"

        if not os.path.exists(f"{cwd}/{save_fig_dir}"):
            os.makedirs(f"{cwd}/{save_fig_dir}")

        # process filename
        filename =\
            "{file}.png".format(
                file=str(save_fig_filename, "utf-8").replace(".png", "")
            )\
            if type(save_fig_filename) == bytes \
            else "{file}.png".format(file=save_fig_filename.replace(".png", "")) \
            if save_fig_filename \
            else f"{prot.types}_{Protein.to_sha1(prot)}.png"

        # save file if a file with that hash doesn't already exist
        if not os.path.exists(f"{path}/{filename}"):
            plot.savefig(f"{cwd}/{path}/{filename}")

    # laat het figuur zien
    plot.show()


def visualize_scores(
        prot_str: str,
        algorithm: Callable[[Union[str, Protein]], Any], iterations=100
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
    for i in range(0, iterations):
        prot = Protein(prot_str)
        algorithm(prot)
        scores.append(prot.score)

    score_freq = pd.Series(scores).value_counts()
    ax = score_freq.plot.bar(x="frequency", y="scores")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Score")
    ax.set_title(
        f"Distribution of scores for '{prot.types}' "
        f"at {iterations} iterations"
    )
    plot.show()


if __name__ == "__main__":
    prot1 = Protein("CHPHPPPPH", [1, 2, -1, -1, 2, 2, 1, -2, 0])
    visualize_protein(prot1)
