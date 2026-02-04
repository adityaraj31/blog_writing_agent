from dotenv import load_dotenv

load_dotenv()

def main():
    from graph import build_graph
    app = build_graph()
    out = app.invoke({"topic": "Write a blog on Self Attention", "sections": []})
    print(out["final"])


if __name__ == "__main__":
    main()
