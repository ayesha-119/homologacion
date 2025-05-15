from rapidfuzz import process, fuzz

class FuzzyMatcher:
    @staticmethod
    def match_name(name, master_names):
        result = process.extractOne(name, master_names, scorer=fuzz.token_sort_ratio)
        if result:
            match, score = result[0], result[1]  # Safely extract first two
        else:
            match, score = "", 0
        return match, score
