def main():
    try:
        base = float(input("Enter number: "))
    except ValueError:
        print("Invalid number input.")
        return

    try:
        exponent = int(input("Enter exponent (can be any integer): "))
    except ValueError:
        print("Invalid exponent input. Please enter an integer.")
        return

    result = 1.0
    for _ in range(abs(exponent)):
        if exponent < 0:
            result /= base
        else:
            result *= base

    print(f"{base} raised to the power of {exponent} is {result}")

    return result

if __name__ == "__main__":
    main()
    