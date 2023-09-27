import os
import random
import javalang as jl
import re

# parameters
data_dir = "/Users/lap13494/workspace/ppl-extra-final/java-small/test/hadoop"
output_dir = "/Users/lap13494/workspace/ppl-extra-final/java-small/test/hadoop-splitted"
csv_file_path = "/Users/lap13494/workspace/ppl-extra-final/SIVAND/data/selected_input/mn_c2s/c2s_js_test_randfile.txt"
percent_selected = 0.1

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def __get_start_end_for_node(tree, node_to_find):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def __get_string(data, start, end):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    # remove last line contains @Override or similar
    string_lines = string.splitlines(True)
    # travese from the end
    for i in range(len(string_lines) - 1, -1, -1):
        line = string_lines[i]
        # if line is empty, skip
        if not line.strip():
            continue
        # if line starts with @, remove it and stop
        if line.strip().startswith("@"):
            string_lines.pop(i)
            break
        # if line is not empty and not start with @, stop    
        break        

    string = "".join(string_lines)

    # remove comments
    string = comment_remover(string)

    return string

def extract_methods_from_java_file(file_path):
    data = open(file_path).read()
    tree = jl.parse.parse(data)
    methods = {}

    for _, node in tree.filter(jl.tree.MethodDeclaration):
        start, end = __get_start_end_for_node(tree, node)
        method_key = node.name

        if method_key not in methods:
            methods[method_key] = []

        methods[method_key].append(__get_string(data, start, end))

    return methods

def write_methods_to_files(output_dir, methods, original_file, csv_file_writer):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for method_name, method_strings in methods.items():
        for index, method_string in enumerate(method_strings):
            file_name = f"{original_file}_{method_name}_{index}.java"
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, 'w') as method_file:
                method_file.write(method_string)
            
            csv_file_writer.write(f"{file_path}\n")

if __name__ == "__main__":    
    java_files = [f for f in os.listdir(data_dir) if f.endswith(".java")]
    
    # Calculate the number of files to randomly select
    num_files_to_select = int(len(java_files) * percent_selected)
    
    # Randomly select files
    selected_files = random.sample(java_files, num_files_to_select)

    with open(csv_file_path, 'w') as csv_file_writer:
        csv_file_writer.write(f"path\n")
        for java_file in selected_files:
            file_path = os.path.join(data_dir, java_file)
            methods = extract_methods_from_java_file(file_path)
            original_file_name = os.path.splitext(java_file)[0]
            write_methods_to_files(output_dir, methods, original_file_name, csv_file_writer)
