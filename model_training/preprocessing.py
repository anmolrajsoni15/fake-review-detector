import pandas as pd
import spacy
from nltk.corpus import stopwords
from transformers import RobertaTokenizer
import numpy as np

nlp = spacy.load("en_core_web_sm")
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
stop_words = set(stopwords.words("english"))

def load_data(file_path):
    """
    Load a dataset from a CSV file, rename columns, handle missing values, and map labels.
    
    :param file_path: Path to the CSV file containing the review data.
    :return: A sampled pandas DataFrame with columns 'review_text' and 'label'.
    """
    df = pd.read_csv(file_path)
    
    df = df.rename(columns={
        "text_": "review_text",
        "label": "label"
    })
    df = df[["review_text", "label"]].dropna()
    
    df["label"] = df["label"].map({"CG": 0, "OR": 1})  # Adjust based on your dataset
    
    return df.sample(2000)

def clean_text(text):
    """
    Perform text cleaning using spaCy to remove stopwords and non-alphabetic tokens, then lemmatize the text.
    
    :param text: The raw text to be cleaned.
    :return: A cleaned string representing the lemmatized tokens.
    """
    doc = nlp(text)
    cleaned = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop
        and token.is_alpha
        and len(token) > 2
    ]
    return " ".join(cleaned)

def preprocess_data(df, test_size=0.2):
    """
    Tokenize cleaned text using a Roberta tokenizer, then split the dataset into training and test sets.
    
    :param df: Pandas DataFrame containing 'review_text' and 'label'.
    :param test_size: Fraction of data to use for testing. Defaults to 0.2.
    :return: A tuple containing encoded train/test data and the corresponding label arrays.
    """
    df["cleaned_text"] = df["review_text"].apply(clean_text)
    
    encodings = tokenizer(
        df["cleaned_text"].tolist(),
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="np"
    )
    
    indices = np.arange(len(df))
    np.random.shuffle(indices)
    split_idx = int(len(df) * (1 - test_size))
    
    return {
        "train": {k: v[indices[:split_idx]] for k, v in encodings.items()},
        "test": {k: v[indices[split_idx:]] for k, v in encodings.items()}
    }, df["label"].values[indices[:split_idx]], df["label"].values[indices[split_idx:]]

if __name__ == "__main__":
    df = load_data("data/Fake_Reviews_Detection_Dataset.csv")
    print("Sample labels:")
    print(df["label"].value_counts())