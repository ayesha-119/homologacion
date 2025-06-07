from rapidfuzz import process, fuzz

class FuzzyMatcher:
    @staticmethod
    def match_name(name, master_df):
        choices = master_df["Clean Name"].tolist()
        result = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
        if result:
            match_name = result[0]
            score = result[1]
            # Now get the matching row to extract CodigoProducto
            matched_row = master_df[master_df["Clean Name"] == match_name]
            if not matched_row.empty:
                codigo = matched_row.iloc[0]["CodigoProducto"]
            else:
                codigo = None
        else:
            match_name, score, codigo = "", 0, None
        return match_name, score, codigo
