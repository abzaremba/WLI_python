from openai import OpenAI
import os
from hs9_fn import classify_hs, prepare_config, protected_char_repackage
from pprint import pprint

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

import pandas as pd

############################################################
# read information about community context
# and messages to analyse
 
contexts_file_name   = "hs9/data/Demo_context_impact - context.csv"
messages_file_name   = "hs9/data/Demo_context_impact - message.csv"

df_context = pd.read_csv(contexts_file_name)
messages = pd.read_csv(messages_file_name, header = None)
messages.rename(columns={0: 'message'}, inplace=True)


# # do you want to choose a community context and message now? or later in a loop?
# row_context = 0
# row_message = 0
# config_values = prepare_config(df_context, row_context)
# message = messages['message'][row_message]

# pprint(config_values)
# print(messages)

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
     "explanation":"This statement combines hostility toward the LGBTQ community with derogatory references to religion, specifically Muslims, and assigns blame. It targets multiple identities and is hate speech."},
    # {'example input':"stop acting like such a pretentious tosspot, you're not blessing us with your knowledge here, dude",
    #  'example output':['not hate speech',[], [1]],
    #  "explanation":"This message expresses frustration and includes insults, but does not target any group or protected identity. It can be a part of heated debate. So it is not hate speech."},
    # {'example input':'jesus fuck man do you ever listen to others?',
    #  'example output':['not hate speech',[], [1]],
    #  "explanation":"This message expresses frustration and includes insults, but does not target any group or protected identity. It can be a part of heated debate. So it is not hate speech."},
    # {'example input':"you're talking like such a pretentious douchebag. calm down!",
    #  'example output':['not hate speech',[], [1]],
    #  "explanation":"This message expresses frustration and includes insults, but does not target any group or protected identity. It can be a part of heated debate. So it is not hate speech."},
]

chain_ot_str = '\n'
for ind in range(len(chain_of_thought_dict)):
  chain_ot_str += "\n" + str(chain_of_thought_dict[ind])[1:-1]
############################################################

#####
# # read community context and message now in a loop?
# # for individual read, with a context nr cc, and message nr mm:
# row_context = cc
# row_message = mm
# config_values = prepare_config(df_context, row_context)
# message = messages['message'][row_message]
# # to pretty print the context and normal print the message
# pprint(config_values)
# print(messages)



# verbose?
verbose_switch = False

results = []

# no request for input, just use the context and message read from csv files
for row_context in range(df_context.shape[0]):
    config_values = prepare_config(df_context, row_context)

    print(f"{'#'*30} Context provided number {row_context:3}:")
    print(f"\n{'#'*5} community_context:\n{config_values['community_context']}")
    print(f"\n{'#'*5} languages:\n{config_values['languages']}")
    print(f"\n{'#'*5} geography:\n{config_values['geography']}")
    print(f"\n{'#'*5} protected_characteristics_str:\n{config_values['protected_characteristics_str']}")
    print(f"\n{'#'*5} safeguarding_focus:\n{config_values['safeguarding_focus']}")

    for row_message in range(29,30):#messages.shape[0]): 
          message = messages['message'][row_message]
          message = "You deserve to die!"
          print(f"{'#'*20} Context message number {row_message:3}:")
          print(message)

          # with context
          print("with context                  ", end="-->") 
          response = classify_hs(
                 message = message, 
                 protected_characteristics_str = config_values['protected_characteristics_str'], 
                 HS_definition=HS_definition, 
                 examples=hs_examples_str,
                 chain_ot=chain_ot_str,
                 verbose = verbose_switch,
                 community_context=config_values['community_context'], 
                 languages = config_values['languages'], 
                 geography = config_values['geography'], 
                 safeguarding_focus = config_values['safeguarding_focus']
                 )
          print(response.choices[0].message.content)
          result_with_context = response.choices[0].message.content

          # # without context 
          # print(f"{'#'*80} ")
          # print(f"{'#'*20} Without context!!!")
          
          print("without context               ", end="-->") 
          response = classify_hs(
                 message = message, 
                 protected_characteristics_str = '', 
                 HS_definition=HS_definition, 
                 examples=hs_examples_str,
                 chain_ot=chain_ot_str,
                 verbose = verbose_switch,
                 community_context='', 
                 languages = '', 
                 geography = '', 
                 safeguarding_focus = ''
                 )
          print(response.choices[0].message.content)
          result_no_context = response.choices[0].message.content

          # # without context, examples or chain of thought
          # print(f"{'#'*80} ")
          # print(f"{'#'*20} Without context, examples or chain of thought!!!")
          print("no context,examples or c-o-t  ", end="-->") 
          response = classify_hs(
                 message = message, 
                 protected_characteristics_str = '', 
                 HS_definition=HS_definition, 
                 examples=[],
                 chain_ot=[],
                 verbose = verbose_switch,
                 community_context='', 
                 languages = '', 
                 geography = '', 
                 safeguarding_focus = ''
                 )
          print(response.choices[0].message.content)
          result_no_context_no_examples = response.choices[0].message.content
          print(f"{'#'*30}")

          results.append({
            'Name': config_values.get('community_type', ''),
            'Organisation_context': config_values.get('community_context', ''),
            'Geography': config_values.get('geography', ''),
            'Languages_used': config_values.get('languages', ''),
            'Safeguarding_focus': config_values.get('safeguarding_focus', ''),
            'Protected_characteristics': config_values.get('protected_characteristics_str', ''),
            'Message': message,
            'Result_with_context': result_with_context,
            'Result_no_context': result_no_context,
            'Result_no_context_no_examples': result_no_context_no_examples
            })
          
# # Create DataFrame and save to CSV
# results_df = pd.DataFrame(results)
# results_df.to_csv("hs9/data/demo_classification_results.csv", index=False)
          
    
