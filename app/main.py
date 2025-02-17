import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from explanation.enhanced_explain import generate_enhanced_explanation
import json

app = FastAPI(
    title="Fake Product Review Detector API",
    description="API that classifies product reviews and provides a detailed explanation.",
    version="1.0.0"
)

class ReviewRequest(BaseModel):
    review: str

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/final_model")
tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH)
model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH)

@app.post("/predict_with_explanation", summary="Predict review authenticity with explanation")
def predict_with_explanation(review_req: ReviewRequest):
    """
    Predict the authenticity of a review and generate an explanation.
    
    :param review_req: Request body containing a 'review' string.
    :return: JSON response with predicted label, summary, and explanation of the review.
    """
    try:
        inputs = tokenizer(review_req.review, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
        print(f"Prediction: {prediction}")
        label = "Fake" if prediction == 1 else "Genuine"
        
        explanation_result = generate_enhanced_explanation(review_req.review, label)
        return {
            "label": label,
            "summary": explanation_result.get("summary", ""),
            "explanation": explanation_result.get("explanation", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import asyncio
from fastapi.responses import StreamingResponse
from explanation.enhanced_explain import generate_explanation_stream

@app.post("/predict_with_explanation_stream", summary="Predict review authenticity with streaming explanation")
async def predict_with_explanation_stream(review_req: ReviewRequest):
    """
    Predict the authenticity of a review and stream the explanation tokens as they are generated.
    
    :param review_req: Request body containing a 'review' string.
    :return: A streaming response of JSON objects, each containing partial explanation tokens.
    """
    try:
        inputs = tokenizer(review_req.review, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
        label = "Fake" if prediction == 1 else "Genuine"
        
        summary, token_iter = generate_explanation_stream(review_req.review, label)
        
        async def event_generator():
            header = {"type": "header", "label": label, "summary": summary}
            yield f"data: {json.dumps(header)}\n\n"
            explanation_text = ""
            for token in token_iter:
                explanation_text += token
                payload = {"type": "token", "token": token, "explanation": explanation_text}
                yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0)  # yield control
            yield f"data: {json.dumps({'type': 'end'})}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
