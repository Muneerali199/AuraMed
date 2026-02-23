"""
AuraMed: Edge-Based Agentic Clinical Co-Pilot
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "streamlit",
        "langchain",
        "transformers",
        "torch",
        "pandas",
        "numpy"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("Installing dependencies from requirements.txt...")
    os.system("pip install -r requirements.txt")

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting AuraMed Clinical Co-Pilot...")
    print("=" * 60)
    print("Application will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Run Streamlit
    os.system("streamlit run src/streamlit_app.py")

def run_tests():
    """Run test suite"""
    print("🧪 Running test suite...")
    os.system("python test_agent.py")

def run_demo():
    """Run a quick demo"""
    print("🎬 Running quick demo...")
    
    # Import and run demo
    try:
        from src.medgemma_agent import MedGemmaAgent
        from data.mtsamples_loader import MTSamplesLoader
        
        agent = MedGemmaAgent()
        agent._create_fallback_agent()
        
        loader = MTSamplesLoader()
        sample = loader.get_sample_by_id(1)
        
        print("\nDemo Transcript:")
        print("-" * 40)
        print(sample["transcription"][:300] + "...")
        print("-" * 40)
        
        result = agent.process_transcript(sample["transcription"])
        
        print("\nAgent Results:")
        if result.get("success"):
            print("✅ Processing successful!")
            
            res = result.get("result", {})
            if "soap_notes" in res:
                print(f"📋 SOAP notes extracted")
            if "chads2_score" in res:
                print(f"📊 CHADS2 score calculated")
            if "drug_interactions" in res:
                print(f"💊 Drug interactions checked")
        else:
            print("❌ Processing failed")
            
    except Exception as e:
        print(f"Demo failed: {e}")

def show_menu():
    """Show main menu"""
    print("\nAuraMed: Edge-Based Agentic Clinical Co-Pilot")
    print("=" * 60)
    print("1. Run Streamlit Application")
    print("2. Run Test Suite")
    print("3. Run Quick Demo")
    print("4. Install Dependencies")
    print("5. Check System Status")
    print("6. Exit")
    print("=" * 60)
    
    choice = input("\nSelect option (1-6): ").strip()
    
    if choice == "1":
        run_streamlit()
    elif choice == "2":
        run_tests()
    elif choice == "3":
        run_demo()
    elif choice == "4":
        install_dependencies()
    elif choice == "5":
        check_system_status()
    elif choice == "6":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")

def check_system_status():
    """Check system status and dependencies"""
    print("\n📊 System Status Check")
    print("=" * 60)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run option 4 to install dependencies")
    else:
        print("✅ All required packages installed")
    
    # Check directories
    required_dirs = ["src", "tools", "data"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory exists: {dir_name}")
        else:
            print(f"❌ Missing directory: {dir_name}")
    
    # Check files
    required_files = [
        "src/medgemma_agent.py",
        "src/streamlit_app.py", 
        "tools/clinical_tools.py",
        "requirements.txt",
        "README.md"
    ]
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
    
    print("\nSystem check complete.")

def main():
    """Main entry point"""
    try:
        while True:
            show_menu()
            
            # After completing an action, ask if user wants to continue
            if input("\nReturn to menu? (y/n): ").lower() != 'y':
                print("Goodbye! 👋")
                break
                
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main()