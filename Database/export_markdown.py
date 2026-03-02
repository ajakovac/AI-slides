import json
import re
import argparse
import os

def make_markdown_link_0(line):
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

def make_markdown_link(line):
    def repl_link(match: re.Match) -> str:
        type = match.group(1)
        name = match.group(2)
        value = match.group(3)
        if type == "keyword":
            return f'[{name}](#{value})'
        elif type == "image":
            return f'[image: {name}](#image:{value})'
        elif type == "external-link":
            return f'[{name}]({value})'
        else:
            raise ValueError(f"Unknown link type: {type}")

    return LINK_RE.sub(repl_link, line)

def create_markdown(database):
    final = []
    final.append("""
<style>
    .image-link {
        display: inline-block;
        text-align: center;
        margin: 10px;
        scroll-margin-top: 20px;
    }
    .image-link img {
        max-width: 100%;
        height: auto;
    }
    .image-link span {
        display: block;
        margin-top: 5px;
        font-size: 0.9em;
        color: #555;
    }
</style>
                 """)
    for k in database:
        if k.startswith('$'):
            continue
        final.append(f'<a id="{k}"></a>')
        final.append(f'## {database[k]["$keyword_name"]}')
        for property, property_list in database[k].items():
            if property == '>remark':
                final.append(f'> {",".join(database[k][">remark"][1:])}')
                continue
            if property.startswith('$'):
                continue
            final.append(f'- {property_list[0]}')
            for line in property_list[1:]:
                line =  make_markdown_link(line)
                final.append(f'\t- {line}')
        if database[k]['$links']:
            final.append('- referenced by:')
            for link in database[k]['$links']:
                final.append(f'\t- [{link[0]}](#{link[1]}) via "{link[2]}"')
        if database[k]['$images']:
            final.append('- images:')
            for image in database[k]['$images']:
                #final.append(f'\t- {image[0]}: <div id="image:{image[1]}">\n![{image[0]}](../Images/{image[1]})\n</div>')
                final.append(f'\t- {image[0]}: \n <div id="image:{image[1]}", class="image-link">\n')
                final.append(f'\n<img src="../Images/{image[1]}" alt="{image[0]}">\n</div>\n')

    return "\n".join(final)

parser = argparse.ArgumentParser(description="Process markdown notes into a database")
parser.add_argument("--database", type=str, default="data/database.json")
parser.add_argument("--output", type=str, default="content.md")

args = parser.parse_args()

with open(args.database, 'r') as f:
    database = json.load(f)

link_separator = database['$system']['link_separator']
item_separator = database['$system']['item_separator']
LINK_RE = re.compile(link_separator  + r'(.*?)' + item_separator + r'(.*?)' + item_separator + r'(.*?)' + link_separator)

with open(os.path.join(os.path.dirname(__file__), '../Rendered Content', args.output), 'w') as f:
    print(create_markdown(database), file=f)
print(f"Markdown file created at {args.output}")
