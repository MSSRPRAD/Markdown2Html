import sys
import re
from enum import Enum


def lines_from_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def strip(line):
    return line.lstrip()


# class syntax
class Type(Enum):
    HashTag = 1
    Number = 2
    Table = 3
    Char = 4
    List = 5
    Empty = 6
    OrderedList = 7
    Undefined = 9


def type(char):
    if char in "1234567890":
        return Type.Number
    elif char in "#":
        return Type.HashTag
    elif char in "-*":
        return Type.List
    elif char is None:
        return Type.Empty
    elif char in "|":
        return Type.Table
    else:
        return Type.Char
    
def handle_hashtag(line):
    no_of_hashtags = 0
    for i in range(len(line)):
        if line[i]=="#":
            no_of_hashtags += 1
        else:
            break
    if no_of_hashtags == 1:
        return f'<h1>{line[no_of_hashtags:-1].lstrip()}</h1>\n'  
    if no_of_hashtags == 2:
        return f'<h2>{line[no_of_hashtags:-1].lstrip()}</h2>\n'
    if no_of_hashtags == 3:
        return f'<h3>{line[no_of_hashtags:-1].lstrip()}</h3>\n'  
    if no_of_hashtags == 4:
        return f'<h4>{line[no_of_hashtags:-1].lstrip()}</h4>\n'
    else:
        return f'<p>{line[no_of_hashtags:-1].lstrip()}</p>\n'

def convert(lines):
    output = ""
    prev_line_type = Type.Undefined
    next_line_type = Type.Undefined
    length = len(lines)
    for i in range(length):
        line = lines[i]
        line = strip(line)
        if i+1<length:
            if len(lines[i+1]) == 0:
                next_line_type = Type.Empty
            else:
                next_line_type = type(lines[i+1][0])
        if(len(line) == 0):
            if prev_line_type == Type.Char:
                output += f'\n<br>\n'
            prev_line_type = Type.Empty
        else:
            match type(line[0]):
                case Type.HashTag:
                    output += (handle_hashtag(line))
                    prev_line_type = Type.HashTag
                case Type.Empty:
                    if prev_line_type == Type.Char:
                        output += f'\n<br>\n'
                    prev_line_type = Type.Empty
                case Type.Char:
                        output += line
                        prev_line_type = Type.Char
                case Type.List:
                    if prev_line_type != Type.List:
                        output += f'\n<ul>\n'
                    output += f'<li>{line[1:-1].lstrip()}</li>\n'    
                    if next_line_type != Type.List:
                        output += f'\n</ul>\n'
                    prev_line_type = Type.List
                
                case Type.Number:
                    if line[1] == '.' and line[2] == ' ':
                        if prev_line_type != Type.OrderedList:
                            output += f'\n<div>\n'
                        output += f'&emsp;\t{line[:-1].lstrip()}\n<br>\n'    
                        if next_line_type != Type.Number:
                            output += f'\n</div>\n'
                        prev_line_type = Type.OrderedList
                    else:
                        output += line
                        prev_line_type = Type.Char

                case Type.Table:

                    if prev_line_type != Type.Table:
                        output += '\n<table>\n'
                    
                    words = line.split('|')
                    # print(words[1].strip()[0])
                    if words[1].strip()[0] != ':':                            
                        output += '\n<tr>\n'
                        for i,word in enumerate(words):
                            if i == 0 or i == len(words) - 1:
                                continue
                            word = word.strip()
                            if prev_line_type == Type.Table:
                                output += f'<td>{word}</td>\n'
                            else:
                                output += f'<th>{word}</th>\n'
                        output += '</tr>\n'

                    if next_line_type != Type.Table:
                        output += '\n</table>\n'

                    prev_line_type = Type.Table


    return output

def lines_to_file(lines, file_path):
    with open(file_path, 'w') as f:
        f.write(lines)

if __name__ == '__main__':

    markdown_path = sys.argv[1]
    output_path = sys.argv[2]
    
    lines = lines_from_file(markdown_path)
    converted_lines = convert(lines)
    lines_to_file(converted_lines, output_path)