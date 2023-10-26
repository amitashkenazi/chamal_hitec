#load csv file

import pandas as pd
import openai
from glob import glob
import os

openai.api_type = "azure"
openai.api_base = os.environ['OPENAI_ENDPOINT']
openai.api_version = "2023-03-15-preview"
openai.api_key = os.environ['OPENAI_API_KEY']


file_needs = "data/_1698141705_needs.csv"
file_vol = "data/_1698142363_volunties.csv"
file_needs_updates = "data/_1698141705_needs_updates.csv"
file_vol_updates = "data/_1698142363_volunties_updates.csv"

df_updates = pd.read_csv(file_vol_updates)
df_needs_updates = pd.read_csv(file_needs_updates)

df_vol = pd.read_csv(file_vol)
df_needs = pd.read_csv(file_needs)
prompt = ""
name = "שולמית מויאל"
# get all the rows with the value {name} under the column "Name"
df_need = df_needs[df_needs['Name'] == name]
print(f"Number of rows: {len(df_need)}")
print("*****------*****------")
# print rows
print(df_need.head())
prompt += "the details of the person asking for help is:\n"
prompt += "name: " + name + "\n"
prompt += "סוג בקשה הסיוע לו אני זקוק: " + df_need['סוג בקשה הסיוע לו אני זקוק'].iloc[0] + "\n"
prompt += "נכס מבוקש: " + df_need['נכס מבוקש'].iloc[0] + "\n"
prompt += "פירוט אירוח: " + df_need['פירוט אירוח'].iloc[0] + "\n"
prompt += "לאיזה סוג סיוע ועזרה אתם נדרשים: " + str(df_need['לאיזה סוג סיוע ועזרה אתם נדרשים'].iloc[0]) + "\n"

prompt += "Updates for the request:\n"


df_need_updates = df_needs_updates[df_needs_updates['Item Name'] == name]
print(f"Number of rows: {len(df_need_updates)}")
print("*****------*****------")
for index, row in df_need_updates.iterrows():
    prompt += row['Created At'] + ": " + row['Update Content'] + "\n"
print("prompt:\n")
print(prompt)
name_vol = "ואלרי וגיא כהן"
df_vol = df_vol[df_vol['Name'] == name_vol]
prompt += "We have a volumteer for evaluation:\n"
prompt += 'איך אתה יכול לתרום ?' + df_vol['איך אתה יכול לתרום ?'].iloc[0] + "\n"
try:
    shelter = df_vol['האם יש במקום האירוח מרחב מוגן ?']
    prompt += 'האם יש במקום האירוח מרחב מוגן ?' + df_vol['האם יש במקום האירוח מרחב מוגן ?'].iloc[0] + "\n"
except:
    print("no mention of shelter")

prompt += 'כמה אנשים אתה יכול לארח' + str(df_vol['כמה אנשים אתה יכול לארח'].iloc[0]) + "\n"
prompt += 'מיקום האירוח' + str(df_vol['מיקום האירוח'].iloc[0]) + "\n"
prompt += 'מתי תהיו פנויים? - Start' + str(df_vol['מתי תהיו פנויים? - Start'].iloc[0]) + "\n"
prompt += 'מתי תהיו פנויים? - End' + str(df_vol['מתי תהיו פנויים? - End'].iloc[0]) + "\n"
prompt += 'הערות מתנדבי חמ״ל' + str(df_vol['הערות מתנדבי חמ״ל'].iloc[0]) + "\n"

df_updates = df_updates[df_updates['Item Name'] == name_vol]
prompt += "updates for the volunteer:\n"
for index, row in df_updates.iterrows():
    prompt += row['Created At'] + ": " + row['Update Content'] + "\n"

prompt += "evaluate the match between the person asking for help and the volunteer:\n"
prompt += "the result should be in a json format as follows:\n"
prompt += "{\n"
prompt += "    \"match\": \"High\",\n" 
prompt += "    \"reason\": \"The volunteer is a good match for the person asking for help\" # give as much details as possible \n" 
prompt += "    \"details_volunteer\": \"The volunteer can host up to 4 person, with a shelter in the building with out elevator. the volunteer can host between the date: Nov 1st to December 1st\"\n"
prompt += "    \"details_need\": \"The person asking for help needs a place to stay for 2 weeks, with a shelter in the building with out elevator\"\n"

prompt += "}\n"
model = "gpt-35-turbo"
messages = []


messages.append({"role":"system","content":prompt})
print("messages")
print(messages)
response = openai.ChatCompletion.create(
    engine=model,
    messages = messages,
    temperature=1.0,
    max_tokens=300,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)
print(response)
