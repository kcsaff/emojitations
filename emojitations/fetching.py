import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from emojitations.emojitypes import EmojiAnnotations, slug
import os.path


LANG_URL = 'http://unicode.org/repos/cldr/tags/latest/common/annotations/{}.xml'
DIR_URL = 'http://unicode.org/repos/cldr/tags/latest/common/annotations/'


DIRECTORY_PATTERN = re.compile(r'\>((\w+)\.xml)\<\/a')


def fetch_emojitations_xml(url=LANG_URL.format('en'), lang=None):
    if lang:
        url = LANG_URL.format(lang)
    with urllib.request.urlopen(url) as response:
        return response.read()


def fetch_emojitations_directory(url=DIR_URL):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        if isinstance(html, bytes):
            html = html.decode()
    for match in DIRECTORY_PATTERN.finditer(html):
        lang = match.group(2)
        lang_url = urllib.parse.urljoin(url, match.group(1))
        yield (lang, lang_url)


def parse_emojitations_xml(data):
    root = ET.fromstring(data)
    for annotation_element in root.findall('.//annotation'):
        name = annotation_element.get('tts')
        if name:
            emoji = annotation_element.get('cp').strip('[]')
            codepoints = tuple(ord(c) for c in emoji)
            annotations = frozenset(
                annotation.strip() for annotation in annotation_element.text.split(';')
            ) if annotation_element.text else frozenset()
            yield EmojiAnnotations(emoji, codepoints, name, slug(name), annotations)


def write_emojitations_py(filename, emoji_annotations):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('from emojitations.emojitypes import EmojiAnnotations\n')
        f.write('emoji = [\n  ')
        for i, emoji_annotation in enumerate(emoji_annotations):
            if i > 0:
                f.write('\n  ')
            f.write(repr(emoji_annotation))
            f.write(',')
        f.write(']')


if __name__ == '__main__':
    # Fetch all current emoji annotations and SAVE to the data directory.
    for lang, lang_url in fetch_emojitations_directory():
        print((lang, lang_url))
        filename = os.path.join(os.path.dirname(__file__), 'data', '{}.py'.format(lang))
        emojis = parse_emojitations_xml(fetch_emojitations_xml(lang_url))
        write_emojitations_py(filename, emojis)
