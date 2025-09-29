def main():
    # Get user input
    expression = input("Enter an expression (e.g., 3 8 23 24): ")
    numbers = expression.strip().split()
    
    tmp_value = 0
    for i in range(len(numbers)):
        try:
            tmp_value = float(numbers[i])
            if i == 0:
                min_value = tmp_value
                max_value = tmp_value
            else:
                if tmp_value < min_value:
                    min_value = tmp_value
                if tmp_value > max_value:
                    max_value = tmp_value
        except ValueError:
            print(f"Invalid number: {numbers[i]}")
            return
        
        print(f"Current number: {tmp_value}, Min: {min_value}, Max: {max_value}")

    print(f"Min: {min_value}, Max: {max_value}")

if __name__ == "__main__":
    main()
