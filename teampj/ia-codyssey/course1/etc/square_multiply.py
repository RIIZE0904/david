import math

def input_numbers():
    # 정수
    try:
        number_input = input("Enter number: ")
        number = float(number_input)
    except ValueError:
        print("Invalid number input.")
        exit(1)

    # 지수
    try:
        exponent_input = input("Enter exponent: ")
        exponent = int(exponent_input)
    except ValueError:
        print("Invalid exponent input.")
        return 0,

    if number == 0 and exponent < 0:
        print("Invalid input: 0 cannot be raised to a negative power.")
        return

    return number, exponent

# 지수 함수 (pow)
def square(number, exponent):
    result = 1
    is_negative = exponent < 0
    exponent = abs(exponent)

    for _ in range(exponent):
        result *= number

    return 1 / result if is_negative else result

def main():
    number, exponent = input_numbers()
    result = square(number, exponent)

    if math.isinf(result):  # 너무 숫자가 클 때 예외 처리
        print("Result is too large to display.")
    elif result >= 1 or result == 0:  # 정수 출력
        print(int(result))
    else:
        print(result)

print()

if __name__ == "__main__":
    main()