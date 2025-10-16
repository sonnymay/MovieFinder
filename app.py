import os
import streamlit as st
import requests
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(page_title="MovieFinder", page_icon="🎬", layout="centered")

st.title("🎬 MovieFinder")
st.write("Find movie ideas based on what you feel like watching. Simple, quick, and fun!")

# --- Initialize session state ---
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "previous_movies" not in st.session_state:
    st.session_state.previous_movies = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# --- User input ---
user_input = st.text_input("What kind of movie do you feel like watching?", "")

# --- Function to get movie info from TMDb ---
def fetch_movie_info(title):
    if not TMDB_API_KEY:
        return title, "", None
    
    try:
        # Clean the title - remove year if present in parentheses
        clean_title = re.sub(r'\s*\(\d{4}\)\s*', '', title).strip()
        
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={clean_title}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("results"):
            movie = data["results"][0]
            title = movie.get("title")
            year = movie.get("release_date", "")[:4] if movie.get("release_date") else ""
            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
            return title, year, poster_url
    except Exception as e:
        st.warning(f"Could not fetch info for: {title}")
    
    return title, "", None

# --- Function to get movie recommendations from OpenAI ---
def recommend_movies(description, previous_movies=[]):
    excluded = ""
    if previous_movies:
        excluded = f" Do NOT recommend any of these movies: {', '.join(previous_movies)}."
    
    prompt = f"Recommend 5 different movies based on this description: {description}.{excluded} " \
             "Format each recommendation EXACTLY like this:\n" \
             "Movie Title (Year) - Brief description in 1-2 sentences.\n" \
             "Use this exact format with the movie title, then year in parentheses, then a dash, then description."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful movie recommendation assistant. Always format responses with 'Movie Title (Year) - Description' format."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content.strip()

# --- Function to parse movie titles from response ---
def parse_movies(result_text):
    """Extract movie titles from the OpenAI response"""
    movies = []
    lines = result_text.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line or line.lower().startswith("enjoy") or line.lower().startswith("here"):
            continue
        
        # Remove numbering (1., 2., etc.) and bullet points
        line = re.sub(r'^\d+[\.\)]\s*', '', line)
        line = line.strip("•-— ")
        
        # Extract title (everything before " - " or before year in parentheses)
        if " - " in line:
            title_part = line.split(" - ")[0].strip()
        else:
            title_part = line
        
        # Remove year in parentheses from title for searching
        clean_title = re.sub(r'\s*\(\d{4}\)\s*$', '', title_part).strip()
        
        if clean_title:
            movies.append((clean_title, line))
    
    return movies

# --- Find button ---
if st.button("Find Movies"):
    if not user_input.strip():
        st.warning("Please describe what kind of movie you want.")
    else:
        with st.spinner("Finding movies for you..."):
            # Reset previous movies when new search
            st.session_state.previous_movies = []
            st.session_state.user_query = user_input
            result = recommend_movies(user_input)
            st.session_state.last_result = result

# --- Show results ---
if st.session_state.last_result:
    st.success("🎬 Here are some movies you might enjoy:")

    result = st.session_state.last_result
    parsed_movies = parse_movies(result)

    for clean_title, full_line in parsed_movies:
        # Fetch movie info
        title, year, poster = fetch_movie_info(clean_title)
        
        # Track this movie
        if title not in st.session_state.previous_movies:
            st.session_state.previous_movies.append(title)
        
        # Display title
        display_title = f"{title} ({year})" if year else title
        st.markdown(f"**{display_title}**")
        
        # Display poster if available
        if poster:
            st.image(poster, width=150)
        
        # Show description
        if " - " in full_line:
            summary = full_line.split(" - ", 1)[1]
            st.write(summary)
        
        st.write("---")

    # Next Suggestions button
    if st.button("Next Suggestions 🎞️"):
        with st.spinner("Fetching new suggestions..."):
            result = recommend_movies(
                st.session_state.user_query, 
                st.session_state.previous_movies
            )
            st.session_state.last_result = result
            st.rerun()