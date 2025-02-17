from openai import OpenAI
import os
from hs7_fn_verb import classify_hs

# Initialize the OpenAI client
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

# Models and costs per 1M tokens
models = [
   {"name": "gpt-3.5-turbo", "input_cost": 3.00, "output_cost": 6.00},
#    # {"name": "gpt-4", "input_cost": 30.00, "output_cost": 60.00},
#    {"name": "gpt-4o", "input_cost": 2.50, "output_cost": 10.00},
   {"name": "gpt-4o-mini", "input_cost": 0.15, "output_cost": 0.60}
]


# Messages to classify by the model(s):
msgs = [
  'I would kill for a burger',
  "Hey dude, just because you think you are a woman, doesn't mean we have to accept it. Male and female is not a belief, its just reality.",
  "Tesla CEO Elon Musk has revealed that he was tricked into giving consent for his child to go on puberty blockers, adding that 'the woke mind virus' figuratively killed his elder son. \nIn an interview with Canadian psychologist and author Jordan Peterson, Musk spoke about his concerns regarding children undergoing procedures related to gender dysphoria—the clinical diagnosis for significant distress resulting from an incongruence between a person’s gender identity and the sex they were assigned at birth. \nHis comments came two years after reports emerged that his son Xavier Alexander Musk decided to transition into a woman. In 2022, Xavier turned into Vivian Jenna Wilson and dropped the surname 'Musk' to sever ties with the Tesla and SpaceX founder, according to US media reports. \n‘Tricked into signing documents’\nDuring a live stream on social media platform X, Musk described the term 'gender-affirming care' as a misleading euphemism. Musk, who is one of the richest men on Earth, described these procedures as unethical practices that lead to sterilisation and irreversible changes among teens. \n'I was essentially tricked into signing documents for one of my older boys,' Musk revealed, reflecting on his experience with his son Xavier’s transition. 'I lost my son, essentially,' he said, referring to the concept of ‘deadnaming’ as the loss of a child due to what he termed the 'woke mind virus.' \nPeterson, known for his critique of political correctness and social justice movements, supported Musk’s views. 'No reliable clinician ever believed that,' Peterson stated regarding claims of increased suicide risk among transgender individuals due to gender dysphoria. Musk further slammed the promotion of these procedures, suggesting those advocating for them should face legal consequences. \n'It’s incredibly evil,' he said, advocating for stricter oversight and education on the implications of such medical decisions, particularly for minors. The discussion between Musk and Peterson comes amid ongoing debate on the ethical considerations of medical interventions for minors struggling with gender dysphoria. \nIn the United States, Republican-led states have passed several laws in recent years targeting medications or surgical interventions for adolescents with gender dysphoria. The law bans healthcare workers from administering puberty blockers and hormones for purposes 'inconsistent with the minor’s sex.' Providers can be sued and face fines and professional discipline for violations."
]

# add a file!
with open('sandpit/clarkson.txt', 'r') as file:
    data = file.read().rstrip()
msgs.append(data)


# Which part of the prompt are included
includes = [
  ",",
  "hs_examples_str,chain_ot_str"
]

# at least for now
user_input_context = ""

############################################################
############################################################
protected_characteristics = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity'
]
# DEFINITION OF HATE SPEECH:
HS_definition = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics) +'.'

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
############################################################




# Initialize an empty list to store results

results = []

# Loop through each model and send the request

for msg in msgs:
   for model in models:
    for inc in includes:
           

#    completion = client.chat.completions.create(
#        model=model["name"],
#        messages=[
#            {"role": "user", "content": question}
#        ]
#    )
   
        response = classify_hs(
                        message = msg, 
                        protected_characteristics_str = ", ".join(protected_characteristics), 
                        HS_definition=HS_definition, 
                        #  examples=[],
                        examples=inc.split(',')[0],
                        #  chain_ot=[],
                        chain_ot=inc.split(',')[1],
                        verbose = False,
                        context=user_input_context,
                        model = model["name"]
                        )

        # Extract the response content and token usage from the completion
        response_content = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        model_name = response.model 

        # Calculate the cost based on token usage (cost per million tokens)
        input_cost = (input_tokens / 1_000_000) * model["input_cost"]
        output_cost = (output_tokens / 1_000_000) * model["output_cost"]
        total_cost = input_cost + output_cost

        # Append the result to the results list
        results.append({
            "Text": msg[:20],
            "Model": model_name,
            "Includes":inc,
            "Input Tokens": input_tokens,
            "Output Tokens": output_tokens,
            "Total cost": total_cost,
            "Response": response_content
        })

        # print(results)

import pandas as pd

# display the results in a table format

df = pd.DataFrame(results)

# print(df)

for msg in msgs:
    print('######################################\n')
    print(f'{msg}\n')
    print(df[df["Text"]== msg[:20]])


# saving the dataframe to a csv file
df.to_csv('sandpit/estimates.csv')