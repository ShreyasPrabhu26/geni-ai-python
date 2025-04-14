from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def get_weather(city:str):
    # Simulate a weather API call
    return f"21 degree celcius."

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


    Example:
    User query: "whats the weather at udupi?"
    Output:{{"step":""plan","content":"The user is intrested in weather data of Udupi"}}
    Output:{{"step":""plan","content":"From the available tools i should call get_weather""}}
    Output:{{"step":""action","function":"get_weather","input":"udupi"}}
    Output:{{"step":""observe","output":21 degree celcius"}}}
    Output:{{"step":""output","content":The weather at udupi seems to be 21 degree celcius"}}}
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "whats the weather at udupi?"
        },
    ],
)

print(completion.choices[0].message.content)