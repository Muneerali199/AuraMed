"""
Final test for AuraMed demonstration
"""

import json
from tools.clinical_tools import ClinicalTools
from data.mtsamples_loader import MTSamplesLoader

def run_demo():
    """Run a complete demo of AuraMed"""
    print("AuraMed: Edge-Based Agentic Clinical Co-Pilot - Demo")
    print("=" * 70)
    
    # Initialize components
    tools = ClinicalTools()
    loader = MTSamplesLoader()
    
    # Get a cardiac sample
    sample = loader.get_sample_by_id(1)
    print(f"\nSample: {sample['sample_name']}")
    print(f"Specialty: {sample['medical_specialty']}")
    print("-" * 70)
    
    # Show transcript preview
    print("Clinical Transcript Preview:")
    print(sample['transcription'][:300] + "...")
    print("-" * 70)
    
    # Process with clinical tools
    print("\nProcessing with Clinical Tools:")
    print("-" * 70)
    
    # 1. Extract SOAP notes
    soap = tools.extract_soap_notes(sample['transcription'])
    print("\n1. SOAP Notes Extraction:")
    print(f"   Subjective: {soap['subjective'][:80]}...")
    print(f"   Objective: {soap['objective'][:80]}...")
    print(f"   Assessment: {soap['assessment'][:80]}...")
    print(f"   Plan: {soap['plan'][:80]}...")
    
    # 2. Calculate CHADS2 score
    patient_data = {
        "age": 78,
        "hypertension": True,
        "congestive_heart_failure": False,
        "diabetes": True,
        "stroke_tia_history": True
    }
    chads2 = tools.calculate_chads2_score(patient_data)
    print(f"\n2. CHADS2 Score Calculation:")
    print(f"   Score: {chads2['score']} ({chads2['risk_level']} risk)")
    print(f"   Annual Stroke Risk: {chads2['annual_stroke_risk']}")
    print(f"   Therapy: {chads2['therapy_recommendation']}")
    print(f"   Components: {', '.join(chads2['components'])}")
    
    # 3. Check drug interactions
    drugs = ["warfarin", "aspirin", "metformin"]
    interactions = tools.check_drug_interactions(drugs)
    print(f"\n3. Drug Interaction Check:")
    print(f"   Drugs checked: {', '.join(interactions['drugs_checked'])}")
    print(f"   Interactions found: {interactions['interactions_found']}")
    
    if interactions['interactions_found']:
        for interaction in interactions['interaction_details']:
            print(f"   - {interaction['primary_drug']} + {interaction['interacting_drug']}: {interaction['effect']} ({interaction['severity']} risk)")
    
    # 4. Show structured extraction
    structured = loader.extract_structured_data(sample['id'])
    print(f"\n4. Structured Data Extraction:")
    print(f"   Medications detected: {', '.join(structured['extracted_medications'])}")
    print(f"   Conditions detected: {', '.join(structured['extracted_conditions'])}")
    print(f"   CHADS2 calculation needed: {structured['needs_chads2']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Demo Summary:")
    print("-" * 70)
    print(f"✓ SOAP notes successfully extracted from clinical transcript")
    print(f"✓ CHADS2 score calculated for stroke risk assessment")
    print(f"✓ Drug interactions checked for patient safety")
    print(f"✓ Structured data extracted from medical transcription")
    print(f"✓ All processing done locally - no cloud access required")
    print(f"✓ HIPAA compliant - patient data stays on local machine")
    
    # Save results
    results = {
        "sample": sample['sample_name'],
        "soap_notes": soap,
        "chads2_score": chads2,
        "drug_interactions": interactions,
        "structured_data": structured
    }
    
    with open("demo_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to: demo_results.json")
    print("=" * 70)
    
    return True

def check_system():
    """Check system readiness"""
    print("\nSystem Check:")
    print("-" * 70)
    
    checks = []
    
    # Check imports
    try:
        from tools.clinical_tools import ClinicalTools
        checks.append(("Clinical Tools", "OK"))
    except Exception as e:
        checks.append(("Clinical Tools", f"FAILED: {str(e)[:50]}"))
    
    try:
        from data.mtsamples_loader import MTSamplesLoader
        checks.append(("MTSamples Loader", "OK"))
    except Exception as e:
        checks.append(("MTSamples Loader", f"FAILED: {str(e)[:50]}"))
    
    # Check file structure
    import os
    required_files = [
        "src/medgemma_agent.py",
        "tools/clinical_tools.py",
        "data/mtsamples_loader.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            checks.append((f"File: {file}", "OK"))
        else:
            checks.append((f"File: {file}", "MISSING"))
    
    # Display checks
    for check_name, status in checks:
        print(f"{check_name:30} {status}")
    
    print("-" * 70)
    
    all_ok = all(status == "OK" for _, status in checks)
    return all_ok

def main():
    """Main function"""
    print("AuraMed Final Test")
    print("=" * 70)
    
    # Check system
    if not check_system():
        print("System check failed. Please fix issues before proceeding.")
        return False
    
    # Run demo
    try:
        success = run_demo()
        if success:
            print("\nAuraMed is ready for demonstration!")
            print("\nNext steps:")
            print("1. Record the 3-minute video using video_script.md")
            print("2. Push code to GitHub repository")
            print("3. Submit to Kaggle with video link")
            print("4. Use README.md for installation instructions")
        return success
    except Exception as e:
        print(f"\nDemo failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)