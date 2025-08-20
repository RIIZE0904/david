def main():
    print("Welcome to the Calculator!")
    print("You can perform basic arithmetic operations or evaluate expressions.")
    print("Choose an option:")
    print("1) Input a number and perform operations")
    print("2) Input an expression (e.g., 1 + 2 * 3)")
    

    
    expr = input("Enter expression: ")
    parts = expr.strip().split()
    # 입력이 "숫자 연산자 숫자" 형태인지 확인
    if len(parts) >= 3:
        # 곱셈/나눗셈 먼저 처리
        parts = process(parts, ["*", "/"])
        # 덧셈/뺄셈 처리
        parts = process(parts, ["+", "-"])
        if parts and len(parts) == 1:
            print(f"Result: {parts[0]}")
        else:
            print("Error: Invalid or incomplete expression.")
    else:
        print("Error: Please enter expression in the form 'number operator number' (e.g., 1 + 2).")


def process(parts,operators):
    if not parts:
        print("No expression to evaluate.")
        return
    for i, part in enumerate(parts):
        if len(parts) >=  3:
            if part in operators:
                try:
                    num1 = float(parts[i - 1])
                    num2 = float(parts[i + 1])
                except ValueError:
                    print("Invalid number input.")
                    return
                operator = part
                # Remove the processed parts
                parts = parts[: i - 1] + parts[i + 2 :]
                # Perform the operation and replace the part in the list
                result = operation(num1, num2, operator)
                if result is not None:
                    parts.insert(i - 1, str(result))
                    return process(parts, operators)
                else:
                    print("Error in operation.")
                    return
                
    

    return parts


def operation(num1, num2, operator):
    try:
        if operator == "+":
            result = add(num1, num2)
        elif operator == "-":
            result = subtract(num1, num2)
        elif operator == "*":
            result = multiply(num1, num2)
        elif operator == "/":
            result = divide(num1, num2)

    
        print(f"Result: <{result}>")
        return result
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None
    return None

1
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
