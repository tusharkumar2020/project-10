import unittest
from sentiment_analysis import analyze_text

class TestTextAnalyzer(unittest.TestCase):

    def test_analyze_text(self):
        print("Running test_analyze_text")
        
        # Test case for positive sentiment
        result_1 = analyze_text('I love working with Python')
        self.assertEqual(result_1['sentiment']['document']['label'], 'positive')
        
        # Test case for negative sentiment
        result_2 = analyze_text('I hate working with Python')
        self.assertEqual(result_2['sentiment']['document']['label'], 'negative')
        
        # Test case for neutral sentiment
        result_3 = analyze_text('I am neutral on Python')
        self.assertEqual(result_3['sentiment']['document']['label'], 'neutral')

    def test_empty_input(self):
        print("Running test_empty_input")
        result = analyze_text('')
        self.assertIsNone(result)

    def test_invalid_input(self):
        print("Running test_invalid_input")
        result = analyze_text(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()