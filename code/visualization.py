# Module imports
import matplotlib.pyplot as plot
from matplotlib.path import Path
import matplotlib.patches as patches

# Local imports
from classes.protein import Protein


def visualize_protein(prot: Protein):
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
    codes = [Path.MOVETO]
    min_x = max_x = min_y = max_y = 0

    for amino in prot.aminos:
        x, y = points[len(points)-1]

        # creëer cirkel
        amino_circle = plot.Circle(
            (x, y),
            .10,
            color="{}".format("red" if amino.letter == "H" else "blue")
        )
        circles.append(amino_circle)

        # voeg lijn naar volgende amino toe
        match amino.direction:
            case -2:
                y -= 1
                min_y = min(y, min_y)
            case -1:
                x -= 1
                min_x = min(x, min_x)
            case 1:
                x += 1
                max_x = max(x, max_x)
            case 2:
                y += 1
                max_y = max(y, max_y)
            case _:
                continue
        points.append((x, y))
        codes.append(Path.LINETO)

    # sluit het pad af
    points.append((0.0, 0.0))
    codes.append(Path.STOP)

    # voeg de lijntekening toe
    path = Path(points, codes)
    fig, ax = plot.subplots()
    patch = patches.PathPatch(path, facecolor="none", lw=2)
    ax.add_patch(patch)

    # voeg de cirkels toe
    for circle in circles:
        ax.add_patch(circle)

    # zet de x en y axis
    ax.set_xlim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)
    ax.set_ylim(min(min_x, min_y)-.5, max(max_x, max_y)+.5)

    # voeg legende toe
    # zie:
    #   https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
    legend = [
        patches.Patch(color="red", label="Hydrofoob"),
        patches.Patch(color="blue", label="Polair")
    ]

    ax.legend(handles=legend)

    # laat het figuur zien
    plot.show()


if __name__ == "__main__":
    prot = Protein("HHPHPPPPH", [1, 2, -1, -1, 2, 2, 1, -2, 0])
    visualize_protein(prot)
