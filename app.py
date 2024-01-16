import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input , image[0] , prompt ])
    return response.text


def image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts =[
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="CAR PRICE PREDICTOR USING GEMINI")

st.header("CAR ANALYZER using GEMINI")
input = "Tell me the car model and car price and some specifications regarding it"
uploaded_file = st.file_uploader("Choose a image ..... " , type=["jpg","jpeg",'png'])
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image , width = 350)


submit = st.button("ANALYZE THE CAR")

input_prompt = """
You are a expert in predicting car models and their price based on image you have shown . You will find the correct model of car corresponding to image and also tell the near about price of that car . Tell me some of major aspecifications of car too. The fromat will be 

**Car Brand** : 

**Car Model** :

**Car Price** :

Some of Car Specifications : 
1.
2.
3.
"""

if submit:
    image_data = image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Response : ")
    st.write(response)
