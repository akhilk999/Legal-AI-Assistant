from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()
chroma_client = chromadb.Client()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model_name = "llama3-groq-70b-8192-tool-use-preview"
json_output = ""
page_ids = []
page_texts = []
collection = None
case_info = '''- "case" <string> Case name
    - "court" <string> Level of court
    - "judge" <string> Head judge of the court
    - "location" <string> Court location
    - "year" <number> Year of judgement
'''
other_info = '''- "crpc" <string> Criminal Procedure Code section number
    - "verdict" <string> Verdict of the case
    - "verdict_summary" <string> Summary of the verdict
    - "cases_referred" <string> Cases referred in the judgement separated by ", "
    - "plaintiff_lawyer" <string> plaintiff, petitioner, applicant, decree holder or appellant lawyer name, N/A if not found
    - "defendant_lawyer" <string> defendant, respondent, accused, judgment debtor lawyer name, N/A if not found
    - disposition_prosecutor" <string> Disposition of the prosecutor lawyer
    - disposition_defendant" <string> Disposition of the defendant lawyer'''


def convert_pdf_to_text(file):
    reader = PdfReader(os.path.join("pdf case files", file + '.pdf'))
    for i, p in enumerate(reader.pages):
        page_ids.append(str(i))
        page_texts.append(p.extract_text())
    
def embed_search():
    global collection
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-ada-002")
    collection = chroma_client.create_collection(
        name='my_case',
        embedding_function = openai_ef)
    collection.add(documents = page_texts, ids = page_ids)

def search_index(query):
    results = collection.query(
        query_texts=[query],
        n_results=1)
    page = results["documents"][0][0]
    return page

def create_prompt(page, data):
    q = f'''
    Extract specified values from the source text.
    Return answer as JSON object with following fields:\n'''
    + data + '''\n\nDo not infer any data based on previous training, strictly use only source text given below as input.
    ========
    {page}
    ========
    '''
    print(q)

    completion = groq_client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a text processing agent working with an Indian Supreme Court case document."},
            {"role": "user", "content": q}
            ])
    return completion.choices[0].message.content

convert_pdf_to_text(input("Enter PDF file name (no .PDF): "))
embed_search()
json_output += create_prompt(search_index("Equivalent citations"),case_info)
json_output += create_prompt(search_index("Equivalent citations"),other_info)