from openai_cost_tracker import query_openai

def classify_hs_cost_test(message:str, protected_characteristics_str:str, HS_definition:str, examples:str, chain_ot:str, verbose=False, context="", extra_notes="",simulation_switch=True):
    
    # is context provided
    if context==[]:
       context_section = ""
    else:
       context_section = f"""
    CONTEXT:
    Consider the following CONTEXT:{context}"""
       
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
    Consider the following definition: {HS_definition}. 
    {context_section}

    INSTRUCTION: 
    Using the provided definition of hate speech, classify the following fragment from a chat as either hate speech with respect to one or more of protected characteristics from the following list: {protected_characteristics_str}, or not hate speech with respect to the protected characteristics from the following list: {protected_characteristics_str}.
    {extra_notes}

    OUTPUT:
    The output should only contain 3 elements: 
    1) "hate speech" or "not hate speech", 
    2) list of protected characteristic labels from the list: {protected_characteristics_str}, 
    3) list of probabilities with two decimal points, one for each protected characteristic.

    OUTPUT FORMAT:
    ['hate speech', ['sexual orientation'], [0.98]]

    {examples_section}
    {chain_ot_section}
    
    MESSAGE:
    {message}
    """
    ### part that if added suddenly doesn't recognise transphobia and misogyny:

    # OUTPUT FORMAT EXAMPLE:
    # 'hate speech', 'religion', 0.98


    if verbose:
       print(prompt)

    # response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    # temperature = 0.0,
    # messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )

    response = query_openai(
        model="gpt-3.5-turbo-1106",  # support gpt-4-0125-preview,  gpt-3.5-turbo-1106,  gpt-4
        messages=[{'role': 'user', 'content': prompt}],            
        max_tokens=30,
        # rest of your OpenAI params here ...
        simulation=simulation_switch,  # set to True to test the cost of a request without actually sending it to OpenAI 
        print_cost=True   # set to True to print the cost of each request
    )

    # return response.choices[0].message.content
    return response

# response = completion["choices"][0]["text"].strip()

# for text in test_texts:
#     print("=============================")
#     print(classify_hs(
#             message = text, 
#             protected_characteristics_str = ", ".join(protected_characteristics), 
#             HS_definition=HS_definition, 
#             examples=hs_examples_str))