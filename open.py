import json
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

def get_api_response(prompt : str, model : str = "gemma3:4b", ctx : int = 4000) :
    response = requests.post(
        os.getenv("OLLAMA_URL") + "/generate",
        json={
            "model" : model,
            "prompt" : prompt,
            "stream" : False,
            "options" : {
                "num_ctx" : ctx
            }
        }
    )
    try : 
        response.raise_for_status()
    except requests.HTTPError as e :
        print (f"Http error occured : {e}")
        return ""
    except Exception as e :
        print (f"Some Error occured : {e}")
        return ""
    data = response.json()

    if "response" not in data :
        print ("Unexpected response : ", data)
        return ""
    
    return data["response"]

def remove_tags(html : str) :
    soup = BeautifulSoup(html, "html.parser")

    # Remove Noise :
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

def get_website_html(url : str) :
    try : 
        response = requests.get(url)
        response.raise_for_status() # raise for an error or exceptions
        return response.text
    except requests.RequestException as e :
        print (f"Error fetching the url : {url} : {e}" )
        return ""
    
def extract_web_content(html : str) :
    response = get_api_response(
        model="gemma3:4b",
        prompt= f"""
            You are an expert web content extractor. Your job is to extract the core content of the given html page.
            The core content will be the main text. Exluding the page header, footer & other non essential componets like scripts etc.

            Here is the HTML content :
            <html>
                {html}
            </html>

            Extract the core content and return it as a plain text.
        """,
        ctx=4000
    )
    return response

def summarize_content(content : str) :
    response = get_api_response(
        model="gemma3:4b",
        prompt=f"""
            You are an expert summerizer. Your task it to summerize the given content into consize and clear message.

            Here is the content to summerize : 

            <content>
                {content}
            </content> 

            Please provide a brief summary of the main points in the content. Preffer bullet points and avoid explaination.
        """,
        ctx=2000
    )
    return response

def generate_x_post(summary : str) : 
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
                </generated-post>
            </example-{i}>
        </examples>
        """

    prompt = f"""
        Write a post on the topic under 255 char. Which will contains minimal emoji, images avoid hashtag.

        Topic is as follows : 
        <topic>
            {summary}
        </topic>

        Here are some examples of topics and generated Posts :
        {example_str}
        Please use the language, structure & style of the example provided above to generate a post that is engaging and relavent to the topic.
    """ 
    response = get_api_response(
        model="gemma:2b",
        prompt=prompt,
        ctx=4000
    )

    return response

def main() :
    website_url = input("Website URL : \n")
    print ("Fetching website HTML: \n")

    try :
        html_content = get_website_html(website_url)
    except Exception as e :
        print (f"An error occured while pulling html {e}")
    
    if not html_content : 
        print ("Failed to fetch website content. Exiting!")
        return
    
    print ("------------")
    print ("Removing tags")
    refined_content = remove_tags(html_content)
    print ("------------")
    print ("Extracting the core content : ")
    core_content = extract_web_content(refined_content)
    print ("Extracted Content : ")
    print (core_content)

    print ("--------")
    print ("Summurize the core content")
    summary = summarize_content(core_content)
    print ("Summarized content : ")
    print (summary)

    print ("--------")
    print ("Generating the X post for the summary : ")
    x_post = generate_x_post(summary)
    print ("Generated X post")
    print (x_post)

print (__name__)

if __name__ == "__main__" :
    main()