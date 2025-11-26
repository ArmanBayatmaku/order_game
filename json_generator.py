import json
import random
import pandas as pd
import os
import re


class AnimalSortingGenerator:
    def __init__(self, dataset_path, valid_columns):
        self.dataset_path = dataset_path
        self.valid_columns = valid_columns
        self.df = None

    def load_dataset(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")

        self.df = pd.read_csv(self.dataset_path)

        for col in self.valid_columns:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' is not in dataset.")

    def pick_feature(self):
        return random.choice(self.valid_columns)

    def pick_animals(self, n=5, feature = "height"):
        valid_rows = self.df[self.df[feature].notna()]
        return valid_rows.sample(n)
    

    def parse_feature_value(raw):
        if raw is None:
            return None

        if not isinstance(raw, str):
            try:
                return float(raw)
            except:
                return None

        s = raw.strip().lower()

        
        s = s.replace("~", "").replace("approx.", "").replace("approximately", "").strip()

        s = s.replace("–", "-").replace("—", "-")


        if s.startswith("up to "):
            s = s.replace("up to ", "").strip()


        is_months = "month" in s
        is_days = "day" in s


        numbers = re.findall(r"\d+\.?\d*", s)

        if not numbers:
            return None

        numbers = [float(n) for n in numbers]


        value = np.mean(numbers)


        if is_months:
            value = value / 12.0 
        elif is_days:
            value = value / 365.0  

        return float(value)


    def generate_json(self, output_path="generated_challenge.json"):

        feature = self.pick_feature()
        sample = self.pick_animals(5, feature)

        animals = []
        for _, row in sample.iterrows():
            animals.append({
                "name": row["Animal"],          
                "value": float(row[feature])
            })

        sorted_animals = sorted(animals, key=lambda x: x["value"])

        json_data = {
            "challenge_type": "animal_sorting",
            "feature": feature,
            "order": "ascending",
            "animals": animals,
            "correct_order": [a["Animal"] for a in sorted_animals],
            "hints": [
                "Ascending means smallest to largest.",
                f"Focus on the '{feature}' values."
            ]
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        return output_path



if __name__ == "__main__":
    generator = AnimalSortingGenerator(dataset_path = "Dataset/Zoo_Animals_Dataset.csv", valid_columns= ["Weight (kg)", "Height (cm)", "Lifespan (years)", "Average Speed (km/h)", "Gestation Period (days)"])

    generator.load_dataset()
    path = generator.generate_json("challenge1.json")
    print(f"Generated challenge saved to: {path}")