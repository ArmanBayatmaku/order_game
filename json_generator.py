import json
import random
import pandas as pd
import os
import re
import numpy as np


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
        a = random.choice(self.valid_columns)
        return a

    def pick_animals(self, n=5, feature = "Height (cm)"):
        sample_rows = self.df.sample(5)
        sample_rows = sample_rows[["Animal", feature]]
        wrong_format = 0
        s = str(sample_rows[feature]).strip().lower()
        if "varies" or "not applicable" in s:
            wrong_format = 1

        while wrong_format == 1:
            sample_rows = self.df.sample(5)
            sample_rows = sample_rows[["Animal", feature]]
            s = str(sample_rows[feature]).strip().lower()
            if "varies" or "not applicable" not in s: 
                wrong_format = 0
        return sample_rows
    

    def parse_feature_value(self, raw, challenge_type):
        s = str(raw).strip().lower()
        
        if s.startswith("up to "):
            s = s.replace("up to ", "").strip()

        is_years = "years" in s
        is_months = "months" in s
        is_days = "days" in s

        numbers = re.findall(r"\d+\.?\d*", s)

        numbers2 = [float(n) for n in numbers]

        value = np.mean(numbers2)

        if("(days)" in challenge_type):
            if is_months:
                value = value * 30.0
            elif is_years:
                value = value * 365.0
        
        if("(years)" in challenge_type):
            if is_months:
                value = value / 12.0
            elif is_days:
                value = value / 365.0


        return float(value)


    def generate_json(self, output_path="generated_challenge.json"):

        feature = self.pick_feature()
        sample = self.pick_animals(5, feature)
        #parsed_sample = []

        sample[feature] = sample[feature].apply(lambda x: self.parse_feature_value(x, feature))
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
            "correct_order": [a["name"] for a in sorted_animals],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        return output_path


if __name__ == "__main__":
    generator = AnimalSortingGenerator(dataset_path = "Dataset/Zoo_Animals_Dataset.csv", valid_columns= ["Weight (kg)", "Height (cm)", "Lifespan (years)", "Average Speed (km/h)", "Gestation Period (days)"])

    generator.load_dataset()
    path = generator.generate_json("challenge1.json")
    print(f"Generated challenge saved to: {path}")