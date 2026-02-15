import json
import re
from collections.abc import Iterable
import argparse

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

def resolve_link(database:dict, line:str, ref_to_line:str):
    link_separator = database['$system']['link_separator']
    item_separator = database['$system']['item_separator']
    segments = line.split("__")
    # parts count must be odd: text, special, text, special, text, ...
    if len(segments) % 2 == 0:
        raise ValueError("Unmatched __ found.")
    for i in range(1, len(segments), 2):  # Process only the segments between __
        skey = segments[i].lower().replace(" ", "-")
        found = []
        for k in database:
            if skey in k:
                found.append(k)
        if len(found) >1:
            for k in found:
                if k == skey:
                    found = [k]
            if len(found) == 0:
                raise ValueError(f"Multiple matches found for keyword: '{skey}' in line: '{line}'")
        if len(found) == 0:
            raise ValueError(f"No match found for keyword: '{skey}' in line: '{line}'")
        segments[i] = f'{link_separator}{segments[i]}{item_separator}{found[0]}{link_separator}'
        database[found[0]]['$links'].append([database[ref_to_line]['$keyword_name'], ref_to_line, skey])
    return "".join(segments)


default="../Markdowns/modern-learning.md"

parser = argparse.ArgumentParser(description="Process markdown notes into a database")
parser.add_argument("--database", type=str, default="data/database.json")
parser.add_argument("--delete", action='store_true', help="Delete entries of the file instead of adding/updating them")
parser.add_argument("rest", nargs=argparse.REMAINDER, help="All remaining command line arguments")

args = parser.parse_args()

try:
    with open(args.database, 'r') as f:
        database = json.load(f)
except FileNotFoundError:
    print(f"Database file '{args.database}' not found. Starting with an empty database.")
    database = {
        "$system": {
            "link_separator": "\x1e",
            "item_separator": "\x1f"
        }
    }

input_files = args.rest if args.rest else [default]
input_lines = []
for filename in input_files:
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == '__END__':
                break
            input_lines.append(line)

keyword = None
depth_descriptor = [-1]
content = ""

if args.delete:
    delete_entries = set()
    for line in input_lines:
        if not line.strip():
            continue
        keyword_name, _, _, _ = extract_keyword(line)
        if keyword_name is not None:
            keyword = keyword_name.lower().replace(" ", "-")
            delete_entries.add(keyword)
    for entry in delete_entries:
        if entry in database:
            del database[entry]
    with open(args.database, 'w') as f:
        json.dump(database, f, indent=4)
    exit(0)

for line in input_lines:
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
        database[key][property][-1] += " " +content.strip()
        content = ""
    if depth == 0:
        depth_descriptor = [0, keyword]
        numbering = [0,0]
    if depth > depth_descriptor[0]:
        depth_descriptor[0] = depth
        depth_descriptor.append(keyword)
    if depth == depth_descriptor[0]:
        depth_descriptor[-1] = keyword
        if is_numbered:
            numbering[len(depth_descriptor)-3] += 1
            numbering = (numbering + [0,0])[:2]
    if depth < depth_descriptor[0]:
        depth_descriptor[0] = depth
        depth_descriptor.pop()
        depth_descriptor[-1] = keyword
        if is_numbered:
            numbering[len(depth_descriptor)-3] += 1
            numbering = (numbering[:len(depth_descriptor)-2] + [0,0])[:2]
    depth_level = len(depth_descriptor) - 2
    if is_numbered:
        my_numbers = list(filter(lambda x: x > 0, numbering[:depth_level]))
        keyword_name = f"{'.'.join(str(num) for num in my_numbers)}. {keyword_name}"
    if depth_level == 0:
        database[keyword] = {
            '$links': [],
            '$keyword_name': keyword_name
            }
    elif depth_level == 1:
        if keyword not in database[depth_descriptor[1]]:
            database[depth_descriptor[1]][keyword] = [keyword_name]
        if rest:
            database[depth_descriptor[1]][keyword].append(rest)
    elif depth_level == 2:
        database[depth_descriptor[1]][depth_descriptor[2]].append(rest)
    else:
        raise ValueError(f"Unexpected depth level at line: {line}")

# add remaining content to the last keyword
if content.strip():
    key, property = (depth_descriptor + [None,None])[1:3]
    database[key][property][-1] += " " +content.strip()


for k in database:
    if k.startswith('$'):
        continue
    for property in database[k]:
        if property in ['$links', '$keyword_name']:
            continue
        for line_index, line in enumerate(database[k][property]):
            resolved_line = resolve_link(database, line, k)
            try:
                database[k][property][line_index] = resolved_line
            except Exception as e:
                print(f"Error resolving link in {k}.{property}: {e}")

with open(args.database, 'w') as f:
    json.dump(database, f, indent=4)
