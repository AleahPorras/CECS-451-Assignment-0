import argparse
import requests
import json
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

def get_text(url):

    """Extracts HTML content from teh URL to extract the main text."""
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout = 10)
        response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        return RuntimeError(f"Network error, try again with a different link: {e}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    results = [p.get_text() for p in soup.find_all("p")]
    
    if not results:
        print("No text content found at the URL. Try again.")
        return
    
    return results

# tests if article text is working correctly
# print(get_text(args.url))

###------------------------------------------------------###
### Actual Summarizer
# Status: Not Started

def summarize_text(url):     

    url_text = get_text(url)

    ### Class Example
    SYSTEM = (
        "You are a professional summarization assistant."
        "Do not invent facts that are not present in the source."
        "Always output only pure JSON, no code block or extra explanation."
    )
    TASK = (
        "Produce a summary of the given URL in 3 sentences."
        "Include at least 5 core keywords/phrases from the source (no duplicates)."
        f'Put the provided source URL "{url if url else "N/A"} "into the "url" field.'
        f'Put the provided source URL "{url if url else "N/A"} "into the "references" field.'
        "All this information should be given in true JSON format, url, summary, keywords, and references."

        # """
        # Expected Terminal Output:
        
        # From URL: {url}

        # Summary: 
        # ...(3 sentence paragraph here)...

        # Keywords:...

        # References: {url}
        # """
    )
    try:
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

        results = response.text.strip()

        proper_json = results.strip("```json").strip("```")

        data = json.loads(proper_json)
        json_output = json.dumps(data, indent=4)
        with open("output.json", "w") as f:
            f.write(json_output)

        print(f"\nFrom URL: {data.get('url')}\n")
        print(f"Summary:\n {data.get('summary')}\n")
        print(f"Keywords: {data.get('keywords')}\n")
        print(f"References: {data.get('references')}\n")

    except Exception as e:
        print(f"An error has occured during the summarization of the article, please try again: {e}")
        return

summarize_text(args.url)
