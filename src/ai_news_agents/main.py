#!/usr/bin/env python
import warnings
import sys
from datetime import datetime
import os

try:
    from .crew import AiNewsAgents
except ImportError as e:
    print(f"ImportError: {e}. Make sure 'crew.py' exists in the ai_news_agents package and is accessible.")
    raise

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    # Check for required environment variables
    if not os.getenv('SERPER_API_KEY'):
        print("Warning: SERPER_API_KEY not found in environment variables.")
        print("The SerperDevTool may not work without this API key.")
        print("Please create a .env file with your SERPER_API_KEY from https://serper.dev/")
        print("Example: SERPER_API_KEY=your_api_key_here")
        print()
    
    inputs = {
        'topic': 'AI LLMs',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    try:
        print("Creating AiNewsAgents crew...")
        crew_instance = AiNewsAgents()
        print("Starting crew execution...")
        result = crew_instance.crew().kickoff(inputs=inputs)
        print("Crew execution completed!")
        return result
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        import traceback
        traceback.print_exc()
        return None

def train():
    """
    Train the crew for a given number of iterations.
    """
    if len(sys.argv) < 4:
        print("Usage: python main.py train <n_iterations> <filename>")
        return
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        AiNewsAgents().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py replay <task_id>")
        return
    try:
        AiNewsAgents().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        print(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    if len(sys.argv) < 4:
        print("Usage: python main.py test <n_iterations> <eval_llm>")
        return
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        AiNewsAgents().crew().test(
            n_iterations=int(sys.argv[2]),
            eval_llm=sys.argv[3],
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <run|train|replay|test> [args...]")
    else:
        command = sys.argv[1]
        if command == "run":
            run()
        elif command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        else:
            print(f"Unknown command: {command}")
