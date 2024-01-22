import streamlit as st
import pandas as pd
import pickle
import bs4 as bs
import urllib.request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the NLP model and tf-idf vectorizer
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('./tranform.pkl', 'rb'))

@st.cache_data
def create_similarity():
    data = pd.read_csv('main_data.csv')
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    similarity = cosine_similarity(count_matrix)
    return data, similarity

@st.cache_data
def rcmd(m, data, similarity):
    m = m.lower()
    if m not in data['movie_title'].unique():
        return 'Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies'
    else:
        i = data.loc[data['movie_title'] == m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]  # Excluding the first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list

@st.cache_data
def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())

def main():
    st.title("Movie Recommendation App")
    
    st.write("Welcome to the Movie Recommendation App. Find the best movies related to your favorite films.")
    suggestions = get_suggestions()
    movie = st.text_input("Enter a movie name:")
    
    if st.button("Recommend"):
        data, similarity = create_similarity()
        rc = rcmd(movie, data, similarity)
        if type(rc) == str:
            st.error(rc)
        else:
            st.success("Top 10 recommended movies:")
            for i, movie_title in enumerate(rc, start=1):
                st.write(f"{i}. {movie_title}")

if __name__ == '__main__':
    main()
