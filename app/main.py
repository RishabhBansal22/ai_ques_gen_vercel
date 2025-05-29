from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .generator import generate_response, generate_answers
from fastapi.responses import FileResponse
import tempfile
import os


app = FastAPI()

# Allow frontend to access backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-ques-gen-vercel.vercel.app"],  # Updated to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/solutions")
async def generate_solutions(request: Request):
    data = await request.json()
    questions = data.get("questions")
    if not questions:
        return JSONResponse({"error": "Questions are required"}, status_code=400)
    try:
        answers = generate_answers(questions)
        # Write answers to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as tmp:
            tmp.write(answers)
            tmp_path = tmp.name
        filename = "solutions.txt"
        # Just return the file, don't try to clean up (for compatibility)
        return FileResponse(tmp_path, media_type="text/plain", filename=filename)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)



@app.post("/api/generate")
async def generate_questions(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return JSONResponse({"error": "Prompt is required"}, status_code=400)
    try:
        questions = generate_response(prompt)
        return {"questions": questions}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)