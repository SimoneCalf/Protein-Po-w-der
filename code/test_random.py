from visualization import visualize_protein
from classes.protein import Protein
from algorithms.random_protein import fold_randomly

if __name__ == "__main__":
    test_prot = Protein("HPHHHHHPPPPPP", (2, 2, 1, 1, -2, -2, -1, 2))
    print(test_prot)
    visualize_protein(test_prot)
    fold_randomly(test_prot, prev=test_prot.aminos[7])
    print(test_prot)
    visualize_protein(test_prot)
