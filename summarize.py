from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key = load_dotenv("GEMINI_API_KEY"))

# with GenerateContentConfig, you can guide the behavior of Gemini models
response = client.models.generate_content(
    model = "gemini-1.5-flash",
    config = types.GenerateContentConfig(
        system_instruction = "You are a cat. You name is Neko.",
        # GenerateContentConfig also lets you override default generation parameters
        temperature= 0.2,
        top_p = 0.8,
        top_k = 60,
        max_output_tokens = 512),
    contents = "Hello there!",
)
print(response.text)
