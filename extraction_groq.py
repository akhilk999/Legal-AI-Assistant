import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model_name = "llama-3.1-70b-versatile"

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
- "judge" <string> Judges on the bench
- "location" <string> Court location
- "year" <number> Year of judgement
- "verdict" <string> Verdict of the case
- "verdict_summary" <string> Summary of the verdict
- "cases_referred" <string> Cases referred in the judgement separated by ", "
- "plaintiff_lawyer" <string> plaintiff, petitioner, applicant, decree holder or appellant lawyer name, N/A if not found
- "defendant_lawyer" <string> defendant, respondent, accused, judgment debtor lawyer name, N/A if not found
- disposition" <string> Disposition/final outcome of the case

Do not infer any data based on previous training, strictly use only source text given below as input.
Only include notes about assumed data.
Do not include a note about data that is not found in the source text.
Do not include a note for explicitly mentioned data.
========
{text}
========
'''

completion = client.chat.completions.create(
    model=model_name,
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a text processing agent working with an Indian Supreme Court case document."},
        {"role": "user", "content": q}
        ])
c = completion.choices[0].message.content
print(c)