import streamlit as st

story_generation_page = st.Page(
    page= "app.py",
    title="Story Generator",
    default= True,
)

writing_assistent_page = st.Page(
    page= "writing_assistent_page.py",
    title="Writing Assistant",
)

images_for_story_page = st.Page(
    page= "images_for_story.py",
    title="Images for Story",
)

pg = st.navigation(pages=[story_generation_page, writing_assistent_page, images_for_story_page])
pg.run()