def main():
    try:
        user_input = input("Enter numbers separated by space: ")
        tokens = user_input.strip().split()

        numbers = [float(token) for token in tokens]

        minimum = numbers[0]
        maximum = numbers[0]

        for num in numbers[1:]:
            if num < minimum:
                minimum = num
            if num > maximum:
                maximum = num

                print(f"Min: {minumum}")