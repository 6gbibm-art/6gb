from config import client, MODEL_NAME
def generate(prompt: str) -> str:
    """
    Generates a complete response from Gemini.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text
