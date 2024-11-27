from openai import OpenAI
import os
# import json

# def show_json(obj):
#     display(json.loads(obj.model_dump_json()))


client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


# input file
client.files.create(
  file=open("mini_dict.txt", "rb"),
  purpose="assistants"
)

# create or retrieve?
create_assistant = 0
assistant_id = "asst_Gijmrp69n9dC4Zy1jSQZoczt"

# other inputs:
model_used="gpt-3.5-turbo"
# possibly try json?
response_format = "auto"
message = ""
prompt = "Classify the following fragment from a chat as either hate speech: {message}."

if create_assistant == 1:

    my_assistant = client.beta.assistants.create(
        instructions=prompt,
        name="Jude",
        tools=[{"type": "file_search"}],
        model=model_used,
        response_format = response_format
    )

else:
    my_assistant = client.beta.assistants.retrieve(assistant_id)

# show_json(my_assistant)
print(my_assistant)


# response = client.chat.completions.create(
# model="gpt-3.5-turbo",
# temperature = 0.0,
# messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

# print(response.choices[0].message.content)