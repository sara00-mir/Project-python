# quiz_generator.py

import random
import pandas as pd
import numpy as np

class QuizGenerator:
    """
    Class to generate quiz questions.
    """

    def __init__(self, movies_df):
        self.movies_df = movies_df

    def generate_movie_quiz(self, difficulty='easy'):
        """
        Generate a multiple-choice movie quiz question.
        """
        # Adjust the pool based on difficulty
        if difficulty == 'easy':
            # Use movies with high number of votes
            quiz_pool = self.movies_df[self.movies_df['numVotes'] > 100000]
        elif difficulty == 'medium':
            quiz_pool = self.movies_df[
                (self.movies_df['numVotes'] > 50000) & (self.movies_df['numVotes'] <= 100000)
            ]
        else:  # hard
            quiz_pool = self.movies_df[self.movies_df['numVotes'] <= 50000]

        # Ensure quiz_pool is not empty
        if quiz_pool.empty:
            quiz_pool = self.movies_df

        # **Ensure 'genres' is not NaN in quiz_pool**
        quiz_pool = quiz_pool.dropna(subset=['genres'])

        # Randomly select a movie
        question_movie = quiz_pool.sample(1).iloc[0]

        # Select question type
        question_types = ['year', 'genre', 'actor']
        question_type = random.choice(question_types)

        if question_type == 'year':
            # Question about release year
            question = f"In what year was the movie '{question_movie['title']}' released?"
            correct_answer = str(int(question_movie['startYear']))
            # Generate incorrect answers
            years = self.movies_df['startYear'].astype(int).unique()
            incorrect_years = list(set(years) - {int(correct_answer)})
            incorrect_years = random.sample(
                incorrect_years,
                min(3, len(incorrect_years))
            )
            incorrect_answers = [str(year) for year in incorrect_years]
        elif question_type == 'genre':
            # Question about genre
            genres_list = question_movie['genres'].split(',')
            correct_answer = genres_list[0].strip()
            all_genres = set(
                genre.strip() for genres in self.movies_df['genres'].dropna() for genre in genres.split(',')
            )
            incorrect_genres = list(all_genres - {correct_answer})
            incorrect_genres = random.sample(
                incorrect_genres,
                min(3, len(incorrect_genres))
            )
            incorrect_answers = incorrect_genres
            question = f"Which of the following is a genre of the movie '{question_movie['title']}'?"
        else:  # actor
            # Question about actor
            question = f"Which actor starred in the movie '{question_movie['title']}'?"
            correct_answer = question_movie['actor']
            all_actors = set(self.movies_df['actor'].dropna().unique())
            incorrect_actors = list(all_actors - {correct_answer})
            incorrect_actors = random.sample(
                incorrect_actors,
                min(3, len(incorrect_actors))
            )
            incorrect_answers = incorrect_actors

        # Prepare options and shuffle
        options = [correct_answer] + incorrect_answers
        random.shuffle(options)

        return question, options, correct_answer
