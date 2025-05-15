import pandas as pd
import re

# Load your distributor file
file_path = "data/base_homologacion_ml.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

# Sample 50 random product descriptions
sample = df['NOMBREPRODUCTODISTRIBUIDOR'].dropna().sample(50, random_state=42)


# -----------------------------
# Old Extractor (legacy logic, basic pattern)
# -----------------------------
def old_extract_sizes(text):
    text = str(text).lower()
    pattern = re.compile(r'\d+[.,]?\d*\s*(kg|gr|g|lt|l|ml|cc|und|uni|pqt|bot|bol|fco|pk)', re.IGNORECASE)
    matches = pattern.findall(text)
    return matches if matches else []


# -----------------------------
# New Improved Extractor (bulletproof)
# -----------------------------
def improved_extract_sizes(text):
    text = str(text).lower()
    text = text.replace(' krx', ' kg').replace(' kr', ' kg').replace(' lts', ' lt').replace(' lt.', ' lt')
    text = re.sub(r'\s*\.', '', text)
    text = re.sub(r'\s+', ' ', text)

    unit_map = {
        "g": "gr",
        "gr": "gr",
        "kg": "kg",
        "ml": "ml",
        "l": "lt",
        "lt": "lt",
        "cc": "cc",
        "und": "und",
        "uni": "und",
        "un": "und"
    }

    patterns = [
        r'(\d+[.,]?\d*)\s*(kg|gr|g|lt|l|ml|cc|und|uni|un)',
        r'(\d+[.,]?\d*)\s*[*xX]\s*(\d+)',
        r'(\d+[.,]?\d*)\s*(kg|gr|g|lt|l|ml|cc)\s*[*xX]\s*(\d+)',
        r'(\d+)\s*(und|uni|un)\s*[*xX]\s*(\d+)\s*(gr|g|ml|kg)',
        r'(\d+)\s*[xX]\s*(\d+)',
        r'(\d+[.,]?\d*)\+\d+[.,]?\d*\s*(ml|gr|lt|kg|cc)',
        r'(\d+[.,]?\d*)\s*(ml|gr|lt|kg|cc)[.]?'
    ]

    sizes = set()

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            flat = " ".join([m for m in match if m]).strip()
            for k, v in unit_map.items():
                flat = re.sub(rf'\b{k}\b', v, flat)
            flat = re.sub(r'[*xX]', 'x', flat)
            flat = re.sub(r'\s+', '', flat)
            sizes.add(flat)

    return list(sizes)


# -----------------------------
# Compare and export to CSV for VS Code
# -----------------------------
results = []

for desc in sample:
    old_result = old_extract_sizes(desc)
    new_result = improved_extract_sizes(desc)
    results.append({
        "Description": desc,
        "Old Extractor": old_result,
        "Improved Extractor": new_result
    })

df_results = pd.DataFrame(results)
print(df_results)

# Save as CSV for VS Code
df_results.to_csv("validation_size_extraction_comparison.csv", index=False)
print("✅ Comparison saved to validation_size_extraction_comparison.csv")
