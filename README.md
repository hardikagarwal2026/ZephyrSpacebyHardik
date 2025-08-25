# Zephyr Space: Your Ultimate Book Journey

Welcome to **Zephyr Space**, a comprehensive web application designed to enhance your reading experience through intelligent book discovery, AI-powered insights, and interactive learning tools.

## Overview

Zephyr Space is a Streamlit-based web application that combines the power of Google Books API, Google's Gemini AI model, and Wikipedia to create a one-stop platform for book enthusiasts. Whether you're searching for your next read, analyzing book reviews, or testing your literary knowledge, this application provides all the tools you need.

## Features

### Book Search & Exploration
- **Comprehensive Search**: Find books by title, author, or keywords
- **Detailed Information**: Access book details including descriptions, authors, publishers, and publication dates
- **Preview Links**: Direct access to book previews when available through Google Books
- **Book Covers**: Visual representation of books with thumbnail images

### AI-Powered Book Q&A
- **Intelligent Responses**: Ask questions about any book and receive AI-generated answers
- **Context-Aware**: AI analyzes book summaries and provides relevant information
- **Knowledge Enhancement**: When book context is insufficient, AI supplements with additional knowledge

### Sentiment Analysis
- **Review Analysis**: Input book reviews to receive sentiment analysis
- **Reading Recommendations**: Get AI-powered suggestions on whether to read a book based on review sentiment
- **Insightful Feedback**: Understand the emotional tone of reviews before making reading decisions

### Author Information
- **Comprehensive Biographies**: Access detailed author information including birth dates, nationalities, and literary movements
- **Awards & Honors**: Discover authors' achievements and recognition
- **Writing Style Analysis**: Learn about authors' unique writing approaches and influences
- **Wikipedia Integration**: Direct links to author Wikipedia pages for additional research

### Personalized Recommendations
- **Custom Preferences**: Input your reading preferences to receive tailored book suggestions
- **Curated Lists**: Get personalized book recommendations based on your interests
- **Discovery Engine**: Find new authors and genres that match your taste

### Interactive Book Quiz
- **Knowledge Testing**: Challenge yourself with 10 multiple-choice questions about any book
- **Instant Scoring**: Receive immediate feedback on your performance
- **Learning Tool**: Use quizzes to reinforce your understanding of book content
- **Adaptive Questions**: AI-generated questions based on book content

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Google API key for Gemini AI
- Google Books API key

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hardikagarwal2026/zephyr-space.git
   cd zephyr-space
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your-google-api-key
   BOOKS_API_KEY=your-google-books-api-key
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the application**
   Open your web browser and navigate to the URL displayed in the terminal (typically `http://localhost:8501`)

## How to Use

### Getting Started
1. Launch the application using the sidebar navigation
2. Choose from six main sections based on your needs
3. Input your queries or preferences in the provided text fields
4. Explore results and interact with the AI-powered features

### Navigation
- **Book Search**: Find and explore books with detailed information
- **Book Q&A**: Ask questions about specific books
- **Customized Recommendations**: Get personalized book suggestions
- **Sentiment Analysis**: Analyze book review sentiments
- **Author Search**: Discover author information and biographies
- **Book Quiz**: Test your knowledge with interactive quizzes

## Technical Architecture

### Backend Technologies
- **Python**: Core application logic and data processing
- **Streamlit**: Web application framework for interactive user interface
- **LangChain**: AI framework for natural language processing and AI interactions
- **Google Gemini**: Advanced language model for intelligent responses

### API Integrations
- **Google Books API**: Comprehensive book database and metadata
- **Wikipedia API**: Author information and biographical data
- **Google AI Services**: Gemini model for natural language understanding

### Key Components
- **Modular Design**: Separate functions for each feature area
- **Error Handling**: Robust error handling for API failures and edge cases
- **Session Management**: Persistent quiz state and user interactions
- **Responsive UI**: Clean, intuitive interface with consistent styling

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for AI-powered features using Gemini
- `BOOKS_API_KEY`: Required for accessing Google Books API


## Troubleshooting

### Common Issues
- **API Key Errors**: Ensure both Google API keys are properly set in your `.env` file
- **No Results**: Check your internet connection and API key validity
- **Quiz Generation Issues**: Some books may not have sufficient content for quiz generation

## Contributing

We welcome contributions to improve Zephyr Space! Here's how you can help:

1. Fork the repository
2. Create a feature branch for your changes
3. Implement your improvements or bug fixes
4. Test thoroughly to ensure functionality
5. Submit a pull request with detailed descriptions


## Author

**Hardik Agarwal**
- LinkedIn: [Hardik Agarwal](https://www.linkedin.com/in/hardik-agarwal2004/)
- GitHub: [hardikagarwal2026](https://github.com/hardikagarwal2026)

---

**Zephyr Space** - Transforming the way you discover, explore, and engage with literature through intelligent technology and comprehensive book resources.
