from input_output import output
from algorithms.random_protein import fold_randomly
from algorithms.depth_first import DepthFirstFold
from classes.protein import Protein
from visualization import visualize_protein
from algorithms.hillclimber import HillClimber


def create_protein(string: str = None) -> Protein:
    """Creates a protein based on user input

    Returns
    -------
    Protein
        The created protein
    """
    # ask user for the aminos and directions
    if string:
        return Protein(string)

    string = input("protein: ")

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
    # protein = create_protein()
    # print("Random: ")
    # fold_randomly(protein, prev=protein.aminos[0])
    # output(protein)
    # visualize_protein(protein)

    # do depth first fold
    dff = DepthFirstFold("HHPHHHPHPHH")
    solution = dff.run()
    print(solution)
    output(solution)
    visualize_protein(solution, True)
    
    hcb = hillclimber("HHPHHHPHPHH")
    solution = hcb.run()
    print(solution)
    output(solution)
    visualize_protein(solution, True)


    hcb = HillClimber("HHPHHHPHPHH")
    solution = hcb.run()
    print(solution)
    output(solution)
    visualize_protein(solution, True)


if __name__ == "__main__":
    main()
