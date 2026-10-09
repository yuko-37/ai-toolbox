import hashlib

import streamlit as st

from logger import configure_logging
from datahandler import (
    read_last_shows_from_memory,
    set_video_seen,
    write_last_shows_to_memory,
)

configure_logging()

st.set_page_config(page_title="VK Videos", layout="wide")

# st.markdown(
#     "<style>div[data-testid='stCheckbox'] { margin-bottom: -1rem; }</style>",
#     unsafe_allow_html=True,
# )

if st.sidebar.button("Update"):
    write_last_shows_to_memory()

st.title("VK Videos")

try:
    shows = read_last_shows_from_memory()
except FileNotFoundError:
    st.info("No data yet. Click **Update** in the sidebar to fetch videos.")
    shows = {}

def checkbox_key(url):
    return f"seen_{hashlib.sha256(url.encode()).hexdigest()}"


def save_seen_state(url, key):
    set_video_seen(url, st.session_state[key])


for data in shows.values():
    video = data[0]
    date = video['date']
    title = video['title']
    url = video['url']
    key = checkbox_key(url)

    if key not in st.session_state:
        st.session_state[key] = video.get('seen', False)

    checkbox_column, text_column = st.columns([1,10])
    with checkbox_column:
        st.checkbox(
            label="Seen",
            key=key,
            on_change=save_seen_state,
            label_visibility="hidden",
            args=(url, key),
        )

    with text_column:
        st.write(f"{date} | [{title}]({url})")
