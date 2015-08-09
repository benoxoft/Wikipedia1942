import unittest

from src.wiki1942 import wiki

class TestWiki(unittest.TestCase):
    
    def test_randomize_page(self):
        page = wiki.randomize_page()
        print(page.url)
    
    def test_open_page(self):
        page = wiki.open_page("Montreal")
        print(page.url)
        print(page.summary)
        
    def test_gemify_page(self):
        page = wiki.open_page("Montreal")
        x = wiki.gemify_page(page)
        print(x)
        
    def test_next_gem(self):
        page = wiki.open_page("Montreal")
        x = wiki.gemify_page(page)
        
        self.assertEqual(None, wiki.next_gem(0, x))
        first = x[0]
        self.assertEqual(first, wiki.next_gem(200, x))
        self.assertNotEqual(first, x[0])
        first = x[0]
        self.assertEqual(first, wiki.next_gem(200, x))
        
        while len(x) != 0:
            print (wiki.next_gem(600, x))
        