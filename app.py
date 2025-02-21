import streamlit as st
import json
from main import StoryMain

st.set_page_config(layout="wide")

# Custom CSS styling for background
st.markdown(
    f"""
    <style>
        body {{
            background-image: url('https://img.freepik.com/free-vector/dark-gradient-background-with-copy-space_53876-99548.jpg?semt=ais_hybrid');
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }}
        .main-title {{
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #00bfff;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
        }}
        .main-caption {{
            text-align: center;
            font-size: 22px;
            font-style: italic;
            color: #dcdcdc;
            margin-bottom: 20px;
        }}
        .stButton>button {{
            background-color: #007bff;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #0056b3;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='main-title'>Narrato</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='main-caption'>Turn thoughts into stories</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    user_age = st.slider("User Age", min_value=1, max_value=15, value=10, step=1)
    col1_1, col1_2 = st.columns([1, 1])
    with col1_1:
        story_genre = st.selectbox("Story Genre", options=["Adventure", "Fantasy", "Science Fiction", "Mystery", "Historical", "Comedy", "Drama", "Horror"])
    with col1_2:
        story_theme = st.text_input("Story Theme", value="Friendship")
    story_length = st.slider("Length of the Story (words)", min_value=100, max_value=1000, value=300, step=50)
    user_prompt = st.text_area("Enter your custom story prompt", value="Once upon a time...")
    art_style = st.selectbox("Select Art Style for Image Generation", options=["Realistic", "Anime", "Cartoon", "Watercolor", "Pixel Art", "Cyberpunk", "Fantasy"])
    generate_button = st.button("Generate Story")

with col2:
    if generate_button:
        main = StoryMain()
        main.generate_story(user_age, story_genre, story_theme, story_length, user_prompt)
        
        file_path = "D:/repositories/story generation data/outputs/final.json"
        with open(file_path, "r") as file:
            story_data = json.load(file)
        
        st.subheader(story_data.get("title", "Generated Story"))
        
        story_text = story_data["story"]
        image_prompts = {item["marker"]: item["image_url"] for item in story_data.get("image_prompts", [])}

        # Split story into paragraphs and track processed image markers
        story_paragraphs = story_text.split("\n\n")  
        processed_markers = set()

        for line in story_paragraphs:
            inserted_image = False  # Flag to ensure one image per marker
            for marker, image_url in image_prompts.items():
                if marker in line and marker not in processed_markers:
                    line = line.replace(marker, "")
                    processed_markers.add(marker)  # Prevent duplicate images
                    st.markdown(f"""
                        <div style="overflow: hidden; margin-bottom: 15px;">
                            <img src="{image_url}" style="float: left; max-width: 250px; margin-right: 15px; margin-bottom: 10px;"/>
                            <p style="font-size: 18px; color: white; text-align: justify; text-justify: inter-word;">{line}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    inserted_image = True
                    break  # Stop searching for other markers in this paragraph
            
            # If no image was inserted, show text normally
            if not inserted_image:
                st.markdown(f'<div style="padding: 15px; border-left: 5px solid #007bff; background: rgba(255, 255, 255, 0.1); border-radius: 5px; margin-bottom: 10px; color: white;">{line}</div>', unsafe_allow_html=True)

        st.subheader("Moral of the Story")
        st.markdown(f'<div style="font-size: 18px; font-weight: bold; background: rgba(255, 255, 255, 0.2); padding: 10px; border-radius: 5px; color: white;">{story_data.get("moral", "No moral provided.")}</div>', unsafe_allow_html=True)
    else:
        st.info("Adjust the inputs and click 'Generate Story' to create your personalized story.")
