# AutoDS - Agent 🤖📊

**AutoDS - Agent** is an advanced, autonomous multi-agent system designed to perform end-to-end Exploratory Data Analysis (EDA). Built on top of the [CrewAI](https://crewai.com) framework and powered by Google's **Gemini 2.5 Flash** model, it simulates a real-world data science team where specialized AI agents collaborate to research, code, validate, and report on data insights—all without human intervention.

## 🚀 Why AutoDS?

Data science projects often involve repetitive setup: finding data, writing boilerplate pandas code, fixing syntax errors, and formatting reports. **AutoDS - Agent** automates this pipeline.

- **Autonomous Research**: It doesn't just ask for data; it goes online to find the best datasets and context.
- **Self-Healing Code**: The coding agent detects errors, analyzes the traceback, and rewrites its own code until it works.
- **Stateful Execution**: Unlike simple LLM code generators, this agent maintains a persistent Python session (variables are remembered across steps).
- **Quality Control**: A dedicated Reviewer agent critiques the analysis before the final report is written.

---

## ⚙️ How It Works (The Workflow)

The system follows a **Sequential Process** where the output of one agent becomes the context for the next.

1.  **User Input**: You provide a high-level topic (e.g., _"Housing Prices in California"_).
2.  **🕵️ Phase 1: Research**: The **Researcher Agent** uses Google Search (via Serper) to understand the domain, find dataset links, and formulate a 3-step EDA plan.
3.  **💻 Phase 2: Execution**: The **Developer Agent** spins up a Python environment. It creates dummy data (simulating the real dataset structure), runs the EDA plan, generates plots, and fixes any bugs that arise.
4.  **🧐 Phase 3: Review**: The **Reviewer Agent** analyzes the logs and charts. It checks for logical inconsistencies (e.g., negative ages, empty plots) and assigns a Pass/Fail grade.
5.  **� Phase 4: Reporting**: The **Writer Agent** compiles all findings, code snippets, and reviews into a polished `final_report.md`.

---

## 🤖 The Crew (Agent Breakdown)

### 1. Senior Data Science Researcher

- **Role**: Domain Expert & Strategist.
- **Tools**: `SerperDevTool` (Google Search).
- **Responsibility**: Scours the web for context. It decides _what_ to analyze before any code is written.

### 2. Python Data Science Developer

- **Role**: The Builder.
- **Tools**: `PythonInterpreterTool` (Custom).
- **Superpower**: **Persistence**. If a script fails (e.g., `KeyError`), this agent reads the error message, adjusts the code, and retries up to 5 times.
- **Environment**: Uses a custom-built, stateful Python sandbox where `df` created in step 1 is accessible in step 5.

### 3. Senior Data Science Reviewer

- **Role**: Quality Assurance (QA).
- **Responsibility**: Acts as the "Human-in-the-Loop". It ensures the developer didn't just run code, but produced _meaningful_ output.

### 4. Technical Report Writer

- **Role**: Communicator.
- **Responsibility**: Synthesizes technical logs into a readable narrative. It uses "Context Compaction" to avoid dumping thousands of lines of logs into the final report.

---

## �️ Technical Architecture

### The Stateful Python Tool (`tools/code_tool.py`)

Standard LLM tools are often stateless (they forget what happened in the previous turn). AutoDS uses a custom `PythonInterpreterTool` that:

- Maintains a `global_scope` dictionary.
- Captures `sys.stdout` to feed print statements back to the LLM.
- Pre-loads libraries like `pandas` and `matplotlib`.

### The Brain: Gemini 2.5 Flash

We utilize Google's Gemini 2.5 Flash via the `google-genai` library.

- **High Speed**: Essential for multi-step agent loops.
- **Large Context Window**: Allows the agents to read long error logs and documentation.
- **Safety Settings**: Configured to `BLOCK_NONE` to prevent the model from refusing to process benign data outliers.

---

## 📋 Installation & Setup

### Prerequisites

- Python 3.10+
- [Google AI Studio API Key](https://aistudio.google.com/)
- [Serper.dev API Key](https://serper.dev/) (Free tier available)

### Step-by-Step Guide

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd AutoDS-Agent
    ```

2.  **Set up Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_gemini_key_here
    SERPER_API_KEY=your_serper_key_here
    ```

---

## ▶️ Usage

Run the main application:

```bash
python main.py
```

**Example Interaction:**

```text
## Welcome to AutoDS-Agent ##
-------------------------------
Enter the dataset topic you wanna perform EDA on: Titanic Survival Rates
```

**Output Location:**
Once finished, check the `output/` folder:

- `output/final_report.md`: The comprehensive analysis.

---

## � Customization

### Changing the LLM

Open `config/agents.py`. You can swap `gemini-2.5-flash` for `gemini-pro` or even OpenAI models (requires `crewai[openai]`):

```python
self.llm = LLM(model="gemini/gemini-pro", ...)
```

### Adjusting "Patience"

If the code is complex and the agent gives up too soon, increase `max_iter` in `config/agents.py`:

```python
max_iter=10  # Give the developer more attempts to fix bugs
```

### Modifying the Analysis Plan

Edit `config/tasks.py` to change what the Researcher looks for or what specific plots the Developer must generate.

---

## 🤝 Contributing

We welcome contributions!

1.  Fork the repo.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.
