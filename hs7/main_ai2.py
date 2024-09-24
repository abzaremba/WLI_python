from openai import OpenAI
import os
from hs7_fn import classify_hs

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


################### SCRIPT SUGGESTIONS from Miro board #####
# Opening message:
     # Hey! I'm sorry you've experienced hate speech online.
     # You can report it here and we'll get straight on
     # classifying it for you.

     # But before doing the report, would you like to try something that might make you feel better?
# Options:
     # 1. Mindfulness and breathing exercises
     # 2. Read inspiring quotes from social justice warriors.
     # 3. Take a look at some organisations you can reach out to for mental health support.
     # 4. No thanks, I just want to continue with reporting

############################################################
# scripted messages:
msg_opening = "Hey! I'm sorry you've experienced hate speech online."
msg_options = "You can report it here and we'll get straight on \nclassifying it for you. \n\nBut before doing the report, would you like to try something that might make you feel better?"
msg_options2 = "You can report hate speech here and we'll get straight on to classifying it for you."
msg_options3 = "\n\nBut before doing the report, would you like to try something that might make you feel better? Chat to a friendly bot, who will help you with these options."
msg_op1 = 'Mindfulness and breathing exercises'
msg_op2 = 'Read inspiring quotes from social justice warriors.'
msg_op3 = 'Take a look at some organisations you can reach out to for mental health support.'
msg_op4 = 'No thanks, I just want to continue with reporting.'
msg_op5 = 'Exit'

options_block = [msg_options2, "\nOption 1: ", msg_op1, "\nOption 2: ", msg_op1, "\nOption 2: ", msg_op1, "\nOption 3: ", msg_op3, "\nOption 4: ", msg_op4]


print("#"*70)
print(msg_opening, "\n", msg_options2, "\n", msg_options3, "\n", "\nOption 1: ", msg_op1, "\nOption 2: ", msg_op2, "\nOption 3: ", msg_op3, "\nOption 4: ", msg_op4, "\n\nOption 5: ", msg_op5)
print("#"*70)

############################################################
# PROTECTED CHARACTERISTICS!
# OR CATEGORIES 

protected_characteristics = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity',
    'body size'
    #'neurotype', 'body size'
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
    # {'example input':'Aspie my ass. too slow to remember, so dont waste our time playing',
    #  'example output':['hate speech','neurotype', 1]},
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
     "explanation":"This is a statement naming people's religions. It is neutral in tone, regadless if it's factually correct or not. So it is not hate speech"},
    {"example input":"There are Jews and Muslims here. Let's watch as they k*ll each other.",
     "example output":['hate speech','religion', 1],
     "explanation":"A neutral statement naming people's religions is followed by an implied suggestion that having those religious beliefs will cause people to fight each other. So it is hate speech"},
    {"example input":"You're saying you're a Sikh? I say turban wearing bin laden",
     "example output":['hate speech','religion', 1],
     "explanation":"Person's religion (Sikhism) is devalued and their religious clothing (turban) is compared to a symbol of terrorism - Osama bin Laned. So it is hate speech"},
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


messages = [
     {
          "role": "system",
          "content": "You're a kind and empathetic companion that helps people who might be experiencing hate speech. You'll be interacting with a person who decided to report hate speech. They will most likely be upset, and might be anxious. Be sympathetic in your responses, but not overburdening. Write short messages.",
     }
]


messages.append(
    {
        "role": "user",
        "content": f"{options_block}"
    }
)

model = "gpt-3.5-turbo"

stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

while True:
    print("\n")
    user_input = input()
    if user_input in ["exit", "Exit", "Bye"]:
          print("Godbye!")
          break
    elif user_input in ["4", "Option 4", "Option4", "option4", "option 4", "report"]:
          print("Okay, let's start with the experience itself. What did they say to you?")
          hs_message = input()
          # print(hs_message)
          
          print(classify_hs(
                 message = hs_message, 
                 protected_characteristics_str = ", ".join(protected_characteristics), 
                 HS_definition=HS_definition, 
                #  examples=[],
                #  chain_ot=[],
                 examples=hs_examples_str,
                 chain_ot=chain_ot_str,
                 ))
    else:
          messages.append(
               {
                    "role": "user",
                    "content": user_input
               }
          )
          stream = client.chat.completions.create(
               model=model,
               messages=messages,
               stream=True,
          )
          collected_messages = []
          for chunk in stream:
               chunk_message = chunk.choices[0].delta.content or ""
               print(chunk_message, end="")
               collected_messages.append(chunk_message)
          
          messages.append(
               {
                    "role": "system",
                    "content": "".join(collected_messages)
               }
          )