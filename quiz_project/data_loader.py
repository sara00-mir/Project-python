# data_loader.py

import pandas as pd
import os

class DataLoader:
    """
    Class to load and merge IMDb datasets.
    """

    def __init__(self, file_paths, rating_threshold=7):
        self.file_name_basics = file_paths['name_basics']
        self.file_title_basics = file_paths['title_basics']
        self.file_title_principals = file_paths['title_principals']
        self.file_title_ratings = file_paths['title_ratings']
        self.rating_threshold = rating_threshold

    def check_files_exist(self):
        """
        Check if all the specified files exist.
        """
        files = [
            self.file_name_basics,
            self.file_title_basics,
            self.file_title_principals,
            self.file_title_ratings
        ]
        missing_files = [file for file in files if not os.path.isfile(file)]
        if missing_files:
            print("The following required files are missing:")
            for file in missing_files:
                print(f"- {file}")
            print("Please ensure all files are downloaded and placed in the correct directory.")
            exit(1)  # Exit the script if files are missing

    def load_and_merge_datasets(self):
        """
        Load IMDb datasets and merge them into a single DataFrame.
        """
        # Check if all files exist before proceeding
        self.check_files_exist()

        # Load title.basics.tsv
        print("Loading title.basics.tsv...")
        title_basics = pd.read_csv(
            self.file_title_basics,
            sep='\t',
            na_values='\\N',
            usecols=['tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'genres'],
            dtype={
                'tconst': 'object',
                'titleType': 'category',
                'primaryTitle': 'object',
                'isAdult': 'category',
                'startYear': 'object',  # Initially as object to handle non-numeric values
                'genres': 'object'
            },
            low_memory=False
        )

        # Filter for movies and exclude adult films
        movies = title_basics[
            (title_basics['titleType'] == 'movie') & (title_basics['isAdult'] == '0')
        ].copy()

        # Convert startYear to numeric and drop rows with NaNs in startYear
        movies['startYear'] = pd.to_numeric(movies['startYear'], errors='coerce')
        movies = movies.dropna(subset=['startYear'])
        movies['startYear'] = movies['startYear'].astype(int)  # Convert to integer

        # **Drop movies with missing genres**
        movies = movies.dropna(subset=['genres'])

        # Load title.ratings.tsv
        print("Loading title.ratings.tsv...")
        title_ratings = pd.read_csv(
            self.file_title_ratings,
            sep='\t',
            na_values='\\N',
            usecols=['tconst', 'averageRating', 'numVotes'],
            dtype={
                'tconst': 'object',
                'averageRating': 'float64',
                'numVotes': 'int64'
            },
            low_memory=False
        )

        # Merge movies with ratings
        print("Merging movies with ratings...")
        movies = movies.merge(title_ratings, on='tconst', how='inner')  # Use inner join to keep only rated movies

        # Keep only movies with IMDb rating >= rating_threshold
        movies = movies[movies['averageRating'] >= self.rating_threshold]

        # Load title.principals.tsv
        print("Loading title.principals.tsv...")
        title_principals = pd.read_csv(
            self.file_title_principals,
            sep='\t',
            na_values='\\N',
            usecols=['tconst', 'nconst', 'category'],
            dtype={
                'tconst': 'object',
                'nconst': 'object',
                'category': 'category'
            },
            low_memory=False
        )

        # Filter for actors and actresses
        principals = title_principals[
            title_principals['category'].isin(['actor', 'actress'])
        ].copy()

        # Merge movies with principals
        print("Merging movies with principals...")
        movies = movies.merge(principals, on='tconst', how='left')

        # Load name.basics.tsv
        print("Loading name.basics.tsv...")
        name_basics = pd.read_csv(
            self.file_name_basics,
            sep='\t',
            na_values='\\N',
            usecols=['nconst', 'primaryName'],
            dtype={
                'nconst': 'object',
                'primaryName': 'object'
            },
            low_memory=False
        )

        # Merge movies with names
        print("Merging movies with names...")
        movies = movies.merge(name_basics, on='nconst', how='left')

        # Rename columns for clarity
        movies = movies.rename(columns={
            'primaryTitle': 'title',
            'primaryName': 'actor'
        })

        # Drop rows where actor is NaN (in case some principals don't have names)
        movies = movies.dropna(subset=['actor'])

        # Reset index
        movies = movies.reset_index(drop=True)

        print("Data loading and merging completed.")
        return movies
