from collections import namedtuple
from importlib import import_module


SLUG_REPLACEMENTS = {
    '-': '_',
    ' ': '_',
    '!': '',
}


def slug(name):
    for char, replacement in SLUG_REPLACEMENTS.items():
        if char in name:
            name = name.replace(char, replacement)
    if not name.islower():
        name = name.lower()
    return name


class EmojiAnnotations(namedtuple('EmojiAnnotations', ['emoji', 'codepoints', 'name', 'slug', 'annotations'])):
    __slots__ = ()
    def __str__(self):
        return self.emoji


class Annotations(object):
    def __init__(self, module=None):
        self.__module = module

    def _add_emoji(self, emoji):
        for annotation in emoji.annotations:
            annotation_set = self.__dict__.get(annotation, None)
            if not annotation_set:
                annotation_set = set()
                self.__dict__[annotation] = annotation_set
            annotation_set.add(emoji)

    def _freeze(self):
        for key, value in list(self.__dict__.items()):
            if isinstance(value, set):
                self.__dict__[key] = frozenset(value)


class Emoji(object):
    def __init__(self, emojis=(), langs=(), module=None):
        self.__module = module
        self.__by_emoji = dict()
        self.__langs = {lang: None for lang in langs}
        self.annotation = Annotations()
        for emoji in emojis:
            self._add_emoji(emoji)

    def __getattr__(self, item):
        if item in self.__langs:
            loaded_lang = self.__langs[item]
            if not loaded_lang:
                loaded_lang = self._load_lang(item)
            return loaded_lang

        return self._get_desperate(item, AttributeError)

    def __getitem__(self, item):
        result = self.__dict__.get(item, None)
        if result is not None:
            return result
        else:
            return self._get_desperate(item, KeyError)

    def get(self, item, default=None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def _get_desperate(self, item, error_class):
        slugged_item = slug(item)
        if slugged_item != item:
            emoji = self.__dict__.get(slugged_item)
            if emoji:
                return emoji
            else:
                raise error_class('No known emoji named `{}` or `{}`'.format(item, slugged_item))
        else:
            emoji = self.__by_emoji.get(item)
            if emoji:
                return emoji
            else:
                raise error_class('No known emoji named `{}`'.format(item))

    def _add_emoji(self, emoji):
        self.__dict__[emoji.slug] = emoji
        self.__by_emoji[emoji.emoji] = emoji
        self.annotation._add_emoji(emoji)

    def _load_lang(self, lang):
        data = import_module('emojitations.data.{}'.format(lang))
        emoji = Emoji(data.emoji)
        self.__langs[lang] = emoji
        return emoji

