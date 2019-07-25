import sys
import re
import regex

lng = sys.argv[1]


def clean_wiki(text):
    text = re.sub(r"''+", '', text)  # wiki bold and double quotes
    text = re.sub(r'==+.+?==+', '', text)  # wiki titles
    text = re.sub(r'<ref[^<]*<\/ref>', '', text)  # remove references <ref...> ... </ref>
    text = re.sub(r'<!--[\s\S\n]*?-->', '', text)  # html comments
    text = re.sub(r'<([A-Z][A-Z0-9]*)\b[^>]*>(.*?)</\1>', '', text)  # <tag>...</tag>
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'<[^>|<]*/>', '', text)  # self-closing html tags
    text = re.sub(r'\[http:[^] ]*', '[', text)  # remove normal url, preserve visible text
    text = re.sub(r'\[\[[^\|\]]*\|', '[[', text)  # remove wiki url, preserve visible text
    text = re.sub(r'\[\[[^\]]*:[^\]|\|]*\]\]', '', text)  # remove links to other languages & categories
    text = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)  # remove bare URLs
    text = regex.sub(r'\{\{((?>[^{}]+|(?R))*)\}\}', '', text)  # remove embedded {{icons and comments}} recursively
    text = re.sub(r'\{[^\}]*\}', '', text)  # remove {tables}
    text = re.sub(r'\[[^\[]*\|[^\]]*', '', text)  # remove [image|titles|& other tags]
    text = re.sub(r'\}|\{', '', text)  # trailing {}
    text = re.sub(r'\]|\[', '', text)  # trailing []
    text = re.sub(r'<[^>]*>', '', text)  # trailing HTML tags
    text = re.sub(r'&.{4,6};', '', text)  # HTML unicode characters
    text = re.sub(r'\s\*', '.', text)  # end list items with . and remove bullet points
    text = re.sub(r'\d+((,|\.)*\d+)*', 'NUMTKN ', text)  # replace numbers by a token
    text = re.sub(r'[. ]{3,}', '. ', text)  # clean multiple .
    text = re.sub(r'\s{2,}', ' ', text)  # clean multiple spaces
    return text


def clean_punct(text):
    if lng.lower() == "fr":
        text = re.sub(r"[.,\/#!?†‡•$%‰\^&\*;:{}|=–\-_—‗‾⁄`~′″‴‵‶‷()‚‛“”„‟‹›№«»]", ' ', text) # keep U+0027, U+2018 and U+2019 (=apostrophies)
    else:
        text = re.sub(r"[.,\/#!?†‡•$%‰\^&\*;:{}|=–\-_—‗‾⁄`~′″‴‵‶‷()‘’‚‛“”„‟‹›'№]", ' ', text)  # remove punctuation and symbols
    text = re.sub(r'"', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)  # clean multiple spaces
    return text.strip()


def clean_tag(tag):
    tag = re.sub(r"[{}]", '', tag)
    tag = re.sub(r"\|.*", '', tag)
    return tag.lower()
