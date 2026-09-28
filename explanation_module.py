import os


MODEL_ID = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)

USE_LOCAL_MODEL = os.getenv(
    "USE_LOCAL_EXPLANATION_MODEL",
    "true"
).lower() == "true"


_generator = None


def get_local_generator():

    global _generator

    if _generator is not None:
        return _generator

    try:
        from transformers import pipeline

        _generator = pipeline(
            "text2text-generation",
            model=MODEL_ID,
            tokenizer=MODEL_ID
        )

        return _generator

    except Exception as exc:

        raise RuntimeError(
            f"Unable to load local explanation model: {exc}"
        ) from exc


def explain_with_local_model(
    topic: str
) -> str:

    generator = get_local_generator()

    prompt = f"""
Explain the following topic to a beginner to advanced.

Topic:
{topic}

Requirements:

- Use simple language.
- Explain the main idea.
- Give a small example.
- Avoid unnecessary technical terms.
- Make the explanation easy for a student to understand.

Explanation:
"""

    result = generator(
        prompt,
        max_new_tokens=250,
        do_sample=True,
        temperature=0.3
    )

    if not result:
        raise RuntimeError(
            "Local model returned no result."
        )

    return result[0]["generated_text"].strip()


def explain_topic(
    topic: str
) -> str:

    if USE_LOCAL_MODEL:

        try:
            return explain_with_local_model(
                topic
            )

        except Exception:
            pass

    # Fallback to Gemini if the local model
    # cannot be loaded.

    from gemini_service import generate_text

    prompt = f"""
You are EduGenie.

Explain this educational topic in very simple language:

{topic}

Give:

1. Definition
2. Main idea
3. How it works
4. Simple example
5. Short conclusion

Keep the explanation clear and student-friendly.
"""

    return generate_text(
        prompt
    )