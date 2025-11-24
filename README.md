# AI Communication Scorer

A Streamlit-based AI tool to analyze and score spoken communication skills from text transcripts. This tool evaluates content, structure, grammar, and sentiment based on the Nirmaan AI rubric.

## 🚀 Features

- **Text-Only Analysis**: Scores transcripts without requiring audio files.
- **Rubric-Based Scoring**: Implements specific criteria for:
    - **Salutation**: Detects formal vs. informal greetings.
    - **Keywords**: Checks for mandatory (e.g., Name, Age) and optional (e.g., Ambition) keywords.
    - **Flow**: Verifies the logical structure of the introduction.
    - **Grammar**: Uses `language-tool-python` to detect and penalize errors.
    - **Vocabulary**: Calculates Type-Token Ratio (TTR) for richness.
    - **Filler Words**: Penalizes excessive use of fillers (e.g., "um", "uh").
    - **Sentiment**: Uses VADER analysis to score positive tone.
- **Interactive UI**: Built with Streamlit for real-time analysis and feedback.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Language**: Python 3.10+
- **NLP Libraries**:
    - `sentence-transformers` (Semantic Analysis)
    - `language-tool-python` (Grammar Checking)
    - `vaderSentiment` (Sentiment Analysis)
- **Data Handling**: `pandas`, `openpyxl`

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Uvais5/AI-Based-Transcript-Scoring-System.git
    cd AI-Based-Transcript-Scoring-System
    ```

2.  **Create a Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

1.  **Run the App**
    ```bash
    streamlit run app.py
    ```

2.  **Analyze a Transcript**
    - Paste your self-introduction text into the input box.
    - Click **Analyze Transcript**.
    - View the **Overall Score** and **Detailed Breakdown** table.

## 📊 Scoring Logic

| Criterion | Max Score | Description |
| :--- | :--- | :--- |
| **Salutation** | 5 | "Good morning/afternoon" (5), "Hello everyone" (4), "Hello/Hi" (3). |
| **Keywords** | 30 | 4 pts for Must-haves (Name, Age, Class, Family, Hobbies). 2 pts for Good-to-haves. |
| **Flow** | 5 | Checks order: Salutation → Basic Details → Closing. |
| **Grammar** | 10 | Penalizes based on error density per 100 words. |
| **Vocabulary** | 10 | Based on Type-Token Ratio (TTR). >0.7 is excellent. |
| **Filler Words** | 15 | 0-3 fillers (15 pts), 4-6 (10 pts), >6 (5 pts). |
| **Sentiment** | 15 | VADER Positive Score > 0.9 (15 pts), > 0.7 (12 pts). |
| **Total** | **100** | |

## 📂 Project Structure

- `app.py`: Main Streamlit application.
- `scorer.py`: Core scoring engine implementing the rules above.
- `nlp_utils.py`: Wrapper for NLP models (VADER, LanguageTool, etc.).
- `rubric_loader.py`: Utility to load rubric data from Excel.
- `requirements.txt`: Project dependencies.


