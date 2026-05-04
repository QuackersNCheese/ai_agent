import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

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
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools =[available_functions], 
            system_instruction=system_prompt
            ),
        )   
    if response.function_calls:
        function_responses = [] # This will hold our results to send back to the AI later

    for call in response.function_calls:
        # Execute the function
        function_call_result = call_function(call, verbose=args.verbose)
    
        # Validation checks as requested in the assignment
        if not function_call_result.parts:
            raise Exception("Function call returned no parts")
    
        part = function_call_result.parts[0]
        print(f"-> {part.function_response.response}")
        if part.function_response is None:
            raise Exception("Part does not contain a function_response")
            
        if part.function_response.response is None:
            raise Exception("FunctionResponse does not contain a response field")

        # Save the part for the next step of the conversation
        function_responses.append(part)
        
        # display metadata
        if args.verbose:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print(response.text)


if __name__ == "__main__":
    main()
