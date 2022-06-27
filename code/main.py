from typing import Union
from input_output import output
from algorithms.random_protein import fold_randomly
from algorithms.depth_first import DepthFirstFold
from classes.protein import Protein
from visualization import visualize_protein
from algorithms.hillclimber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing


def create_protein(string: str = None) -> Union[Protein, None]:
    """Creates a protein based on user input

    Returns
    -------
    Union[Protein, None]:
        The created protein if user protein was given, None otherwise
    """
    # ask user for the aminos and directions
    if string:
        return Protein(string)

    string = input("protein: ")

    if not string:
        return None

    print("Please also provide some optional directions, seperated by commas.")
    while True:
        # Ask user for directions
        directions = input("directions: ")

        # if no directions were given fold amino into a straight line
        if not directions:
            return Protein(string)

        # otherwise, try to parse them into ints and return the protein
        dir_list = directions.split(",")
        try:
            dir_list = list(map(lambda dir: int(dir), dir_list))

            # pad list with last directions if necessary
            if len(dir_list) < len(string):
                dir_list += [dir_list[-1]] * (len(string) - len(dir_list))

            # return string
            return Protein(string, dir_list)
        except ValueError:
            # Couldn't map dir_list to ints, show message and
            print(
                "Input contained invalid directions, " +
                "must be a list of valid integers, seperated by commas"
            )
            continue


def main():
    # protein = None
    # if protein:
    #     print("Random: ")
    #     fold_randomly(protein, prev=protein.aminos[0])
    #     output(protein)
    #     visualize_protein(protein)

    # # do depth first fold
    # dff = DepthFirstFold("HHPHHHPHPHHHPH")
    # print("Starting Depth First Fold...")
    # solution = dff.run()
    # print(solution)
    # output(solution)
    # visualize_protein(
    #    solution,
    #     save_fig=True,
    #     save_fig_filename=f"{dff.__class__.__name__}.png"
    # )

    # hcb = HillClimber("HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH")
    # print("Starting Hill Climber")
    # solution = hcb.run(repeat=20, iterations=250, verbose=True)
    # print(solution)
    # output(solution)
    # visualize_protein(
    #     solution,
    #     save_fig=True,
    #     save_fig_filename=f"{hcb.__class__.__name__}{solution.types}"
    # )

    Sima = SimulatedAnnealing("HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH")
    print("Starting simulated annealing")
    solution = Sima.run(iterations=250, verbose=True)
    print(solution)
    output(solution)
    visualize_protein(
        solution,
        save_fig=True,
        save_fig_filename=f"{dff.__class__.__name__}.png"
    )

    hcb = HillClimber("HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH")
    print("Starting Hill Climber")
    solution = hcb.run(repeat=20, iterations=250, verbose=True)
    print(solution)
    output(solution)
    visualize_protein(
        solution,
        save_fig=True,
        save_fig_filename=f"{hcb.__class__.__name__}_{solution.types}"
        save_fig_filename=f"{Sima.__class__.__name__}{solution.types}"
    )


if __name__ == "__main__":
    main()
