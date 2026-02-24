import openai
from pprint import pprint
from prompt import sys_prompt
from oprosnik import opros
import datetime
import json
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY")

dt = datetime.datetime.now().strftime('%A %d %B %Y года')

res = opros()
answer = {
    "0": "Ситуация, не дающая покоя",
    "1": "Эмоциональное состояние «здесь и сейчас»",
    "2": "Текущие стрессоры и проблемы",
    "3": "Поддержка и социальные связи",
    "4": "Самоощущение и внутренний ресурc",
    "5": "Цели, надежды и ожидания"
    }
prompt = sys_prompt.format(first_answer=answer[res["first_answer"]])

client = openai.OpenAI(
    api_key=f"{API_KEY}",
    base_url="https://api.intelligence.io.solutions/api/v1/",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"{res['itog']}"},
    ],
    temperature=0.7,
    stream=False,
    max_completion_tokens=2500
)

print(response.choices[0].message.content)
# pprint(response)
itog_dict = json.loads((response.choices[0].message.content).replace("```json", "").replace("```", "").strip())
print(itog_dict)
print(type(itog_dict))

with open("itog_dict.json", "r", encoding="utf-8") as f:
    current_dict = json.load(f)

current_dict[dt] = itog_dict

with open("itog_dict.json", "w", encoding="utf-8") as f:
    json.dump(current_dict, f, ensure_ascii=False, indent=4)