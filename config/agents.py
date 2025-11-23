from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from tools.code_tool import PythonInterpreterTool
import os

class AutoDSAgents:
    def __init__(self):
        # 1. SETUP LLM: Use Gemini 2.5 Flash with Safety Filters DISABLED
        # This prevents the "None or empty" error caused by data output.
        self.llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
    def research_agent(self):
        return Agent(
            role='Senior Data Science Researcher',
            goal='Research the Kaggle dataset context and create a robust EDA plan.',
            backstory=(
                "You are an expert researcher. Your job is to find the dataset, "
                "understand its domain (e.g., medical, finance), and list the key questions "
                "that need to be answered. You do NOT write code."
            ),
            tools=[SerperDevTool()], # Built-in Google Search Tool
            llm=self.llm,
            verbose=True,
            max_rpm=10
        )

    def code_execution_agent(self):
        return Agent(
            role='Python Data Science Developer',
            goal='Write, execute, and fix Python code to analyze the data.',
            backstory=(
                "You are a skilled Python developer. You are responsible for the actual "
                "data processing. You have a persistent Python environment. "
                "If your code fails, you MUST analyze the error and retry. "
                "You do not stop until the code runs successfully."
            ),
            tools=[PythonInterpreterTool()],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,    # INCREASED: Give it more attempts to fix errors
            max_rpm=10,     # NEW: Limits speed to prevent API blocking
            max_execution_time=300 # NEW: Prevents it from hanging forever
        )

    def reviewer_agent(self):
        return Agent(
            role='Senior Data Science Reviewer',
            goal='Review code execution outputs for quality and logical correctness.',
            backstory=(
                "You are a strict QA engineer. You look at the logs and outputs "
                "from the Developer. If a plot has no title, or the analysis is superficial, "
                "you act as a 'Human-in-the-Loop' and demand corrections. "
                "You ensure the final work is professional."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=True,# Can delegate back to the Coder if needed (A2A Protocol)
            max_rpm = 10
        )

    def report_agent(self):
        return Agent(
            role='Technical Report Writer',
            goal='Compile all findings into a professional Markdown report.',
            backstory=(
                "You transform raw logs, code outputs, and research notes into a "
                "beautiful, readable Data Science report. You summarize technical "
                "jargon into clear insights."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_rpm = 10    
        )