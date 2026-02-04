from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import State, Plan, Task
from pathlib import Path

from langgraph.types import Send

llm = ChatGroq(model="llama-3.3-70b-versatile")

from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def researcher(state: State) -> dict:
    try:
        print(f"DEBUG: Starting research on topic: {state['topic']}")
        response = tavily.search(query=state["topic"], search_depth="advanced", max_results=3)
        context = "\n\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in response.get("results", [])])
        print(f"DEBUG: Research completed. Found {len(response.get('results', []))} sources.")
        # print(f"DEBUG: Context preview: {context[:200]}...") 
        return {"context": context}
    except Exception as e:
        # Fallback if search fails
        print(f"Research failed: {e}")
        return {"context": "No external context available."}

import time

def generate_plan(topic: str, context: str):
    retries = 0
    while retries < 5:
        try:
            return llm.with_structured_output(Plan).invoke([
                SystemMessage(content="Create a blog plan with 5-7 sections on the following topic. Use the provided context to ensure accurately structured content."),
                HumanMessage(content=f"Topic: {topic}\n\nContext:\n{context}")
            ])
        except Exception as e:
            if "429" in str(e):
                retries += 1
                wait_time = 2 ** retries
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded for plan generation")

def orchestrator(state: State) -> dict:
    context = state.get("context", "")
    plan = generate_plan(state['topic'], context)
    return {"plan": plan}

def fanout(state: State):
    return [
        Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"], "context": state.get("context", "")})
        for task in state["plan"].tasks
    ]

def generate_section(blog_title, topic, context, title, brief):
    retries = 0
    while retries < 5:
        try:
            return llm.invoke([
                SystemMessage(content="Write one clean Markdown section. Use the context provided to add depth, facts or statistics if relevant."),
                HumanMessage(content=(
                    f"Blog: {blog_title}\n"
                    f"Topic: {topic}\n\n"
                    f"Context:\n{context}\n\n"
                    f"Section: {title}\n"
                    f"Brief: {brief}\n\n"
                    "Return only the section content in Markdown."
                )),
            ]).content.strip()
        except Exception as e:
            if "429" in str(e):
                retries += 1
                wait_time = 2 ** retries
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded for section generation")

def worker(payload: dict) -> dict:
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]
    context = payload.get("context", "")
    blog_title = plan.blog_title
    section_md = generate_section(blog_title, topic, context, task.title, task.brief)
    return {"sections": [section_md]}

def reducer(state: State) -> dict:
    title = state["plan"].blog_title
    body = "\n\n".join(state["sections"]).strip()
    final_md = f"# {title}\n\n{body}\n"
    filename = title.lower().replace(" ", "_") + ".md"
    output_path = Path(filename)
    output_path.write_text(final_md, encoding="utf-8")
    return {"final": final_md}
