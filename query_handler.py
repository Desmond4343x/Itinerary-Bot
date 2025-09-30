# ------------------------ mapping_test.py ------------------------
from mapping import get_maps
import spacy
from itertools import permutations

# ------------------------ Load maps ------------------------
heading_tags_map, section_map = get_maps()

# ------------------------ spaCy model ------------------------
nlp = spacy.load("en_core_web_sm")  # small English model

def get_nouns(text):
    """Extract nouns and proper nouns from text using spaCy"""
    doc = nlp(text.lower())
    nouns = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN", "VERB"}]
    return nouns

def get_relevant_canonical_headings(query: str) -> set:
    """Return canonical headings relevant to the query"""
    nouns = get_nouns(query)
    matched_canonical_headings = set()
    
    # Generate all 1,2-word permutations of nouns
    for r in range(1, min(2, len(nouns)+1)):
        for perm in permutations(nouns, r):
            phrase = " ".join(perm)
            for heading, tags in heading_tags_map.items():
                if heading in matched_canonical_headings:
                    continue  # Skip this canonical heading if already matched
                if phrase in tags:
                    matched_canonical_headings.add(heading)
    
    return matched_canonical_headings


if __name__ == "__main__":
        query = "house"
        result = get_relevant_canonical_headings(query)
        print("\nResult:", result)
