from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import State, Plan, Task
from pathlib import Path

from langgraph.types import Send

llm = ChatGroq(model="llama-3.3-70b-versatile")

def orchestrator(state: State) -> dict:
    plan = llm.with_structured_output(Plan).invoke([
        SystemMessage(content="Create a blog plan with 5-7 sections on the following topic."),
        HumanMessage(content=f"Topic: {state['topic']}")
    ])
    return {"plan": plan}

def fanout(state: State):
    return [
        Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"]})
        for task in state["plan"].tasks
    ]

def worker(payload: dict) -> dict:
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]
    blog_title = plan.blog_title
    section_md = llm.invoke([
        SystemMessage(content="Write one clean Markdown section."),
        HumanMessage(content=(
            f"Blog: {blog_title}\n"
            f"Topic: {topic}\n\n"
            f"Section: {task.title}\n"
            f"Brief: {task.brief}\n\n"
            "Return only the section content in Markdown."
        )),
    ]).content.strip()
    return {"sections": [section_md]}

def reducer(state: State) -> dict:
    title = state["plan"].blog_title
    body = "\n\n".join(state["sections"]).strip()
    final_md = f"# {title}\n\n{body}\n"
    filename = title.lower().replace(" ", "_") + ".md"
    output_path = Path(filename)
    output_path.write_text(final_md, encoding="utf-8")
    return {"final": final_md}
