from agent import ResearchAgent
from dotenv import load_dotenv

load_dotenv()

def run_chat():
    agent = ResearchAgent()
    print("🤖 Агент-дослідник готовий! (exit для виходу)")
    
    while True:
        user_input = input("\nВи: ")
        if user_input.lower() in ["exit", "quit","ні"]:
            break
            
        final_answer = agent.run(user_input)
        print(f"\n📝 [Final Answer]: {final_answer}")

if __name__ == "__main__":
    run_chat()