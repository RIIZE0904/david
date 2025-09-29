def main():
    print("Welcome to the Calculator!")
    print("You can perform basic arithmetic operations or evaluate expressions.")
    print("Choose an option:")
    print("1) Input a number and perform operations")
    print("2) Input an expression (e.g., 1 + 2)")
    option = input("Enter option (1 or 2): ")


    if option == "1":
        num1 = input("Enter a number: ")
        num2 = input("Enter another number: ")
        operator = input("Enter an operator (+, -, *, /): ")
    elif option == "2":
        expr = input("Enter expression: ")
        parts = expr.strip().split()
        if len(parts) != 3:
            print("Invalid expression format.")
            return
        num1, operator, num2 = parts
    
    else:
        print("Invalid option.")
        return
    
    # Check if num1 and num2 are valid integers
    try:
        num1 = int(float(num1))
        num2 = int(float(num2))
        
    except ValueError:
        print("Invalid number input.")
        return
    # Check if operator is valid
    if operator not in ('+', '-', '*', '/'):
        print("Invalid operator.")
        return

    # Perform the operation
    operation(num1, num2, operator)

    return

def operation(num1, num2, operator):   

    try:
        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)

        result = int(result)
        print(f"Result: <{result}>")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    return

def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Error: Division by zero.")
    return num1 / num2

def multiply(num1, num2):
    return num1 * num2

def subtract(num1, num2):
    return num1 - num2

def add(num1, num2):
    return num1 + num2

if __name__ == "__main__":
    main()

