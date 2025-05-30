from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "Shreyas is Indian"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small",
)

print("Response:", response)