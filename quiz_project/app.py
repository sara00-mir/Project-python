# app.py

import streamlit as st
from data_loader import DataLoader
from quiz_generator import QuizGenerator
import pandas as pd

@st.cache_data
def load_data(file_paths, rating_threshold):
    """
    Caches the loading and merging of IMDb datasets to improve performance.

    Args:
        file_paths (dict): Dictionary containing paths to IMDb TSV files.
        rating_threshold (float): Minimum average rating to filter movies.

    Returns:
        pd.DataFrame: Merged DataFrame containing movie information and associated actors.
    """
    data_loader = DataLoader(file_paths, rating_threshold)
    return data_loader.load_and_merge_datasets()

def main():
    """
    Main function to run the Streamlit-based web quiz application.
    """
    # Set the title of the Streamlit app
    st.title("🎬 Movie Quiz App")
    st.write("Test your knowledge about popular movies with high IMDb ratings!")

    # Sidebar for quiz settings
    st.sidebar.header("Quiz Settings")

    # Define paths to IMDb dataset files
    file_paths = {
        'name_basics': r"C:\Users\Sara\Desktop\python\name.basics.tsv",
        'title_basics': r"C:\Users\Sara\Desktop\python\title.basics.tsv",
        'title_principals': r"C:\Users\Sara\Desktop\python\title.principals.tsv",
        'title_ratings': r"C:\Users\Sara\Desktop\python\title.ratings.tsv",
    }

    # Set the rating threshold for filtering movies
    rating_threshold = 9

    # Load movie data if not already in session state
    if 'movies_df' not in st.session_state:
        with st.spinner("📥 Loading data, please wait..."):
            try:
                movies_df = load_data(file_paths, rating_threshold)
                st.session_state['movies_df'] = movies_df
                st.success("✅ Data loaded successfully.")
            except Exception as e:
                st.error(f"❌ Error loading data: {e}")
                return

    # Retrieve the movies DataFrame from session state
    movies_df = st.session_state['movies_df']

    # Sidebar inputs for number of questions and difficulty level
    num_questions = st.sidebar.number_input("Number of Questions", min_value=1, max_value=50, value=5)
    difficulty = st.sidebar.selectbox("Select Difficulty", options=['easy', 'medium', 'hard'])

    # Determine if a new quiz should be initialized based on user inputs
    initialize_quiz = (
        'current_question' not in st.session_state or
        'questions' not in st.session_state or
        len(st.session_state['questions']) != num_questions or
        st.session_state.get('difficulty') != difficulty
    )

    if initialize_quiz:
        # Initialize quiz parameters in session state
        st.session_state['current_question'] = 1
        st.session_state['score'] = 0
        st.session_state['quiz_generator'] = QuizGenerator(movies_df)
        questions = []
        for _ in range(num_questions):
            # Generate questions using QuizGenerator
            question, options, correct_answer = st.session_state['quiz_generator'].generate_movie_quiz(difficulty)
            questions.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer,
                'user_answer': None
            })
        st.session_state['questions'] = questions
        st.session_state['difficulty'] = difficulty

    # Get the current question number from session state
    current_q = st.session_state['current_question']

    if current_q <= num_questions:
        # Retrieve the current question data
        q_data = st.session_state['questions'][current_q - 1]
        st.header(f"Question {current_q} of {num_questions}")
        st.write(q_data['question'])

        # Create a form for user to submit their answer
        with st.form(key=f"form_{current_q}"):
            user_answer = st.radio("Choose your answer:", options=q_data['options'], key=f"question_{current_q}")
            submit_button = st.form_submit_button(label="Submit Answer")

        if submit_button:
            # Record the user's answer
            st.session_state['questions'][current_q - 1]['user_answer'] = user_answer

            # Check if the answer is correct and update score
            if user_answer == q_data['correct_answer']:
                st.success("✅ Correct!")
                st.session_state['score'] += 1
            else:
                st.error(f"❌ Wrong! The correct answer was: {q_data['correct_answer']}")

            # Move to the next question
            st.session_state['current_question'] += 1

    else:
        # Quiz has been completed; display results
        total_possible_score = num_questions

        st.header("🎉 Quiz Completed!")
        st.write(f"Your final score is **{st.session_state['score']}** out of **{total_possible_score}**.")

        # Prepare detailed results table
        table_data = []
        for idx, q in enumerate(st.session_state['questions'], start=1):
            is_correct = q['user_answer'] == q['correct_answer']
            status = "✅" if is_correct else "❌"
            table_data.append({
                'Question': q['question'],
                'Correct Answer': q['correct_answer'],
                'Your Answer': q['user_answer'],
                'Result': status
            })

        df = pd.DataFrame(table_data)

        st.subheader("🔍 Detailed Results")
        st.table(df)

        # Button to restart the quiz
        if st.button("Restart Quiz"):
            # Clear relevant session state variables
            for key in ['current_question', 'score', 'questions', 'quiz_generator', 'difficulty']:
                st.session_state.pop(key, None)
            # Rerun the app to restart
            st.experimental_rerun()

if __name__ == "__main__":
    main()
