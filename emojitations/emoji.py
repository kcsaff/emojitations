from emojitations.emojitypes import Emoji
from emojitations.data.en import emoji
import emojitations.data
import sys
import pkgutil

langs = [name.split('.')[-1] for _, name, _ in pkgutil.iter_modules(emojitations.data.__path__, emojitations.data.__name__+'.')]

module_overwrite = Emoji(emoji, langs=langs, module=sys.modules[__name__])
module_overwrite.annotation._freeze()

sys.modules[__name__] = module_overwrite
