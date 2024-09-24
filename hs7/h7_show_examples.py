from openai import OpenAI
import os
from hs7_fn import classify_hs

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


############################################################
# PROTECTED CHARACTERISTICS!
# OR CATEGORIES 

protected_characteristics = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity',
    # 'body size'
]

# DEFINITION OF HATE SPEECH:1
HS_definition = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics) +'.'
############################################################


############################################################
# EXAMPLES!!!
hs_examples_dict = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech','', 1]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech','', 1]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech','sexual orientation', 1]},
    {'example input':'She said she identifies as queer',
     'example output':['not hate speech','', 1]},
    {'example input':'“Kept being called a "Jew" for no reason.”; "A player on the other team was named Hitler.” “[One player] threatened to get antisemitic if I didnt talk. [They] talked about Jew tunnels.”',
     'example output':['hate speech','race', 1]},
    {'example input':'if money was grown on trees women would be dating monkeys oh wait never mind',
     'example output':['hate speech','sex', 1]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'], 1]}
]


hs_examples_str = '\n'
for ind in range(len(hs_examples_dict)):
  hs_examples_str += "\n" + str(hs_examples_dict[ind])[1:-1]
############################################################

############################################################
# CHAIN OF THOUGHT EXAMPLES!!!
  

chain_of_thought_dict = [
    {"example input":"There are Jews and Muslims here",
     "example output":['not hate speech','', 1],
     "explanation":"This is a statement naming people's religions. It is neutral in tone, regardless if it's factually correct or not. So it is not hate speech"},
    {"example input":"There are Catholics and Muslims here. Let's watch as they k*ll each other.",
     "example output":['hate speech','religion', 1],
     "explanation":"A neutral statement naming people's religions is followed by an implied suggestion that having those religious beliefs will cause people to fight each other. So it is hate speech"},
    {"example input":"You're saying you're a Sikh? I say turban wearing bin laden",
     "example output":['hate speech','religion', 1],
     "explanation":"Person's religion (Sikhism) is devalued and their religious clothing (turban) is compared to a symbol of terrorism - Osama bin Laden. So it is hate speech"},
     {"example input":"Queers are welcome here",
     "example output":['not hate speech',['sexual orientation','gender identity'], 1],
     "explanation":"Statement implies inclusion and acceptance. So it is not hate speech"},
     {"example input":"All those alphabet people should f**k off from here and stop grooming children",
     "example output":['hate speech',['sexual orientation','gender identity'], 1],
     "explanation":"'alphabet people' is a slang term referring to LGBTQ+ community and is used in a hostile context. Suggestion about hurt children is used to incite hatred against LGBTQ+ people. So it is hate speech"},
]


chain_ot_str = '\n'
for ind in range(len(chain_of_thought_dict)):
  chain_ot_str += "\n" + str(chain_of_thought_dict[ind])[1:-1]
############################################################




############################################################
############################################################
############################################################
############################################################
# EXAMPLES TO SHOW EFFECTS OF PROMPT ENGINEERING

print("#"*70)
print(f"Begin with prompt that includes definition of hate speech, but no examples - so called 'zero-shot prompt'")
print(f'The definition of hate speech uses the following characteristics:')
print(protected_characteristics)

############################################################
# no examples, no chain of thought
# FATPHOBIA
#
# original protected characteristics:
# protected_characteristics = [
#     'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity',
#     'body size'
# ] 
# 
# add body size
protected_characteristics_body_size = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity',
    'body size'
]
HS_definition_body_size = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics_body_size) +'.'
message1 = "You'd be cute if you lost some weight."


print("#"*70)
print('Original prompt:')
print("#"*15)
output1_prm1 = classify_hs(
            message = message1, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            examples=[],
            chain_ot=[],
            verbose=True
            )
output1_prm2 = classify_hs(
            message = message1, 
            protected_characteristics_str = ", ".join(protected_characteristics_body_size), 
            HS_definition=HS_definition_body_size, 
            examples=[],
            # examples=hs_examples_str,
            chain_ot=[],
            # chain_ot=chain_ot_str,
            )


print("#"*70)
print(f"\nThis example shows the effect of adding 'body size' to the characteristics used in the hate speech definition")
print(f'Message....... {message1}')
print(f'Before....... {str(output1_prm1)}')
print(f'After........ {str(output1_prm2)}')


 

############################################################
# too sensitive,
# add --> chain of thought
# 

message2 = "You're Jewish"


print("#"*70)
output2_prm1 = classify_hs(
            message = message2, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            examples=[],
            chain_ot=[],
            )
print('Prompt with train of thougth:')
print("#"*15)
output2_prm3 = classify_hs(
            message = message2, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            examples=[],
            # examples=hs_examples_str,
            # chain_ot=[],
            chain_ot=chain_ot_str,
            verbose=True
            )


print("#"*70)
print(f"\nThis example shows the effect of adding chain of thought")
print(f'Message....... {message2}')
print(f'Before....... {str(output2_prm1)}')
print(f'After........ {str(output2_prm3)}')
 

############################################################
# too sensitive,
# add --> chain of thought
# 

message3 = "So very queer in this green scarf!"


print("#"*70)
output3_prm1 = classify_hs(
            message = message3, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            examples=[],
            chain_ot=[],
            )
print('Prompt with examples:')
print("#"*15)
output3_prm2 = classify_hs(
            message = message3, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            # examples=[],
            examples=hs_examples_str,
            chain_ot=[],
            # chain_ot=chain_ot_str,
            verbose=True
            )
output3_prm3 = classify_hs(
            message = message3, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            examples=[],
            chain_ot=chain_ot_str,
            )
output3_prm4 = classify_hs(
            message = message3, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            # examples=[],
            examples=hs_examples_str,
            # chain_ot=[],
            chain_ot=chain_ot_str,
            # verbose=True
            )

print("#"*70)
print(f"\nThis example shows the effect of adding examplesand/or chain of thought")
print(f'Message...................... {message3}')
print(f'Before anything.............. {str(output3_prm1)}')
print(f'After examples............... {str(output3_prm2)}')
print(f'After chain of thought....... {str(output3_prm3)}')
print(f'After BOTH................... {str(output3_prm4)}')

############################################################
# ADDITIONAL CONTEXT
# 

message4 = "come here ciota and fight"


print("#"*70)
output4_prm1 = classify_hs(
            message = message4, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            # examples=[],
            examples=hs_examples_str,
            # chain_ot=[],
            chain_ot=chain_ot_str,
            verbose=False,            
            )
# print('Prompt with extra comments warning of possible use of slang in Polish:')
# print("#"*15)
output4_prm2 = classify_hs(
            message = message4, 
            protected_characteristics_str = ", ".join(protected_characteristics), 
            HS_definition=HS_definition, 
            # examples=[],
            examples=hs_examples_str,
            # chain_ot=[],
            chain_ot=chain_ot_str,
            # verbose=True,
            extra_notes = "Slurs in Polish language should also be considered as potential hate speech."
            )


print("#"*70)
print(f"\nThis example shows the effect of adding additional contextual information.")
print(f'Message....... {message4}')
print(f'Before....... {str(output4_prm1)}')
print(f'After........ {str(output4_prm2)}')



    
