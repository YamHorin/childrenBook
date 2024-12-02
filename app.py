from openai import OpenAI
from PIL import Image
import streamlit as st
#get api key
from apiKey import apikey


st.set_page_config(page_title="demo children book app" , page_icon=":camera:" , layout="wide")
st.title("demo")

input_text = st.text_input("enter description for the book")
num_of_images = st.number_input("select the number of images you want in the book" , min_value=1 , max_value=
                                10 , value=1)

if (st.button("Genrate")):
    pass

