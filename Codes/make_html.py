import json
import re
from html import escape
from Codes.utils import make_segments
import argparse

def make_html_link(line):
    segments = make_segments(line)
    final = []
    for i, segment in enumerate(segments):
        if i % 2 == 0:
            final.append(escape(segment))
            continue

        match = re.match(r'(.*), link-(.*), (.*)', segment)
        if match:
            s, link_number, resolved_keyword = match.groups()
            final.append(
                f'<a id="link-{escape(link_number)}"></a>'
                f'<a class="inline-link" href="#{escape(resolved_keyword)}">{escape(s)}</a>'
            )
        else:
            raise ValueError("Invalid link format.")
    return "".join(final)

def create_html(database, title="Automatically Generated Notes"):
    sections = []
    for k in database:
        if k in ['linknumber']:
            continue

        entry = database[k]
        section = [
            '<section class="card">',
            f'<a id="{escape(k)}"></a>',
            f'<h2>{escape(entry["$keyword_name"])}</h2>'
        ]

        for property, property_list in entry.items():
            if property in ['$links', '$keyword_name']:
                continue

            if property == '>remark':
                remark = ", ".join(escape(text) for text in property_list[1:])
                section.append(f'<blockquote>{remark}</blockquote>')
                continue

            if not property_list:
                continue

            section.append('<div class="topic">')
            section.append(f'<h3>{escape(property_list[0])}</h3>')
            section.append('<ul>')
            for line in property_list[1:]:
                section.append(f'<li>{make_html_link(line)}</li>')
            section.append('</ul>')
            section.append('</div>')

        if entry['$links']:
            section.append('<div class="references">')
            section.append('<h3>Referenced by</h3>')
            section.append('<ul>')
            for link in entry['$links']:
                print(f'backlink for {k}: {database[link[2]]["$keyword_name"]} via {link[1]}')
# back-link the individual link
#                section.append(
#                    f'<li><a class="back-link" href="#link-{escape(link[0].split("-")[1])}">'
#                    f'{escape(link[1])}</a> in section "{escape(link[2])}"</li>'
#                )
# back-link the whole section
                section.append(
                    f'<li><a class="back-link" href="#{escape(link[2])}">'
                    f'{database[link[2]]["$keyword_name"]}</a> via {link[1]}"</li>'
                )
            section.append('</ul>')
            section.append('</div>')

        section.append('</section>')
        sections.append("\n".join(section))

    return "".join(sections)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown notes into a database")
    parser.add_argument("--input", type=str, default="data.json")
    parser.add_argument("--output", type=str, default="data.html")
    parser.add_argument("--title", type=str, default="Automatically Generated Notes")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        database = json.load(f)

    html_content = create_html(database)
    html_file =f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + escape(args.title) + """</title>
<link rel="stylesheet" href="./style.css">
</head>
<script>
window.MathJax = {
tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$','$$'], ['\\\\[','\\\\]']]
}
};
</script>

<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<body>
<main class="page">""" + f"""
{html_content}
</main>
</body>
</html>"""

    with open(args.output, 'w') as f:
        f.write(html_file)
    print(f"HTML file created at {args.output}")