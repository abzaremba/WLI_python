from openai import OpenAI
import os
from hs8_fn import classify_hs

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


############################################################
# PROTECTED CHARACTERISTICS!
# OR CATEGORIES 

protected_characteristics = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity',
    # 'body size'
    #'neurotype', 'body size'
]

# DEFINITION OF HATE SPEECH:1
HS_definition = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics) +'.'
############################################################


############################################################
# EXAMPLES!!!
hs_examples_dict = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech',[''], [1]]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech',[''], [1]]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech',['sexual orientation'], [1]]},
    # {'example input':'Aspie my ass. too slow to remember, so dont waste our time playing',
    #  'example output':['hate speech',['neurotype'], [1]]},
    {'example input':'“Kept being called a "Jew" for no reason.”; "A player on the other team was named Hitler.” “[One player] threatened to get antisemitic if I didnt talk. [They] talked about Jew tunnels.”',
     'example output':['hate speech',['race'], [1]]},
    {'example input':'if money was grown on trees women would be dating monkeys oh wait never mind',
     'example output':['hate speech',['sex'], [1]]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'], [0.97,0.97,1]]}
]


hs_examples_str = '\n'
for ind in range(len(hs_examples_dict)):
  hs_examples_str += "\n" + str(hs_examples_dict[ind])[1:-1]
############################################################

############################################################
# CHAIN OF THOUGHT EXAMPLES!!!
  

chain_of_thought_dict = [
    {"example input":"There are Jews and Muslims here",
     "example output":['not hate speech',[''], [1]],
     "explanation":"This is a statement naming people's religions. It is neutral in tone, regadless if it's factually correct or not. So it is not hate speech"},
    {"example input":"There are Catholics and Muslims here. Let's watch as they k*ll each other.",
     "example output":['hate speech',['religion'], [1]],
     "explanation":"A neutral statement naming people's religions is followed by an implied suggestion that having those religious beliefs will cause people to fight each other. So it is hate speech"},
    {"example input":"You're saying you're a Sikh? I say turban wearing bin laden",
     "example output":['hate speech',['religion'], [1]],
     "explanation":"Person's religion (Sikhism) is devalued and their religious clothing (turban) is compared to a symbol of terrorism - Osama bin Laned. So it is hate speech"},
     {"example input":"Queers are welcome here",
     "example output":['not hate speech',['sexual orientation','gender identity'], [1]],
     "explanation":"Statement implies inclusion and acceptance. So it is not hate speech"},
     {"example input":"All those alphabet people should f**k off from here and stop grooming children",
     "example output":['hate speech',['sexual orientation','gender identity'], [1]],
     "explanation":"'alphabet people' is a slang term referring to LGBTQ+ community and is used in a hostile context. Suggestion about hurt children is used to incite hatred against LGBTQ+ people. So it is hate speech"},
]


chain_ot_str = '\n'
for ind in range(len(chain_of_thought_dict)):
  chain_ot_str += "\n" + str(chain_of_thought_dict[ind])[1:-1]
############################################################



while True:
    print("\nWrite a description of the context for hate speech classification. \nFor example: what's the community, is there a common theme, a common demographic?")
    user_input_context = input()
    print("\nEnter text you wan't classified as 'hate speech' or 'not hate speech'. Enter 'exit' to finish.")
    user_input = input()
    if user_input in ["exit", "Exit", "Bye"]:
          print("Godbye!")
          break
    else:
          response = classify_hs(
                 message = user_input, 
                 protected_characteristics_str = ", ".join(protected_characteristics), 
                 HS_definition=HS_definition, 
                #  examples=[],
                 examples=hs_examples_str,
                #  chain_ot=[],
                 chain_ot=chain_ot_str,
                 verbose = True,
                 community_context="", 
                 languages = "", 
                 geography = "", 
                 safeguarding_focus = ""
                 )
          print(response.choices[0].message.content)
          
    
