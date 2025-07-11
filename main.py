from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY")
)
def generateXPost(user_input : str) -> str :
    return call_api(user_input)

def call_api(topic : str):
    prompt = f"""
        Write a post on the topic under 255 char. Which will contains minimal emoji, images avoid hashtag.

        Topic is as follows : 
        <topic>
            {topic}
        </topic>
    """ 
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text

def main():
    # User input => Generate X post using AI
    user_input = input("What should be the post about?")
    user_post = generateXPost(user_input)
    print (f"Generated X post : ", user_post)

if __name__ == "__main__":
    main()
