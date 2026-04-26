import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
import argparse
from prompts import system_prompt

# load environment variables, grab api key and load into Gemini client object
load_dotenv()   
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API Key not found")
client = genai.Client(api_key=api_key)

# set up parsing object to enable command line input
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

""" Project Title: AI-Agent
Objective: Build an AI Agent that is a coding assistant CLI tool- 'A toy version of Claude Code'
1) Accepts a coding task
2) Chooses from a set of predefined functions to work on the task, for example:
  - Scan the files in a dictionary
  - Read a file's contents
  - Overwrite a file's contents
  - Execute the Python interpreter on a file
3) Repeats step 2 until the task is complete (or it fails miserably, which is possible)
"""
def main():
    print("Hello from ai-agent!")
    # grant the agent memory with a message history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Prompt the model
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0),
            )   
        if response.usage_metadata == None:
            raise RuntimeError("failed genai response")
    except genai.errors.ServerError as e:
        print("Gemini Service is unavailable due to high demand", e)
    
    # display metadata
    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)



if __name__ == "__main__":
    main()
