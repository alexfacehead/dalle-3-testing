import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import argparse
from src.utils.constants_for_prompt_enhancement import *
from src.completions.completion_generator import ChatCompletionGenerator
from src.utils.helpers import update_message_with_new_prompt
from dotenv import load_dotenv
from termcolor import colored

def main(prompt: str) -> str:
    imported_env = load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    generator = ChatCompletionGenerator(temperature=0.1, openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k-0613")

    user_defined_input = update_message_with_new_prompt(USER_INPUT_FOR_ENHANCEMENT, prompt)

    prompt_optimizer_list_and_dict = [{"role": "system", "content": SYSTEM_MESSAGE_OPTIMIZER},
                                      {"role": "user", "content": STATIC_USER_QUESTION_INPUT},
                                      {"role": "assistant", "content": LLM_RESPONSE_FOR_CONTEXT},
                                      {"role": "user", "content": user_defined_input}]
    optimized_prompt = generator.generate_completion(prompt_optimizer_list_and_dict)
    print(colored("Optimized prompt:\n\n", 'magenta'))
    print(colored(optimized_prompt, 'green'))
    return optimized_prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a vastly improved prompt using your basal prompt as input.")
    parser.add_argument("--prompt", type=str, help="The user-defined prompt for completion generation. This is the pre-optimized version.")
    
    args = parser.parse_args()
    
    main(args.prompt)
