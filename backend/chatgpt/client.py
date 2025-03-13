from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

try:
    OPENAI_API = os.getenv("OPENAI_API")
    print(OPENAI_API)
    openai_client = OpenAI(api_key=OPENAI_API)

except Exception as e:
    raise Exception(f"🚨 Failed to connect to OpenAI: {e}")

class KeywordsResponse(BaseModel):
    case_id: str
    case_title: str
    events: list[str]
    description: str
    location: str
    names: list[str]
    ages: list[str]
    genders: list[str]
    addresses: list[str]
    type: str

def get_keywords(user_prompt):
    generate_keywords_prompt = """
    You will be given a Crime Case related question.
    Please extract important keywords based on the question.
    The keywords may contain information such as the case id, case title, events that took place, description of crime, location of crime, type of crime, name of persons, age of persons, gender of persons and address of persons.

    The response case_id should default to an empty string "" if case id is not found.
    The response case_title should default to an empty string "" if case title is not found.
    The response events should default to an empty list [] if no events are found.
    The response description should default to an empty string "" if no description is not found.
    The response location should default to an empty string "" if location of crime is not found.
    The response names should default to an empty list [] if no name of persons are found.
    The response ages should default to an empty list [] if no age of persons are found.
    The response genders should default to an empty list [] if no gender of persons are found.
    The response addresses should default to an empty list [] if no address of persons are found.
    The response type should default to an empty string "" if type of crime not found.

    Your response should be structured as follows:
    {
      "case_id": <str>,
      "case_title": <str>,
      "events": [<str>, <str>, ...],
      "description": <str>,
      "location": <str>,
      "names": [<str>, <str>, ...],
      "ages": [<str>, <str>, ...],
      "genders": [<str>, <str>, ...],
      "addresses": [<str>, <str>, ...],
      "type": <str>
    }
    """

    user_prompt = f"The following is the crime case question: {user_prompt}. Please extract important keywords based on the question."

    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": generate_keywords_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=KeywordsResponse,
    )

    return completion.choices[0].message.parsed


def get_case_vectors(KeywordsResponse):
    query = f"{KeywordsResponse.case_id} {KeywordsResponse.case_title} {KeywordsResponse.description} {KeywordsResponse.type} {KeywordsResponse.location}"

    cases = requests.get(f"http://localhost:5000/pinecone_cases/{query}")
    return cases.json()

def get_evidence_vectors(case_context, evidence_id):
    query = f"{evidence_id} {case_context['case_id']} {case_context['title']} {case_context['description']} {case_context['type']} {case_context['location']}"
    evidence = requests.get(f"http://localhost:5000/pinecone_evidence/{query}")
    return evidence.json()


def get_summary(user_input, relevant_information):
    generate_summary_prompt = f"""
    You will be given a Crime Case related question and relevant information about the Case.
    Please form connections between the relevant information and provide answers about the Case using the relevant information.
    If there is no good answer, write "I'm not sure."

    The Relevant Information below is in JSON format and contains the case id, case title, case description, case type, case location, events and evidence related to the Crime Case.

    Relevant Information:
    {relevant_information}

    """

    user_prompt = f"The following is the crime case question: {user_input}. Please help to provide answers about the Case using the relevant information."

    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": generate_summary_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    print(generate_summary_prompt)

    return completion.choices[0].message.content
