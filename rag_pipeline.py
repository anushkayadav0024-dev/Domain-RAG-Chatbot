import os
import time

from dotenv import load_dotenv
from google import genai

from prompt import create_prompt


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(
        chunk.page_content
        for chunk in retrieved_chunks
    )

    prompt = create_prompt(context, question)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config={"tools": []}
            )

            answer = response.text.strip()

            return answer

        except Exception as e:
            error_message = str(e)

            is_server_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "high demand" in error_message.lower()
            )

            if is_server_error:
                if attempt < 2:
                    time.sleep(3)
                    continue

                return (
                    "⚠️ Gemini is temporarily unavailable "
                    "because the model is experiencing high demand. "
                    "Please try your question again in a few seconds."
                )

            return (
                "⚠️ An error occurred while generating the answer. "
                "Please try again."
            )
