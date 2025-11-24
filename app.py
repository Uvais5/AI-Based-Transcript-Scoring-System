import streamlit as st
import pandas as pd
from rubric_loader import load_rubric
from nlp_utils import NLPProcessor
from scorer import Scorer
import os

# Set page config
st.set_page_config(page_title="AI Communication Scorer", layout="wide")

@st.cache_resource
def load_nlp_and_rubric():
    nlp = NLPProcessor()
    rubric = load_rubric("Case study for interns.xlsx")
    return nlp, rubric

def main():
    st.title("AI Communication Skills Scorer")
    st.markdown("Analyze and score spoken communication transcripts based on the Nirmaan AI rubric.")

    # Load resources
    with st.spinner("Loading AI models..."):
        nlp, rubric = load_nlp_and_rubric()
        # Initialize scorer dynamically to pick up code changes
        scorer = Scorer(nlp)

    # Sidebar
    st.sidebar.header("Configuration")
    uploaded_file = st.sidebar.file_uploader("Upload Transcript (txt)", type="txt")
    
    # Main Input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        transcript_input = st.text_area("Enter Transcript", height=300, placeholder="Paste transcript here...")
        if uploaded_file:
            transcript_input = uploaded_file.read().decode("utf-8")
            st.info("Loaded transcript from file.")

    with col2:
        analyze_btn = st.button("Analyze Transcript", type="primary", use_container_width=True)

    if analyze_btn and transcript_input:
        with st.spinner("Analyzing..."):
            results = scorer.score_transcript(transcript_input, rubric=rubric)
            
            # Display Results
            st.divider()
            st.subheader("Analysis Results")
            
            # Overall Score
            score = results["overall_score"]
            st.metric("Overall Score", f"{score:.1f}/100")
            st.progress(score / 100)
            
            # Breakdown
            st.subheader("Detailed Breakdown")
            df = pd.DataFrame(results["breakdown"])
            
            # Formatting
            st.dataframe(
                df.style.format({"Score": "{:.1f}", "Weight": "{:.0f}"}),
                use_container_width=True
            )
            
            # Feedback
            st.subheader("Feedback")
            for item in results["breakdown"]:
                with st.expander(f"{item['Criteria']} (Score: {item['Score']:.1f})"):
                    st.write(f"**Feedback:** {item['Feedback']}")
                    st.write(f"**Weight:** {item['Weight']}")

if __name__ == "__main__":
    main()
