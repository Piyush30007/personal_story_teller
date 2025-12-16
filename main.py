import streamlit as st
from story_generator import generate_story_from_images, narrate_story
from PIL import Image

st.title("Your Personal Story Teller")
st.markdown(
    "Upload 1 to 10 images, choose a style, and let AI write and narrate a story for you"
)

with st.sidebar:
    st.header("Controls")

    uploaded_files = st.file_uploader(
        "Upload the images....",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    story_style = st.selectbox(
        "Choose a story style",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    generate_button = st.button("Generate Story And Narration", type="primary")


if generate_button:
    if not uploaded_files:
        st.error("Please upload at least one image")
    elif len(uploaded_files) > 10:
        st.error("Too many images (max 10)")
    else:
        with st.spinner("Generating story and narration..."):
            try:
                pil_images = [Image.open(file) for file in uploaded_files]

                st.subheader("Your visual inspiration:")
                image_columns = st.columns(len(pil_images))  # ✅ FIXED

                for i, image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, use_container_width=True)

                story_text = generate_story_from_images(pil_images, story_style)

                st.subheader(f"Your {story_style} Story:")
                st.success(story_text)

                st.subheader("Listen to your story:")
                audio_file = narrate_story(story_text)
                st.audio(audio_file, format="audio/mp3")

            except Exception as e:
                st.error(f"An application error occurred: {e}")
