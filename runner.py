import argparse
import pandas as pd
from product_matching.pipeline import ProductMatchingPipeline

def load_category_mapping(dictionary_path):
    df_dict = pd.read_excel(dictionary_path, sheet_name="CATEGORIAS")
    df_dict = df_dict[["ABREVIATURA (Abbreviation)", "DETALLE (Detail)", "CATEGORIA_PROD"]].dropna()
    df_dict.columns = ["Abbreviation", "Detail", "MappedCategory"]
    df_dict = df_dict.apply(lambda col: col.str.lower().str.strip())
    return dict(zip(df_dict["Abbreviation"], df_dict["MappedCategory"]))

def run_matching(master_path, dictionary_path, distributor_path, output_path):
    df_master = pd.read_excel(master_path, sheet_name="Maestro General")
    category_map = load_category_mapping(dictionary_path)
    df_distributor = pd.read_excel(distributor_path)
    
    pipeline = ProductMatchingPipeline(df_master, category_map)
    df_result = pipeline.process(df_distributor)

    # ✅ Select specific columns for output
    output_columns = [
        "CODIGODISTRIBUIDOR",
        "NOMBREPRODUCTODISTRIBUIDOR",
        "CODIGOPRODUCTODISTRIBUIDOR",
        "Matched Name",
        "Match Score",
        "CodigoProducto",
        "Exist in the Product Master?",
        "Match Confidence",
        "Size Match",
        "Category Match",
        "Brand Match",
        "System Observation"
    ]
    df_result[output_columns].to_excel(output_path, index=False)

    # Print summary
    total = len(df_result)
    high = (df_result["Match Confidence"] == "HIGH").sum()
    medium = (df_result["Match Confidence"] == "MEDIUM").sum()
    low = (df_result["Match Confidence"] == "LOW").sum()
    no_match = (df_result["Match Confidence"] == "NO MATCH").sum()

    print(f"✅ Output saved at {output_path}")
    print(f"Total products: {total}")
    print(f"HIGH Confidence Matches: {high}")
    print(f"MEDIUM Confidence Matches: {medium}")
    print(f"LOW Confidence Matches: {low}")
    print(f"NO MATCH: {no_match}")
    print(f"Size Matches: {df_result['Size Match'].sum()} / {total}")
    print(f"Category Matches: {df_result['Category Match'].sum()} / {total}")
    print(f"Brand Matches: {df_result['Brand Match'].sum()} / {total}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Product Matching Pipeline Runner")
    parser.add_argument("--master", type=str, help="Master file path")
    parser.add_argument("--dictionary", type=str, help="Dictionary file path")
    parser.add_argument("--distributor", type=str, help="Distributor file path")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--config", type=str, help="Path to YAML config file", default=None)
    args = parser.parse_args()

    if args.config:
        import yaml
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
        master = config['master']
        dictionary = config['dictionary']
        distributor = config['distributor']
        output = config['output']
    else:
        master = args.master
        dictionary = args.dictionary
        distributor = args.distributor
        output = args.output

    run_matching(master, dictionary, distributor, output)
