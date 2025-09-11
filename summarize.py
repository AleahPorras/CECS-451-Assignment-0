import sys
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

    """Extracts HTML content from the URL to extract the main text."""
    
    try:
        # sends an http request to the website, header allows for compatibility with Mozilla, timeout prevents request to run longer in the case of an error.
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout = 10)
        response.raise_for_status() #checks the HTTPS status code of the request
    
    except Exception:
        # exits the entire program in an error occurs
        sys.exit(f"An error has occured, try again with a different link.")
    
    # structures the raw html into a structured tree representation
    soup = BeautifulSoup(response.text, "html.parser")

    # filters out all text in paragraph attributes
    results = [p.get_text() for p in soup.find_all("p")]
    
    # returns error if no usable text is found
    if not results:
        sys.exit("No text content found at the URL. Try again.")
    
    return results

# tests if article text is working correctly
# print(get_text(args.url))

###------------------------------------------------------###
### Actual Summarizer
# Status: DONE
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
        "If the given URL is invalid, stop the program and print out the error code."
    )
    
    # generates gemini response
    response = client.models.generate_content(
        model = "gemini-1.5-flash",
        config = types.GenerateContentConfig(
            temperature= 0.1,
            top_p = 0.8,
            top_k = 50,
            max_output_tokens = 512
        ),
        # actual prompt for the summarizer
        contents = f"{SYSTEM}\n\n[Input]\n{url_text}\n\n[Task]\n{TASK}"
    )

    # removes whitespace
    results = response.text.strip()

    # removes JSON wrapping
    proper_json = results.strip("```json").strip("```")

    data = json.loads(proper_json)
    json_output = json.dumps(data, indent=4)

    #writes JSON output into a file
    with open("output.json", "w") as f:
        f.write(json_output)

    # prettified output for terminal
    print(f"\nFrom URL: {data.get('url')}\n")
    print(f"Summary:\n {data.get('summary')}\n")
    print(f"Keywords: {data.get('keywords')}\n")
    print(f"References: {data.get('references')}\n")

summarize_text(args.url)
