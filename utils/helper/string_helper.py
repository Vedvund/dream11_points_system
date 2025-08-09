import re


def camel_to_snake(camel_str):
    snake_str = re.sub('([A-Z])', r'_\1', camel_str).lower()
    return snake_str.lstrip('_')


def normalize_text(text):
    return camel_to_snake(re.sub(r'[^A-Za-z0-9_]', '_', text))


if __name__ == '__main__':
    # Example usage:
    # camel_case_string = "camelCaseExample"
    camel_case_string = "NSE:HUDCO-EQ"
    snake_case_string = normalize_text(camel_case_string.lower())
    print(snake_case_string)  # Output: camel_case_example
