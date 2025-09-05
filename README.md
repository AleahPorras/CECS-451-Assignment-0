# Assignment 0: Text Summarizer
### General Instruction
- Submit uncompressed file(s) in the Dropbox folder via Canvas (Not email).
- Use Python 3, any other programming language is not acceptable.
- You can import modules in the following list (please check the full list Announcements
- List of allowed libraries for the assignments.). If you want to use any other library, please consult with the instructor.<br>

<br>
(30 points) Implement an one-paragraph summarizer using Google Gemini 1.5 Flash
(Python).<br>

i. Prepare summarize.py. You will also include a requirements.txt.<br>

ii. Set up environment and get API Key.<br>

iii. Input format. The program must accept command-line arguments (interactive
I/O is not acceptable):<br>
--url URL # a link to summarize<br>

iv. Content extraction. For a URL, fetch HTML and extract the main text (e.g.,
trafilatura with a BeautifulSoup fallback). Respect site policies and handle
errors (timeouts, 404s) with retries.<br>

v. Gemini call. Use gemini-1.5-flash through the Python SDK to produce:
- a single-paragraph summary of 3 sentences,
- at least 5 core keywords/phrases from the source,
- a References line that preserves the original URL.<br>

Use low randomness for determinism (e.g., temperature=0.2, top p=0.9, top k=40,
max output tokens=512). The model must not invent facts not present in the
source.<br>

vi. Design your own prompt template.<br>
vii. Output format. Follow the example below.<br>

python summarize.py --url https://...<br>

From URL: https://...<br>
Summary:<br>
... (your 3 sentence paragraph stays here) ...<br>

Keywords: ...<br>
References: https://...<br>

viii. Program requirements.<br>
- Parse arguments; support a single URL.
- Produce JSON output.
- Handle network/parse errors gracefully.
- Keep summaries factual, concise, and single-paragraph.<br>

ix. Submit the summarize.py, requirements.txt, and test outputs.