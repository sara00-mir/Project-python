# quiz_game.py

from quiz_generator import QuizGenerator
import matplotlib.pyplot as plt

class QuizGame:
    """
    Class to handle the quiz gameplay.
    """

    def __init__(self, movies_df):
        self.movies_df = movies_df

    def play_quiz(self):
        """
        Play the quiz game with the user.
        """
        while True:
            try:
                num_questions = int(input("How many questions would you like to answer? "))
                if num_questions <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        while True:
            difficulty = input("Select difficulty (easy, medium, hard): ").lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                print("Invalid difficulty level. Please choose from easy, medium, or hard.")
                continue
            break

        score = 0
        scores_list = []
        quiz_generator = QuizGenerator(self.movies_df)

        for q_num in range(1, num_questions + 1):
            question, options, correct_answer = quiz_generator.generate_movie_quiz(difficulty)
            print(f"\nQuestion {q_num}: {question}")
            for idx, option in enumerate(options, 1):
                print(f"{idx}. {option}")

            # Get user's answer
            while True:
                try:
                    user_choice = int(input("Enter the number of your answer: "))
                    if 1 <= user_choice <= len(options):
                        user_answer = options[user_choice - 1]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(options)}.")
                except ValueError:
                    print("Invalid input. Please enter a valid option number.")

            if user_answer == correct_answer:
                print("✅ Correct!")
                score += 1
                scores_list.append(1)
            else:
                print(f"❌ Wrong! The correct answer was: {correct_answer}")
                scores_list.append(0)

        total_possible_score = num_questions

        # Calculate final score
        print(f"\n🎉 Your final score is {score} out of {total_possible_score}.")

        # Visualize performance
        self.visualize_performance(scores_list, num_questions)

    def visualize_performance(self, scores, num_questions):
        """
        Visualize the user's performance using Matplotlib.
        """
        cumulative_scores = [sum(scores[:i+1]) for i in range(len(scores))]
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(cumulative_scores) + 1), cumulative_scores, marker='o', linestyle='-', color='b')
        plt.title('Quiz Performance Over Time')
        plt.xlabel('Question Number')
        plt.ylabel('Cumulative Score')
        plt.xticks(range(1, num_questions + 1))
        plt.yticks(range(0, num_questions + 1))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
