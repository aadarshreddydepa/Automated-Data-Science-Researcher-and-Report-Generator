import os
from dotenv import load_dotenv
from crewai import Crew, Process

# Import our custom classes
from config.agents import AutoDSAgents
from config.tasks import AutoDSTasks

# 1. Load Environment Variables (API Keys)
load_dotenv()

def main():
    # --- Setup ---
    print("## Welcome to AutoDS-Agent ##")
    print("-------------------------------")
    
    # 2. Define the Input for the Project
    # You can change this to "Titanic Dataset", "House Prices", "Iris Species", etc.
    dataset_topic = input("Enter the dataset topic you wanna perform EDA on: ")
    
    # 3. Instantiate Agents & Tasks
    agents = AutoDSAgents()
    tasks = AutoDSTasks()

    # Create Agents
    researcher = agents.research_agent()
    coder = agents.code_execution_agent()
    reviewer = agents.reviewer_agent()
    writer = agents.report_agent()

    # Create Tasks (Linking Agents to their work)
    # We pass the 'dataset_topic' to the research task
    task_research = tasks.research_task(researcher, dataset_topic)
    task_coding = tasks.coding_task(coder)
    task_review = tasks.review_task(reviewer)
    task_report = tasks.reporting_task(writer)

    # 4. Create the Crew (The Multi-Agent Team)
    # The order of tasks in the list determines the Sequential Flow
    ds_crew = Crew(
        agents=[researcher, coder, reviewer, writer],
        tasks=[task_research, task_coding, task_review, task_report],
        process=Process.sequential, # Forces them to work one after another
        verbose=True # Shows detailed logs of who is doing what
    )

    # 5. Kickoff the Process!
    print(f"\n🚀 Starting the AutoDS-Agent Crew on topic: {dataset_topic}\n")
    result = ds_crew.kickoff()

    # 6. Final Output
    print("\n\n########################")
    print("##   PROJECT COMPLETE  ##")
    print("########################\n")
    print(f"Final Report stored in 'output/final_report.md'")
    print("Here is the final summary output:")
    print(result)

if __name__ == "__main__":
    main()