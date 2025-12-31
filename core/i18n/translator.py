import gettext
from fastapi import Header, Query
from pathlib import Path


SUPPORTED_LANGUAGES = {"fa": "fa_IR", "en": "en_US"}


BASE_DIR = Path(__file__).parent


def get_locale_lang(
    lang_header: str | None = Header(
        None, alias="lang", description="enter your language.example: fa"
    ),
    lang_query: str | None = Query(
        None, description="enter your language.example: fa"
    ),
):
    lang = lang_query or lang_header
    if not lang:
        return "en_US"
    lang = lang.split(",")[0].split("-")[0]
    return SUPPORTED_LANGUAGES.get(lang, "en_US")


def get_translator(locale: str):
    try:
        translator = gettext.translation(
            domain="messages",
            localedir=str(BASE_DIR / "locales"),
            languages=[locale],
        )
        translator.install()
        return translator.gettext
    except FileNotFoundError:
        return lambda s: s
