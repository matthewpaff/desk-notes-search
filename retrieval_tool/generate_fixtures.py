"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('rank a matching personal note using the documented lexical score', {'query': 'cat', 'limit': 5, 'notes': [{'id': 'a{n}', 'text': 'cat'}, {'id': 'b{n}', 'text': 'dog'}]}, {'results': [{'id': 'a{n}', 'score': 0.5, 'matched_terms': ['cat']}]}), ('break equal lexical scores by source ID', {'query': 'CAT cat', 'limit': 5, 'notes': [{'id': 'b{n}', 'text': 'cat'}, {'id': 'a{n}', 'text': 'cat'}]}, {'results': [{'id': 'a{n}', 'score': 0.333333, 'matched_terms': ['cat']}, {'id': 'b{n}', 'score': 0.333333, 'matched_terms': ['cat']}]}), ('return no results for an empty query', {'query': '', 'limit': 5, 'notes': [{'id': 'a{n}', 'text': 'cat'}]}, {'results': []}), ('reject duplicate personal-note IDs', {'query': 'cat', 'limit': 5, 'notes': [{'id': 'a{n}', 'text': 'cat'}, {'id': 'a{n}', 'text': 'dog'}]}, None), ('reject boolean retrieval limits', {'query': 'cat', 'limit': True, 'notes': []}, None)]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "retrieval-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
