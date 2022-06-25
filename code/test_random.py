from visualization import visualize_protein
from classes.protein import Protein
from algorithms.random_protein import fold_randomly

if __name__ == "__main__":
    test_prot = Protein(
        "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH",
    )
    fold_randomly(test_prot, prev=test_prot.aminos[7])
    print(test_prot)
    visualize_protein(test_prot)
