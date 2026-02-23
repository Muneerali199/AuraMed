"""
MTSamples Dataset Loader
Load and process medical transcription samples for testing
"""

import json
import pandas as pd
from typing import List, Dict, Any
import os

class MTSamplesLoader:
    """Loader for MTSamples medical transcription dataset"""
    
    def __init__(self):
        self.samples = self._create_sample_dataset()
    
    def _create_sample_dataset(self) -> List[Dict[str, Any]]:
        """
        Create a sample dataset of medical transcriptions
        Based on MTSamples structure
        """
        return [
            {
                "id": 1,
                "medical_specialty": "Cardiovascular / Pulmonary",
                "sample_name": "CHEST PAIN",
                "transcription": """SUBJECTIVE:
The patient is a 78-year-old male with a history of hypertension, type 2 diabetes, and atrial fibrillation who presents with complaints of chest pain radiating to his left arm, associated with shortness of breath and diaphoresis. The pain started approximately 2 hours ago while he was watching television. He describes the pain as pressure-like, 8/10 in intensity. He denies any nausea, vomiting, or syncope.

OBJECTIVE:
Vital signs: BP 160/95, HR 110, RR 22, Temp 98.6°F, SpO2 92% on room air.
Physical exam: Patient appears uncomfortable, diaphoretic. Heart: irregularly irregular rhythm, no murmurs. Lungs: clear bilaterally.
ECG: Shows atrial fibrillation with rapid ventricular response, ST elevation in leads V1-V4.
Labs: Pending.

ASSESSMENT:
1. Acute coronary syndrome, likely STEMI
2. Atrial fibrillation with rapid ventricular response
3. Hypertension
4. Type 2 diabetes mellitus

PLAN:
1. Activate cardiac catheterization lab
2. Aspirin 325 mg chewed
3. Nitroglycerin sublingual
4. Morphine for pain control
5. Start heparin drip
6. Cardiology consultation
7. Monitor CHADS2 score for anticoagulation decision""",
                "keywords": ["chest pain", "STEMI", "atrial fibrillation", "hypertension", "diabetes"]
            },
            {
                "id": 2,
                "medical_specialty": "Endocrinology",
                "sample_name": "DIABETES MANAGEMENT",
                "transcription": """SUBJECTIVE:
65-year-old female with type 2 diabetes mellitus presents for routine follow-up. She reports good adherence to her medications including metformin 1000 mg twice daily and insulin glargine 20 units nightly. Her home glucose monitoring shows fasting levels between 90-120 mg/dL and postprandial levels <180 mg/dL. She denies any episodes of hypoglycemia. She continues her diet and exercise regimen.

OBJECTIVE:
Vital signs: BP 128/82, HR 78, RR 16, Temp 98.2°F.
Weight: 85 kg, Height: 165 cm (BMI: 31.2)
Recent labs: HbA1c 6.8%, creatinine 0.9 mg/dL, eGFR >60 mL/min.
Physical exam: No acanthosis nigricans, foot exam normal.

ASSESSMENT:
1. Type 2 diabetes mellitus, well-controlled
2. Obesity (BMI 31.2)
3. Hypertension, controlled

PLAN:
1. Continue current diabetes regimen
2. Encourage weight loss of 5-10% body weight
3. Check for potential drug interactions with new medications
4. Follow-up in 3 months
5. Annual eye and foot exams scheduled""",
                "keywords": ["diabetes", "obesity", "metformin", "insulin", "HbA1c"]
            },
            {
                "id": 3,
                "medical_specialty": "Neurology",
                "sample_name": "STROKE FOLLOW-UP",
                "transcription": """SUBJECTIVE:
72-year-old male with history of ischemic stroke 6 months ago presents for follow-up. He reports good recovery with only mild residual weakness in his right hand. He denies any new neurological symptoms, falls, or seizures. He is currently on warfarin 5 mg daily for stroke prevention. He reports occasional dizziness but no syncope.

OBJECTIVE:
Vital signs: BP 142/88, HR 72, RR 18, Temp 98.4°F.
Neurological exam: Alert and oriented. Cranial nerves intact. Strength 4+/5 in right hand, otherwise 5/5. Sensation intact.
INR: 2.3 (therapeutic range)
Recent imaging: CT head shows old infarct in left MCA territory.

ASSESSMENT:
1. Status post ischemic stroke with good recovery
2. Atrial fibrillation (known)
3. Hypertension
4. CHADS2 score needs reassessment for anticoagulation therapy

PLAN:
1. Continue warfarin with current dose
2. Check drug interactions with any new medications
3. Physical therapy for hand weakness
4. Calculate CHADS2 score today
5. Follow-up in 6 months
6. Consider switching to DOAC if appropriate""",
                "keywords": ["stroke", "warfarin", "atrial fibrillation", "CHADS2", "neurology"]
            },
            {
                "id": 4,
                "medical_specialty": "General Medicine",
                "sample_name": "HYPERTENSION MANAGEMENT",
                "transcription": """SUBJECTIVE:
55-year-old male presents for hypertension management. He reports occasional headaches and fatigue. He is currently taking lisinopril 20 mg daily and hydrochlorothiazide 25 mg daily. He denies chest pain, shortness of breath, or edema. He has tried lifestyle modifications including salt restriction and exercise.

OBJECTIVE:
Vital signs: BP 148/92, HR 84, RR 16, Temp 98.0°F.
Weight: 92 kg, Height: 178 cm (BMI: 29.0)
Physical exam: Funduscopic exam shows grade 1 hypertensive retinopathy. Heart: regular rhythm, no murmurs.
Recent labs: Creatinine 1.1 mg/dL, potassium 4.2 mEq/L.

ASSESSMENT:
1. Essential hypertension, uncontrolled
2. Obesity
3. Hypertensive retinopathy

PLAN:
1. Increase lisinopril to 40 mg daily
2. Add amlodipine 5 mg daily
3. Check for drug interactions with current regimen
4. Strict blood pressure monitoring
5. Weight loss counseling
6. Follow-up in 1 month""",
                "keywords": ["hypertension", "lisinopril", "obesity", "blood pressure"]
            },
            {
                "id": 5,
                "medical_specialty": "Cardiology",
                "sample_name": "HEART FAILURE",
                "transcription": """SUBJECTIVE:
68-year-old female with systolic heart failure (EF 35%) presents with worsening dyspnea on exertion. She reports needing 3 pillows to sleep (3-pillow orthopnea) and awakening short of breath at night. She has gained 2 kg in the past week. She is currently taking furosemide 40 mg daily, lisinopril 20 mg daily, and carvedilol 6.25 mg twice daily.

OBJECTIVE:
Vital signs: BP 118/76, HR 92, RR 24, Temp 98.8°F, SpO2 94% on room air.
Weight: 70 kg (up 2 kg from last visit)
Physical exam: JVP elevated at 8 cm, bilateral crackles at lung bases, 2+ pitting edema to mid-shins.
Labs: BNP 850 pg/mL, creatinine 1.3 mg/dL.

ASSESSMENT:
1. Systolic heart failure, decompensated
2. Volume overload
3. Renal impairment

PLAN:
1. Increase furosemide to 80 mg daily
2. Continue current heart failure medications
3. Daily weight monitoring
4. Salt and fluid restriction
5. Cardiology follow-up in 1 week
6. Consider CHADS2 score calculation (has atrial fibrillation)""",
                "keywords": ["heart failure", "CHADS2", "furosemide", "lisinopril", "dyspnea"]
            }
        ]
    
    def get_all_samples(self) -> List[Dict[str, Any]]:
        """Get all sample transcriptions"""
        return self.samples
    
    def get_sample_by_id(self, sample_id: int) -> Dict[str, Any]:
        """Get specific sample by ID"""
        for sample in self.samples:
            if sample["id"] == sample_id:
                return sample
        return {}
    
    def get_samples_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        """Get samples by medical specialty"""
        return [s for s in self.samples if specialty.lower() in s["medical_specialty"].lower()]
    
    def get_samples_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Get samples containing specific keyword"""
        keyword_lower = keyword.lower()
        return [
            s for s in self.samples 
            if keyword_lower in s["transcription"].lower() or 
            any(keyword_lower in k.lower() for k in s["keywords"])
        ]
    
    def extract_structured_data(self, sample_id: int) -> Dict[str, Any]:
        """Extract structured data from a sample"""
        sample = self.get_sample_by_id(sample_id)
        if not sample:
            return {}
        
        # Simple parsing of SOAP sections (in real implementation, use NLP)
        transcription = sample["transcription"]
        
        sections = {}
        current_section = None
        current_content = []
        
        for line in transcription.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            if line.startswith('SUBJECTIVE:'):
                if current_section:
                    sections[current_section] = ' '.join(current_content)
                current_section = 'subjective'
                current_content = []
            elif line.startswith('OBJECTIVE:'):
                if current_section:
                    sections[current_section] = ' '.join(current_content)
                current_section = 'objective'
                current_content = []
            elif line.startswith('ASSESSMENT:'):
                if current_section:
                    sections[current_section] = ' '.join(current_content)
                current_section = 'assessment'
                current_content = []
            elif line.startswith('PLAN:'):
                if current_section:
                    sections[current_section] = ' '.join(current_content)
                current_section = 'plan'
                current_content = []
            elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                # Numbered list items
                current_content.append(line)
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = ' '.join(current_content)
        
        # Extract medications (simple pattern matching)
        medications = []
        med_keywords = ['mg', 'units', 'daily', 'twice', 'chewed', 'sublingual']
        for line in transcription.split('\n'):
            if any(keyword in line.lower() for keyword in med_keywords):
                # Extract medication names (simplified)
                if 'aspirin' in line.lower():
                    medications.append('aspirin')
                if 'warfarin' in line.lower():
                    medications.append('warfarin')
                if 'metformin' in line.lower():
                    medications.append('metformin')
                if 'lisinopril' in line.lower():
                    medications.append('lisinopril')
                if 'insulin' in line.lower():
                    medications.append('insulin')
                if 'atorvastatin' in line.lower():
                    medications.append('atorvastatin')
        
        # Extract conditions
        conditions = []
        condition_keywords = ['hypertension', 'diabetes', 'atrial fibrillation', 'stroke', 'obesity', 'heart failure']
        for keyword in condition_keywords:
            if keyword in transcription.lower():
                conditions.append(keyword)
        
        return {
            "sample_id": sample["id"],
            "medical_specialty": sample["medical_specialty"],
            "sample_name": sample["sample_name"],
            "sections": sections,
            "extracted_medications": list(set(medications)),
            "extracted_conditions": conditions,
            "keywords": sample["keywords"],
            "needs_chads2": any(cond in ['atrial fibrillation', 'stroke'] for cond in conditions),
            "has_medications": len(medications) > 0
        }
    
    def export_to_json(self, filepath: str):
        """Export samples to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "samples": self.samples,
                "count": len(self.samples),
                "export_date": pd.Timestamp.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, filepath: str):
        """Export samples to CSV file"""
        df = pd.DataFrame(self.samples)
        df.to_csv(filepath, index=False, encoding='utf-8')

def test_mtsamples_loader():
    """Test the MTSamples loader"""
    loader = MTSamplesLoader()
    
    print(f"Total samples: {len(loader.samples)}")
    
    # Test structured extraction
    sample_id = 1
    structured = loader.extract_structured_data(sample_id)
    
    print(f"\nSample {sample_id} - {structured['sample_name']}")
    print(f"Medical Specialty: {structured['medical_specialty']}")
    print(f"Extracted Medications: {structured['extracted_medications']}")
    print(f"Extracted Conditions: {structured['extracted_conditions']}")
    print(f"Needs CHADS2 Calculation: {structured['needs_chads2']}")
    
    # Test keyword search
    keyword = "warfarin"
    warfarin_samples = loader.get_samples_with_keyword(keyword)
    print(f"\nSamples containing '{keyword}': {len(warfarin_samples)}")
    
    # Test specialty filter
    specialty = "Cardiology"
    cardio_samples = loader.get_samples_by_specialty(specialty)
    print(f"\n'{specialty}' samples: {len(cardio_samples)}")
    
    return loader

if __name__ == "__main__":
    loader = test_mtsamples_loader()
    
    # Export data
    os.makedirs("data", exist_ok=True)
    loader.export_to_json("data/mtsamples_samples.json")
    loader.export_to_csv("data/mtsamples_samples.csv")
    
    print("\nData exported to:")
    print("- data/mtsamples_samples.json")
    print("- data/mtsamples_samples.csv")