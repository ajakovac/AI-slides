import json
import re
from collections.abc import Iterable
import argparse

def make_iterable(obj):
    if isinstance(obj, (str, bytes)):  # Strings and bytes are iterable, but we treat them as single items
        return [obj]
    if isinstance(obj, Iterable):
        return obj
    return [obj]

def extract_keyword(line) -> tuple[str | None, str, int, bool]:
    """returns (keyword, rest_of_line, starting_spaces, is_numbered)"""
    converted = line.expandtabs(4).rstrip()
    stripped_line = converted.strip()
    starting_spaces = len(converted) - len(stripped_line)
    if stripped_line.startswith('- **'):
        positions = [m.start() for m in re.finditer(r"\*\*", stripped_line)]
        return stripped_line[positions[0]+2:positions[1]], stripped_line[positions[1]+2:], starting_spaces, False
    elif stripped_line.startswith('1. **'):
        positions = [m.start() for m in re.finditer(r"\*\*", stripped_line)]
        return stripped_line[positions[0]+2:positions[1]], stripped_line[positions[1]+2:], starting_spaces, True
    elif stripped_line.startswith('- '):
        return "notes", stripped_line[2:], starting_spaces, False
    elif stripped_line.startswith('> '):
        return "$remark", stripped_line[2:], starting_spaces, False
    else:
        return None, stripped_line, starting_spaces, False

def make_segments(line:str):
    positions = [m.start() for m in re.finditer(r"__", line)]
    if len(positions) % 2 != 0:
        raise ValueError("Unmatched __ found.")
    if positions:
        pos = 0
        segments = []
        for i in range(0, len(positions), 2):
            segments.append(line[pos:positions[i]])
            segments.append(line[positions[i]+2:positions[i+1]])
            pos = positions[i+1] + 2
        segments.append(line[pos:])
        return segments
    else:
        return [line]

class Processor:
    def __init__(self, input_files: None | str | Iterable[str] = None):
        self.linknumber = 0
        self.database = {}
        self.input_lines = []
        if input_files is not None:
            for filename in make_iterable(input_files):
                self.add_file(filename)
        self.numbering = [0,0,0]

    def add_file(self, filename:str):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() == '__END__':
                    return
                self.input_lines.append(line)

    def resolve_link(self, line:str, entry_title:str):
        segments = make_segments(line)
        for i in range(1, len(segments), 2):  # Process only the segments between __
            s = segments[i].lower().replace(" ", "-")
            found = []
            for k in self.database:
                if s in k:
                    found.append(k)
            if len(found) >1:
                for k in found:
                    if k == s:
                        found = [k]
                if len(found) == 0:
                    raise ValueError(f"Multiple matches found for keyword: '{s}' in line: '{line}'")
            if len(found) == 0:
                raise ValueError(f"No match found for keyword: '{s}' in line: '{line}'")
            segments[i] = f'__{segments[i]}, link-{self.linknumber}, {found[0]}__'
            self.database[found[0]]['$links'].append([f"link-{self.linknumber}", s, entry_title])
            self.linknumber += 1
        return "".join(segments)

    def process(self, save_filename:str|None = None):
        keyword = None
        depth_descriptor = [-1]
        content = ""
        for line in self.input_lines:
            if not line.strip():
                continue
            keyword_name, rest, depth, is_numbered = extract_keyword(line)
            rest = rest.strip()
            if rest.startswith(':'):
                rest = rest[1:].strip()
            if keyword_name is None:
                content += line
                continue
            keyword = keyword_name.lower().replace(" ", "-")
            if depth_descriptor[0] > -1 and content.strip():
                key, property = (depth_descriptor + [None,None])[1:3]
                self.database[key][property][-1] += " " +content.strip()
                content = ""
            if depth == 0:
                depth_descriptor = [0, keyword]
                self.numbering = [0,0,0]
            if depth > depth_descriptor[0]:
                depth_descriptor[0] = depth
                depth_descriptor.append(keyword)
            if depth == depth_descriptor[0]:
                depth_descriptor[-1] = keyword
                if is_numbered:
                    self.numbering[len(depth_descriptor)-2] += 1
                    self.numbering = (self.numbering + [0,0,0])[:3]
            if depth < depth_descriptor[0]:
                depth_descriptor[0] = depth
                depth_descriptor.pop()
                depth_descriptor[-1] = keyword
                if is_numbered:
                    self.numbering[len(depth_descriptor)-2] += 1
                    self.numbering = (self.numbering[:len(depth_descriptor)-1] + [0,0,0])[:3]
            depth_level = len(depth_descriptor) - 2
            if is_numbered:
                my_numbers = list(filter(lambda x: x > 0, self.numbering[:depth_level+1]))
                keyword_name = f"{'.'.join(str(num) for num in my_numbers)}. {keyword_name}"
            if depth_level == 0:
                self.database[keyword] = {
                    '$links': [],
                    '$keyword_name': keyword_name
                    }
            elif depth_level == 1:
                if keyword not in self.database[depth_descriptor[1]]:
                    self.database[depth_descriptor[1]][keyword] = [keyword_name]
                if rest:
                    self.database[depth_descriptor[1]][keyword].append(rest)
            elif depth_level == 2:
                self.database[depth_descriptor[1]][depth_descriptor[2]].append(rest)
            else:
                raise ValueError(f"Unexpected depth level at line: {line}")
        if content.strip():
            key, property = (depth_descriptor + [None,None])[1:3]
            self.database[key][property][-1] += " " +content.strip()
        for k in self.database:
            if k in ['linknumber']:
                continue
            for property in self.database[k]:
                if property in ['$links', '$keyword_name']:
                    continue
                for line_index, line in enumerate(self.database[k][property]):
                    resolved_line = self.resolve_link(line, k)
                    self.database[k][property][line_index] = resolved_line

        if save_filename is not None:
            with open(save_filename, 'w') as f: 
                json.dump(self.database, f, indent=4)

    def show_json(self):
        return json.dumps(self.database, indent=4)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown notes into a database")
    parser.add_argument("--input", type=str, default="../Markdowns/modern-learning.md")
    parser.add_argument("--output", type=str, default="data.json")

    args = parser.parse_args()

    processor = Processor(input_files=args.input)
    processor.process(save_filename=args.output)
