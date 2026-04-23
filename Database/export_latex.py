import json
import re
import argparse
import hashlib
import os

DATA_FILE = "data/database.json"
SYSTEM_FILE = "data/database_system.json"
LAYOUT_FILE = "data/database_layout.json"

def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)

def escape_latex_safe_math(text: str) -> str:
    # In math mode, only a few characters need escaping.
    replacements = {
        "#": r"\#",
        "%": r"\%",
    }
    return "".join(replacements.get(char, char) for char in text)

def key_to_label(key: str) -> str:
    # Keep labels ASCII-safe and deterministic.
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return f"kw:{digest}"


def image_to_label(image_file: str) -> str:
    digest = hashlib.sha1(image_file.encode("utf-8")).hexdigest()[:12]
    return f"img:{digest}"

def make_latex_line(line):
    def repl_link(match: re.Match) -> str:
        type = match.group(1)
        name = match.group(2)
        value = match.group(3)
        if type == "keyword":
            return rf"\hyperref[{key_to_label(value)}]{{{escape_latex(name)}}}"
        elif type == "image":
            return rf"\hyperref[{image_to_label(value)}]{{image: {escape_latex(name)}}}"
        elif type == "external-link":
            return rf"\href{{{value}}}{{{escape_latex(name)}}}"
        else:
            raise ValueError(f"Unknown link type: {type}")

    return LINK_RE.sub(repl_link, escape_latex_safe_math(line))

def create_latex(database):
    final = []
    final.append(r"""
\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage[margin=1in]{geometry}
\usepackage[
    colorlinks=true,
    linkcolor=blue,
    urlcolor=magenta,
    citecolor=green,
    pdfauthor={Your Name},
    pdftitle={Your Document}
]{hyperref}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{tcolorbox}
\usepackage{float}
\usepackage{amsmath, amsfonts, amssymb}
\setlist{leftmargin=1.4em, noitemsep, itemsep=2pt, topsep=4pt}
\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}
% A reusable framed title box
\newtcolorbox{TitleBox}{
  colback=black!3,
  colframe=cyan!60!black,
  boxrule=0.9pt,
  arc=3pt,
  left=8pt,right=8pt,top=6pt,bottom=6pt,
  width=\textwidth
}

% Boxed title with a hyperlink anchor
% Usage: \boxtitle{<anchor>}{<title text>}
\newcommand{\boxtitle}[2]{%
  \par\vspace{1em}
  \phantomsection
  \hypertarget{#1}{}%
  \begin{TitleBox}
    {\Large\bfseries #2}
  \end{TitleBox}
}
\begin{document}
%%%%%%%%%%%%%% Content starts here %%%%%
""")
    images = set()
    for key, entry in database.items():
        if key.startswith('$'):
            continue
        #final.append(rf"\section{{{escape_latex(entry['$keyword_name'])}}}")
        final.append(r"\boxtitle{" + key + r"}{" + escape_latex(entry['$keyword_name']) + r"}")
        final.append(rf"\label{{{key_to_label(key)}}}")

        for property, property_list in entry.items():
            if property == '>remark':
                #final.append(r'\fbox{\parbox{0.8\linewidth}{' + " ".join(entry[">remark"][1:]) + '}}')
                final.append(r'\begin{tcolorbox}[colback=yellow!10,colframe=yellow!50!black,title=Remark]' + " ".join(entry[">remark"][1:]) + r'\end{tcolorbox}')
                continue
            if property.startswith('$'):
                continue
            title = escape_latex(property_list[0])
            final.append(rf"\subsection*{{{title}}}")
            final.append(r"\begin{itemize}")
            for line in property_list[1:]:
                final.append(
                    rf"\item {make_latex_line(line)}"
                )
            final.append(r"\end{itemize}")

        if entry['$links']:
            final.append(r"\subsection*{Referenced by}")
            final.append(r"\begin{itemize}")
            for name, src_key, via in entry["$links"]:
                final.append(
                    rf"\item \hyperref[{key_to_label(src_key)}]{{{escape_latex(name)}}} via ``{escape_latex(via)}''"
                )
            final.append(r"\end{itemize}")
        if entry['$images']:
            #final.append(r"\subsection*{Images}")
            for image_name, image_file in entry["$images"]:
                label = image_to_label(image_file)
                if label not in images:
                    images.add(label)
                    final.extend(
                        [
                            r"\begin{figure}[H]",
                            r"\centering",
                            rf"\includegraphics[width=8 cm]{{\detokenize{{../Images/{image_file}}}}}",
                            rf"\caption{{{escape_latex(image_name)}}}",
                            rf"\label{{{image_to_label(image_file)}}}",
                            r"\end{figure}",
                        ]
                )
    final.append(r"\end{document}")
    return "\n".join(final)

parser = argparse.ArgumentParser(description="Process markdown notes into a database")
parser.add_argument("--database", type=str, default="data/database.json")
parser.add_argument("--output", type=str, default="content.tex")

args = parser.parse_args()

try:
    with open(args.database, 'r') as f:
        database = json.load(f)
    # Load system data
    with open(SYSTEM_FILE, "r", encoding="utf-8") as f:
        system_data = json.load(f)
except FileNotFoundError:
    print(f"Warning: file not found")
except json.JSONDecodeError as e:
    print(f"Error loading: {e}")

link_separator = system_data['link_separator']
item_separator = system_data['item_separator']
LINK_RE = re.compile(link_separator  + r'(.*?)' + item_separator + r'(.*?)' + item_separator + r'(.*?)' + link_separator)

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../Rendered Content')):
    os.makedirs(os.path.join(os.path.dirname(__file__), '../Rendered Content'))

with open(os.path.join(os.path.dirname(__file__), '../Rendered Content', args.output), 'w') as f:
    print(create_latex(database), file=f)
print(f"LaTeX file created at {args.output}")
