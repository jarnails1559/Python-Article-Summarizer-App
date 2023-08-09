import streamlit as st
import requests
from bs4 import BeautifulSoup
import pyttsx3
import random
import re
from gtts import gTTS
import os

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_API_HERE"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def summarize_article(article_text, max_length=150):
    payload = {
        "inputs": article_text,
        "parameters": {"max_length": max_length, "num_beams": 4, "early_stopping": True},
    }
    response = query(payload)
    return response[0]["summary_text"]

def text_to_speech(text):
    # Generate speech using gTTS
    speech = gTTS(text, lang='en', slow=False)
    
    # Save the generated audio to a temporary file
    audio_file_path = 'temp_audio.mp3'
    speech.save(audio_file_path)
    
    # Play the generated audio
    st.audio(open(audio_file_path, 'rb').read(), format='audio/mp3')
    
    # Remove the temporary audio file
    os.remove(audio_file_path)


def get_google_search_results(prompt, num_results=10):
    url = 'https://www.google.com/search'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {'q': prompt}

    content = requests.get(url, headers=headers, params=parameters).text
    soup = BeautifulSoup(content, 'html.parser')

    search = soup.find(id='search')
    links = search.select('.tF2Cxc a')

    unique_urls = set()
    for link in links:
        url = link.get('href')
        if url and url.startswith('http'):
            unique_urls.add(url)

    return list(unique_urls)[:num_results]

def get_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = " ".join(paragraph.get_text() for paragraph in paragraphs)
        return article_text.strip()
    except Exception as e:
        print(f"Error while fetching article text: {e}")
        return None

def extract_paragraph_with_keyword(article_text, keyword):
    paragraphs = re.split(r'\n+', article_text)
    for paragraph in paragraphs:
        if keyword.lower() in paragraph.lower():
            return paragraph.strip()

    return None

def main():
    st.title("Article Summarizer")

    prompt = st.text_input("Enter a prompt to search for related articles")

    if st.button("Summarize"):
        try:
            st.write("Getting search results from Google Search...")
            search_results = get_google_search_results(prompt)

            if not search_results:
                st.error("No articles found for the given prompt.")
                return

            # Filter articles based on prompt words in URLs
            prompt_words = prompt.split()
            matching_results = []
            for url in search_results:
                if any(word.lower() in url.lower() for word in prompt_words):
                    matching_results.append(url)

            if not matching_results:
                st.error("No articles matching the prompt words in URLs.")
                return

            # Automatically choose random article from matching URLs
            chosen_url = random.choice(matching_results)
            st.write("Choosing article from URL:", chosen_url)

            # Extract the article text
            article_text = get_article_text(chosen_url)

            if not article_text:
                st.error("No article text found in the article.")
                return

    
            extracted_context = article_text

            # Summarize the extracted context using the Inference API
            st.write("Summarizing the article...")
            summary = summarize_article(extracted_context)

            st.subheader("Summary:")
            st.write(summary)

            st.subheader("Listen to the Summary:")
            st.button("Listen", on_click=text_to_speech, args=(summary,))

            # Display original article context and summary
            st.subheader("Original Article:")
            st.write(extracted_context)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
