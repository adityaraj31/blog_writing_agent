# ✍️ AI Blog Writing Agent

An intelligent agentic workflow powered by **LangGraph** and **Groq** (Llama 3) to automatically plan, draft, and format high-quality blog posts.

## 🚀 Features
- **Orchestrator-Worker Architecture**: A main orchestrator plans the blog sections, and parallel workers draft each section.
- **Fast Inference**: Uses Groq's LPU inference engine for rapid content generation.
- **Interactive Frontend**: A **Streamlit** app to generate and view blogs easily.
- **History Tracking**: Automatically saves generated blogs as Markdown files and allows viewing past generations.

## 🛠️ Tech Stack
- **Python 3.12+**
- **LangGraph**: For building stateful, multi-agent workflows.
- **LangChain**: For LLM orchestration.
- **Groq**: For high-speed LLM inference (Llama 3).
- **Streamlit**: For the web interface.

## 📦 Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🖥️ Usage

### 1. Run the Streamlit App (Recommended)
This launches a user-friendly interface to generate and read blogs.
```bash
streamlit run app.py
```

### 2. Run via CLI
You can also run the agent directly from the command line. (Edit `main.py` to change the topic if needed).
```bash
python main.py
```

## 📂 Project Structure
- `app.py`: The Streamlit frontend application.
- `graph.py`: Defines the LangGraph workflow structure.
- `nodes.py`: Contains the logic for the agents (Orchestrator, Worker, Reducer).
- `state.py`: Defines the state schema for the graph.
- `main.py`: Entry point for CLI execution.
- `requirements.txt`: Python package dependencies.
- `*.md`: Generated blog posts.

## 🤖 How It Works
1. **Orchestrator**: Receives a topic and breaks it down into a structured plan with sections.
2. **Fanout**: Distributes the sections to multiple worker nodes.
3. **Workers**: Each worker generates the content for its assigned section in parallel.
4. **Reducer**: Compiles all sections into a single, cohesive Markdown document and saves it.
