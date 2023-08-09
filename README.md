# Article Summarizer Python App

The Article Summarizer Python App is a web application built using the Streamlit framework that allows users to quickly find articles related to a given prompt, extract key paragraphs from these articles, generate concise summaries using an AI model, and even listen to the summary using text-to-speech functionality.

## Features

- **Prompt-Based Search**: Users can input a prompt of interest to search for relevant articles on the web.

- **Article Extraction**: The app fetches search results from Google and automatically selects an article based on prompt words found in URLs.

- **Key Paragraph Extraction**: The app extracts key paragraphs from the selected article based on provided keywords.

- **AI Summarization**: Using the Hugging Face model, the app generates concise summaries for the extracted paragraphs.

- **Text-to-Speech**: Users can listen to the generated summary using text-to-speech functionality.

## How to Use

1. Enter a prompt in the provided text input field.
2. Click the "Summarize" button to initiate the process.
3. The app fetches articles related to the prompt and extracts key paragraphs.
4. The app generates a summary for the extracted paragraphs.
5. Click the "Listen" button to listen to the summary.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jarnails1559/Python-Article-Summarizer-App.git
   cd article-summarizer-app
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

## Dependencies

- Streamlit 0.89.0
- Requests 2.26.0
- BeautifulSoup4 4.10.0
- pyttsx3 2.90
- gTTS 2.2.3

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or improvements, feel free to create issues or pull requests in this repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Jass

## Acknowledgments

The app utilizes the Hugging Face model for text summarization and the gTTS library for text-to-speech functionality.
