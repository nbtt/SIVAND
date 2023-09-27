import javalang
from javalang.tokenizer import Separator, Operator
from pathlib import Path


def get_tokens(str_code):
    tokens = list(javalang.tokenizer.tokenize(str_code))
    tokens = [token.value for token in tokens]
    return tokens

def get_main_tokens(str_code):
    tokens = list(javalang.tokenizer.tokenize(str_code))
    tokens = [token.value for token in tokens if not (isinstance(token, Separator) or isinstance(token, Operator))]
    return tokens


if __name__ == '__main__':
    program = Path('sample_input.java').read_text()
    print("program:\n{}".format(program))
    print("tokens = {}".format(get_tokens(program)))
