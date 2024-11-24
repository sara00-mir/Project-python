# main.py

from data_loader import DataLoader
from quiz_game import QuizGame

def main():
    """
    Main function to run the quiz application.
    """
    # Define the file paths
    file_paths = {
        'name_basics': r"C:\Users\Sara\Desktop\python\name.basics.tsv",
        'title_basics': r"C:\Users\Sara\Desktop\python\title.basics.tsv",
        'title_principals': r"C:\Users\Sara\Desktop\python\title.principals.tsv",
        'title_ratings': r"C:\Users\Sara\Desktop\python\title.ratings.tsv",
    }

    # Define the rating threshold
    rating_threshold = 9

    print("📥 Loading data, please wait...")
    data_loader = DataLoader(file_paths, rating_threshold)
    movies_df = data_loader.load_and_merge_datasets()
    print("✅ Data loaded successfully.")

    quiz_game = QuizGame(movies_df)
    quiz_game.play_quiz()

if __name__ == '__main__':
    main()
