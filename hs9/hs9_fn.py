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

# very short list
protected_characteristics_default = [
    'race', 'religion', 'sexual orientation', 'gender'
]

# # list that used to be our usual list
# protected_characteristics = [
#     'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity'
# ]



# older HS definition
# HS_definition = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics_default) +'.'

HS_definition = 'Hate speech is defined as speech that attacks a person or group based on attributes such as ' + ', '.join(protected_characteristics_default) +'.'

context_text = "";


hs_examples_dict = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech',[], [1]]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech',[], [1]]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech',['sexual orientation'], [1]]},
    {'example input':'“Kept being called a "Jew" for no reason.”; "A player on the other team was named Hitler.” “[One player] threatened to get antisemitic if I didnt talk. [They] talked about Jew tunnels.”',
     'example output':['hate speech',['race','religion'], [1,1]]},
    {'example input':'if money was grown on trees women would be dating monkeys oh wait never mind',
     'example output':['hate speech',['sex'], [1]]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'],  [0.97,0.97,1]]}
]


hs_examples_str = '\n'
for ind in range(len(hs_examples_dict)):
  hs_examples_str += "\n" + str(hs_examples_dict[ind])[1:-1]



chain_of_thought_dict = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech',[], [1]],
     "explanation":"This statement expresses frustration and is an insult but does not target any group or individual based on identity. So it is not hate speech."},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech',[], [1]],
     "explanation":"The statement is a personal insult but does not target any specific group or individual based on identity. So it is not hate speech."},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech',['sexual orientation'], [1]],
     "explanation":"The use of the slur 'FA GO TT' is a direct attack on sexual orientation, intended to demean or insult. So it is hate speech."},
    {'example input':'“Kept being called a "Jew" for no reason.”; "A player on the other team was named Hitler.” “[One player] threatened to get antisemitic if I didnt talk. [They] talked about Jew tunnels.”',
     'example output':['hate speech',['race','religion'], [1,1]],
     "explanation":"The use of antisemitic language, association with Hitler, and threats based on Jewish identity constitute hate speech targeting race and religion."},
    {'example input':'if money was grown on trees women would be dating monkeys oh wait never mind',
     'example output':['hate speech',['sex'], [1]],
     "explanation":"This statement uses stereotypes to demean women by comparing them to animals, which is hate speech based on sex."},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'],  [0.97,0.97,1]],
     "explanation":"This statement combines hostility toward the LGBTQ community with derogatory references to religion, specifically Muslims, and assigns blame. It targets multiple identities and is hate speech."}
]


chain_ot_str = '\n'
for ind in range(len(chain_of_thought_dict)):
  chain_ot_str += "\n" + str(chain_of_thought_dict[ind])[1:-1]


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


    prompt = f"""
    DEFINITIONS:
    Consider the following definition: {HS_definition}

    GEOGRAPHIC CONTEXT:
    This organization operates in {geography}. Be mindful of **regional interpretations of hate speech** in these locations.

    - If certain terms or expressions are **legally restricted** in these regions, classify them more strictly.  
    - If cultural nuances affect interpretation, adapt accordingly.  
    - Consider regional dialects and multi-language factors ({languages}).

    ORGANIZATION CONTEXT:
    {community_context}
    Safeguarding Focus: {safeguarding_focus}

    Protected Characteristics: {protected_characteristics_str}


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
