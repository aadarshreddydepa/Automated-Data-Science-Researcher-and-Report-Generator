from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import sys
import io
import pandas as pd # Pre-importing pandas for the agent

# 1. Define the input schema (what the agent sends to the tool)
class CodeInput(BaseModel):
    code: str = Field(description="The Python code to execute. Must be valid, executable Python code.")

# 2. Define the Tool Class
class PythonInterpreterTool(BaseTool):
    name: str = "Python Interpreter"
    description: str = (
        "A Python execution environment. Use this to analyze data, clean data, "
        "and perform calculations. "
        "IMPORTANT: The environment maintains state. Variables you define in one step "
        "are available in the next step. "
        "ALWAYS use print() to output the results you want to see."
    )
    args_schema: type[BaseModel] = CodeInput
    
    # This dictionary acts as the 'Session Memory' for the code
    global_scope: dict = Field(default_factory=dict, exclude=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the scope with some useful libraries pre-loaded
        self.global_scope = {
            "pd": pd,
            "print": print, # Ensure print is available
        }

    def _run(self, code: str) -> str:
        """
        Executes the provided Python code and captures the output.
        """
        # Create a string buffer to capture the standard output (print statements)
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            # EXECUTE THE CODE
            # We pass 'self.global_scope' as both globals and locals
            # This allows variables to persist across different calls to this tool
            exec(code, self.global_scope, self.global_scope)
            
            # Get the output from the buffer
            output = redirected_output.getvalue()
            
            if not output:
                return "Code executed successfully, but produced no output. Did you forget to print()?"
            
            return f"output:\n{output}"

        except Exception as e:
            # If an error occurs, we return the traceback so the Agent can debug it (Loop Agent concept)
            return f"Execution Error: {str(e)}"
        
        finally:
            # Restore standard output so we can see logs in our terminal again
            sys.stdout = old_stdout