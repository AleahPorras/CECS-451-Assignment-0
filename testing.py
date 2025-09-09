import argparse
import requests
from google import genai 
from google.genai import types
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

###------------------------------------------------------###
### Implementing AI
## Status: DONE

client = genai.Client(api_key = load_dotenv("GEMINI_API_KEY"))

###------------------------------------------------------###
### Obtaining HTML from URL
## Status: DONE

# code for an extra argument on the command line

parser = argparse.ArgumentParser()
parser.add_argument('--url', type = str, required = True)
args = parser.parse_args()

# # tests if additional argument works
# if args.url:
#     print("Displaying URL as: % s" % args.url)

###------------------------------------------------------###

def get_text(url:str) -> str:

    """Extracts HTML content from teh URL to extract the main text."""

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        results = [p.get_text(strip=True) for p in soup.find_all("p")]
        
        return "\n".join(results)
    else:
        return f"Failed to retrieve data: {response.status_code}"

# tests if article text is working correctly
# print(get_text(args.url))

###------------------------------------------------------###
### Actual Summarizer
# Status: Not Started

def summarize_text(url:str) -> str:     

    url_text = get_text(url)

    ### No JSON
    # prompt = f"""
    # You are a professional summarization assistant. 

    # Your task is to:
    # - produce a summary of the given URL in 3 sentences.
    # - include at least 5 core keywords/phrases from the source (no duplicates).
    # - put the provided source URL "{url if url else "N/A"} into the References field.
    # - do not create facts that are not present in the orignal source.
    # - the output language should match the input language.
    
    # Output Format:
    
    # From URL: {url}

    # Summary:
    # ...(your 3 sentence paragraph here)...

    # Keywords:...
    # References: {url}
    # """

    ### With JSON
    # prompt = f"""
    # You are a professional summarization assistant. 
    # Always output only valid JSON, no code block or extra explanation.

    # Your task is to:
    # - produce a summary of the given URL in 3 sentences.
    # - include at least 5 core keywords/phrases from the source (no duplicates).
    # - put the provided source URL "{url if url else "N/A"} into the References field.
    # - do not create facts that are not present in the orignal source.
    # - the output language should match the input language.
    
    # Output Format:
    
    # From URL: {url}

    # Summary:
    # ...(your 3 sentence paragraph here)...

    # Keywords:...
    # References: {url}
    # """

    ### Class Example
    SYSTEM = (
        'You are a professional summarization assistant.'
        'Always output only valid JSON, no code block or extra explanation.'
        'JSON schema: {"summary": "...", "keywords": ["...","...","...","...","..."], "source": "URL or N/A"}'
    )
    TASK = (
        "Produce a summary of the given URL in 3 sentences."
        "Include at least 5 core keywords/phrases from the source (no duplicates)."
        f'Put the provided source URL "{url if url else "N/A"} "into the "source" field.'
        "The output language should match the input language."
    )

    response = client.models.generate_content(
        model = "gemini-1.5-flash",
        config = types.GenerateContentConfig(
            temperature= 0.1,
            top_p = 0.8,
            top_k = 50,
            max_output_tokens = 512
        ),
        contents = f"{SYSTEM}\n\n[Input]\n{url_text}\n\n[Task]\n{TASK}"
    )
    return response.text

print(summarize_text(args.url))
