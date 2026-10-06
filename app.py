import streamlit as st
import json
import os
from PIL import Image
import io

from touchgrass.ai_engine import OpenSourceAIEngine
from touchgrass.quest_generator import QuestGenerator
from touchgrass.nature_identifier import NatureIdentifier
from touchgrass.audio_guide import AudioStrollGuide

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="TouchGrass AI - Open-Source Nature Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# Modern Nature-Themed CSS Styling
# -------------------------------------------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #2E7D32;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #4A5568;
        margin-bottom: 25px;
    }
    .quest-card {
        background: linear-gradient(135deg, #F1F8E9 0%, #FFFFFF 100%);
        border: 1px solid #C8E6C9;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .quest-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1B5E20;
        margin-bottom: 8px;
    }
    .badge-pill {
        display: inline-block;
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #A5D6A7;
        margin-right: 6px;
    }
    .bio-card {
        background-color: #FAFAFA;
        border-left: 4px solid #66BB6A;
        padding: 14px 18px;
        border-radius: 4px;
        margin-top: 15px;
        font-size: 0.95rem;
        color: #2D3748;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------------
if "streak_days" not in st.session_state:
    st.session_state.streak_days = 2
if "total_minutes_outside" not in st.session_state:
    st.session_state.total_minutes_outside = 45
if "badges" not in st.session_state:
    st.session_state.badges = ["🌿 First Grass Touched", "☀️ 10-Minute Sun Walker"]
if "completed_quests" not in st.session_state:
    st.session_state.completed_quests = 3

# -------------------------------------------------------------
# Sidebar: Settings & Contributor Profile
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌿 **TouchGrass AI**")
    st.markdown("*Built for Hacktoberfest 2026 Week 1 Challenge (Theme: Touch Grass).*")
    st.markdown("---")
    
    st.markdown("#### ⚙️ **Open-Source AI Engine**")
    provider = st.selectbox(
        "AI Provider",
        [
            "Demo / Offline Mode",
            "Groq (Llama 3 Open-Weights)",
            "Hugging Face Inference API",
            "Local Ollama (Offline)",
        ],
    )
    
    api_key = ""
    if provider in ["Groq (Llama 3 Open-Weights)", "Hugging Face Inference API"]:
        api_key = st.text_input(
            f"Enter {provider.split()[0]} API Key",
            type="password",
            help="Free API keys from groq.com or huggingface.co to run open-weight models.",
        )
    
    model_name = "llama-3.1-8b-instant"
    if provider == "Groq (Llama 3 Open-Weights)":
        model_name = st.selectbox(
            "Model Selection",
            ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        )

    st.markdown("---")
    st.markdown("#### 🏆 **Your Outdoor Stats**")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Streak", f"{st.session_state.streak_days} Days", "+1")
    with c2:
        st.metric("Total Outside", f"{st.session_state.total_minutes_outside}m")
    
    st.markdown("**Earned Badges:**")
    for b in st.session_state.badges:
        st.markdown(f"- {b}")
    
    st.markdown("---")
    st.markdown("👨‍💻 **Developer:** Vimal Sahani (`@VimalN2005`)")
    st.markdown("🌐 [GitHub Repository](https://github.com/VimalN2005/touch-grass-ai)")

# Initialize Engine
engine = OpenSourceAIEngine(
    provider=provider,
    api_key=api_key,
    model_name=model_name,
)
quest_gen = QuestGenerator(engine)
nature_id = NatureIdentifier(engine)
audio_guide = AudioStrollGuide(engine)

# -------------------------------------------------------------
# Main Application Header
# -------------------------------------------------------------
st.markdown('<div class="main-title">🌿 TouchGrass AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">The open-source intelligent outdoor quest companion designed to rescue developers from screen fatigue, debugging loops, and burnout.</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "🎯 Custom Outdoor Quest",
    "📷 Nature Vision Guide",
    "🎧 Mindful Walking Companion",
])

# -------------------------------------------------------------
# TAB 1: Quest Generator
# -------------------------------------------------------------
with tab1:
    st.markdown("### 🧘‍♂️ Generate Your Dopamine & Sunlight Reset Quest")
    st.write("Tell TouchGrass AI about your current coding strain to generate a hyper-targeted outdoor micro-adventure.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        screen_hours = st.slider("Hours spent staring at monitors today:", 1.0, 14.0, 6.5, 0.5)
        task_type = st.selectbox(
            "What have you been working on?",
            [
                "Debugging persistent backend / memory issues",
                "Reviewing complex PRs & writing tests",
                "Deep architectural refactoring & system design",
                "Grinding LeetCode & competitive programming",
                "Endless Zoom / Slack communication overload",
            ],
        )
    with col_input2:
        available_env = st.selectbox(
            "What outdoor environment do you have nearby?",
            [
                "Balcony / Backyard Garden",
                "Quiet Neighborhood Street / Sidewalk",
                "Public Park / Botanical Nature Trail",
                "Building Rooftop under Open Sky",
            ],
        )
        symptoms = st.multiselect(
            "Physical & mental fatigue symptoms:",
            [
                "Dry / Burning Eyes",
                "Stiff Neck & Shoulders",
                "Brain Fog / Inability to focus",
                "Agitation / Tunnel Vision",
                "Mental exhaustion",
            ],
            default=["Dry / Burning Eyes", "Brain Fog / Inability to focus"],
        )
        break_duration = st.slider("Target break duration (minutes):", 5, 45, 15, 5)

    if st.button("🚀 Generate My Touch Grass Quest", key="btn_gen_quest"):
        with st.spinner("Synthesizing open-source AI quest based on neuroscience & nature therapy..."):
            quest_data = quest_gen.generate_quest(
                screen_hours=screen_hours,
                task_type=task_type,
                fatigue_symptoms=symptoms,
                available_environment=available_env,
                available_time_minutes=break_duration,
            )
            st.session_state.current_quest = quest_data

    if "current_quest" in st.session_state:
        q = st.session_state.current_quest
        st.markdown(f"""
        <div class="quest-card">
            <div class="quest-header">🌱 {q.get('quest_title', 'Outdoor Reset Quest')}</div>
            <div>
                <span class="badge-pill">⏱️ {q.get('duration_minutes', 15)} Minutes</span>
                <span class="badge-pill">📍 {q.get('primary_biome', 'Open Air')}</span>
                <span class="badge-pill">⭐ +{q.get('reward_xp', 150)} XP</span>
                <span class="badge-pill">🎖️ {q.get('badge_awarded', 'Grass Toucher')}</span>
            </div>
            <h4 style="margin-top: 18px; color: #1B5E20;">🎯 Quest Objectives:</h4>
            <ul>
                {"".join(f'<li style="margin-bottom: 6px;">{obj}</li>' for obj in q.get('objectives', []))}
            </ul>
            <div class="bio-card">
                <strong>🧠 Neuroscience Rationale:</strong><br>
                {q.get('biological_rationale', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_done, _ = st.columns([1, 4])
        with c_done:
            if st.button("✅ I Completed This Quest!", key="btn_complete_quest"):
                st.session_state.streak_days += 1
                st.session_state.total_minutes_outside += q.get("duration_minutes", 15)
                new_badge = f"🎖️ {q.get('badge_awarded', 'Grass Toucher')}"
                if new_badge not in st.session_state.badges:
                    st.session_state.badges.append(new_badge)
                st.success(f"🎉 Awesome job stepping away! Added {q.get('duration_minutes', 15)}m to your outdoor log. You unlocked: {new_badge}!")
                st.balloons()

# -------------------------------------------------------------
# TAB 2: Nature Vision Guide
# -------------------------------------------------------------
with tab2:
    st.markdown("### 📷 Nature Vision & Flora Field Guide")
    st.write("Encountered an interesting leaf, plant, flower, or tree while outside? Upload a picture to let TouchGrass AI analyze it and share mindfulness trivia.")
    
    col_img_up, col_img_info = st.columns([1, 1])
    with col_img_up:
        uploaded_file = st.file_uploader("Upload an outdoor nature photo (JPG, PNG):", type=["jpg", "jpeg", "png"])
        notes = st.text_input("Any observation notes (optional):", placeholder="e.g. Found growing near the park fountain...")
        
        # Fallback sample button if user has no photo right now
        use_sample = st.checkbox("Or use demo garden sample photo")

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        with col_img_up:
            st.image(image, caption="Your Outdoor Finding", use_container_width=True)
    elif use_sample:
        # Create a tiny synthesized green leaf image
        image = Image.new("RGB", (300, 300), color=(46, 125, 50))
        with col_img_up:
            st.image(image, caption="Sample Flora Foliage", use_container_width=True)

    if image is not None:
        if st.button("🔍 Analyze Nature Finding", key="btn_analyze_flora"):
            with st.spinner("Consulting open-source botanical & ecological model..."):
                flora_res = nature_id.identify_finding(image, notes)
                st.session_state.flora_res = flora_res

    if "flora_res" in st.session_state:
        res = st.session_state.flora_res
        with col_img_info:
            st.markdown(f"""
            <div class="quest-card">
                <div class="quest-header">🌿 {res.get('species_candidate', 'Natural Flora')}</div>
                <span class="badge-pill">📂 {res.get('category', 'Flora')}</span>
                <span class="badge-pill">✨ +{res.get('nature_points', 50)} Nature Pts</span>
                <p style="margin-top: 14px;"><strong>Observed Traits:</strong> {res.get('observed_features', '')}</p>
                <p><strong>Ecological Role:</strong> {res.get('ecological_significance', '')}</p>
                <div class="bio-card">
                    <strong>🍃 Mindfulness & Grounding Trivia:</strong><br>
                    {res.get('mindfulness_note', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: Mindful Walking Companion
# -------------------------------------------------------------
with tab3:
    st.markdown("### 🎧 Guided Nature Stroll Meditation")
    st.write("Put on your earbuds, leave your phone in your pocket, and let TouchGrass AI guide your step-by-step sensory stroll.")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        mood = st.selectbox(
            "Current Mental State:",
            [
                "Severe Bug Tunnel-Vision (Fixated on a problem)",
                "Physical Eye & Neck Tension",
                "Mental Burnout / Exhaustion",
                "Mid-Day Slump / Low Energy",
            ],
        )
    with col_w2:
        style = st.selectbox(
            "Stroll Style:",
            [
                "Slow, Grounded Sensory Walk",
                "Brisk Sunlight Energizer",
                "Deep Breathing Nature Stroll",
            ],
        )

    if st.button("🎧 Generate Mindful Stroll Script", key="btn_gen_stroll"):
        with st.spinner("Writing customized walking meditation script..."):
            stroll_data = audio_guide.generate_stroll_script(mood=mood, walk_style=style)
            st.session_state.stroll_data = stroll_data

    if "stroll_data" in st.session_state:
        s = st.session_state.stroll_data
        st.markdown(f"""
        <div class="quest-card">
            <div class="quest-header">🚶‍♂️ {s.get('title', 'Nature Stroll Guide')}</div>
            <span class="badge-pill">⏱️ {s.get('duration', '5 Minutes')}</span>
            <div style="margin-top: 15px; line-height: 1.7; font-size: 1rem; color: #2D3748; white-space: pre-wrap;">
{s.get('script', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
