from typing import Generator
from config import client, MODEL_NAME
# def generate(prompt: str) -> str:
#     """
#     Generates a complete response from Gemini.
#     """
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt
#     )
#     return response.text

def generate_stream(prompt: str) -> Generator[str, None, None]:
    response = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt
    )
    for chunk in response:
        if hasattr(chunk, "text") and chunk.text:
            yield chunk.text