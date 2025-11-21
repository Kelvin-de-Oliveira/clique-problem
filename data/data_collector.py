import pandas as pd
import os

class DataCollector:
    def __init__(self, raw_folder="data/results/raw"):
        self.raw_folder = raw_folder
        self.df_median = None
        self.df_individual = None

    def load_csvs(self):
        median_csv = os.path.join(self.raw_folder, "benchmark_median.csv")
        individual_csv = os.path.join(self.raw_folder, "benchmark_individual.csv")

        if not os.path.exists(median_csv):
            raise FileNotFoundError(f"{median_csv} não encontrado.")
        if not os.path.exists(individual_csv):
            raise FileNotFoundError(f"{individual_csv} não encontrado.")

        self.df_median = pd.read_csv(median_csv)
        self.df_individual = pd.read_csv(individual_csv)
        return self.df_median, self.df_individual
