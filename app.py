import streamlit as st
import os
from video_processor import extract_audio, resize_video, chunk_if_long

st.set_page_config(page_title="🎬 Video Processor", layout="centered")
st.title("🎬 Video Processor with Audio Extract & Reels Converter")

uploaded_file = st.file_uploader("📤 Upload your video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    input_dir = "input_videos"
    os.makedirs(input_dir, exist_ok=True)
    input_path = os.path.join(input_dir, "input.mp4")

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Video uploaded successfully!")

    if st.button("⚙️ Start Processing"):
        with st.spinner("🔊 Extracting audio..."):
            extract_audio()

        with st.spinner("📱 Resizing video to vertical reel format..."):
            resize_video()

        with st.spinner("⏱ Checking duration for chunking..."):
            chunk_if_long()

        st.success("🎉 All tasks completed! Check 'processed_outputs' folder.")

else:
    st.info("📢 Please upload a video file to begin processing.")
