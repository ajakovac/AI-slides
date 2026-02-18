#!/usr/bin/env python3

import json
import os
import re
from collections.abc import Iterable
import argparse
from pathlib import Path

params = {
    "IMG_RE": re.compile(r'!\[([^\]]*)\]\(([^)]+)\)'),
    "LINK_RE": re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),
    "LINK_SEPARATOR": "\x1e",
    "ITEM_SEPARATOR": "\x1f"
}

def link_format(type, name, value):
    link_separator = params["LINK_SEPARATOR"]
    item_separator = params["ITEM_SEPARATOR"]
    return f'{link_separator}{type}{item_separator}{name}{item_separator}{value}{link_separator}'

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
        return ">remark", stripped_line[2:], starting_spaces, False
    else:
        return None, stripped_line, starting_spaces, False

def resolve_link(database:dict, line:str, keyword:str, property:str):
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
            database['$system']['unresolved_links'].append(skey)
        else:
            if len(found) > 1:
                print(f"\tWARNING -> Multiple matches found for keyword: '{skey}' in line: '{line}'")
                print(f"\t           {found}")
            segments[i] = link_format("keyword", segments[i], found[0])
            database[found[0]]['$links'].append([database[keyword]['$keyword_name'], keyword, property])
    return "".join(segments)

def resolve_markdown_links(database:dict, line:str, keyword:str) -> str:
    def repl_image(match: re.Match) -> str:
        alt = match.group(1)
        url = Path(match.group(2)).name
        database[keyword]['$images'].append([alt, url])

        # ✨ return the link
        return link_format("image", alt, url)

    def repl_external_link(match: re.Match) -> str:
        alt = match.group(1)
        url =match.group(2)

        # ✨ return the link
        return link_format("external-link", alt, url)

    return params["LINK_RE"].sub(repl_external_link, params["IMG_RE"].sub(repl_image, line))


def add_source(
        input_files,
        default_source_dir:str = "../Markdowns/",
        database_name:str = "data/database.json",
        if_delete=False,
        startnew=False
        ):

    try:
        with open(database_name, 'r') as f:
            database = json.load(f)
    except FileNotFoundError:
        print(f"Database file '{database_name}' not found. Starting with an empty database.")
        startnew = True
    
    if startnew:
        database = {
            "$system": {
                "link_separator": "\x1e",
                "item_separator": "\x1f",
                "unresolved_links": []
            }
        }

    for filename in input_files:
        print(f"Processing file: {filename}")
        input_lines = []
        with open(os.path.abspath(os.path.join(default_source_dir, filename)), 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                if line == '__END__':
                    break
                input_lines.append(line)

        params["LINK_SEPARATOR"] = database['$system']['link_separator']
        params["ITEM_SEPARATOR"] = database['$system']['item_separator']

        

        keyword = None
        depth_descriptor = [-1]
        content = ""

        if if_delete:
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
            with open(database_name, 'w') as f:
                json.dump(database, f, indent=4)

        else:
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
                    try:
                        database[key][property][-1] += " " +content.strip()
                    except Exception as e:
                        print(f"Error updating database entry: keyword = {keyword}, key={key}, property={property}, error={e}")
                        raise e
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
                        '$images': [],
                        '$keyword_name': keyword_name,
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

    print("Resolving links...")
    database['$system']['unresolved_links'] = []
    for k in database:
        if k == '$system':
            continue
        for property in database[k]:
            if property.startswith('$'):
                continue
            for line_index, line in enumerate(database[k][property]):
                line = resolve_link(database, line, k, property)
                line = resolve_markdown_links(database, line, k)
                try:
                    database[k][property][line_index] = line
                except Exception as e:
                    print(f"Error resolving link in {k}.{property}: {e}")

    if len(database['$system']['unresolved_links']) > 0:
        print(f"WARNING: unresolved links:")
        for link in database['$system']['unresolved_links']:
            print(f"  - {link}")
        print(f"Total unresolved links: {len(database['$system']['unresolved_links'])}")

    with open(database_name, 'w') as f:
        json.dump(database, f, indent=4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process markdown notes into a database")
    parser.add_argument("--database", type=str, default="data/database.json")
    parser.add_argument("--delete", action='store_true', help="Delete entries of the file instead of adding/updating them")
    parser.add_argument("--startnew", action='store_true', help="Starts with an empty database, even if the database file already exists")
    parser.add_argument("-f", "--files", type=str, help="Input markdown files to process")
    parser.add_argument("rest", nargs=argparse.REMAINDER, help="All remaining command line arguments")

    args = parser.parse_args()

    if args.files:
        with open(args.files, 'r') as f:
            input_files = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        input_files = []
    input_files += args.rest

    add_source(input_files=input_files, database_name=args.database, if_delete=args.delete, startnew=args.startnew)

