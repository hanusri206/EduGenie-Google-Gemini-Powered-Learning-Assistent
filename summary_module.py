from gemini_service import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational content.

CONTENT:
{text}

Requirements:

1. Keep the important information.
2. Remove unnecessary repetition.
3. Use simple language.
4. Preserve important facts and concepts.
5. Make it useful for quick revision.
6. Use short paragraphs or bullet points when appropriate.

Return only the summary.
"""

    return generate_text(
        prompt
    )