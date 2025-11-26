import json
from pathlib import Path


def render_markdown(data: dict) -> str:
    feature = data["feature"]
    order = data.get("order", "ascending")
    animals = data["animals"]
    correct_order = data["correct_order"]

    md = []
    md.append(f"# Animal Sorting Challenge\n")

    direction_text = "smallest → largest" if order == "ascending" else "largest → smallest"

    md.append(
        f"Sort the animals **by their {feature}**, "
        f"from **{direction_text}**.\n"
    )

    md.append("## Animals\n")
    for animal in animals:
        md.append(f"- **{animal['name']}**")

    md.append("")  

    md.append("## Correct Order\n")
    md.append(" → ".join(correct_order))
    md.append("")

    return "\n".join(md)


def render_markdown_file(json_path: str, output_path: str):
    data = json.loads(Path(json_path).read_text())
    markdown_text = render_markdown(data)
    Path(output_path).write_text(markdown_text)


if __name__ == "__main__":
    render_markdown_file("challenge1.json", "challenge1.md")