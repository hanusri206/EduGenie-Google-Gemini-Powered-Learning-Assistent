from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="AI-powered educational assistant",
    version="1.0.0"
)


# --------------------------------------------------
# Static files and templates
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: str = Field(
        default="Beginner",
        max_length=50
    )

    hours_per_week: int = Field(
        default=5,
        ge=1,
        le=80
    )

    goal: str = Field(
        default="Understand the topic",
        max_length=500
    )


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# --------------------------------------------------
# Q&A API
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    answer = answer_question(
        payload.text
    )

    return {
        "answer": answer
    }


# --------------------------------------------------
# Explanation API
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    explanation = explain_topic(
        payload.text
    )

    return {
        "explanation": explanation
    }


# --------------------------------------------------
# Quiz API
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    quiz = generate_quiz(
        payload.text
    )

    return {
        "quiz": quiz
    }


# --------------------------------------------------
# Summary API
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# --------------------------------------------------
# Learning Path API
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_path(
    payload: LearningPathRequest
):

    recommendations = get_learning_recommendations(
        topic=payload.topic,
        level=payload.level,
        hours_per_week=payload.hours_per_week,
        goal=payload.goal
    )

    return {
        "recommendations": recommendations
    }