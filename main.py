import streamlit as st
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import base64
from dotenv import load_dotenv
load_dotenv()

google_api_key = "AIzaSyB7zN_GFklC2F09mqxTiwf3gsBpK-MsYdw"
books_api_key = "AIzaSyCkBsGITR_52hAYdE1zlH1QnaLsuP3W8gk"

if not google_api_key:
    st.error("Google API Key is not set.")
if not books_api_key:
    st.error("Books API Key is not set.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",temperature=0)


books_api_endpoint = 'https://www.googleapis.com/books/v1/volumes'

def search_books(query, api_key):
    try:
        url = f'{books_api_endpoint}?q={query}&key={api_key}'
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return []


def set_background_image(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: contain;
            background-repeat: repeat;
            background-attachment: fixed;
            height: 100vh; /* Set height to full viewport height */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

image_file = "950x350-black-solid-color-background.jpg"

set_background_image(image_file)

st.markdown(
    """
    <style>
    .custom-title {
        font-size: 48px; /* Adjust font size */
        font-weight: bold; /* Make text bold */
        font-family: 'Arial', sans-serif; /* Change font family if needed */
        color: orange; /* Adjust text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.components.v1.html(
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="google-site-verification" content="etMwlH9VoJYC60f30C0QCUPpzTH8Dk67s-TmyjhEEnU" />
    </head>
    <body>
    </body>
    </html>
    """,
    height=0,  # Set to 0 so it doesn't take up any space
)

st.markdown("<h1 class='custom-title'>Zephyr Space 📚</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stTextInput {
        background-color: #E1C48F; /* RGB(225, 196, 143) */
        color: black; /* Adjust text color as needed */
    }

    .stTextArea {
        background-color: #E1C48F; /* RGB(225, 196, 143) */
        color: black; /* Adjust text color as needed */
    }

    .stSelectbox {
        background-color: #E1C48F; /* RGB(225, 196, 143) */
        color: black; /* Adjust text color as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .white-text {
        color: orange;
    }
    .header {
        color: #A9A9A9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="header">Book Search and Exploration</h1>', unsafe_allow_html=True)

query = st.text_input("Search for a book:")

if query:
    books = search_books(query, books_api_key)
    if books:
        for book in books:
            st.markdown(f"<div class='white-text'><strong>Title:</strong> {book['volumeInfo'].get('title', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='white-text'><strong>Authors:</strong> {', '.join(book['volumeInfo'].get('authors', []))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='white-text'><strong>Publisher:</strong> {book['volumeInfo'].get('publisher', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='white-text'><strong>Published Date:</strong> {book['volumeInfo'].get('publishedDate', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='white-text'><strong>Description:</strong> {book['volumeInfo'].get('description', 'N/A')}</div>", unsafe_allow_html=True)
            
            thumbnail = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
            if thumbnail:
                st.image(thumbnail)
            
            st.markdown("<div class='white-text'><strong>Read Book:</strong></div>", unsafe_allow_html=True)
            if 'previewLink' in book['volumeInfo']:
                preview_link = book['volumeInfo']['previewLink']
                st.markdown(f"<div class='white-text'><a href='{preview_link}' target='_blank'>Read Here</a></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='white-text'>No preview available.</div>", unsafe_allow_html=True)
            st.write("---")
    else:
        st.markdown("<div class='white-text'>No books found. Please try searching a different book.</div>", unsafe_allow_html=True)

st.markdown('<h1 class="header">Book Q&A</h1>', unsafe_allow_html=True)
selected_book = st.selectbox("Select a book for Q&A:", [book['volumeInfo'].get('title', 'N/A') for book in books] if query else [])
question = st.text_input("Ask a question about the book:")

if selected_book and question:
    book_info = next(book for book in books if book['volumeInfo'].get('title', 'N/A') == selected_book)
    book_summary = book_info['volumeInfo'].get('description', 'N/A')

    prompt = (f"Book Summary: {book_summary}\n\n"
              f"Question: {question}\n"
              "Answer: If the summary contains sufficient information, use it to answer the question. "
              "If not, use your own knowledge to provide a comprehensive answer.")

    prompt_template = PromptTemplate(
        input_variables=["prompt"], 
        template="{prompt}")

    chain = LLMChain(llm=llm, prompt=prompt_template)

    try:
        answer = chain({"prompt": prompt})
        text_answer = answer["text"]

        st.markdown(f"<div class='white-text'>{text_answer}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error occurred: {e}")

st.markdown('<h1 class="header">Personalized Book Recommendations</h1>', unsafe_allow_html=True)
preferences = st.text_input("Enter your reading preferences:")
if preferences:
    prompt_template = PromptTemplate(
        input_variables=["preferences"], 
        template="Recommend books based on these preferences: {preferences}"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    try:
        recommendations = chain({"preferences": preferences})
        
        if "text" in recommendations:
            text_recommendations = recommendations["text"]
            
            if text_recommendations:
                st.write("<span style='color: orange;'>Recommended Books:</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='white-text'>{text_recommendations}</div>", unsafe_allow_html=True)
            else:
                st.warning("No recommendations found based on your preferences.")
        else:
            st.warning("No recommendations found based on your preferences.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown('<h1 class="header">Sentiment Analysis of Book Reviews</h1>', unsafe_allow_html=True)
review_text = st.text_area("Enter a book review:")
if review_text:
    prompt_template = PromptTemplate(
        input_variables=["review_text"],
        template="Given a review of a book {review_text}, analyze its sentiment and provide a recommendation. If the sentiment of the review is positive, recommend reading the book. If the sentiment of the review is negative, suggest trying another book as you might not enjoy this one."
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    sentiment = chain({"review_text": review_text})
    text_sentiment = sentiment["text"]
    st.write("<span style='color: orange;'>Sentiment Analysis:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='white-text'>{text_sentiment}</div>", unsafe_allow_html=True)

st.markdown('<h1 class="header">Personalized Reading Lists</h1>', unsafe_allow_html=True)
reading_preferences = st.text_input("Enter your reading preferences for a list:")

if reading_preferences:
    prompt_template = PromptTemplate(
        input_variables=["reading_preferences"],
        template="Generate a personalized reading list based on these preferences: {reading_preferences}"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    try:
        reading_list = chain({"reading_preferences": reading_preferences})
        
        if "text" in reading_list:
            text_reading_list = reading_list["text"]
           
            if text_reading_list:
                st.write("<span style='color: orange;'>Your Personalized Reading List:</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='white-text'>{text_reading_list}</div>", unsafe_allow_html=True)
            else:
                st.warning("No books found based on your preferences.")
        else:
            st.warning("No books found based on your preferences.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
