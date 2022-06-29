# system imports
from time import perf_counter as time
from typing import Callable, Union, Dict

# algorithm imports
from algorithms.random_protein import fold_randomly

# class imports
from classes.protein import Protein

# utils import
from input_output import output
from visualization import visualize_protein


def create_protein(protein_input_str: str = None) -> Union[Protein, None]:
    """Creates a protein based on user input

    Returns
    -------
    Union[Protein, None]:
        The created protein if user protein was given, None otherwise
    """
    # ask user for the aminos and directions
    if protein_input_str:
        return Protein(protein_input_str)

    protein_input_str = input("protein: ")

    if not protein_input_str:
        return None

    print("Please also provide some optional directions, seperated by commas.")
    while True:
        # Ask user for directions
        directions = input("directions: ")

        # if no directions were given fold amino into a straight line
        if not directions:
            return Protein(protein_input_str)

        # otherwise, try to parse them into ints and return the protein
        dir_list = directions.split(",")
        try:
            dir_list = list(map(lambda dir: int(dir), dir_list))

            # pad list with last directions if necessary
            if len(dir_list) < len(protein_input_str):
                dir_list += [dir_list[-1]] * (len(protein_input_str) -
                                              len(dir_list))

            # return string
            return Protein(protein_input_str, dir_list)
        except ValueError:
            # Couldn't map dir_list to ints, show message and
            print(
                "Input contained invalid directions, " +
                "must be a list of valid integers, seperated by commas"
            )
            continue


def time_func(func: Callable, msg: str = "", kargs: Dict[any] = {}):
    # !!
    if not isinstance(func, Callable):
        raise TypeError("function argument {func} wasn't callable")

    if not msg:
        msg = f"Starting {func.__qualname__}"

    print(f"{msg}")

    # start and time function
    start = time()
    result = func(**kargs)
    return (result,  time() - start)


def main():
    # !!
    protein = create_protein("HHPHHHPHPHHHPH")
    if protein:
        print("Random: ")
        fold_randomly(protein, prev=protein.aminos[0])
        output(protein)
        visualize_protein(protein)
        for amino in protein.aminos:
            for bond in amino.bonded:
                print(bond.target, amino.bonded.origin)

    # ## do depth first fold
    # # dff = DepthFirstFold("HHPHHHPHPHHHPH")
    # # print("Starting Depth First Fold...")
    # # solution = dff.run()
    # # print(solution)
    # # output(solution, subdir=dff.__class__.__name__)
    # # visualize_protein(
    # #    solution,
    # #    save_fig=True,
    # #    save_fig_dir=dff.__class__.__name__,
    # # )

    # #  hcb = HillClimber(
    # #      "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH"
    # #  )
    # #  solution, time = time_func(
    # #      hcb.run,
    # #      kargs={"runs": 20, "iterations": 250, "verbose": False}
    # #  )
    # #
    # #  print(f"time taken to run {hcb.__class__.__name__}: {time:.1f}")
    # #  print(solution)
    # #  output(solution, hcb.__class__.__name__)
    # #  visualize_protein(
    # #      solution,
    # #      save_fig=True,
    # #      save_fig_dir=hcb.__class__.__name__,
    # #      save_fig_filename=f"{hcb.__class__.__name__}_{solution.types}"
    # #  )

    # #  phc = ParallelHillClimber(
    # #      "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH"
    # #  )
    # #
    # #  # start
    # #  solution, time = time_func(
    # #      phc.run,
    # #      kargs={"runs": 20, "iterations": 250, "verbose": False}
    # #  )
    # #
    # #  print(f"time taken to run {phc.__class__.__name__}: {time:.1f}")
    # #  print(solution)
    # #
    # #  # output
    # #  output(solution, subdir=phc.__class__.__name__)
    # #  visualize_protein(
    # #      solution,
    # #      save_fig=True,
    # #      save_fig_dir=phc.__class__.__name__,
    # #      save_fig_filename=f"{phc.__class__.__name__}_{solution.types}"
    # #  )

    # sim = SimulatedAnnealing(
    #     "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH"
    # )
    # print("Starting simulated annealing")
    # solution = sim.run(iterations=1000, verbose=3)
    # print(solution)
    # output(solution)
    # visualize_protein(
    #     solution,
    #     save_fig=True,
    #     save_fig_filename=f"{sim.__class__.__name__}.png"
    # )


if __name__ == "__main__":
    main()
