import streamlit as st
from PIL import Image
import google.generativeai as genai
from io import BytesIO
import requests


genai.configure(api_key=st.secrets['GEMINI_API_KEY'])

st.set_page_config(page_title='ImageWrite AI - Text from Image GIAIC Growth Challenge', layout='wide')
st.title('📝Generate Text from Image and Prompt, GIAIC Growth Challenge.')
st.write('Upload an image and provide a prompt to get AI-generated insights in chunks using streaming logic!')

# 📸 Image and Prompt Inputs
image_source = st.radio("Select image source:", ('Upload Image', 'Image URL'))

image = None
if image_source == 'Upload Image':
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
else:
    image_url = st.text_input("Enter Image URL:")
    if image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Image from URL", use_column_width=True)
        except:
            st.error("Failed to load image. Check the URL.")

# ✍️ Prompdt Input
prompt = st.text_input("Enter your prompt (e.g., 'Describe this image')", value="Tell me about this image")

# 🎛️ Generate Buttom
if st.button("Generate Text"):
    if image and prompt:
        with st.spinner("🔍 Analyzing image and generating response..."):
             try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response_stream = model.generate_content([image, prompt], stream=True)

                # Create an empty placeholder to update dynamically
                result_placeholder = st.empty()
                generated_text = ""

                for chunk in response_stream:
                    if chunk.text:
                        generated_text += chunk.text  
                        result_placeholder.markdown(f"**AI's Response:**\n\n{generated_text}")  

                st.success("✅ AI Response Completed!")
             except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please upload an image and provide a prompt before generating.")

# 💡 Footer
st.markdown("---")
st.markdown("🚀 Built with ❤️ using Streamlit and Google's Gemini AI by Aans Ahmed For Sir Zia's Challenge.")
