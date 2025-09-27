import unittest
import services



class MyTestCase(unittest.TestCase):
    def test_llm_api(self):
        query = "Give me some information about the Rocks district."
        parsed_answer, raw_dict = services.call_gemini(query)
        print(parsed_answer)
        print(raw_dict)

if __name__ == '__main__':
    unittest.main()
