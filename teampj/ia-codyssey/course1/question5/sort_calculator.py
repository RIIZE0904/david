def main():
    # Get user input
    expression = input("Enter an expression (e.g., 2 4 31 13 88 23): ")
    parts = expression.strip().split()

    # Convert input strings to floats
    numbers = []
    for part in parts:
        try:
            numbers.append(float(part))
        except ValueError:
            print(f"Invalid number: {part}")
            return

    # Sort numbers
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                # Swap to place the smallest number at the current position (selection sort)
                numbers[i], numbers[j] = numbers[j], numbers[i]

    # Display results
    print("Sorted:", " ".join(f"<{num}>" for num in numbers))

if __name__ == "__main__":
    main()
