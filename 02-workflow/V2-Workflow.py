from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os
import urllib.parse

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

def get_weather(city:str):
    # Simulate a weather API call
    print(f"Tool Called :get_weather:city")
    url = f"https://wttr.in/{city}?format=%C+%t"
    weather_response = requests.get(url, timeout=10)

    if weather_response.status_code == 200:
        return f"The weather in {city} is {weather_response.text}."
    else:
        return f"Could not retrieve weather data for {city}."

def search_internet(query:str):
    print(f"Tool Called :search_internet:query")
    # Note: For production use, consider using Google's official Custom Search JSON API which requires an API key
    # This is a simplified example for demonstration purposes
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Simplified parsing - just return a summary
            # For real implementation, you would use BeautifulSoup to properly parse results
            return f"Google search results for '{query}' successfully retrieved. Found multiple results."
        else:
            return f"Failed to search for '{query}' on Google. Status code: {response.status_code}"
    except Exception as e:
        return f"Error searching Google: {str(e)}"

available_tools = {
    "get_weather":{
        "function": get_weather,
        "description": "Takes city name as input and returns the weather data",
    },
    "run_command":{
        "function": run_command,
        "description": "Takes command as input and returns the result of the command",
    },
    "search_internet":{
        "function": search_internet,
        "description": "Takes a search query as input and returns relevant information from the internet",
    }
}

SYSTEM_PROMPT = """
    You are a helpful assistant who is specialized in resolving user query.
    you work on start,plan,action,observe mode.
    For the given user query and available tools, plan the step by step execution,based on the planning,select the relavent tool from the availale tool,based on the tool selection you perform an action to call the tool, wait for the obeservation and based on observation from the tool call the resolve the user query.

    Rules:
    - Follow the Output JSON format
    - Always perform one step at a time and wait for the next input
    - Carefully analyze user query

    Output JSON format:
    {{
        "step":"string",
        "content":"string",
        "function":"The name of the function if the step is action",
        "input":"The input to the function if the step is action",
    }}

    Available tools:
    - get_weather:Takes city name as input and returns the weather data
    - run_command:Takes command as input and returns the result of the command
    - search_internet:Takes a search query as input and returns relevant information from the internet

    Example:
    User query: "whats the weather at udupi?"
    Output:{{"step":""plan","content":"The user is intrested in weather data of Udupi"}}
    Output:{{"step":""plan","content":"From the available tools i should call get_weather""}}
    Output:{{"step":""action","function":"get_weather","input":"udupi"}}
    Output:{{"step":""observe","output":21 degree celcius"}}}
    Output:{{"step":""output","content":The weather at udupi seems to be 21 degree celcius"}}}
"""

messages = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]

userquery = input("> ")
messages.append({"role": "user", "content": userquery})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content":json.dumps(parsed_response)})

    if parsed_response["step"] == "plan":
        print(f"Assistant: {parsed_response['content']}")
        continue

    if parsed_response["step"] == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        if available_tools.get(tool_name,False):
            function_output = available_tools[tool_name].get("function")(tool_input)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":function_output})})
            continue
    
    if parsed_response.get("step") == "output":
        print(f"AI: {parsed_response.get('content')}")
        userquery = input("> ")
        messages.append({"role": "user", "content": userquery})
        continue  