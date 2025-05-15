
# Product Homologation Pipeline (Clean & Modular)

This is a **robust, modular, and client-grade product homologation pipeline** designed to handle complex, messy distributor product descriptions, extract relevant size, packaging, quantity, and clean product names, and perform fuzzy matching against the client product master.

---

## Features

- ✅ Intelligent extraction of size, packaging, quantity, and units from messy descriptions.
- ✅ Strict validation rules (size-first logic, brand/category matching, client business rules).
- ✅ Fuzzy matching using `fuzzywuzzy`.
- ✅ Clean modular code structure (`cleaner`, `matcher`, `validator`, `pipeline`, `runner`).
- ✅ Configurable via `config.yaml`.
- ✅ Pre-check and logging of invalid or empty distributor products.
- ✅ Outputs clean results and logs invalid entries.

---

## Folder Structure

```
product_matching/
├── product_matching/
│   ├── cleaner.py
│   ├── matcher.py
│   ├── validator.py
│   ├── pipeline.py
├── runner.py
├── config.yaml
├── data/
├── output/
└── README.md
```

---

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare your `config.yaml`
```yaml
distributor_file: "data/Base homologación Clorox.xlsx"
master_file: "data/base_homologacion_ml.xlsx"
master_sheet: "Maestro General"
master_description_column: "DescripcionProducto"
dictionary_file: "data/Dictionary.xlsx"
output_file: "output/matched_clorox.xlsx"
```

### 3. Run the pipeline
```bash
python runner.py --config config.yaml
```

### 4. Outputs
- Clean matched file → in `output/`
- Invalid distributor rows → `output/invalid_products.xlsx`

---

## Business Rules (Strict)

- ❗ **If size does not match, no homologation is performed (even if fuzzy, brand, and category match).**
- ✅ Validation follows your logic exactly.
- ✅ 'Exist in Product Master?' column enforces client rules.

---


