import json
import re
from Codes.utils import make_segments
import argparse

def make_markdown_link(line):
    segments = make_segments(line)
    for i in range(1, len(segments), 2):  # Process only the segments between __
        match = re.match(r'(.*), link-(.*), (.*)', segments[i])
        if match:
            s, link_number, resolved_keyword = match.groups()
            segments[i] = f'<a id="link-{link_number}"></a>[{s}](#{resolved_keyword})'
        else:
            raise ValueError("Invalid link format.")
    return "".join(segments)

def create_markdown(database):
    final = []
    for k in database:
        if k in ['linknumber']:
            continue
        final.append(f'<a id="{k}"></a>')
        final.append(f'## {database[k]["$keyword_name"]}')
        for property, property_list in database[k].items():
            if property in ['$links', '$keyword_name']:
                continue
            if property == '>remark':
                final.append(f'> {",".join(database[k][">remark"][1:])}')
                continue
            final.append(f'- {property_list[0]}')
            for line in property_list[1:]:
                line = make_markdown_link(line)
                final.append(f'\t- {line}')
        if database[k]['$links']:
            final.append('- referenced by:')
            for link in database[k]['$links']:
                final.append(f'\t- [{link[1]}](#{link[0]}) in section "{link[2]}"')
    return "\n".join(final)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown notes into a database")
    parser.add_argument("--input", type=str, default="data.json")
    parser.add_argument("--output", type=str, default="data.md")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        database = json.load(f)


    with open(args.output, 'w') as f:
        print(create_markdown(database), file=f)
    print(f"Markdown file created at {args.output}")
