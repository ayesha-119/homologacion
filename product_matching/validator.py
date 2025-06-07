from rapidfuzz import fuzz
import re

class Validator:
    def __init__(self, master_df):
        self.master_df = master_df
        self.present_map = master_df.set_index("Clean Name")["Presentacion"].to_dict()
        self.category_map = master_df.set_index("Clean Name")["Normalized_Categoria"].to_dict()
        self.brand_map = master_df.set_index("Clean Name")["Marca"].to_dict()

    @staticmethod
    def brand_match(master_brand, product_name):
        if not master_brand or not product_name:
            return False
        if str(master_brand).lower() in str(product_name).lower():
            return True
        score = fuzz.partial_ratio(str(master_brand).lower(), str(product_name).lower())
        return score >= 80

    @staticmethod
    def normalize_size_variants(sizes):
        normalized = set()
        for s in sizes:
            if "gr" in s or "ml" in s:
                try:
                    value = float(re.sub(r"[^\d.]", "", s))
                    if value >= 1000:
                        if "gr" in s:
                            normalized.add(f"{value / 1000}kg")
                        if "ml" in s:
                            normalized.add(f"{value / 1000}lt")
                except:
                    pass
            normalized.add(s)
        return list(normalized)

    def check_exist_in_master(self, sizes, brand, category):
        if not sizes or not brand or not category:
            return "NO"
        sizes_all = sizes + self.normalize_size_variants(sizes)
        for _, row in self.master_df.iterrows():
            present = str(row["Presentacion"]).lower().replace(" ", "").replace("lt", "l")
            brand_master = str(row["Marca"]).lower()
            cat_master = str(row["Normalized_Categoria"]).lower()
            if any(size.replace("lt", "l") in present for size in sizes_all) and brand.lower() in brand_master and category.lower() == cat_master:
                return "YES"
        return "NO"

    def validate_row(self, row):
        matched = row["Matched Name"]
        presentacion = str(self.present_map.get(matched, "")).lower().replace(" ", "").replace("lt", "l")
        cat_master = self.category_map.get(matched, None)
        brand = self.brand_map.get(matched, None)
        sizes = row["Extracted_Sizes"]
        cat_extracted = row["Normalized_Category"]
        original_name = row["NOMBREPRODUCTODISTRIBUIDOR"]

        size_match = any(s.replace("lt", "l") in presentacion for s in sizes)
        cat_match = cat_extracted == cat_master
        brand_match_flag = self.brand_match(brand, original_name)

        exist_in_master = self.check_exist_in_master(sizes, brand if brand else "", cat_master if cat_master else "")

        if not size_match:
            return "NO MATCH", "❌ Size mismatch. No homologation allowed.", exist_in_master, size_match, cat_match, brand_match_flag

        score = row["Match Score"]
        if score >= 90 and brand_match_flag:
            return "HIGH", "✅ High confidence match.", exist_in_master, size_match, cat_match, brand_match_flag
        elif score >= 75:
            return "MEDIUM", "⚠ Medium confidence. Review recommended.", exist_in_master, size_match, cat_match, brand_match_flag
        elif score >= 50:
            return "LOW", "⚠ Low confidence. Manual validation needed.", exist_in_master, size_match, cat_match, brand_match_flag
        else:
            return "NO MATCH", "❌ Low score.", exist_in_master, size_match, cat_match, brand_match_flag
        
    