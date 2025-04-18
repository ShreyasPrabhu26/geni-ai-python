from dotenv import load_dotenv
from openai import OpenAI
import json
import requests

load_dotenv()

client = OpenAI()

def get_weather(city:str):
    # Simulate a weather API call
    print(f"Tool Called :get_weather:city")
    url = f"https://wttr.in/{city}?format=%C+%t"
    weather_response = requests.get(url, timeout=10)

    if weather_response.status_code == 200:
        return f"The weather in {city} is {weather_response.text}."
    else:
        return f"Could not retrieve weather data for {city}."

available_tools = {
    "get_weather":{
        "function": get_weather,
        "description": "Takes city name as input and returns the weather data",
    }
}

system_prompt = """
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
    "content": system_prompt
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