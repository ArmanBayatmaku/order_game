import json
import os
import csv
import random


class AnimalSortingRenderer:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = None

    #loads json file
    def load_json(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        required_fields = ["feature", "order", "animals", "correct_order"]
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Missing field in JSON: {field}")

    
    #onordered animal list
    #def _render_animals_list(self):
    #    out = ""
    #    for item in self.data["animals"]:
    #        out += f"- {item['name']}\n"
    #    return out

    #hinte
    def _render_hints(self):
        hints = self.data.get("hints", [])
        if not hints:
            return "No hints provided."

        out = "<details>\n<summary>Click to reveal hints</summary>\n\n"
        for h in hints:
            out += f"- {h}\n"
        out += "</details>\n"
        return out

    #render the markdown
    def generate_markdown(self):
        feature = self.data["feature"]
        order = self.data["order"].capitalize()

        md = f"# 🐾 Animal Sorting Challenge\n\n"
        md += f"**Feature:** `{feature}`\n\n"
        md += f"**Order:** **{order}**\n\n"
        md += "Rearrange the animals below into the correct order:\n\n"

        #randomly ordered animals
        md += self._render_animals_list()
        md += "\n\n---\n\n"

        #hints
        md += "### 🔍 Hints\n"
        md += self._render_hints()
        md += "\n\n---\n\n"

        #
        md += "### Corect order\n"
        md += " → ".join(self.data["correct_order"])
        md += "\n"

        return md

    #save the .md file
    def save_markdown(self, output_path):
        markdown = self.generate_markdown()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        return output_path



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render Animal Sorting Challenge JSON to Markdown.")
    parser.add_argument("json", help="Path to input JSON file")
    parser.add_argument("output", help="Path to save markdown output")

    args = parser.parse_args()

    renderer = AnimalSortingRenderer(args.json)
    renderer.load_json()
    path = renderer.save_markdown(args.output)
    print(f"Markdown generated at: {path}")


