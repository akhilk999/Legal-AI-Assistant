import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_name = "gpt-4o-mini"

file = input("Enter text file name (no .txt): ")
file_path = os.path.join("text case files", file + ".txt")

with open(file_path) as f:
    text = f.read()
q = f'''
Extract specified values from the source text.
Return answer as JSON object with following fields:
- "case" <string> Case name
- "crpc" <string> Criminal Procedure Code section number
- "court" <string> Level of court
- "judge" <string> Head judge of the court
- "location" <string> Court location
- "year" <number> Year of judgement
- "verdict" <string> Verdict of the case
- "verdict_summary" <string> Summary of the verdict
- "cases_referred" <string> Cases referred in the judgement separated by ", "
- "prosecutor" <string> Prosecutor lawyer name, N/A if not found
- "defendant" <string> Defendant lawyer name, N/A if not found
- disposition_prosecutor" <string> Disposition of the prosecutor lawyer
- disposition_defendant" <string> Disposition of the defendant lawyer


========
{text}
========
'''
#Do not infer any data based on previous training, strictly use only source text given below as input.

completion = client.chat.completions.create(
    model=model_name, 
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a text processing agent working with an Indian Supreme Court case document."},
        {"role": "user", "content": q}
        ])
c = completion.choices[0].message.content
print(c)