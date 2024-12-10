from openai import OpenAI
import os
from hs7_fn_categories import classify_hs

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
hs_examples_dict_cat = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech',[''], [1] ,['']]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech',[''], [1], ['']]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech',['sexual orientation'], [1], ['Negative Character']]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'], [0.97,0.97,1], ['Disagreement', 'Disagreement', 'Demonizing and Dehumanizing']]}
]


hs_examples_str = ''
for ind in range(len(hs_examples_dict_cat)):
  hs_examples_str += "\n" + str(hs_examples_dict_cat[ind])[1:-1]
############################################################

############################################################
# CHAIN OF THOUGHT EXAMPLES!!!
  
# todo: get the chain of thought corrected
# note that the rest should work even without it...

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


chain_ot_str = ''
for ind in range(len(chain_of_thought_dict)):
  chain_ot_str += "\n" + str(chain_of_thought_dict[ind])[1:-1]
############################################################
# hate speech intensity scale

hs_intensity = [
    {'intensity':'6',
     'title':'Death',
     'description':'Rhetoric includes literal killing by group. Responses include the literal death/elimination of a group.',
     'examples':'Killed, annihilate, destroy'},
    {'intensity':'5',
     'title':'Violence',
     'description':'Rhetoric includes infliction of physical harm or metaphoric/aspirational physical harm or death. Responses include calld for literal violence or methaphoric/aspirational physical harm or death.',
     'examples':'Punched, raped, starved, torturing, mugging'},
    {'intensity':'4',
     'title':'Demonizing and Dehumanizing',
     'description':'Rhetoric includes subhuman and superhuman characteristics.',
     'examples':'Rat, monkey, Nazi, demon, cancer, monster'},
    {'intensity':'3',
     'title':'Negative Character',
     'description':'Rhetoric includes nonviolent characteristics and insults.',
     'examples':'Stupid, thief, aggressor, fake, crazy'},
    {'intensity':'2',
     'title':'Negative Actions',
     'description':'Rhetoric includes negative nonviolent actions associated with the group. Responses include nonviolent actions including metaphors.',
     'examples':'Thretened, stole, outrageous act, poor treatment, alienate'},
    {'intensity':'1',
     'title':'Disagreement',
     'description':'Rhetoric includes disagreeing at the idea/belief level. Responses include challenging claims, ideas, beliefs, or trying to change their views.',
     'examples':'False, incorrect, wrong, challenge, persuade, change minds'},
    {'intensity':'0',
     'title':'Not hate speech',
     'description':'Rhetoric includes positive or neutral messaging.',
     'examples':'Agree, correct, safe, indifferent, ignore, unbothered'}
]



hs_intensity_str = ''
for ind in range(len(hs_intensity)):
  hs_intensity_str += "\n" + "{" + str(hs_intensity[ind])[1:-1]+ "},"
  
print(hs_intensity_str)
############################################################
# extra instruction and ouput part when intensity levels given

instruction_intensity_str = "Also, using the provided definition of hate speech intensity, classify the with the intensity level."
output_intensity_str = "4) list of intensity levels, one for each protected characteristic."

########################



while True:
    print("\nWrite a description of the context for hate speech classification. \nFor example: what's the community, is there a common theme, a common demographic?")
    user_input_context = input()
    print("\nEnter text you wan't classified as 'hate speech' or 'not hate speech'. Enter 'exit' to finish.")
    user_input = input()
    if user_input in ["exit", "Exit", "Bye"]:
          print("Godbye!")
          break
    else:
          print(classify_hs(
                 message = user_input, 
                 protected_characteristics_str = ", ".join(protected_characteristics), 
                 HS_definition=HS_definition, 
                #  examples=[],
                 examples=hs_examples_str,
                 chain_ot=[],
                #  chain_ot=chain_ot_str,
                 verbose = True,
                 context=user_input_context,
                 hs_categories = hs_intensity_str,
                 extra_notes_instruction=instruction_intensity_str,
                 extra_notes_output=output_intensity_str
                 ))
    
