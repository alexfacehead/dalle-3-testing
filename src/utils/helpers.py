import argparse
import os
from typing import Optional
from src.utils.constants import STATIC_CODE, SYSTEM_MESSAGE_MASTER, USER_MESSAGE_ONE, ASSISTANT_MESSAGE_ONE, USER_MESSAGE_TWO, AI_FILE_IMPORTS, DEFAULT_PLACEHOLDER_PROMPT, SYSTEM_MESSAGE_GPT_3_5, USER_FEEDBACK_SMALL
from termcolor import colored
from dotenv import load_dotenv
from src.completions.completion_generator import ChatCompletionGenerator

loaded_dot_env = load_dotenv()

def update_message_with_new_prompt(input_prompt, replacement: Optional[str] = None) -> str:
    file_path = os.path.join(os.getcwd(), "src/resources/prompt_keys/v1_bengal_cat_base.txt")
    
    with open(file_path, "r") as file:
        new_prompt = file.read().strip()
    if replacement != None:
        new_prompt = replacement
    updated_message = input_prompt.format(new_prompt)
    return updated_message

def analyze_prompt(prompt: Optional[str], model: Optional[str] = "gpt-3.5-turbo-16k") -> str:
    print("Enter analyze prompt")
    print (f"analyze_prompt is using model {model}")
    if prompt != DEFAULT_PLACEHOLDER_PROMPT:
        print(colored("Entering AI-altered metric block, analyze_prompt", 'magenta'))
        # Initialize the API completion objects
        completion_generator = ChatCompletionGenerator()
        completion_generator_small = ChatCompletionGenerator(model="gpt-3.5-turbo-16k-0613")
        
        # Setup base STATIC_CODE in the event of failure
        resultant_code = STATIC_CODE

        # Design prompts and querying to ChatCompletionGenerators
        user_message_updated = update_message_with_new_prompt(USER_MESSAGE_TWO)
        list_msgs_gen_code_large = [{"role": "system", "content": SYSTEM_MESSAGE_MASTER}, 
                                          {"role": "user", "content": USER_MESSAGE_ONE}, 
                                          {"role": "assistant", "content": ASSISTANT_MESSAGE_ONE}, 
                                          {"role": "user", "content": user_message_updated}]
        
        # Generate first big completion (ETA is 1-2 minutes if using gpt-4)
        resultant_feedback = completion_generator.generate_completion(messages=list_msgs_gen_code_large, model="gpt-3.5-turbo-16k-0613", temperature=0.1)

        # Design gpt-3.5-turbo-16k-0613 cheaper prompt to extract code
        user_content_code_small = USER_FEEDBACK_SMALL + "\"\"\"" + resultant_feedback + "\"\"\""
        list_msgs_extract_code_small = [{"role": "system", "content": SYSTEM_MESSAGE_GPT_3_5}, 
                                  {"role": "user", "content": user_content_code_small}]
        
        # Final, pure, AI-updated resultant code generated
        resultant_code = completion_generator_small.generate_completion(messages=list_msgs_extract_code_small, model="gpt-3.5-turbo-16k-0613", temperature=0.1)
        
        res = (f"prompt used for analysis: " + prompt)
        print(colored(res, 'green'))
        print(colored("Evaluation function has been updated, located in `ai_adjusted_eval_metric.py`", 'green'))
    else:
        print(colored("No base prompt for metric enhancement."), 'red')
        return ""
    return resultant_code