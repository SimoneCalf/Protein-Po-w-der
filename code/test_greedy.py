from algorithms.greedy import greedy
from classes.protein import Protein
from visualization import visualize_protein


if __name__ == "__main__":
    test_prot = Protein("HHHHHHHPPP", [1, 2])
    print(test_prot)
    visualize_protein(test_prot)
    greedy(test_prot, prev=test_prot.aminos[1])
    print(test_prot)
    visualize_protein(test_prot)
