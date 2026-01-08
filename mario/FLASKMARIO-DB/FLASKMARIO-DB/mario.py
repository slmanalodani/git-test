while True:
    try:
        height = int(input("Enter a height (1-8): "))
        if 1 <= height <= 8:
            break
        else:
            print("Height must be a number between 1 and 8.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

for i in range(1, height + 1):
    spaces = height - i
    hashes = i

    print(" " * spaces + "#" * hashes, end="")
    print("  " + "#" * hashes)