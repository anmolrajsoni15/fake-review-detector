# Fake Product Review Detector

A robust machine learning project to classify product reviews as **Fake** or **Genuine** using a fine-tuned RoBERTa model. The project also includes a FastAPI-based prediction API and a Streamlit UI for interactive testing. In addition, it features a comprehensive preprocessing pipeline and leverages environment variables via a `.env` file for configuration.

---

## Table of Contents

- [Fake Product Review Detector](#fake-product-review-detector)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Data \& Preprocessing](#data--preprocessing)
  - [Model Training](#model-training)
  - [API Server](#api-server)
  - [User Interface (Streamlit)](#user-interface-streamlit)
  - [Running the Project](#running-the-project)
        - [Dashboard](#dashboard)
        - [Analysis Page](#analysis-page)
  - [Troubleshooting \& Notes](#troubleshooting--notes)
  - [Acknowledgements](#acknowledgements)

---

## Introduction

This project aims to detect fake product reviews by fine-tuning a RoBERTa model on a dataset from Kaggle ([Fake Reviews Detection Dataset](https://www.kaggle.com/datasets/mexwell/fake-reviews-dataset)). In addition to classification, it provides a user-friendly API for predictions and a Streamlit UI for demonstration purposes.

---

## Features

- **Data Preprocessing:**  
  Uses pandas, spaCy, and NLTK to clean, lemmatize, and prepare review text.
  
- **Model Training:**  
  Fine-tunes `roberta-base` using Hugging Face's Transformers and Trainer API.
  
- **Evaluation Metrics:**  
  Accuracy and weighted F1 score.
  
- **API Deployment:**  
  FastAPI provides an endpoint for making predictions.
  
- **Interactive UI:**  
  Streamlit-based front-end for user input and real-time predictions.
  
- **Environment Management:**  
  Uses a `.env` file (with `python-dotenv`) to handle sensitive data and configuration.

---

## Project Structure

```
fake-product-review-detector/
├── app/
│   ├── main.py                   # FastAPI application with prediction endpoint
│   └── ui.py                     # Streamlit UI for interactive testing
├── data/
│   └── raw/
│       └── Fake_Reviews_Detection_Dataset.csv   # Kaggle dataset file (CSV)
├── model_training/
│   ├── preprocessing.py          # Data loading, cleaning, and tokenization
│   └── train.py                  # Model training script
├── models/                       # Directory where trained model is saved
├── logs/                         # Directory for training logs
├── .env                          # Environment configuration file (not committed)
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

---

## Prerequisites

- **Python 3.8+**
- A virtual environment manager (e.g., `venv` or `conda`)
- Basic familiarity with terminal/command-line usage

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd fake-product-review-detector
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Additional Resources:**

   - Download spaCy’s English model:
     ```bash
     python -m spacy download en_core_web_sm
     ```
   - Download NLTK stopwords:
     ```bash
     python -c "import nltk; nltk.download('stopwords')"
     ```

---

## Environment Variables

This project uses a `.env` file to securely store configuration values.

1. **Create a `.env` File** in the project root:

   ```env
   # .env
   OPENAI_API_KEY=your_openai_api_key_here
   CUDA_VISIBLE_DEVICES=   # Empty value forces CPU usage (or set your GPU IDs)
   ```

2. **Usage in Code:**

   At the top of any Python file (e.g., `model_training/train.py`), add:

   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # Loads variables from .env into os.environ
   os.environ["CUDA_VISIBLE_DEVICES"] = os.getenv("CUDA_VISIBLE_DEVICES", "")
   ```

3. **Security:**

   Add `.env` to your `.gitignore` to prevent sensitive data from being committed:

   ```gitignore
   .env
   ```

---

## Data & Preprocessing

- **Dataset:**  
  Download the [Fake Reviews Detection Dataset](https://www.kaggle.com/datasets/mexwell/fake-reviews-dataset) from Kaggle and place the CSV file in `data/raw/` as `Fake_Reviews_Detection_Dataset.csv`.

- **Preprocessing:**  
  The preprocessing script (`model_training/preprocessing.py`) performs the following:
  - Reads the CSV.
  - Renames and maps columns (e.g., `"text_"` to `"review_text"`).
  - Cleans the review text using spaCy (lemmatization, stopword removal).
  - Tokenizes the cleaned text using RoBERTa's tokenizer.
  - Samples 1000 examples for training and splits into train/test sets.

---

## Model Training

The training script (`model_training/train.py`) does the following:

- Loads preprocessed data from `preprocessing.py`.
- Creates custom PyTorch datasets.
- Fine-tunes the `roberta-base` model for binary classification (Genuine vs. Fake).
- Saves the final model and tokenizer to `models/final_model`.

**To Train the Model:**

From the project root, run:

```bash
python -m model_training.train
```

You should see training logs and, upon completion, the model will be saved in the `models/final_model` directory.

---

## API Server

A FastAPI-based API is provided in `app/main.py`:

- **Endpoint:** `/predict`
- **Method:** `POST`
- **Payload:** JSON containing a `review` field.

**Example Request:**

```json
{
  "review": "This product is amazing and very sturdy."
}
```

**Response:**

```json
{
  "label": "Genuine"  // or "Fake"
}
```

**To Run the API Server:**

From the project root, run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

---

## User Interface (Streamlit)

A simple interactive UI is provided in `app/ui.py`:

- Enter a review in the text area.
- Click the **Analyze** button.
- The UI sends the review to the FastAPI endpoint and displays the prediction.

**To Run the UI:**

From the project root, run:

```bash
streamlit run app/ui.py
```

A browser window should open with the Streamlit interface.

---

## Running the Project

1. **Prepare the Environment:**
   - Clone repository, create and activate your virtual environment.
   - Install dependencies and required resources.
   - Set up your `.env` file.

2. **Download Dataset:**
   - Place the Kaggle CSV file in `data/raw/Fake_Reviews_Detection_Dataset.csv`.

3. **Train the Model:**
   ```bash
   python -m model_training.train
   ```

4. **Run the API:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Launch the UI:**
   ```bash
   streamlit run app/ui.py
   ```

##### Dashboard
<img title="dashboard" alt="dashboard" src="/assets/dashboard.png" />

##### Analysis Page
<img title="dashboard" alt="dashboard" src="/assets/analysis_page.png" />

---

## Troubleshooting & Notes

- **CUDA/CPU Issues:**  
  If you do not have a CUDA-enabled GPU, ensure that your `.env` sets `CUDA_VISIBLE_DEVICES=` (empty) and that `no_cuda=True` is passed in TrainingArguments.

- **Model Weights Warning:**  
  Some warnings about unused weights are normal when initializing a classification head from a pretrained checkpoint. They indicate that the model is being adapted for a new task.

- **Dataset Issues:**  
  If column names or data formatting cause errors, ensure that the CSV file has the expected columns (`text_` and `label`), and adjust the mapping in `preprocessing.py` as needed.

- **Environment Variables:**  
  Ensure your `.env` file is properly loaded (check with `print(os.getenv("OPENAI_API_KEY"))` in your code if needed).

---

## Acknowledgements

- **Hugging Face Transformers:** For providing robust models and APIs.
- **FastAPI:** For the efficient API framework.
- **Streamlit:** For a quick and interactive UI.
- **Kaggle:** For the dataset.
- **spaCy & NLTK:** For powerful text preprocessing and cleaning.
- **Community Contributions:** Thanks to the open-source community for the tools and libraries used in this project.

---

Happy coding and best of luck with your Fake Product Review Detector!
