import re


def read_file(file_name):
    with open(file_name, "r") as f:
        data = f.read()
        return data

def add_basic_tags(data):
    return f"<html>\n<body>\n{data}\n</body>\n</html>\n"

def replace_heading(matchobj):
    data = matchobj.group()
    hashtags = len(data) - len(data.lstrip('#'))
    return f'<h{hashtags}>{data}</h{hashtags}>'

def solve_heading(data):
    pattern = r"#{1,6}\s.*\n" 
    data = re.sub(pattern, replace_heading, data)
    return data   

def replace_linebreak(matchobj):
    return f"\n<br>\n"

def solve_linebreak(data):
    pattern = r"[\s]{2,}\n"
    data = re.sub(pattern, replace_linebreak, data)
    return data

def replace_bold(matchobj):
    return f"<strong>{matchobj.group()[2:-2]}</strong>"


def solve_bold(data):
    pattern_bold_1 = r"\*\*[\S].*[\S]\*\*"
    pattern_bold_2 = r"\_\_[\S].*[\S]\_\_"
    pattern_bold_3 = r"\*\*[\S]\*\*"
    pattern_bold_4 = r"\_\_[\S]\_\_"
    data = re.sub(pattern_bold_1, replace_bold, data)
    data = re.sub(pattern_bold_2, replace_bold, data)
    data = re.sub(pattern_bold_3, replace_bold, data)
    data = re.sub(pattern_bold_4, replace_bold, data)
    return data

def replace_italics(matchobj):
    return f"<em>{matchobj.group()[1:-1]}</em>"

def solve_italics(data):
    pattern_italic_1 = r"\*[\S].*[\S]\*"
    pattern_italic_2 = r"\_[\S].*[\S]\_"
    pattern_italic_3 = r"\*[\S]\*"
    pattern_italic_4 = r"\_[\S]\_"
    data = re.sub(pattern_italic_1, replace_italics, data)
    data = re.sub(pattern_italic_2, replace_italics, data)
    data = re.sub(pattern_italic_3, replace_italics, data)
    data = re.sub(pattern_italic_4, replace_italics, data)
    return data

def write_file(data, file_name):
    with open(file_name, "w") as f:
        f.write(data)


if __name__ == "__main__":
    markdown_path = "input.md"
    output_path = "output.html"

    data = read_file(markdown_path)

    data = add_basic_tags(data)

    data = solve_heading(data)
    data = solve_linebreak(data)
    data = solve_bold(data)
    data = solve_italics(data)

    write_file(data, output_path)
