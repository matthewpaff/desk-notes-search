import unittest
from copy import deepcopy
from pathlib import Path
from retrieval_tool.core import evaluate
from retrieval_tool.fixture_check import check
from retrieval_tool.generate_fixtures import make_case


class CoreTests(unittest.TestCase):
    def test_independent_expected_results_for_the_corpus(self):
        self.assertGreater(check(Path(__file__).resolve().parents[1]/"fixtures/cases.jsonl",evaluate),0)

    def test_supplied_input_is_unchanged(self):
        case=make_case(0)
        original=deepcopy(case["input"])
        self.assertEqual(evaluate(case["input"]),case["expected"])
        self.assertEqual(case["input"],original)

    def test_missing_required_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({})

    def test_accented_words_are_searchable(self):
        result=evaluate({'query':'CAFÉ','notes':[{'id':'one','text':'A café visit'},{'id':'two','text':'Coffee visit'}],'limit':5})
        self.assertEqual([row['id'] for row in result['results']],['one'])
        self.assertEqual(result['results'][0]['matched_terms'],['café'])

if __name__=="__main__":
    unittest.main()
