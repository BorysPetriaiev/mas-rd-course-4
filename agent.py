import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import tools_schema, tools_map
from config import SYSTEM_PROMPT, MAX_ITERATIONS, MODEL

load_dotenv() 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ResearchAgent:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        for i in range(MAX_ITERATIONS):
            response = client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=tools_schema,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            self.messages.append(response_message)

            if not response_message.tool_calls:
                return response_message.content

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 [Tool Call]: {function_name}({function_args})")
                
                function_to_call = tools_map[function_name]
                try:
                    tool_result = function_to_call(**function_args)
                    print(f"📎 [Result]: {str(tool_result)[:100]}...") 
                except Exception as e:
                    tool_result = f"Error: {str(e)}"
                
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result,
                })
        
        return "Досягнуто ліміту ітерацій."