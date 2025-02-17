import torch
from transformers import RobertaForSequenceClassification, RobertaTokenizer, Trainer, TrainingArguments  # Added RobertaTokenizer
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
from preprocessing import preprocess_data, load_data

# Initialize tokenizer globally
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")  # <-- Added this line

class ReviewDataset(torch.utils.data.Dataset):
    """
    A custom PyTorch Dataset for handling tokenized review data and associated labels.
    """
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        """
        Retrieve a single sample of tokenized data and the corresponding label by index.
        
        :param idx: Index into the dataset.
        :return: A dictionary of tokenized inputs and label tensor.
        """
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        """
        Return the length of the dataset.
        
        :return: Integer count of samples.
        """
        return len(self.labels)

def compute_metrics(pred):
    """
    Compute accuracy and F1 score from the model predictions.
    
    :param pred: An object containing 'predictions' and 'label_ids'.
    :return: A dictionary with 'accuracy' and 'f1'.
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted")
    }

def train_model():
    """
    Train a Roberta model on the preprocessed dataset, then save the trained model and tokenizer.
    
    :return: None
    """
    # Load preprocessed data
    df = load_data("data/Fake_Reviews_Detection_Dataset.csv")
    encodings, train_labels, test_labels = preprocess_data(df)
    
    # Create datasets
    train_dataset = ReviewDataset(encodings["train"], train_labels)
    test_dataset = ReviewDataset(encodings["test"], test_labels)
    
    # Model configuration
    model = RobertaForSequenceClassification.from_pretrained(
        "roberta-base",
        num_labels=2,
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="model/",
        num_train_epochs=4,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="logs/",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=10
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )
    
    # Train and save
    print("Starting training...")
    trainer.train()
    trainer.save_model("model/final_model")
    tokenizer.save_pretrained("model/final_model")  # Now uses the global tokenizer
    print("Training complete! Model saved.")

if __name__ == "__main__":
    train_model()