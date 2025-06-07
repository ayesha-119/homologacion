import pandas as pd
from .cleaner import DataCleaner
from .matcher import FuzzyMatcher
from .validator import Validator

class ProductMatchingPipeline:
    def __init__(self, master_df, category_dict):
        self.master_df = master_df.copy()
        self.category_map = category_dict
        self.master_df["Clean Name"] = self.master_df["DescripcionProducto"].fillna("").apply(DataCleaner.clean_name)
        self.master_df["Normalized_Categoria"] = self.master_df["Categoria"].fillna("").str.lower().str.strip().map(
            lambda x: self.category_map.get(x, x))
        self.validator = Validator(self.master_df)

    def process(self, distributor_df):
        df = distributor_df.copy()
        df["Clean Name"] = df["NOMBREPRODUCTODISTRIBUIDOR"].astype(str).apply(DataCleaner.clean_name)
        df["Extracted_Sizes"] = df["NOMBREPRODUCTODISTRIBUIDOR"].apply(DataCleaner.extract_sizes)
        df["Normalized_Category"] = df["Clean Name"].apply(
            lambda x: DataCleaner.extract_category(x, self.category_map))

        master_names = self.master_df["Clean Name"].tolist()
        df["Matched Name"] = df["Clean Name"].apply(lambda x: FuzzyMatcher.match_name(x, master_names)[0])
        df["Match Score"] = df["Clean Name"].apply(lambda x: FuzzyMatcher.match_name(x, master_names)[1])


        results = df.apply(self.validator.validate_row, axis=1)
        (df["Match Confidence"], df["System Observation"],
         df["Exist in the Product Master?"], df["Size Match"],
         df["Category Match"], df["Brand Match"]) = zip(*results)

        return df
