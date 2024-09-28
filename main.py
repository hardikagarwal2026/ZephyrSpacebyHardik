import streamlit as st
import requests
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate 
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import wikipediaapi
import warnings
import json
import re
# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

google_api_key = "AIzaSyB7zN_GFklC2F09mqxTiwf3gsBpK-MsYdw"
books_api_key = "AIzaSyCkBsGITR_52hAYdE1zlH1QnaLsuP3W8gk"

if not google_api_key:
    st.error("Google API Key is not set.")
if not books_api_key:
    st.error("Books API Key is not set.")
    
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=1,
)

books_api_endpoint = 'https://www.googleapis.com/books/v1/volumes'
def search_books(query, api_key):
    try:
        url = f'{books_api_endpoint}?q={query}&key={api_key}'
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        #st.write("We're sorry, but we couldn't find the book you're searching for. Please try refining your search or explore other titles.")
        st.markdown("<p style='color: orange;'>We're sorry, but we couldn't find the book you're searching for. Please try refining your search or explore other titles.</p>", unsafe_allow_html=True)
        return []

def get_books_with_links(query, api_key):
    books = search_books(query, api_key)
    book_details = []
    for book in books[:10]:  # Limit to 10 books
        title = book['volumeInfo'].get('title', 'N/A')
        preview_link = book['volumeInfo'].get('previewLink', '')
        if preview_link:
            book_details.append(f"<div class='book-item'><strong>{title}</strong> - <a href='{preview_link}' target='_blank'>Read Here</a></div>")
        else:
            book_details.append(f"<div class='book-item'><strong>{title}</strong> - No preview available</div>")
    return "<br>".join(book_details)

def perform_sentiment_analysis(review_text):
    prompt_template = ChatPromptTemplate.from_template(
        template="Given a review of a book {review_text}, analyze its sentiment and provide a recommendation. If the sentiment of the review is positive, recommend reading the book. If the sentiment of the review is negative, suggest trying another book as you might not enjoy this one."
    )
    
    chain = prompt_template | llm
    
    try:
        sentiment = chain.invoke({"review_text": review_text})
        return sentiment.content
    except Exception as e:
        return f"An error occurred: {e}"

def set_background_image(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_wikipedia_page(author_name):
    try:
        endpoint = 'https://en.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'titles': author_name,
            'prop': 'info',
            'inprop': 'url'
        }
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        pages = data['query']['pages']
        page = next(iter(pages.values()))

        if 'missing' in page:
            return "No information found for this author."

        page_url = page.get('fullurl', '#')
        return page_url

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_author_details(author_name):
    prompt_template = ChatPromptTemplate.from_template(
    template=("Provide detailed information about the author named {author_name}. "
              "Include the following details if available:\n"
              "- Full name: \n"
              "- Birth Date: \n"
              "- Death Date: \n"
              "- Nationality: \n"
              "- Genre(s): \n"
              "- Top 5 awards and honors: \n"
              "- Biographical summary: \n"
              "- Influences: \n"
              "- Writing style: \n"
              "- Education: \n"
              "- Occupation: \n"
              "- Personal life: \n"
              "- Literary movements: \n")
            )    
    chain = prompt_template | llm
    
    try:
        details = chain.invoke({"author_name": author_name})
        return details.content
    except Exception as e:
        return f"An error occurred: {e}"
    

image_file = "950x350-black-solid-color-background.jpg"

set_background_image(image_file)

# Navigation Sidebar
st.sidebar.title("Navigate Your Book Journey")
st.sidebar.markdown("Select a section to explore:")
section = st.sidebar.radio(
    "",
   # ("Book Search", "Book Q&A", "Customized Recommendations", "Sentiment Analysis", "Author Search")
    ("Book Search", "Book Q&A", "Customized Recommendations", "Sentiment Analysis", "Author Search", "Book Quiz")
)

# Main UI Styling
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 48px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        color: orange;
        text-align: center;
    }
    .stTextInput, .stTextArea, .stSelectbox {
        background-color: orange; 
        color: black;
    }
    .section-card {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .header {
        color: #A9A9A9;
    }
    .white-text {
        color: orange;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def generate_quiz(llm, query):
    prompt_template = ChatPromptTemplate.from_template(
    template="Generate 10 multiple-choice quiz questions based on the content of the book titled '{query}'. "
              "Each question should have 4 answer options. Ensure that the correct answer is randomly distributed among the options. "
              "Return the result as a JSON object with fields 'questions', where each question contains 'question', 'options' (as a list), and 'correct_answer'."
)

    chain = prompt_template | llm
    try:
        response = chain.invoke({"query": query})
        response_text = response.content

        # Extract JSON from the code block and clean it
        json_str = extract_and_clean_json(response_text)
        if json_str:
            try:
                quiz = json.loads(json_str)
                return quiz.get("questions", [])
            except json.JSONDecodeError:
               # st.error("There was an issue decoding the quiz data. The format might not match our expectations.")
                return None
        else:
            #st.error("We were unable to extract the quiz data. Please try again later.")
            return None

    except Exception as e:
       # st.error("We encountered a problem while generating the quiz for the entered book. We're working on resolving this and appreciate your patience.")
        return None

def extract_and_clean_json(text):
    # Find the JSON part
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        cleaned_json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL).strip()
        return cleaned_json_str
    return None

def display_quiz(quiz):
    user_answers = {}
    for i, q in enumerate(quiz):
        st.markdown(f"<div class='quiz-question' style='color: orange;'>Question {i+1}: {q['question']}</div>", unsafe_allow_html=True)
        options = q['options']
        selected_option = st.selectbox(f"Select your option for Question {i+1}:", options, key=f"q{i}")

        user_answers[i] = selected_option
    return user_answers


def calculate_score(user_answers, correct_answers):
    score = sum([1 for i, answer in user_answers.items() if answer == correct_answers[i]])
    st.markdown(f"<div style='color: orange;'>Your Score: {score} / {len(correct_answers)}</div>", unsafe_allow_html=True)
    for i, correct_answer in enumerate(correct_answers):
        user_answer = user_answers.get(i, '')
        if user_answer == correct_answer:
            st.markdown(f"<div style='color: orange;'>Question {i+1}: Correct!</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: orange;'>Question {i+1}: Incorrect! The correct answer was {correct_answer}.</div>", unsafe_allow_html=True)

    st.write("---")

st.sidebar.header("Made by Hardik Agarwal")
st.sidebar.markdown("<a href='https://www.linkedin.com/in/hardik-agarwal2004/' target='_blank' style='display: inline-block; background-color: #0077B5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>LinkedIn</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href='https://github.com/hardikagarwal2026' target='_blank' style='display: inline-block; background-color: #333; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>GitHub</a>", unsafe_allow_html=True)

# Application Title
st.markdown("<h1 class='custom-title'>Zephyr Space 📚</h1>", unsafe_allow_html=True)

if section == "Book Search":
    st.markdown('<div class="section-card"><h2 class="header">Book Search and Exploration</h2>', unsafe_allow_html=True)

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
    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Book Q&A":
    st.markdown('<div class="section-card"><h2 class="header">Book Q&A</h2>', unsafe_allow_html=True)
    
    query = st.text_input("Search for a book:")
    if query:
        books = search_books(query, books_api_key)
        selected_book = st.selectbox("Select a book for Q&A:", [book['volumeInfo'].get('title', 'N/A') for book in books] if query else [])
        question = st.text_input("Ask a question about the book:")

        if selected_book and question:
            book_info = next(book for book in books if book['volumeInfo'].get('title', 'N/A') == selected_book)
            book_summary = book_info['volumeInfo'].get('description', 'N/A')

            prompt = ChatPromptTemplate.from_template(
                   "Book Summary: {book_summary}\n\n"
                   "Question: {question}\n"
                   "Answer: If the summary contains sufficient information, use it to answer the question. "
                   "If not, use your own knowledge to provide a comprehensive answer.Don't mention in answer that you are using book summary to answer the question."
                )
            chain = prompt | llm
            
            try:
                answer = chain.invoke({"book_summary": book_summary, "question": question})
                st.markdown(f"<div class='white-text'>Answer: {answer.content}</div>", unsafe_allow_html=True)
            except Exception as e:
                #st.error(f"An error occurred: {e}")
                st.markdown("<p style='color: orange;'>We're sorry, but we are currently unable to retrieve information for this book. Please try querying another book, and we appreciate your understanding.</p>", unsafe_allow_html=True)
               # st.write("We're sorry, but we are currently unable to retrieve information for this book. Please try querying another book, and we appreciate your understanding.")
    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Customized Recommendations":
    st.markdown('<div class="section-card"><h2 class="header">Customized Book Recommendations</h2>', unsafe_allow_html=True)

    preferences = st.text_input("Enter your book preferences:")
    if preferences:
        book_links = get_books_with_links(preferences, books_api_key)
        st.markdown(f"<div class='white-text'>{book_links}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Sentiment Analysis":
    st.markdown('<div class="section-card"><h2 class="header">Sentiment Analysis</h2>', unsafe_allow_html=True)

    review_text = st.text_area("Enter the book review text for sentiment analysis:")
    if review_text:
        try:
            sentiment = perform_sentiment_analysis(review_text)
            st.markdown(f"<div class='white-text'>Sentiment: {sentiment}</div>", unsafe_allow_html=True)
        except Exception as e:
           # st.error(f"Error occurred: {e}")
           st.markdown("<p style='color: orange;'>We regret that we are currently unable to conduct sentiment analysis for this book. Kindly consider choosing a different one.</p>", unsafe_allow_html=True)
          # st.write("We regret that we are currently unable to conduct sentiment analysis for this book. Kindly consider choosing a different one.")
    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Author Search":
    st.markdown('<div class="section-card"><h2 class="header">Author Search and Information</h2>', unsafe_allow_html=True)
    
    author_name = st.text_input("Enter the author's name:")
    if author_name:
        author_info = get_author_details(author_name)
        wiki_page = get_wikipedia_page(author_name)

        st.markdown(f"<div class='white-text'>{author_info}</div>", unsafe_allow_html=True)
        
        if wiki_page:
            st.markdown(f"<div class='white-text'><a href='{wiki_page}' target='_blank'>Wikipedia Page</a></div>", unsafe_allow_html=True)
        else:
            st.warning("No Wikipedia page found for this author.")
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Book Quiz":
    st.markdown('<div class="section-card"><h2 class="header">Challenge Your Literary Acumen</h2>', unsafe_allow_html=True)

    query = st.text_input("Share the book title you're curious about for a quiz.")

    if query:
        quiz = generate_quiz(llm, query)
        if quiz:
            user_answers = display_quiz(quiz)
            if st.button("Submit"):
                correct_answers = [q['correct_answer'] for q in quiz]
                calculate_score(user_answers, correct_answers)
        else:
            st.markdown("<p style='color: orange;'>We couldn't find a quiz for the entered book at the moment. We're working to update our data and hope to have it available soon. Thank you for your patience!</p>",unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


footer = """
<style>
    footer {
        font-size: 16px;
        color: white;
        text-align: center;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.8); /* Semi-transparent black background */
        padding: 10px 0;
    }
</style>
<footer>
    ©2024 Hardik Agarwal. All rights reserved.
</footer>
"""

st.markdown(footer, unsafe_allow_html=True)
