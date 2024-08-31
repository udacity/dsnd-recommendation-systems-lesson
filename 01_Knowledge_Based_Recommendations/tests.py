import numpy as np
import pandas as pd

def q1_check(input_dict):
    a = 8022
    b = 10
    c = 7
    d = 35479
    e = 15
    f = 0
    g = 4
    h = 100001
    i = 28

    dict_sol1 = {
    'The number of movies in the dataset': d,
    'The number of ratings in the dataset': h,
    'The number of different genres': i,
    'The number of unique users in the dataset': a,
    'The number missing ratings in the reviews dataset': f,
    'The average rating given across all ratings': c,
    'The minimum rating given across all ratings': f,
    'The maximum rating given across all ratings': b
    }

    if input_dict == dict_sol1:
        print("That looks good to me!")

    else:
        print("Oops!  That doesn't look quite right.  Try again.")



def create_ranked_df(movies, reviews):
    '''
    INPUT
    movies - the movies dataframe
    reviews - the reviews dataframe

    OUTPUT
    ranked_movies - a dataframe with movies that are sorted by highest avg rating, more reviews,
                    then time, and must have more than 4 ratings
    '''

    # Pull the average ratings and number of ratings for each movie
    movie_ratings = reviews.groupby('movie_id')['rating']
    avg_ratings = movie_ratings.mean()
    num_ratings = movie_ratings.count()
    last_rating = pd.DataFrame(reviews.groupby('movie_id').max()['date'])
    last_rating.columns = ['last_rating']

    # Add Dates
    rating_count_df = pd.DataFrame({'avg_rating': avg_ratings, 'num_ratings': num_ratings})
    rating_count_df = rating_count_df.join(last_rating)

    # merge with the movies dataset
    movie_recs = movies.set_index('movie_id').join(rating_count_df)

    # sort by top avg rating and number of ratings
    ranked_movies = movie_recs.sort_values(['avg_rating', 'num_ratings', 'last_rating'], ascending=False)

    # for edge cases - subset the movie list to those with only 5 or more reviews
    ranked_movies = ranked_movies[ranked_movies['num_ratings'] > 4]

    return ranked_movies




def popular_recommendations(user_id, n_top, ranked_movies):
    '''
    INPUT:
    user_id - the user_id (str) of the individual you are making recommendations for
    n_top - an integer of the number recommendations you want back
    ranked_movies - a pandas dataframe of the already ranked movies based on avg rating, count, and time

    OUTPUT:
    top_movies - a list of the n_top recommended movies by movie title in order best to worst
    '''

    top_movies = list(ranked_movies['movie'][:n_top])

    return top_movies




def popular_recs_filtered(user_id, n_top, ranked_movies, years=None, genres=None):
    # Filter movies based on year and genre
    if years is not None:
        ranked_movies = ranked_movies[ranked_movies['date'].isin(years)]

    if genres is not None:
        num_genre_match = ranked_movies[genres].sum(axis=1)
        ranked_movies = ranked_movies.loc[num_genre_match > 0, :]


    # create top movies list
    top_movies = list(ranked_movies['movie'][:n_top])

    return top_movies
