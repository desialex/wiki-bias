import sys
import spacy
import getopt

languages = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es',
             'et', 'fa', 'fi', 'fr', 'ga', 'he', 'hi', 'hr', 'hu', 'id', 'is',
             'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mr', 'nb', 'nl', 'pl', 'pt',
             'ro', 'ru', 'si', 'sk', 'sl', 'sq', 'sv', 'ta', 'te', 'th', 'tl',
             'tr', 'tt', 'uk', 'ur', 'vi', 'xx', 'zh']


lang = None
opts, args = getopt.getopt(sys.argv[1:], "l:i:o:", ["ifile=", "ofile=", "lang="])

for opt, arg in opts:
    if opt in ("-l", "--lang"):
        # two-letter ISO code for the language
        lang = arg

exceptions = dict()
exceptions['bg'] = ['г.', 'т.', 'нар.', 'т.нар.', 'стр.', 'гр.', 'Св.',
                    'НУМТКН.', 'инж.', 'млн.', 'лв.', 'проф.', 'бул.', 'ул.',
                    'пл.', 'вр.', 'обл.', 'т.ч.', 'др.', 'сп.', 'виж.',
                    'т.е.', 'дн.', 'в.', 'чл.', 'тур.', 'напр.', 'мин.', 'яз.',
                    'ез.', 'с.', 'р.', 'пр.н.е.', 'ген.']

if lang in languages:
    nlp = spacy.blank(lang.lower())
else:
    raise Exception("Language not supported by spaCy 2.1.3")

nlp.max_length = 2000000
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)


def sbd(string):
    """
    Takes a string and returns a list of sentences
    longer than 5 tokens.
    string: param
    """
    doc = nlp(string)
    doc.is_parsed = True
    return [str(sent) for sent in list(doc.sents) if 5 < len(sent) < 300]
