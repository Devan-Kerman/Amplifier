import data.wikipedia.wikipedia_dataset as wikiset
import mwparserfromhell as mwparser

with open('test_wikipedia_page.txt', 'r') as f:
    contents = f.read()

cleaned = wikiset._parse_and_clean_wikicode(contents, mwparser, "en")

print(cleaned)