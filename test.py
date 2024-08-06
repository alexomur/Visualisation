def split_once(expr: str) -> list:
    """
    Splits the expression at the first outermost '/' found.

    :param expr: The expression to split.
    :return: A list containing two parts of the expression split at the first outermost '/'.
    """
    depth = 0
    for i, char in enumerate(expr):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == '/' and depth == 0:
            return [expr[:i], expr[i + 1:]]

    if expr[0] == '(' and expr[-1] == ')' and expr.count('(') == expr.count(')'):
        return split_once(expr[1:-1])

    return [expr, '']


def split_division(div: str) -> list:
    """
    Recursively splits the division expression into nested lists.

    :param div: The division expression to split.
    :return: A nested list representing the split expression.
    """
    if not ('/' in div):
        return [div]
    sp = split_once(div)
    sp[0] = split_division(sp[0])
    sp[1] = split_division(sp[1])
    return sp


def join_expression(nested_list) -> str:
    """
    Joins a nested list into a string with multiplication for inner elements.

    :param nested_list: The nested list to join.
    :return: A string representing the joined expression.
    """
    if isinstance(nested_list, str):
        return nested_list
    elif isinstance(nested_list, list):
        if len(nested_list) == 1:
            return join_expression(nested_list[0])
        else:
            return '*'.join(join_expression(item) for item in nested_list)


def remove_unnecessary_parentheses(expr: str) -> str:
    """
    Removes unnecessary parentheses from the expression.

    :param expr: The expression to clean.
    :return: The cleaned expression.
    """

    def is_redundant(expression):
        if expression.startswith('(') and expression.endswith(')'):
            inner_expr = expression[1:-1]
            depth = 0
            for char in inner_expr:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth < 0:
                        return False
            return depth == 0
        return False

    while is_redundant(expr):
        expr = expr[1:-1]
    return expr


def normalize(div: str) -> str:
    """
    Will convert the string of the form (a/b)/(c/d) to the form (a*d)/(b*c)
    or (a/b)/c to the form a/(b*c) or a/(b/c) to the form (a*c)/b

    :param div: The expression to normalize
    :return: Normalized expression
    """
    div_list = split_division(div)

    # Check the structure of the div_list to determine how to normalize it
    if len(div_list) == 2:
        if isinstance(div_list[0], list) and len(div_list[0]) == 2 and isinstance(div_list[1], list) and len(
                div_list[1]) == 2:
            # Case (a/b)/(c/d)
            numerator = join_expression(div_list[0][0]) + '*' + join_expression(div_list[1][1])
            denominator = join_expression(div_list[0][1]) + '*' + join_expression(div_list[1][0])
        elif isinstance(div_list[0], list) and len(div_list[0]) == 2:
            # Case (a/b)/c
            numerator = join_expression(div_list[0][0])
            denominator = join_expression(div_list[0][1]) + '*' + join_expression(div_list[1])
        elif isinstance(div_list[1], list) and len(div_list[1]) == 2:
            # Case a/(b/c)
            numerator = join_expression(div_list[0]) + '*' + join_expression(div_list[1][1])
            denominator = join_expression(div_list[1][0])
        else:
            # Generic case a/b
            numerator = join_expression(div_list[0])
            denominator = join_expression(div_list[1])
    else:
        # This should handle simple cases where there's no division
        numerator = join_expression(div_list[0])
        denominator = '1'

    normalized_expression = f"({numerator})/({denominator})"
    return remove_unnecessary_parentheses(normalized_expression)


def remove_inner_unnecessary_parentheses(expr: str) -> str:
    """
    Removes unnecessary inner parentheses from the expression.

    :param expr: The expression to clean.
    :return: The cleaned expression.
    """
    result = []
    i = 0
    while i < len(expr):
        if expr[i] == '(':
            # Find the matching closing parenthesis
            depth = 1
            for j in range(i + 1, len(expr)):
                if expr[j] == '(':
                    depth += 1
                elif expr[j] == ')':
                    depth -= 1
                if depth == 0:
                    # Recursively clean the inner expression
                    inner_expr = remove_inner_unnecessary_parentheses(expr[i + 1:j])
                    if '*' in inner_expr or '/' in inner_expr:
                        result.append(f'({inner_expr})')
                    else:
                        result.append(inner_expr)
                    i = j
                    break
        else:
            result.append(expr[i])
        i += 1
    return ''.join(result)


# Apply the additional cleaning function after the initial normalization
def normalize_and_clean(div: str) -> str:
    normalized = normalize(div)
    return remove_inner_unnecessary_parentheses(normalized)


# Example usage
print(normalize_and_clean("(a/b)/(c/d)"))  # Expected result: (a*d)/(b*c)
print(normalize_and_clean("(a/b)/c"))  # Expected result: a/(b*c)
print(normalize_and_clean("a/(b/c)"))  # Expected result: (a*c)/b
print(normalize_and_clean("a/b"))  # Expected result: a/b


# TODO: Запихнуть всё это в сраный Scalar.py