import streamlit as st
import os
import glob
from dotenv import load_dotenv

# Load environment variables before importing other modules
load_dotenv()

from graph import build_graph

st.set_page_config(page_title="Blog Writing Agent", layout="wide")

st.title("AI Blog Writing Agent")
st.markdown("Generate high-quality blogs using LangGraph and Groq.")

# Sidebar for History
st.sidebar.header("Blog History")
md_files = glob.glob("*.md")
# Exclude README.md if it exists
if "README.md" in md_files:
    md_files.remove("README.md")

# Sort files by modification time (newest first)
md_files.sort(key=os.path.getmtime, reverse=True)

selected_file = st.sidebar.radio("Select a previously generated blog:", md_files, index=0 if md_files else None)

def main():
    # Input Section
    with st.container():
        st.subheader("🚀 Generate New Blog")
        topic = st.text_input("Enter the blog topic:")
        
        if st.button("Generate Blog", type="primary"):
            if not topic:
                st.warning("Please enter a topic first.")
            else:
                try:
                    with st.spinner(f"Drafting blog on '{topic}'... This may take a minute."):
                        # Build and run the graph
                        app = build_graph()
                        # Initialize state with topic only; sections will be populated by the graph
                        initial_state = {"topic": topic, "sections": []}
                        result = app.invoke(initial_state)
                        
                        final_content = result.get("final", "")
                        
                        if final_content:
                            st.success("Blog Generated Successfully!")
                            st.markdown("---")
                            st.markdown(final_content)
                            
                            # Rerun to update history sidebar
                            st.rerun()
                        else:
                            st.error("Failed to generate content.")
                            
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Display History Selection if no generation is happening
    if selected_file:
        st.markdown("---")
        st.subheader(f"📄 Viewing: {selected_file}")
        try:
            with open(selected_file, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)
        except Exception as e:
            st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
