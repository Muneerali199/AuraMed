"""
Clinical Tools for AuraMed Agent
Implementation of medical tools for clinical workflow
"""

import json
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PatientInfo:
    """Patient information structure"""
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    blood_pressure: str
    heart_rate: int
    temperature: float
    oxygen_saturation: float

class ClinicalTools:
    """Collection of clinical tools for medical workflow"""
    
    def __init__(self):
        # Mock drug interaction database
        self.drug_interaction_db = self._load_drug_interaction_db()
        
        # Clinical guidelines and scoring systems
        self.clinical_scores = {
            "chads2": self._chads2_guidelines(),
            "bmi": self._bmi_categories(),
            "map": self._map_categories(),
            "gcs": self._glasgow_coma_scale()
        }
    
    def _load_drug_interaction_db(self) -> Dict[str, Dict]:
        """Load mock drug interaction database"""
        return {
            "warfarin": {
                "category": "anticoagulant",
                "interactions": [
                    {"drug": "aspirin", "severity": "high", "effect": "Increased bleeding risk", "recommendation": "Monitor INR closely"},
                    {"drug": "ibuprofen", "severity": "moderate", "effect": "Increased bleeding risk", "recommendation": "Use with caution"},
                    {"drug": "omeprazole", "severity": "low", "effect": "Reduced absorption", "recommendation": "Monitor effectiveness"},
                    {"drug": "antibiotics", "severity": "high", "effect": "Increased INR", "recommendation": "Adjust dose as needed"}
                ]
            },
            "metformin": {
                "category": "antidiabetic",
                "interactions": [
                    {"drug": "alcohol", "severity": "high", "effect": "Risk of lactic acidosis", "recommendation": "Avoid alcohol consumption"},
                    {"drug": "contrast_dye", "severity": "high", "effect": "Renal impairment risk", "recommendation": "Hold 48 hours before procedure"}
                ]
            },
            "lisinopril": {
                "category": "ace_inhibitor",
                "interactions": [
                    {"drug": "potassium_supplements", "severity": "moderate", "effect": "Hyperkalemia", "recommendation": "Monitor potassium levels"},
                    {"drug": "nsaids", "severity": "moderate", "effect": "Reduced antihypertensive effect", "recommendation": "Monitor blood pressure"}
                ]
            },
            "atorvastatin": {
                "category": "statin",
                "interactions": [
                    {"drug": "grapefruit_juice", "severity": "moderate", "effect": "Increased statin levels", "recommendation": "Avoid grapefruit products"},
                    {"drug": "erythromycin", "severity": "high", "effect": "Increased risk of myopathy", "recommendation": "Consider alternative"}
                ]
            },
            "insulin": {
                "category": "antidiabetic",
                "interactions": [
                    {"drug": "beta_blockers", "severity": "moderate", "effect": "Masked hypoglycemia symptoms", "recommendation": "Educate patient on symptoms"}
                ]
            }
        }
    
    def _chads2_guidelines(self) -> Dict:
        """CHADS2 scoring guidelines"""
        return {
            "congestive_heart_failure": {"points": 1, "description": "Congestive heart failure"},
            "hypertension": {"points": 1, "description": "Hypertension"},
            "age_75": {"points": 1, "description": "Age ≥ 75 years"},
            "diabetes": {"points": 1, "description": "Diabetes mellitus"},
            "stroke_tia": {"points": 2, "description": "Stroke/TIA history"},
            "risk_stratification": {
                0: {"risk": "Low", "stroke_rate": "0.6%/year", "therapy": "Aspirin or no therapy"},
                1: {"risk": "Low", "stroke_rate": "1.9%/year", "therapy": "Anticoagulation considered"},
                2: {"risk": "Moderate", "stroke_rate": "2.8%/year", "therapy": "Anticoagulation recommended"},
                3: {"risk": "Moderate", "stroke_rate": "3.9%/year", "therapy": "Anticoagulation recommended"},
                4: {"risk": "High", "stroke_rate": "5.9%/year", "therapy": "Anticoagulation recommended"},
                5: {"risk": "High", "stroke_rate": "7.3%/year", "therapy": "Anticoagulation recommended"},
                6: {"risk": "High", "stroke_rate": "9.8%/year", "therapy": "Anticoagulation recommended"}
            }
        }
    
    def _bmi_categories(self) -> Dict:
        """BMI categories"""
        return {
            "underweight": {"range": (0, 18.4), "risk": "Increased mortality"},
            "normal": {"range": (18.5, 24.9), "risk": "Lowest risk"},
            "overweight": {"range": (25.0, 29.9), "risk": "Increased risk"},
            "obese_class1": {"range": (30.0, 34.9), "risk": "High risk"},
            "obese_class2": {"range": (35.0, 39.9), "risk": "Very high risk"},
            "obese_class3": {"range": (40.0, 100.0), "risk": "Extremely high risk"}
        }
    
    def _map_categories(self) -> Dict:
        """Mean Arterial Pressure categories"""
        return {
            "hypotension": {"range": (0, 59), "action": "Consider fluid resuscitation"},
            "normal": {"range": (60, 99), "action": "Monitor"},
            "mild_hypertension": {"range": (100, 109), "action": "Lifestyle modifications"},
            "moderate_hypertension": {"range": (110, 129), "action": "Consider medication"},
            "severe_hypertension": {"range": (130, 1000), "action": "Urgent treatment"}
        }
    
    def _glasgow_coma_scale(self) -> Dict:
        """Glasgow Coma Scale"""
        return {
            "eye_response": {
                4: "Spontaneous",
                3: "To speech",
                2: "To pain",
                1: "None"
            },
            "verbal_response": {
                5: "Oriented",
                4: "Confused",
                3: "Inappropriate words",
                2: "Incomprehensible sounds",
                1: "None"
            },
            "motor_response": {
                6: "Obeys commands",
                5: "Localizes pain",
                4: "Withdrawal from pain",
                3: "Flexion to pain",
                2: "Extension to pain",
                1: "None"
            }
        }
    
    def extract_soap_notes(self, transcript: str) -> Dict[str, str]:
        """
        Extract structured SOAP notes from clinical transcript
        """
        # Analyze transcript for key components
        subjective_keywords = ["reports", "complains", "states", "describes", "feels", "experiences"]
        objective_keywords = ["exam", "findings", "results", "measurements", "vitals", "lab", "imaging"]
        assessment_keywords = ["diagnosis", "impression", "assessment", "likely", "probable", "consistent with"]
        plan_keywords = ["plan", "recommend", "order", "prescribe", "follow-up", "monitor"]
        
        # Simple extraction logic (in production, this would use NLP)
        lines = transcript.split('. ')
        
        subjective = []
        objective = []
        assessment = []
        plan = []
        
        for line in lines:
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in subjective_keywords):
                subjective.append(line.strip())
            elif any(keyword in line_lower for keyword in objective_keywords):
                objective.append(line.strip())
            elif any(keyword in line_lower for keyword in assessment_keywords):
                assessment.append(line.strip())
            elif any(keyword in line_lower for keyword in plan_keywords):
                plan.append(line.strip())
        
        # Default values if extraction fails
        if not subjective:
            subjective = ["Patient reports symptoms as described in transcript."]
        if not objective:
            objective = ["Physical exam findings and vitals not specified in transcript."]
        if not assessment:
            assessment = ["Clinical assessment based on presented symptoms and history."]
        if not plan:
            plan = ["Follow up as needed, consider additional testing."]
        
        return {
            "subjective": " ".join(subjective),
            "objective": " ".join(objective),
            "assessment": " ".join(assessment),
            "plan": " ".join(plan),
            "extraction_confidence": "high" if len(lines) > 3 else "medium"
        }
    
    def calculate_chads2_score(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate CHADS2 score for stroke risk assessment
        """
        score = 0
        components = []
        details = []
        
        guidelines = self.clinical_scores["chads2"]
        
        # Calculate score
        if patient_data.get("congestive_heart_failure", False):
            score += guidelines["congestive_heart_failure"]["points"]
            components.append("CHF")
            details.append(f"Congestive Heart Failure: +{guidelines['congestive_heart_failure']['points']}")
        
        if patient_data.get("hypertension", False):
            score += guidelines["hypertension"]["points"]
            components.append("HTN")
            details.append(f"Hypertension: +{guidelines['hypertension']['points']}")
        
        if patient_data.get("age", 0) >= 75:
            score += guidelines["age_75"]["points"]
            components.append("Age≥75")
            details.append(f"Age ≥75: +{guidelines['age_75']['points']}")
        
        if patient_data.get("diabetes", False):
            score += guidelines["diabetes"]["points"]
            components.append("DM")
            details.append(f"Diabetes: +{guidelines['diabetes']['points']}")
        
        if patient_data.get("stroke_tia_history", False):
            score += guidelines["stroke_tia"]["points"]
            components.append("Stroke/TIA")
            details.append(f"Stroke/TIA History: +{guidelines['stroke_tia']['points']}")
        
        # Get risk stratification
        risk_info = guidelines["risk_stratification"].get(score, {
            "risk": "Unknown",
            "stroke_rate": "N/A",
            "therapy": "Consult guidelines"
        })
        
        return {
            "score": score,
            "components": components,
            "details": details,
            "risk_level": risk_info["risk"],
            "annual_stroke_risk": risk_info["stroke_rate"],
            "therapy_recommendation": risk_info["therapy"],
            "score_interpretation": self._interpret_chads2_score(score)
        }
    
    def _interpret_chads2_score(self, score: int) -> str:
        """Interpret CHADS2 score"""
        interpretations = {
            0: "Low stroke risk - aspirin or no therapy may be sufficient",
            1: "Low stroke risk - anticoagulation should be considered",
            2: "Moderate stroke risk - anticoagulation is recommended",
            3: "Moderate stroke risk - anticoagulation is strongly recommended",
            4: "High stroke risk - anticoagulation is essential",
            5: "High stroke risk - anticoagulation is essential",
            6: "High stroke risk - anticoagulation is essential"
        }
        return interpretations.get(score, "Consult stroke risk guidelines")
    
    def check_drug_interactions(self, drugs: List[str]) -> Dict[str, Any]:
        """
        Check for potential drug interactions
        """
        interactions_found = []
        warnings = []
        recommendations = []
        
        for drug in drugs:
            drug_lower = drug.lower()
            
            # Check if drug is in database
            for db_drug, info in self.drug_interaction_db.items():
                if db_drug in drug_lower or drug_lower in db_drug:
                    # Check interactions with other drugs in the list
                    for other_drug in drugs:
                        if other_drug.lower() != drug_lower:
                            for interaction in info["interactions"]:
                                if interaction["drug"] in other_drug.lower():
                                    interactions_found.append({
                                        "primary_drug": drug,
                                        "interacting_drug": other_drug,
                                        "severity": interaction["severity"],
                                        "effect": interaction["effect"],
                                        "recommendation": interaction["recommendation"]
                                    })
                    
                    # Add general warnings for this drug
                    warnings.append({
                        "drug": drug,
                        "category": info["category"],
                        "general_warnings": [f"Be cautious with {interaction['drug']}" for interaction in info["interactions"]]
                    })
        
        # Generate recommendations
        if interactions_found:
            high_severity = [i for i in interactions_found if i["severity"] == "high"]
            moderate_severity = [i for i in interactions_found if i["severity"] == "moderate"]
            
            if high_severity:
                recommendations.append("⚠️ HIGH RISK INTERACTIONS DETECTED - Immediate attention required")
                for interaction in high_severity:
                    recommendations.append(f"- {interaction['primary_drug']} + {interaction['interacting_drug']}: {interaction['effect']}")
            
            if moderate_severity:
                recommendations.append("⚠️ Moderate risk interactions - Monitor closely")
                for interaction in moderate_severity:
                    recommendations.append(f"- {interaction['primary_drug']} + {interaction['interacting_drug']}: {interaction['effect']}")
        else:
            recommendations.append("✅ No significant drug interactions detected")
        
        return {
            "drugs_checked": drugs,
            "interactions_found": len(interactions_found) > 0,
            "interaction_details": interactions_found,
            "warnings": warnings,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> Dict[str, Any]:
        """Calculate BMI and categorize"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        category = "unknown"
        risk = "unknown"
        
        for cat_name, cat_info in self.clinical_scores["bmi"].items():
            if cat_info["range"][0] <= bmi <= cat_info["range"][1]:
                category = cat_name
                risk = cat_info["risk"]
                break
        
        return {
            "bmi": round(bmi, 1),
            "category": category,
            "risk_level": risk,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "interpretation": self._interpret_bmi(bmi)
        }
    
    def _interpret_bmi(self, bmi: float) -> str:
        """Interpret BMI value"""
        if bmi < 18.5:
            return "Underweight - Consider nutritional assessment"
        elif 18.5 <= bmi < 25:
            return "Normal weight - Maintain healthy lifestyle"
        elif 25 <= bmi < 30:
            return "Overweight - Consider weight management"
        elif 30 <= bmi < 35:
            return "Obesity Class I - Weight loss recommended"
        elif 35 <= bmi < 40:
            return "Obesity Class II - Medical intervention recommended"
        else:
            return "Obesity Class III - Urgent medical intervention needed"
    
    def calculate_map(self, systolic: int, diastolic: int) -> Dict[str, Any]:
        """Calculate Mean Arterial Pressure"""
        map_value = diastolic + (1/3) * (systolic - diastolic)
        
        category = "unknown"
        action = "unknown"
        
        for cat_name, cat_info in self.clinical_scores["map"].items():
            if cat_info["range"][0] <= map_value <= cat_info["range"][1]:
                category = cat_name
                action = cat_info["action"]
                break
        
        return {
            "map": round(map_value, 1),
            "category": category,
            "recommended_action": action,
            "systolic": systolic,
            "diastolic": diastolic,
            "interpretation": self._interpret_map(map_value)
        }
    
    def _interpret_map(self, map_value: float) -> str:
        """Interpret MAP value"""
        if map_value < 60:
            return "Hypotension - Consider fluid resuscitation"
        elif 60 <= map_value < 100:
            return "Normal MAP - Continue monitoring"
        elif 100 <= map_value < 110:
            return "Mild hypertension - Lifestyle modifications"
        elif 110 <= map_value < 130:
            return "Moderate hypertension - Consider medication"
        else:
            return "Severe hypertension - Urgent treatment needed"

# Example usage
if __name__ == "__main__":
    tools = ClinicalTools()
    
    # Test SOAP extraction
    transcript = "Patient reports chest pain and shortness of breath. Exam shows elevated blood pressure. ECG shows ST elevation. Plan: Admit for cardiac monitoring."
    soap = tools.extract_soap_notes(transcript)
    print("SOAP Notes:", json.dumps(soap, indent=2))
    
    # Test CHADS2 calculation
    patient_data = {
        "age": 78,
        "hypertension": True,
        "congestive_heart_failure": False,
        "diabetes": True,
        "stroke_tia_history": True
    }
    chads2 = tools.calculate_chads2_score(patient_data)
    print("\nCHADS2 Score:", json.dumps(chads2, indent=2))
    
    # Test drug interactions
    drugs = ["warfarin", "aspirin", "metformin"]
    interactions = tools.check_drug_interactions(drugs)
    print("\nDrug Interactions:", json.dumps(interactions, indent=2))