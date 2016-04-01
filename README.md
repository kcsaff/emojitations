Emojitations
============

A library for using Unicode emoji annotations.  Emoji annotations can provide your scripts with a simple way to
interpret emoji, or select a random one satisfying certain criteria.  Annotations can be seen listed here on
the Unicode website: http://unicode.org/emoji/charts/full-emoji-list.html

Requirements
------------

1. Python 3.+

This library is pure python 3 and has no other requirements.

Installation
------------

`python3 setup.py install`

Usage
-----

Emoji are available under their names at `emoji.whatever`.  These objects include an `annotations` set and you can
use the `emoji` attribute or `str()` to get their emoji strings.  To get all emoji in an annotation, use
`emoji.annotation.whatever`.  This returns frozen sets which then can be combined using set operations.

The library also provides (preliminary) support for foreign languages, available as `emoji.de.kreditkarte` for example.

See the examples below for details.

```python

>>> from emojitations import emoji
>>> emoji.grinning_face.annotations
frozenset({'grin', 'face'})
>>> print(''.join(str(grin) for grin in emoji.annotation.grin))
😸😁😀
>>> print(''.join(str(grin) for grin in emoji.annotation.grin & emoji.annotation.cat))
😸
>>> print(str(emoji.de.kreditkarte))
💳

```
