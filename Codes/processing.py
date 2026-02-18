import json
import re
from html import escape
from collections.abc import Iterable

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
        return ">remark", stripped_line[2:], starting_spaces, False
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

    def process(self):
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
        
    def show_json(self):
        return json.dumps(self.database, indent=4)

    def make_markdown_link(self, line):
        segments = make_segments(line)
        for i in range(1, len(segments), 2):  # Process only the segments between __
            match = re.match(r'(.*), link-(.*), (.*)', segments[i])
            if match:
                s, link_number, resolved_keyword = match.groups()
                segments[i] = f'<a id="link-{link_number}"></a>[{s}](#{resolved_keyword})'
            else:
                raise ValueError("Invalid link format.")
        return "".join(segments)

    def create_markdown(self):
        final = []
        for k in self.database:
            if k in ['linknumber']:
                continue
            final.append(f'<a id="{k}"></a>')
            final.append(f'## {self.database[k]["$keyword_name"]}')
            for property, property_list in self.database[k].items():
                if property in ['$links', '$keyword_name']:
                    continue
                if property == '>remark':
                    final.append(f'> {",".join(self.database[k][">remark"][1:])}')
                    continue
                final.append(f'- {property_list[0]}')
                for line in property_list[1:]:
                    line = self.make_markdown_link(line)
                    final.append(f'\t- {line}')
            if self.database[k]['$links']:
                final.append('- referenced by:')
                for link in self.database[k]['$links']:
                    final.append(f'\t- [{link[1]}](#{link[0]}) in section "{link[2]}"')
        return "\n".join(final)

    def make_html_link(self, line):
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

    def create_html(self, title="Automatically Generated Notes"):
        sections = []
        for k in self.database:
            if k in ['linknumber']:
                continue

            entry = self.database[k]
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
                    section.append(f'<li>{self.make_html_link(line)}</li>')
                section.append('</ul>')
                section.append('</div>')

            if entry['$links']:
                section.append('<div class="references">')
                section.append('<h3>Referenced by</h3>')
                section.append('<ul>')
                for link in entry['$links']:
                    section.append(
                        f'<li><a class="back-link" href="#link-{escape(link[0].split("-")[1])}">'
                        f'{escape(link[1])}</a> in section "{escape(link[2])}"</li>'
                    )
                section.append('</ul>')
                section.append('</div>')

            section.append('</section>')
            sections.append("\n".join(section))

        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>""" + escape(title) + """</title>
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
    {"".join(sections)}
  </main>
</body>
</html>"""

