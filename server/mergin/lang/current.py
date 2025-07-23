from decouple import config
from .languages import PL
from .languages import EN

TRANSLATION_LANG = config("TRANSLATION_LANG")

EN = EN.EN
PL = PL.PL

def returnTranslation(key):
    if(TRANSLATION_LANG == "PL"):
        return PL[key]
    elif(TRANSLATION_LANG == "EN"):
        return EN[key]


