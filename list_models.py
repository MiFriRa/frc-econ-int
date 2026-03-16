from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

print("Listing available models...")
try:
    for model in client.models.list():
        # Check attributes of the model object
        print(f"Name: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
