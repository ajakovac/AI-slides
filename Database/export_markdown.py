import json
import re
import argparse

def make_markdown_link(line, link_separator="\x1e", item_separator="\x1f"):
    segments = line.split(link_separator)
    # parts count must be odd: text, special, text, special, text, ...
    if len(segments) % 2 == 0:
        raise ValueError("Unmatched link separator found.")
    for i in range(1, len(segments), 2):  # Process only the segments between __
        match = re.match(r'(.*)'+ item_separator + r'(.*)', segments[i])
        if match:
            s, resolved_keyword = match.groups()
            segments[i] = f'[{s}](#{resolved_keyword})'
        else:
            raise ValueError("Invalid link format.")
    return "".join(segments)

def create_markdown(database):
    link_separator = database['$system']['link_separator']
    item_separator = database['$system']['item_separator']
    final = []
    for k in database:
        if k.startswith('$'):
            continue
        final.append(f'<a id="{k}"></a>')
        final.append(f'## {database[k]["$keyword_name"]}')
        for property, property_list in database[k].items():
            if property in ['$links', '$keyword_name']:
                continue
            if property == '$remark':
                final.append(f'> {",".join(database[k]["$remark"][1:])}')
                continue
            final.append(f'- {property_list[0]}')
            for line in property_list[1:]:
                line =  make_markdown_link(line, link_separator, item_separator)
                final.append(f'\t- {line}')
        if database[k]['$links']:
            final.append('- referenced by:')
            for link in database[k]['$links']:
                final.append(f'\t- [{link[0]}](#{link[1]}) via "{link[2]}"')
    return "\n".join(final)

parser = argparse.ArgumentParser(description="Process markdown notes into a database")
parser.add_argument("--database", type=str, default="data/database.json")
parser.add_argument("--output", type=str, default="content.md")

args = parser.parse_args()

with open(args.database, 'r') as f:
    database = json.load(f)


with open(args.output, 'w') as f:
    print(create_markdown(database), file=f)
print(f"Markdown file created at {args.output}")
