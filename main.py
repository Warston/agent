import sys
from prompts import system_prompt
import argparse
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types
from functions.call_function import *



def main():
    parser = argparse.ArgumentParser(description="Gemini Bot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API Key not found!")

    print("Hello from agent!")

    messages: list [types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    function_results = []
    for _ in range(20):
        client = genai.Client(api_key=api_key)
        message = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        if message.candidates != None:
            for candidate in message.candidates:
                messages.append(candidate.content)
        if message.usage_metadata == None:
            raise RuntimeError("Metadata empty!")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {message.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {message.usage_metadata.candidates_token_count}")
        print(f"{message.text}")
        if message.function_calls != None:
            for fun_call in message.function_calls:
                print(f"Calling function: {fun_call.name}({fun_call.args})")
                function_call_result = call_function(fun_call, fun_call.args)
                if len(function_call_result.parts) == 0:
                    raise Exception ("Parts List Empty")
                if function_call_result.parts[0].function_response == None:
                    raise Exception ("Parts first response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception ("Response field is None")

                function_results.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=function_results))
        else:
            print(message.text)
            print("Got to return")
            return


        if args.verbose == True:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    print("Max Loop reached non final response generated")
    sys.exit(1)




if __name__ == "__main__":
    main()
