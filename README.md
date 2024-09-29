📚 **Zephyr Space: Your Ultimate Book Journey** 🌟

Welcome to **Zephyr Space**, a dynamic web application designed to elevate your reading experience! Whether you're searching for your next great read, diving into book recommendations, analyzing reviews, or even challenging yourself with book-themed quizzes, we've got you covered. 🚀

🚀 **Features:**

🔍 **Book Search & Exploration**

Easily find and explore books with just a few clicks. Get detailed information about titles, authors, and descriptions. Search and start reading immediately if a preview is available! 💡

>**Search by title, author, or keywords** to discover your next favorite book.

>Preview available books directly in the app with a link to the full text.

>📖 **Preview** links for available books.

🤖 **Book Q&A (Powered by AI)**

Got questions about a book? Ask anything, and our AI will provide intelligent answers based on the book's content! ❓💬

>**AI-Powered Q&A:** Ask questions and receive insightful answers related to the book you're exploring.

📊 **Sentiment Analysis of Book Reviews**

Analyze the sentiment of book reviews and decide whether it’s worth a read! 😊😟

>**Sentiment Analysis:** Get an AI-generated review sentiment (positive or negative) along with recommendations on whether you should read the book.

👨‍🏫 **Author Search**

Explore detailed biographies of your favorite authors and learn about their literary journey. From their full name to their literary influences, discover it all! ✍️

>**Author Bio**: Full name, birthdate, genres, awards, and even a biography for your favorite authors.

🎯 **Customized Book Recommendations**

Not sure what to read next? We provide personalized book recommendations based on your preferences! 🎯📚

🎮 **Fun Book Quiz**

Test your book knowledge with a fun multiple-choice quiz based on the book of your choice! 🧠🎉

>**10 Quiz Questions:** Take a quiz about the book, test your knowledge, and get your score immediately.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🛠️ **Installation:**
To get started with Zephyr Space, follow these steps:

1. **Clone the repository:**

git clone https://github.com/yourusername/zephyr-space.git

2. **Install dependencies:** Make sure you have Python 3.11 or above. You can install all necessary packages with:

pip install -r requirements.txt

3. **Set up your environment variables:** Create a .env file in the root of the project and add your API keys:

env
GOOGLE_API_KEY=your-google-api-key
BOOKS_API_KEY=your-google-books-api-key

4. **Run the application:** Once everything is set up, you can run the app using Streamlit:

streamlit run main.py

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📚 **How It Works:**
1. **Book Search:** Enter the name of the book in the search bar and explore various titles. The app fetches book data using the Google Books API. You'll get a brief description, authors, and a preview link to start reading! 🎉

2. **Book Q&A:** Type your book-related question, and our AI (powered by the Gemini language model) will generate accurate answers for you. 🤖

3. **Sentiment Analysis:** Input a review of any book, and our AI will analyze whether the sentiment is positive or negative and give a reading recommendation. 📊

4. **Author Search:** Learn more about your favorite authors, including their biographical details, awards, and writing style. Just enter their name and discover all! 👨‍🏫

5. **Customized Recommendations:** Based on your input, get personalized book recommendations to fit your unique tastes. 🎯

6. **Book Quiz:** Take a fun quiz to test your knowledge about any book. Get instant feedback and see how well you score. 🎮
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🛠️ **Technologies Used:**

>**Python**: Backend logic.

>**Streamlit**: Interactive web app development.

>**LangChain**: For AI-powered Q&A, sentiment analysis, and author information.

>**Google Books API**: For fetching book data.

>**Wikipedia API**: To retrieve author biographies.

🌟 **Contributing:**

Feel free to contribute to this project! Whether it's adding new features, fixing bugs, or improving documentation, all contributions are welcome. Create a fork, make your changes, and submit a pull request
