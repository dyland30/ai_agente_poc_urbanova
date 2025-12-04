import os
import glob
from google.adk.agents.llm_agent import Agent

# 1. Define the Tool
# In ADK, we wrap functions as Tools so the agent knows how/when to use them.
def read_knowledge_base():
    """
    Reads all .txt files in the 'data' directory and returns their content.
    Useful for answering questions about specific documents.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(current_dir, "data")
    combined_text = ""
    file_paths = glob.glob(os.path.join(data_dir, "*.txt"))
    
    if not file_paths:
        return "No text files found."

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                combined_text += f"\n--- FILE: {os.path.basename(file_path)} ---\n"
                combined_text += f.read()
        except Exception as e:
            return f"Error reading file: {e}"
            
    return combined_text


# 2. Initialize the Agent
# We use the GeminiProvider, but ADK is model-agnostic.
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    tools=[read_knowledge_base], 
    description = "Root agent for document-based queries",
    instruction="""
        You are a helpful assistant. 
        When a user asks a question, use the 'read_knowledge_base' tool to get the content 
        of the available text files. Answer ONLY based on that content.
    """
)


if __name__ == "__main__":
    knowledge_base = read_knowledge_base()
    print("Knowledge Base Content:")
    print(knowledge_base)