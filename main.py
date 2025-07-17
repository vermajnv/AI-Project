from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY")
)
def generateXPost(user_input : str) -> str :
    return call_api(user_input)

def call_api(topic : str):
    with open("post-example.json", "r") as f :
        examples = json.load(f)

    example_str = ""
    
    for i, example in enumerate(examples) :
        example_str += f"""
        <examples>
            <example-{i}>
                <topic>
                    {example['topic']}
                </topic>
                <generated-post>
                    {example['post']}
                </generated-post
            </example-{i}>
        </examples>"""

    prompt = f"""
        Write a post on the topic under 255 char. Which will contains minimal emoji, images avoid hashtag.

        Topic is as follows : 
        <topic>
            {topic}
        </topic>

        Here are some examples of topics and generated Posts :
        {example_str}
        Please use the language, structure & style of the example provided above to generate a post that is engaging and relavent to the topic.
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
