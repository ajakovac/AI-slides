import argparse
import hashlib
import json
import re


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


def key_to_label(key: str) -> str:
    # Keep labels ASCII-safe and deterministic.
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return f"kw:{digest}"


def image_to_label(image_file: str) -> str:
    digest = hashlib.sha1(image_file.encode("utf-8")).hexdigest()[:12]
    return f"img:{digest}"


def make_latex_text(
    line: str, label_map: dict[str, str], image_label_map: dict[str, str]
) -> str:
    last = 0
    chunks: list[str] = []

    for match in LINK_RE.finditer(line):
        chunks.append(escape_latex(line[last:match.start()]))

        link_type = match.group(1)
        name = match.group(2)
        value = match.group(3)

        if link_type == "keyword":
            target = label_map.get(value, key_to_label(value))
            chunks.append(rf"\hyperref[{target}]{{{escape_latex(name)}}}")
        elif link_type == "image":
            image_target = image_label_map.get(value, image_to_label(value))
            chunks.append(rf"\hyperref[{image_target}]{{image: {escape_latex(name)}}}")
        elif link_type == "external-link":
            chunks.append(rf"\href{{{value}}}{{{escape_latex(name)}}}")
        else:
            raise ValueError(f"Unknown link type: {link_type}")

        last = match.end()

    chunks.append(escape_latex(line[last:]))
    return "".join(chunks)


def create_latex(database: dict) -> str:
    label_map = {k: key_to_label(k) for k in database if not k.startswith("$")}
    image_label_map: dict[str, str] = {}
    for key, entry in database.items():
        if key.startswith("$"):
            continue
        for _, image_file in entry.get("$images", []):
            image_label_map[image_file] = image_to_label(image_file)
    final: list[str] = []

    final.extend(
        [
            r"\documentclass[11pt]{article}",
            r"\usepackage{fontspec}",
            r"\usepackage[margin=1in]{geometry}",
            r"\usepackage{hyperref}",
            r"\usepackage{graphicx}",
            r"\usepackage{enumitem}",
            r"\usepackage{float}",
            r"\setlist[itemize]{leftmargin=1.4em}",
            r"\setlength{\parskip}{0.4em}",
            r"\setlength{\parindent}{0pt}",
            r"\begin{document}",
        ]
    )

    for key in database:
        if key.startswith("$"):
            continue

        entry = database[key]
        final.append(rf"\section{{{escape_latex(entry['$keyword_name'])}}}")
        final.append(rf"\label{{{label_map[key]}}}")

        for property_key, property_list in entry.items():
            if property_key == ">remark":
                remark = ", ".join(property_list[1:]).strip()
                if remark:
                    final.append(
                        rf"\begin{{quote}}\textit{{{make_latex_text(remark, label_map, image_label_map)}}}\end{{quote}}"
                    )
                continue

            if property_key.startswith("$"):
                continue

            title = escape_latex(property_list[0])
            final.append(rf"\subsection*{{{title}}}")
            final.append(r"\begin{itemize}")
            for line in property_list[1:]:
                final.append(
                    rf"\item {make_latex_text(line, label_map, image_label_map)}"
                )
            final.append(r"\end{itemize}")

        if entry["$links"]:
            final.append(r"\subsection*{Referenced by}")
            final.append(r"\begin{itemize}")
            for name, src_key, via in entry["$links"]:
                src_label = label_map.get(src_key, key_to_label(src_key))
                final.append(
                    rf"\item \hyperref[{src_label}]{{{escape_latex(name)}}} via ``{escape_latex(via)}''"
                )
            final.append(r"\end{itemize}")

        if entry["$images"]:
            final.append(r"\subsection*{Images}")
            for image_name, image_file in entry["$images"]:
                final.extend(
                    [
                        r"\begin{figure}[H]",
                        r"\centering",
                        rf"\label{{{image_label_map[image_file]}}}",
                        rf"\includegraphics[width=0.85\linewidth]{{\detokenize{{../Images/{image_file}}}}}",
                        rf"\caption{{{escape_latex(image_name)}}}",
                        r"\end{figure}",
                    ]
                )

    final.append(r"\end{document}")
    return "\n".join(final)


parser = argparse.ArgumentParser(description="Export the JSON database to a LaTeX file")
parser.add_argument("--database", type=str, default="data/database.json")
parser.add_argument("--output", type=str, default="content.tex")

args = parser.parse_args()

with open(args.database, "r", encoding="utf-8") as f:
    database = json.load(f)

link_separator = database["$system"]["link_separator"]
item_separator = database["$system"]["item_separator"]
LINK_RE = re.compile(
    re.escape(link_separator)
    + r"(.*?)"
    + re.escape(item_separator)
    + r"(.*?)"
    + re.escape(item_separator)
    + r"(.*?)"
    + re.escape(link_separator)
)

with open(args.output, "w", encoding="utf-8") as f:
    print(create_latex(database), file=f)

print(f"LaTeX file created at {args.output}")
