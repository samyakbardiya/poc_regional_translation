from fastapi.params import Body
from fastapi.routing import APIRouter
from loguru import logger

import toi_translation.models.gemini as gemini
from toi_translation.models.language import Language

router = APIRouter(tags=["Translation"])


@router.post("/generate_content")
async def translate_via_generate_content(
    text: str = Body(embed=True),
    from_language=Language.ENGLISH,
    to_language=Language.HINDI,
):
    logger.debug(f"Text: {text}")

    prompt = gemini.translate_prompt(text, from_language, to_language)
    response = gemini.model.generate_content(prompt)
    logger.debug(f"Response: {response}")

    return gemini.to_markdown(response.text)


@router.post("/chat")
async def translate_via_chat(
    text: str = Body(embed=True),
    from_language=Language.ENGLISH,
    to_language=Language.HINDI,
):
    logger.debug(f"Text: {text}")

    chat = gemini.model.start_chat(history=[])

    paragraphs = text.split("\n\n")
    for paragraph in paragraphs:
        prompt = gemini.translate_chat_prompt(paragraph, from_language, to_language)
        response = chat.send_message(prompt)
        logger.debug(f"Text: {paragraph}")
        logger.debug(f"Response: {response.text}")

    logger.debug(f"Chat: {chat}")
    logger.debug(f"Chat history: {chat.history}")

    for message in chat.history:
        logger.debug(f"**{message.role}**: {message.parts[0].text}")

    translated_text = "\n\n".join(
        [message.parts[0].text for message in chat.history if message.role == "model"]
    )
    return gemini.to_markdown(translated_text)
