"""
Streamlit UI for AuraMed: Edge-Based Agentic Clinical Co-Pilot
Powered by MedGemma
"""

import streamlit as st
import json
import time
from datetime import datetime
from src.medgemma_agent import MedGemmaAgent, load_sample_transcripts

# Page configuration
st.set_page_config(
    page_title="AuraMed: Clinical Co-Pilot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-response {
        background-color: #f8f9fa;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .tool-card {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #bbdefb;
    }
    .success-badge {
        background-color: #c8e6c9;
        color: #2e7d32;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .warning-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

class AuraMedUI:
    """Streamlit UI for AuraMed Clinical Co-Pilot"""
    
    def __init__(self):
        self.agent = None
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'agent_initialized' not in st.session_state:
            st.session_state.agent_initialized = False
        if 'processing' not in st.session_state:
            st.session_state.processing = False
        if 'results' not in st.session_state:
            st.session_state.results = {}
        if 'transcript_history' not in st.session_state:
            st.session_state.transcript_history = []
    
    def initialize_agent(self):
        """Initialize the MedGemma agent"""
        try:
            with st.spinner("🔄 Initializing MedGemma Clinical Agent..."):
                self.agent = MedGemmaAgent()
                self.agent.initialize_model()
                st.session_state.agent_initialized = True
                st.success("✅ MedGemma Agent Initialized Successfully!")
                return True
        except Exception as e:
            st.error(f"❌ Error initializing agent: {str(e)}")
            st.info("⚠️ Running in fallback mode with demo tools...")
            # Create agent without model loading
            self.agent = MedGemmaAgent()
            self.agent._create_fallback_agent()
            st.session_state.agent_initialized = True
            return True
    
    def render_sidebar(self):
        """Render sidebar with controls and info"""
        with st.sidebar:
            st.markdown("## 🏥 AuraMed Settings")
            
            # Agent status
            st.markdown("### Agent Status")
            if st.session_state.agent_initialized:
                st.markdown('<span class="success-badge">✅ Active</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="warning-badge">⚠️ Not Initialized</span>', unsafe_allow_html=True)
            
            # Initialize button
            if not st.session_state.agent_initialized:
                if st.button("🚀 Initialize MedGemma Agent", use_container_width=True):
                    self.initialize_agent()
            
            st.markdown("---")
            
            # Sample transcripts
            st.markdown("### Sample Transcripts")
            samples = load_sample_transcripts()
            
            for sample in samples:
                if st.button(f"📝 {sample['description']}", key=f"sample_{sample['id']}", use_container_width=True):
                    st.session_state.sample_transcript = sample['transcript']
                    st.rerun()
            
            st.markdown("---")
            
            # Tools info
            st.markdown("### Available Tools")
            
            with st.expander("🔧 Clinical Tools", expanded=True):
                st.markdown("""
                **1. SOAP Note Extractor**  
                Extracts structured Subjective, Objective, Assessment, Plan notes
                
                **2. CHADS2 Calculator**  
                Calculates stroke risk score for atrial fibrillation
                
                **3. Drug Interaction Checker**  
                Checks for potential drug interactions
                """)
            
            st.markdown("---")
            
            # About section
            st.markdown("### About AuraMed")
            st.markdown("""
            **Edge-Based Clinical Co-Pilot**  
            Powered by MedGemma  
            
            Privacy-preserving, offline-first  
            Agentic workflow for rural clinics
            """)
    
    def render_main_content(self):
        """Render main content area"""
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('<h1 class="main-header">🏥 AuraMed</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Edge-Based Agentic Clinical Co-Pilot powered by MedGemma</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
            if st.session_state.agent_initialized:
                st.markdown('<span class="success-badge">Agent Ready</span>', unsafe_allow_html=True)
        
        # Main area
        tab1, tab2, tab3 = st.tabs(["📝 Clinical Transcript", "🔍 Analysis Results", "📊 Agent Dashboard"])
        
        with tab1:
            self.render_transcript_input()
        
        with tab2:
            self.render_results()
        
        with tab3:
            self.render_dashboard()
    
    def render_transcript_input(self):
        """Render transcript input area"""
        st.markdown("### Enter Clinical Transcript")
        
        # Load sample if selected
        transcript = ""
        if 'sample_transcript' in st.session_state:
            transcript = st.session_state.sample_transcript
            del st.session_state.sample_transcript
        
        # Text area for transcript
        transcript_input = st.text_area(
            "Paste patient transcript or clinical notes:",
            value=transcript,
            height=200,
            placeholder="Example: Patient presents with chest pain, shortness of breath. History of hypertension and diabetes. Currently on metformin and lisinopril..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            process_btn = st.button(
                "🚀 Process with Agent",
                disabled=not st.session_state.agent_initialized,
                use_container_width=True
            )
        
        with col2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
        
        with col3:
            download_btn = st.button("📥 Download Results", disabled=not st.session_state.results, use_container_width=True)
        
        if clear_btn:
            st.session_state.results = {}
            st.rerun()
        
        if download_btn and st.session_state.results:
            results_json = json.dumps(st.session_state.results, indent=2)
            st.download_button(
                label="Download JSON",
                data=results_json,
                file_name=f"auramed_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        if process_btn and transcript_input:
            st.session_state.processing = True
            st.session_state.current_transcript = transcript_input
            
            # Add to history
            st.session_state.transcript_history.append({
                "timestamp": datetime.now().isoformat(),
                "transcript_preview": transcript_input[:100] + "..." if len(transcript_input) > 100 else transcript_input
            })
            
            # Process with agent
            with st.spinner("🔍 Analyzing transcript with MedGemma agent..."):
                result = self.agent.process_transcript(transcript_input)
                st.session_state.results = result
                st.session_state.processing = False
                st.rerun()
    
    def render_results(self):
        """Render analysis results"""
        if not st.session_state.results:
            st.info("👈 Enter a clinical transcript and click 'Process with Agent' to see results")
            return
        
        result = st.session_state.results
        
        if not result.get("success", False):
            st.error("❌ Processing failed")
            if "error" in result:
                st.error(f"Error: {result['error']}")
            return
        
        st.success("✅ Analysis Complete!")
        
        # Display results in expandable sections
        result_data = result.get("result", {})
        
        # SOAP Notes
        if "soap_notes" in result_data:
            with st.expander("📋 SOAP Notes", expanded=True):
                soap = result_data["soap_notes"]
                cols = st.columns(4)
                
                with cols[0]:
                    st.markdown("**Subjective**")
                    st.info(soap.get("subjective", "N/A"))
                
                with cols[1]:
                    st.markdown("**Objective**")
                    st.info(soap.get("objective", "N/A"))
                
                with cols[2]:
                    st.markdown("**Assessment**")
                    st.warning(soap.get("assessment", "N/A"))
                
                with cols[3]:
                    st.markdown("**Plan**")
                    st.success(soap.get("plan", "N/A"))
        
        # CHADS2 Score
        if "chads2_score" in result_data:
            with st.expander("📊 CHADS2 Score Assessment", expanded=True):
                chads2 = result_data["chads2_score"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("CHADS2 Score", chads2.get("score", 0))
                    st.markdown(f"**Stroke Risk:** {chads2.get('stroke_risk', 'N/A')}")
                
                with col2:
                    st.markdown("**Score Components:**")
                    for component in chads2.get("components", []):
                        st.markdown(f"- {component}")
                
                st.markdown(f"**Recommendation:** {chads2.get('recommendation', 'N/A')}")
        
        # Drug Interactions
        if "drug_interactions" in result_data:
            with st.expander("💊 Drug Interaction Check", expanded=True):
                interactions = result_data["drug_interactions"]
                
                st.markdown(f"**Drugs Checked:** {', '.join(interactions.get('drugs_checked', []))}")
                
                if interactions.get("interactions_found", False):
                    st.warning("⚠️ Potential Interactions Found")
                    
                    for interaction in interactions.get("interactions", []):
                        with st.container():
                            st.markdown(f"**{interaction['drug']}**")
                            st.markdown(f"- **Risk Level:** {interaction['risk']}")
                            st.markdown(f"- **Potential Effect:** {interaction['effect']}")
                            st.markdown(f"- **Interacts With:** {', '.join(interaction['interactions'])}")
                else:
                    st.success("✅ No significant interactions found")
                
                st.markdown(f"**Recommendation:** {interactions.get('recommendation', 'N/A')}")
        
        # Raw JSON
        with st.expander("📄 Raw JSON Output"):
            st.json(result_data)
    
    def render_dashboard(self):
        """Render agent dashboard"""
        st.markdown("### Agent Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Agent Status", "Active" if st.session_state.agent_initialized else "Inactive")
        
        with col2:
            history_count = len(st.session_state.transcript_history)
            st.metric("Transcripts Processed", history_count)
        
        with col3:
            agent_type = st.session_state.results.get("agent_type", "N/A") if st.session_state.results else "N/A"
            st.metric("Agent Type", agent_type)
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### Recent Activity")
        if st.session_state.transcript_history:
            for item in st.session_state.transcript_history[-5:]:  # Show last 5
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Transcript:** {item['transcript_preview']}")
                with col2:
                    st.caption(item['timestamp'])
        else:
            st.info("No recent activity")
        
        st.markdown("---")
        
        # System info
        st.markdown("### System Information")
        st.markdown("""
        - **Framework:** Streamlit + LangChain
        - **Model:** MedGemma (Google)
        - **Deployment:** Local/Edge (Ollama/llama.cpp compatible)
        - **Privacy:** Fully local, HIPAA-compliant
        - **Tools:** SOAP Extractor, CHADS2 Calculator, Drug Interaction Checker
        """)

def main():
    """Main function"""
    app = AuraMedUI()
    app.render_sidebar()
    app.render_main_content()

if __name__ == "__main__":
    main()