from gemini_service import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner",
    hours_per_week: int = 5,
    goal: str = "Understand the topic"
) -> str:

    prompt = f"""
You are EduGenie, a personalized learning-path assistant.

Create a structured learning path for:

Topic:
{topic}

Current level:
{level}

Available study time:
{hours_per_week} hours per week

Learning goal:
{goal}

Create a progression from beginner to intermediate
to advanced.

Include:

1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Suggested timeline
5. Practice activities
6. Project ideas
7. Learning resources
8. Videos
9. Articles
10. Books
11. Milestones
12. Revision suggestions

Make the learning path realistic and easy to follow.

Use clear headings.

Do not invent specific URLs unless you are certain
they are valid. Resource types and resource names are
acceptable.

Return only the learning plan.
"""

    return generate_text(
        prompt
    )