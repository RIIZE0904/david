# priority_calculator.py
# 참고: 알고리즘 설계 아이디어는 Khan Academy 강의에서 차용함


import re

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero.")
    return a / b


class Calculator:
    def __init__(self, allow_parentheses=False):
        self.allow_parentheses = allow_parentheses
        self.operators = {
            '+': (1, add),
            '-': (1, subtract),
            '*': (2, multiply),
            '/': (2, divide)
        }

    def compute(self, tokens):
        nums = []
        ops = []

        def apply_operator():
            b = nums.pop()
            a = nums.pop()
            op = ops.pop()
            func = self.operators[op][1]
            nums.append(func(a, b))

        def precedence(op):
            return self.operators[op][0]

        try:
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token == '(' and self.allow_parentheses:
                    # 괄호 시작: 내부 계산
                    depth = 1
                    j = i + 1
                    sub_expr = []
                    while j < len(tokens) and depth > 0:
                        if tokens[j] == '(':
                            depth += 1
                        elif tokens[j] == ')':
                            depth -= 1
                        if depth > 0:
                            sub_expr.append(tokens[j])
                        j += 1
                    if depth != 0:
                        raise ValueError("Mismatched parentheses.")
                    value = self.compute(sub_expr)
                    nums.append(value)
                    i = j
                    continue

                elif token == ')':
                    if not self.allow_parentheses:
                        raise ValueError("Parentheses not allowed.")
                    else:
                        raise ValueError("Unexpected ')'.")
                elif token in self.operators:
                    while ops and precedence(ops[-1]) >= precedence(token):
                        apply_operator()
                    ops.append(token)
                else:
                    nums.append(float(token))
                i += 1

            while ops:
                apply_operator()

            if len(nums) != 1:
                raise ValueError("Invalid expression structure.")
            return nums[0]

        except ZeroDivisionError:
            return "Error: Division by zero."
        except (ValueError, IndexError):
            return "Invalid input."


def tokenize(expression):
    # 공백 제거
    expression = expression.replace(' ', '')

    # 음수와 소수, 연산자, 괄호를 모두 포함한 패턴
    pattern = r'(\d+\.\d+|\d+|[+\-*/()]|\.\d+|-\d+(?:\.\d+)?)'
    tokens = re.findall(pattern, expression)

    # 음수를 연산자와 구분: 첫 토큰이 "-"이면 음수로 처리
    processed_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and (i == 0 or tokens[i-1] in '()+-*/'):
            # 음수 시작
            if i + 1 < len(tokens):
                processed_tokens.append(str(float('-' + tokens[i + 1])))
                i += 2
                continue
        processed_tokens.append(token)
        i += 1

    return processed_tokens



def main():
    use_parens = input("괄호를 포함한 수식을 계산하시겠습니까? (y/n): ").strip().lower() == 'y'

    user_input = input("수식을 입력하세요 (예: 3 + 5 * (2 - 1)): ").strip()
    if not user_input:
        print("Invalid input.")
        return

    try:
        tokens = tokenize(user_input)
        calc = Calculator(allow_parentheses=use_parens)
        result = calc.compute(tokens)

        if isinstance(result, str):
            print(result)
        else:
            print(f"Result: {float(result)}")
    except Exception as e:
        print(f"Invalid input. ({e})")


if __name__ == "__main__":
    main()
