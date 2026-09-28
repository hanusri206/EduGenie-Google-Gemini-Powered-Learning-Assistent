from typing import List

from pydantic import BaseModel, Field

from gemini_service import (
    generate_json,
    clean_json_block
)


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


QUIZ_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "questions": {
            "type": "ARRAY",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "OBJECT",
                "properties": {
                    "question": {
                        "type": "STRING"
                    },
                    "options": {
                        "type": "ARRAY",
                        "minItems": 4,
                        "maxItems": 4,
                        "items": {
                            "type": "STRING"
                        }
                    },
                    "correct_answer": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "question",
                    "options",
                    "correct_answer"
                ]
            }
        }
    },
    "required": [
        "questions"
    ]
}


def generate_quiz(
    passage: str
) -> dict:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions from the
following topic or passage.

PASSAGE:
{passage}

Rules:

1. Generate exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option should be correct.
4. The questions must be relevant to the passage.
5. Distractors should be plausible.
6. The correct_answer must exactly match one of the options.
7. Return valid JSON.
8. Do not add explanations outside the JSON.

Required JSON structure:

{{
  "questions": [
    {{
      "question": "Question",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "Option A"
    }}
  ]
}}
"""

    result = generate_json(
        prompt,
        QUIZ_SCHEMA
    )

    # Keep the cleaning function available as required
    # by the documented quiz workflow.
    if isinstance(result, str):
        result = clean_json_block(result)

    quiz = QuizResponse.model_validate(
        result
    )

    for item in quiz.questions:

        if item.correct_answer not in item.options:

            raise ValueError(
                "Quiz generation error: "
                "correct answer is not present "
                "in the options."
            )

    return quiz.model_dump()