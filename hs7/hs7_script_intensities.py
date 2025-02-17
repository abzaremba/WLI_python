from openai import OpenAI
import os
from hs7_fn_intensities import classify_hs

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
# hate speech INTENSITY scale

hs_intensity_def = [
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
for ind in range(len(hs_intensity_def)):
  hs_intensity_str += "\n" + "{" + str(hs_intensity_def[ind])[1:-1]+ "},"
  
print(hs_intensity_str)


############################################################
# EXAMPLES!!!
# without intensities
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

# with intensities
hs_examples_dict_intens = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech',[''], [] ,['']]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech',[''], [], ['']]},
    {'example input':'Tell your kids to keep away from this creep. He has been convicted for child pornography.',
     'example output':['not hate speech',[''], [], ['']]},
    {'example input':'You say your religion is about peace, but we know better.',
     'example output':['hate speech',['religion'], [1] ,['Disagreement']]},
    {'example input':'All those Jews are scheming to take over the world.',
     'example output':['hate speech',['religion', 'race','ethnic origin'], [1,1,1] ,['Negative Actions','Negative Actions','Negative Actions']]},
    {'example input':'In our days we didnt call them Roma, just gypsies: thieving, dirty, lazy gypsies.',
     'example output':['hate speech',['race','ethnic origin'], [0.98,1] ,['Negative Character','Negative Character']]},
    {'example input':'In reference to trans people. You can put a pig in a stable, but its still a pig',
     'example output':['hate speech',['gender identity'], [1] ,['Demonizing and Dehumanizing']]},
    {'example input':"These monkeys don't belong in our football team",
     'example output':['hate speech',['race'], [1] ,['Demonizing and Dehumanizing']]},
    {'example input':"All trans kids can be starved, they don't deserve any resoures.",
     'example output':['hate speech',['gender identity'], [1] ,['Violence']]},
    {'example input':'Seriously, just kill all those dirty towel heads.',
     'example output':['hate speech',['religion', 'religion'], [1,0.93] ,['Death','Death']]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech',['sexual orientation'], [1], ['Negative Character']]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'], [0.97,0.97,1], ['Disagreement', 'Disagreement', 'Demonizing and Dehumanizing']]},
]


hs_examples_str = ''
for ind in range(len(hs_examples_dict_intens)):
  hs_examples_str += "\n" + "{"  + str(hs_examples_dict_intens[ind])[1:-1] + "},"
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
     "example output":['not hate speech',['sexual orientation','gender identity'], [1,1]],
     "explanation":"Statement implies inclusion and acceptance. So it is not hate speech"},
     {"example input":"All those alphabet people should f**k off from here and stop grooming children",
     "example output":['hate speech',['sexual orientation','gender identity'], [1,1]],
     "explanation":"'alphabet people' is a slang term referring to LGBTQ+ community and is used in a hostile context. Suggestion about hurt children is used to incite hatred against LGBTQ+ people. So it is hate speech"},
]



chain_of_thought_dict_intens = [
    {"example input":"There are Jews and Muslims here",
     "example output":['not hate speech',[''], [1] ,['']],
     "explanation":"This is a statement naming people's religions. It is neutral in tone, regadless if it's factually correct or not. So it is not hate speech"},
    {"example input":"There are Catholics and Muslims here. Let's watch as they k*ll each other.",
     "example output":['hate speech',['religion'], [1],['Death']],
     "explanation":"A neutral statement naming people's religions is followed by an implied suggestion that having those religious beliefs will cause people to fight each other. So it is hate speech"},
    {"example input":"You're saying you're a Sikh? I say turban wearing bin laden",
     "example output":['hate speech',['religion'], [1],['Negative Character']],
     "explanation":"Person's religion (Sikhism) is devalued and their religious clothing (turban) is compared to a symbol of terrorism - Osama bin Laned. So it is hate speech"},
     {"example input":"Queers are welcome here",
     "example output":['not hate speech',['sexual orientation','gender identity'], [1,1]],
     "explanation":"Statement implies inclusion and acceptance. So it is not hate speech"},
     {"example input":"All those alphabet people should f**k off from here and stop grooming children",
     "example output":['hate speech',['sexual orientation','gender identity'], [1,1],['Demonizing and Dehumanizing','Demonizing and Dehumanizing']],
     "explanation":"'alphabet people' is a slang term referring to LGBTQ+ community and is used in a hostile context. Suggestion about hurt children is used to incite hatred against LGBTQ+ people. So it is hate speech"},
    {"example input":"Jews killed babies and made bread with their blood",
     "example output":['hate speech',['religion', 'race','ethnic origin'], [1,0.99,0.99],['Demonizing and Dehumanizing', 'Demonizing and Dehumanizing', 'Demonizing and Dehumanizing']],
     "explanation":"This is a statement naming people's religions. It is neutral in tone, regadless if it's factually correct or not. So it is not hate speech"},
     {"example input":"Nazis killed many Jews and made soap out of their bones.",
     "example output":['not hate speech',[''], [1] ,['']],
     "explanation":"This is a factual statement about Nazis and it is historically correct and therefore not hate speech."},
    {"example input":"There is a swarm of people coming across the Mediterranean, seeking a better life, wanting to come to Britain.",
     "example output":['hate speech',['race','ethnic origin'], [0.95, 0.95] ,['Demonizing and Dehumanizing', 'Demonizing and Dehumanizing']],
     "explanation":"The statement might seem factually correct and neutral in tone, but it is not because the use of the word 'swarm' which implies comparing humans to insects, which is hate speech."},
]

# chain_ot_str = ''
# for ind in range(len(chain_of_thought_dict)):
#   chain_ot_str += "\n" + "{"  + str(chain_of_thought_dict[ind])[1:-1]+ "},"

chain_ot_str = ''
for ind in range(len(chain_of_thought_dict_intens)):
  chain_ot_str += "\n" + "{"  + str(chain_of_thought_dict_intens[ind])[1:-1]+ "},"

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
                 hs_intensities = hs_intensity_str,
                 extra_notes_instruction=instruction_intensity_str,
                 extra_notes_output=output_intensity_str
                 ))
    
