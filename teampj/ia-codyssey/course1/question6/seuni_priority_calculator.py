# this function is used to tokenize a mathematical expression
def tokenize(expr):
    tokens = []
    num = ""
    prev = ""
    for i, char in enumerate(expr):
        if char == " ":
            continue
        if char in "0123456789.":
            num += char
        else:
            if num:
                tokens.append(num)
                num = ""
            # 음수 처리: -가 처음이거나 직전에 연산자 또는 ( 가 있을 경우
            if char == "-" and (i == 0 or prev in "+-*/("):
                num = "-"
            else:
                tokens.append(char)
        prev = char
    if num:
        tokens.append(num)
    return tokens

# this function is used to convert infix expression to postfix expression
def to_postfix(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    # this variable is used to store the precedence of operators
    output = []
    # this variable is used to store the output of the postfix expression
    stack = []

    for token in tokens:
        if token.replace('.', '', 1).lstrip('-').isdigit():
            output.append(token)
        elif token in '+-*/':
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # '(' 제거

    while stack:
        output.append(stack.pop())

    return output


# this function is test for the fuction tokenize
def test_tokenize():
    assert tokenize("3 + 5") == ["3", "+", "5"]
    assert tokenize("10 - 2 * 3") == ["10", "-", "2", "*", "3"]
    assert tokenize("(1 + 2) * 3") == ["(", "1", "+", "2", ")", "*", "3"]
    assert tokenize("-4 + 5") == ["-4", "+", "5"]
    assert tokenize("6 / (2 - 1)") == ["6", "/", "(", "2", "-", "1", ")"]


def main():
    user_input = input("수식을 입력하세요 (예: 3 + 5 * (2 - 1)): ").strip()
    if not user_input:
        print("Invalid input.")
        return

    try:
        tokens = tokenize(user_input)
        print("토큰화된 결과:", tokens)
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    test_tokenize()



