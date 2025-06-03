import os

from openai import OpenAI
# import openai
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# remember the model choices between completions and chat/completions
# /v1/chat/completions: gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
# /v1/completions:    text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
# remember about the different endpoints!!!

def classify_hs(message:str, protected_characteristics_str:str, HS_definition:str, examples:str, chain_ot:str, verbose=False, 
                community_context="", languages = "", geography = "", safeguarding_focus = "", model="gpt-3.5-turbo"):
    
    # are examples provided?
    if examples==[]:
       examples_section = ""
    else:
       examples_section = f"""
    EXAMPLES:
    Consider the following examples:{examples}"""
    
    # is chain of thoughts provided?
    if chain_ot==[]:
       chain_ot_section = ""
    else:
       chain_ot_section = f"""
    CHAIN-OF-THOUGHT:
    Consider the following chain-of-thought:{chain_ot}"""
    
    # context section - if at least one is nonempty
    if any((community_context, languages, geography, safeguarding_focus)):
       context_section = f"""ORGANIZATION CONTEXT:
    {community_context}
    
    Safeguarding Focus: {safeguarding_focus}

    Protected Characteristics: {protected_characteristics_str}

    GEOGRAPHIC CONTEXT:
    This organization operates in {geography}. Be mindful of **regional interpretations of hate speech** in these locations.

    - If certain terms or expressions are **legally restricted** in these regions, classify them more strictly.  
    - If cultural nuances affect interpretation, adapt accordingly.  
    - Consider regional dialects and multi-language factors ({languages})."""
       
    else:
       context_section = ""

    prompt = f"""
    DEFINITIONS:
    Consider the following definition: {HS_definition}

    INSTRUCTION: 
    Using the provided definition of "hate speech",  classify the chat fragment delimited by triple backticks as either "hate speech" with respect to one or more of "protected characteristics" or not "hate speech".

    {context_section}    

    OUTPUT:
    The output should only contain 3 elements: 
    1) "hate speech" or "not hate speech", 
    2) list of "protected characteristic" labels from the list {protected_characteristics_str}, 
    3) list of probabilities with two decimal points, one for each protected characteristic.

    OUTPUT FORMAT:
    ['hate speech', ['sexual orientation'], [0.98]]

    {examples_section}
    {chain_ot_section}
    
    MESSAGE:
    ```{message}```
    """


    if verbose:
       print(prompt)

    response = client.chat.completions.create(
      # model="gpt-3.5-turbo",
      model = model,
      temperature = 0.0,
      messages=[
               {"role": "user", "content": prompt}
         ]
    )

    return response

def prepare_config(df, ii = 0):
  # returns config variable with relevant values about community/context
  # reads in a dataframe and a row
  config_values = {
      'community_type':df['Community type'][ii],
      'community_context':df['Context'][ii],
      'geography':df['Geography'][ii],
      'protected_characteristics_str':df['Community values'][ii],
      'languages':df['Language Used'][ii],
      'safeguarding_focus':df['Safeguarding Focus'][ii]
  }
  return config_values


def protected_char_repackage(p1_list, p2_str):
   # combine two sources of protected characteristics
   # first input is a list, second is a string
   all_pch_string = ','.join(p1_list) + p2_str

   # it's easiest to edit in a string, but to remove replacements in a set, so...
   # make sure to have low caps and remove spaces after comas, if any
   all_pch_string = all_pch_string.lower().replace(", ", ",")

   # cut again into a list
   all_pch_list = all_pch_string.split(",")
   
   # remove repetitions with set, sort... and shove back into a string lol
   final_pch_str = ",".join(sorted(set(all_pch_list)))

   return final_pch_str