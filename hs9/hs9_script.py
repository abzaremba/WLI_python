from openai import OpenAI
import os
from hs9_fn import classify_hs

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


############################################################
# PROTECTED CHARACTERISTICS!
# OR CATEGORIES 

# very short list
protected_characteristics_default = [
    'race', 'religion', 'sexual orientation', 'gender' 
#   'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity'
]

# DEFINITION OF HATE SPEECH:1
HS_definition = 'Hate speech is defined as speech that attacks a person or group based on attributes such as ' + ', '.join(protected_characteristics_default) +'.'
############################################################


############################################################
# EXAMPLES!!!
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
############################################################

############################################################
# CHAIN OF THOUGHT EXAMPLES!!!
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
                 protected_characteristics_str = ", ".join(protected_characteristics_default), 
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
          
    
