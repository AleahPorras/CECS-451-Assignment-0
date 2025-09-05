from google import genai
from google.genai import types
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# loads the API key from a different environment
client = genai.Client(api_key = load_dotenv("GEMINI_API_KEY"))

# # with GenerateContentConfig, you can guide the behavior of Gemini models
# response = client.models.generate_content(
#     model = "gemini-1.5-flash",
#     config = types.GenerateContentConfig(
#         system_instruction = 'You are a professional summarization assistant. Always output only valid JSON, no code block or extra explanation. JSON schema: {"Summary": "...", "keywords": ["...","...","...","...","..."], "source": "URL or N/A"}',
#         # GenerateContentConfig also lets you override default generation parameters
#         temperature= 0.2,
#         top_p = 0.8,
#         top_k = 60,
#         max_output_tokens = 512),
#     contents = "Hello there!",
# )

def summarize_prompt(article_text: str, source_url: str) -> str:
    """Builds the system prompt for article summarization."""
    SYSTEM = (
        'You are a professional summarization assistant. Always output only valid JSON, no code block or extra explanation. JSON schema: {"Summary": "...", "keywords": ["...","...","...","...","..."], "source": "URL or N/A"}'
    )
    TASK = (
        "Summarize the input into 3 sentences." 
        "Extract exactly 5 key terms (nouns or important concepts, no duplicates)."
        f'Put the provided source URL"{source_url if source_url else "N/A"}" into the "source" field.'
        "The output language should match the input language."
    )
    prompt = f"{SYSTEM}\n\n[Input]\n{article_text}\n\n[Task]\n{TASK}"
    return prompt
# print(response.text)
