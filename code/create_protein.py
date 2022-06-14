from classes.protein import Protein


def create_protein():
    string = input("protein: ") 
    return Protein(string)