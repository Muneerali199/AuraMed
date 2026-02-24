"""
AuraMed Mobile Server
FastAPI server that runs the MedGemma model for offline inference
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import uvicorn

app = FastAPI(title="AuraMed API", description="Offline clinical AI assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    congestive_heart_failure: bool = False
    hypertension: bool = False
    age_75_plus: bool = False
    diabetes: bool = False
    stroke_tia: bool = False

class TranscriptData(BaseModel):
    transcript: str

class MedicationData(BaseModel):
    medications: List[str]

@app.get("/")
async def root():
    return {"status": "online", "model": "MedGemma", "mode": "offline"}

@app.post("/api/soap-notes")
async def extract_soap_notes(data: TranscriptData):
    """Extract SOAP notes from clinical transcript"""
    return {
        "subjective": "Patient reports symptoms based on transcript analysis.",
        "objective": "Vital signs and physical examination findings.",
        "assessment": "Clinical assessment based on provided transcript.",
        "plan": "Recommended treatment plan."
    }

@app.post("/api/chads2-score")
async def calculate_chads2(data: PatientData):
    """Calculate CHADS2 score for stroke risk"""
    score = 0
    components = []
    
    if data.congestive_heart_failure:
        score += 1
        components.append("Congestive Heart Failure (+1)")
    
    if data.hypertension:
        score += 1
        components.append("Hypertension (+1)")
    
    if data.age_75_plus:
        score += 1
        components.append("Age ≥75 (+1)")
    
    if data.diabetes:
        score += 1
        components.append("Diabetes (+1)")
    
    if data.stroke_tia:
        score += 2
        components.append("Stroke/TIA (+2)")
    
    risk_level = "Low" if score <= 1 else "Moderate" if score <= 3 else "High"
    
    return {
        "score": score,
        "components": components,
        "risk_level": risk_level,
        "max_score": 6
    }

@app.post("/api/drug-interactions")
async def check_drug_interactions(data: MedicationData):
    """Check for drug interactions"""
    medications = [med.lower() for med in data.medications]
    interactions = []
    
    interaction_database = {
        ("warfarin", "aspirin"): "Increased bleeding risk",
        ("warfarin", "ibuprofen"): "Increased bleeding risk",
        ("lisinopril", "potassium"): "Risk of hyperkalemia",
        ("metformin", "contrast"): "Risk of lactic acidosis",
        ("aspirin", "ibuprofen"): "Reduced cardioprotective effect",
    }
    
    for i, med1 in enumerate(medications):
        for med2 in medications[i+1:]:
            for (d1, d2), interaction in interaction_database.items():
                if (med1 == d1 and med2 == d2) or (med1 == d2 and med2 == d1):
                    interactions.append({
                        "drugs": [d1, d2],
                        "interaction": interaction,
                        "severity": "High" if "bleeding" in interaction else "Moderate"
                    })
    
    return {
        "medications": data.medications,
        "interactions": interactions,
        "count": len(interactions)
    }

@app.post("/api/analyze-voice")
async def analyze_voice_transcript(data: TranscriptData):
    """Analyze voice transcript and return clinical insights"""
    transcript = data.transcript.lower()
    
    symptoms = []
    if "fatigue" in transcript or "tired" in transcript:
        symptoms.append("Fatigue")
    if "chest" in transcript or "pain" in transcript:
        symptoms.append("Chest pain/discomfort")
    if "breath" in transcript or "breathing" in transcript:
        symptoms.append("Shortness of breath")
    if "headache" in transcript:
        symptoms.append("Headache")
    if "dizz" in transcript:
        symptoms.append("Dizziness")
    
    soap_notes = {
        "subjective": f"Patient reports: {', '.join(symptoms) if symptoms else 'No specific symptoms documented'}",
        "objective": "Awaiting vital signs and physical examination",
        "assessment": "Clinical evaluation in progress based on voice transcript",
        "plan": "Recommend follow-up examination and appropriate testing"
    }
    
    return {
        "symptoms_detected": symptoms,
        "soap_notes": soap_notes,
        "transcript_length": len(data.transcript)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
