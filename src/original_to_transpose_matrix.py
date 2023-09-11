import numpy as np

def main():
    print("Matrix Transposition Program")

    while True:
        print("\nMenu:")
        print("1. Transpose a matrix")
        print("2. Exit")
        
        choice = input("Enter your choice (1/2): ")
        
        if choice == '1':
            transpose_matrix()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def get_matrix_input():
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    
    matrix = []
    print(f"Enter the {rows}x{cols} matrix:")
    
    for _ in range(rows):
        row = [float(x) for x in input().split()]
        matrix.append(row)
    
    return np.array(matrix)

def transpose_matrix():
    matrix = get_matrix_input()
    transposed_matrix = np.transpose(matrix)
    
    print("\nOriginal matrix:")
    print(matrix)
    print("\nTransposed matrix:")
    print(transposed_matrix)


main()