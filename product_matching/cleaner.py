import re

class DataCleaner:
    @staticmethod
    def clean_name(text):
        text = str(text).lower()
        text = re.sub(r"\([^)]*\)", "", text)
        text = re.sub(r"\b(b|b und b|bonif|bonif:|bonif\.)\b", "", text)
        text = re.sub(r"\d+[.,]?\d*\s*(kg|gr|g|k|lt|l|ml|cc|und|uni|bot|bol|pqt|fco|pk)", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        return text.strip()

    @staticmethod
    def clean_unit_match(value):
        match = re.match(r'(\d+[.,]?\d*)\s*(kg|gr|g|k|lt|l|ml|cc|und|uni)', value.lower().strip())
        if not match:
            return value
        number, unit = match.groups()
        unit_map = {
            "g": "gr", "gr": "gr",
            "k": "kg", "kg": "kg",
            "ml": "ml",
            "l": "lt", "lt": "lt",
            "cc": "cc",
            "und": "und", "uni": "und"
        }
        normalized_unit = unit_map.get(unit.lower(), unit.lower())
        return f"{number.strip().replace(',', '.').replace(' ', '')}{normalized_unit}"

    @staticmethod
    def extract_sizes(text):
        pattern = re.compile(r"(\d+[.,]?\d*)\s*(kg|gr|g|k|lt|l|ml|cc|und|uni|bot|bol|pqt|fco|pk)(\s*[\*\+xX]\s*\d+)?")
        matches = pattern.findall(str(text).lower())
        sizes = set()
        for qty, unit, multi in matches:
            qty_clean = qty.replace(',', '.').strip()
            unit_map = {"g": "gr", "gr": "gr", "k": "kg", "kg": "kg", "ml": "ml", "l": "lt", "lt": "lt", "cc": "cc"}
            unit_norm = unit_map.get(unit, unit)
            size = f"{qty_clean}{unit_norm}"
            if multi:
                multi_clean = re.sub(r"\D", "", multi)
                size = f"{size}x{multi_clean}"
            sizes.add(size)
        return list(sizes)

    @staticmethod
    def extract_category(text, category_map):
        text = str(text).lower()
        for abbr in category_map:
            if re.search(rf"\b{re.escape(abbr)}\b", text):
                return category_map[abbr]
        return None
