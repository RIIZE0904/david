def power(base, exponent):
    result = 1
    positive_exp = abs(exponent)  # 지수 절댓값 처리

    for _ in range(positive_exp):
        result *= base

    if exponent < 0:
        return 1 / result  # 음수 지수 처리: 역수 반환
    else:
        return result

def main():
    try:
        number = float(input("Enter number: "))
    except ValueError:
        print("Invalid number input.")
        return

    try:
        exponent = int(input("Enter exponent: "))
    except ValueError:
        print("Invalid exponent input.")
        return

    result = power(number, exponent)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()

