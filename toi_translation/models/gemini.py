# import pathlib
# import textwrap

import google.generativeai as genai
from IPython.display import Markdown

from toi_translation.models.language import Language
from toi_translation.settings import setting_cfg, setting_env


def to_markdown(text):
    # text = text.replace("•", "  *")
    # return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))
    return Markdown(text)


genai.configure(api_key=setting_env.GOOGLE_API_KEY)

model = genai.GenerativeModel(setting_cfg.GEMINI_MODEL)


def translate_prompt(text: str, from_language: Language, to_language: Language) -> str:
    return f"Translate the following {from_language} text to {to_language}:\n\n{text}"


def translate_chat_prompt(
    text: str, from_language: Language, to_language: Language
) -> str:
    return (
        f"Translate the following {from_language} text to {to_language} while "
        f"pertaining the previous context:\n\n{text}"
    )
