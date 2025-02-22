import streamlit as st
import pickle as pk
import pandas as pd

# Define the recommendation function
def recommend(selected_song):
    try:
        # Use the song DataFrame correctly
        index = song_df[song_df['name'] == selected_song].index[0]
    except IndexError:
        st.error(f"Song '{selected_song}' not found in the dataset.")
        return []  # Return an empty list if the song is not found

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_songs = []
    for i in distances[1:6]:
        recommended_songs.append(song_df.iloc[i[0]]['name'])  # Append song name to the list

    return recommended_songs

# Load similarity matrix
with open("similarity.pkl", "rb") as fd:
    similarity = pk.load(fd)  # Load directly as DataFrame

# Load the pickled dataset
try:
    with open("Song_list.pkl", "rb") as f:
        song_df = pk.load(f)  # Renamed to avoid confusion
    st.write(f"Data type of song_df: {type(song_df)}")  # Debugging
except Exception as e:
    st.error(f"Error loading pickle file: {e}")
    song_df = pd.DataFrame(columns=['name'])  # Assign empty DataFrame to avoid crashes

# Check if 'name' column exists
if 'name' not in song_df.columns:
    st.error("The dataset does not contain a 'name' column!")
    song_df = pd.DataFrame(columns=['name'])

# Streamlit UI
st.title("Spotify Song Recommendation System")

# Use the correct DataFrame for the select box
selected_song = st.selectbox("Enter song here", song_df['name'].values if not song_df.empty else [])

if st.button("Recommend"):
    recommended_songs = recommend(selected_song)
    for i in recommended_songs:
        st.write(i)
