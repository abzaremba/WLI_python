from openai import OpenAI
import os

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


my_assistant = client.beta.assistants.retrieve("asst_7UEymD2McoXmoPY04TccmmZs")
print(my_assistant)