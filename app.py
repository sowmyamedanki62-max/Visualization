import streamlit as st
import pdfplumber
import docx
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# 📄 Extract text from PDF using pdfplumber
def extract_text_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# 📄 Extract text from DOCX
def extract_text_docx(file):
    doc = docx.Document(file)
    return " ".join(para.text for para in doc.paragraphs)

# 🧹 Tokenize and clean using regex (no NLTK needed)
def get_tokens(text):
    return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

# 📊 Histogram
def plot_histogram(word_freq):
    top_words = word_freq.most_common(10)
    words, counts = zip(*top_words)
    fig, ax = plt.subplots()
    ax.bar(words, counts, color='teal')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🥧 Pie chart
def plot_pie_chart(word_freq):
    top_words = word_freq.most_common(5)
    labels, sizes = zip(*top_words)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

# 🌥️ Word cloud
def plot_wordcloud(word_freq):
    wc = WordCloud(width=800, height=400, background_color='white')
    wc.generate_from_frequencies(word_freq)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# 🚀 Streamlit UI
st.title("📚 Text Visualizer from PDF & DOCX")
uploaded_file = st.file_uploader("Upload a .pdf or .docx file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith('.pdf'):
        text = extract_text_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        text = extract_text_docx(uploaded_file)
    else:
        text = ""

    if text:
        st.subheader("Extracted Text")
        st.write(text[:500] + "..." if len(text) > 500 else text)

        tokens = get_tokens(text)
        word_freq = Counter(tokens)

        st.subheader("🔠 Word Cloud")
        plot_wordcloud(word_freq)

        st.subheader("📊 Word Frequency Histogram")
        plot_histogram(word_freq)

        st.subheader("🥧 Top Words Pie Chart")
        plot_pie_chart(word_freq)
    else:
        st.error("No text could be extracted from the file.")
