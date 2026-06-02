import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime

# Import helper functions and classes from the project
from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from chat import execute_tool_call, trim_history, assistant_tool_message, tool_results_message, json_text

# Load environment variables
ROOT = Path(__file__).parent
load_lab_env(ROOT)

st.set_page_config(
    page_title="🔍 Research Agent UI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern premium glassmorphism styling
st.markdown("""
<style>
    /* Dark Mode styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff4b4b, #ff8585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }

    /* Sidebar glassmorphism styling */
    section[data-testid="stSidebar"] {
        background-color: #161920 !important;
        border-right: 1px solid #2d3139;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1f232d !important;
        border-radius: 8px !important;
        border: 1px solid #2d3139 !important;
    }
    
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App Titles
st.markdown('<div class="main-header">🔍 Research Agent UI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive web interface to query, execute tools, and view agent logs in real time.</div>', unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "transcript_path" not in st.session_state:
    st.session_state.transcript_path = None

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")

version_input = st.sidebar.text_input(
    "Version Label",
    value="v3",
    help="Version tag used for saving transcripts (e.g. v3)"
)

provider_option = st.sidebar.selectbox(
    "Select Model Provider",
    ["openrouter", "openai", "anthropic", "gemini"],
    index=0
)

# Default models
default_models = {
    "openrouter": "openai/gpt-4o-mini",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-latest",
    "gemini": "gemini-1.5-flash"
}

model_input = st.sidebar.text_input(
    "Model Name (leave blank for provider default)",
    value=default_models[provider_option]
)

max_rounds = st.sidebar.slider(
    "Max Tool Rounds",
    min_value=1,
    max_value=10,
    value=4
)

show_trace = st.sidebar.checkbox(
    "Show Agent Execution Trace",
    value=True,
    help="Display LLM thoughts, tool invocation details, and live outputs during run."
)

# Quick Test Prompts Sidebar Selection
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Quick Test Prompts")
quick_prompts = {
    "Out of Scope (Math)": "Giải giúp mình bài toán tích phân: nguyên hàm của x^2 là gì?",
    "Missing Twitter Handle": "Tóm tắt 5 tweet mới nhất giúp mình",
    "Missing Article URL": "Tóm tắt bài viết này hộ mình",
    "Telegram Confirmation": "Đăng bản tin này lên Telegram giúp mình",
    "Wikipedia Search": "Tra Wikipedia về lịch sử phát triển của mạng Internet.",
    "Twitter Topic Search": "Mọi người đang bàn gì về GPT-5 trên Twitter?",
    "Translate Tool": "Dịch giúp mình câu 'Artificial Intelligence is transforming our future' sang tiếng Việt nhé.",
    "Crypto Price": "Giá của đồng tiền điện tử ETH hiện tại trên Binance là bao nhiêu?",
    "Weather Info": "Cho mình biết thời tiết hiện tại ở Đà Nẵng thế nào?"
}

for label, prompt_text in quick_prompts.items():
    if st.sidebar.button(label, key=f"btn_{label}", use_container_width=True):
        st.session_state.temp_prompt = prompt_text
        st.rerun()

# System Prompt display and customization
st.sidebar.markdown("---")
st.sidebar.subheader("📝 System Prompt")

system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
if system_prompt_path.exists():
    try:
        sys_prompt = system_prompt_path.read_text(encoding="utf-8")
    except Exception:
        sys_prompt = "You are a research assistant with access to tools."
else:
    sys_prompt = "You are a research assistant with access to tools."

system_prompt = st.sidebar.text_area(
    "Active System Prompt",
    value=sys_prompt,
    height=200
)

# Reset Button
if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.transcript = None
    st.session_state.transcript_path = None
    st.rerun()

# Setup Agent dependencies
tool_declarations = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
openai_tools = to_openai_tools(tool_declarations)
provider = make_provider(provider_option)
model_name = model_input if model_input.strip() else getattr(provider, "default_model", None)

# Initialize unique transcript file for this Streamlit session
if st.session_state.transcript is None:
    import re
    from versioning import build_artifact_version, artifact_version_dict
    from chat import now_iso, safe_slug
    
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version_input),
        safe_slug(provider_option),
        timestamp,
    ])
    
    # Path to save
    transcripts_dir = ROOT / "transcripts"
    transcript_path = transcripts_dir / f"{transcript_id}.transcript.json"
    
    # Load artifact version
    try:
        artifact_version = build_artifact_version(version_input, ROOT / "artifacts" / "system_prompt.md", ROOT / "artifacts" / "tools.yaml")
        version_details = artifact_version_dict(artifact_version)
    except Exception:
        version_details = {"version": version_input}
        
    st.session_state.transcript_path = transcript_path
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **version_details,
        "provider": provider_option,
        "model": model_name,
        "system_prompt": str(ROOT / "artifacts" / "system_prompt.md"),
        "tools": str(ROOT / "artifacts" / "tools.yaml"),
        "history_window": 5,
        "max_tool_rounds": max_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

# Top-level helper function for agent loop execution
def run_agent_loop(working_messages, openai_tools, provider, model_name, max_rounds, show_trace, status_box):
    all_tool_events = []
    agent_final_text = ""
    for round_index in range(1, max_rounds + 1):
        if show_trace and status_box:
            status_box.update(label=f"Running Round {round_index}...")
        
        # Call LLM
        try:
            response = provider.complete(working_messages, openai_tools, model=model_name, temperature=0.0)
        except Exception as exc:
            st.error(f"⚠️ Error from provider: {str(exc)}")
            agent_final_text = f"An error occurred while calling the AI provider: {str(exc)}"
            if show_trace and status_box:
                status_box.update(label="Provider Error", state="error")
            break
        
        calls = response.tool_calls
        assistant_text = response.text or ""
        
        # Log LLM's response if trace is enabled
        if show_trace and assistant_text:
            st.markdown(f"**LLM Thought**: {assistant_text}")
        
        if not calls:
            agent_final_text = assistant_text
            if show_trace and status_box:
                status_box.update(label="Complete!", state="complete")
            break
        
        # If there are tool calls, display them
        if show_trace:
            st.markdown(f"**Round {round_index} Tool Call(s):**")
        
        working_messages.append(assistant_tool_message(assistant_text, calls))
        non_clarification_events = []
        is_clarifying = False
        clarify_question = ""
        
        for call in calls:
            if show_trace:
                st.markdown(f"👉 Calling `{call.name}` with parameters:")
                st.json(call.args)
            
            # Execute tool call
            if show_trace:
                with st.spinner(f"Running `{call.name}`..."):
                    event = execute_tool_call(call)
            else:
                event = execute_tool_call(call)
            
            all_tool_events.append(event)
            non_clarification_events.append(event)
            
            if show_trace:
                st.markdown("✅ Result received.")
            
            # Check if clarification is needed
            result = event.get("result", {})
            if isinstance(result, dict) and result.get("awaiting_user"):
                is_clarifying = True
                clarify_question = result.get("question") or call.args.get("question") or "Bạn bổ sung thêm thông tin nhé."
        
        if is_clarifying:
            agent_final_text = clarify_question
            if show_trace and status_box:
                status_box.update(label="Awaiting User Info", state="complete")
            break
        
        # Append tool results for next round
        working_messages.append(tool_results_message(non_clarification_events))
    else:
        agent_final_text = f"Stopped after {max_rounds} tool rounds."
        if show_trace and status_box:
            status_box.update(label="Stopped (Max Rounds Reached)", state="error")
            
    return agent_final_text, all_tool_events

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display logs of tool calls if trace is enabled
        if show_trace and "tool_events" in msg and msg["tool_events"]:
            with st.expander("🔧 View tool execution logs", expanded=False):
                for event in msg["tool_events"]:
                    st.markdown(f"**Tool Name**: `{event['tool']}`")
                    st.markdown("**Arguments**:")
                    st.json(event["args"])
                    st.markdown("**Result**:")
                    st.json(event["result"])
                    st.markdown("---")

# Handle user input (either from quick prompts or standard chat input box)
user_query = None
if "temp_prompt" in st.session_state and st.session_state.temp_prompt:
    user_query = st.session_state.temp_prompt
    del st.session_state.temp_prompt  # clear it immediately

chat_input_val = st.chat_input("Enter your request here...")
if chat_input_val:
    user_query = chat_input_val

if user_query:
    # Render user query
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Prepare messages for LLM loop
    history_window = 5
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_query},
    ]
    
    # Render Assistant placeholder
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        working_messages = list(messages)
        all_tool_events = []
        agent_final_text = ""
        
        # Render trace / spinner based on user preference
        if show_trace:
            with st.status("Agent thinking and executing tools...", expanded=True) as status_box:
                agent_final_text, all_tool_events = run_agent_loop(
                    working_messages, openai_tools, provider, model_name, max_rounds, show_trace, status_box
                )
        else:
            with st.spinner("Agent is thinking..."):
                agent_final_text, all_tool_events = run_agent_loop(
                    working_messages, openai_tools, provider, model_name, max_rounds, show_trace, None
                )
        
        # Display final response
        response_placeholder.markdown(agent_final_text)
        
        # Show tool logs expander if trace is enabled
        if show_trace and all_tool_events:
            with st.expander("🔧 View round execution logs", expanded=False):
                for event in all_tool_events:
                    st.markdown(f"**Tool Name**: `{event['tool']}`")
                    st.markdown("**Arguments**:")
                    st.json(event["args"])
                    st.markdown("**Result**:")
                    st.json(event["result"])
                    st.markdown("---")
                    
        # Save response and history
        st.session_state.messages.append({
            "role": "assistant",
            "content": agent_final_text,
            "tool_events": all_tool_events
        })
        st.session_state.history.append({"role": "user", "content": user_query})
        st.session_state.history.append({"role": "assistant", "content": agent_final_text})

        # Build turn record and save to transcript file
        from chat import now_iso, write_transcript
        turn_record = {
            "turn_index": len(st.session_state.transcript["turns"]) + 1,
            "started_at": now_iso(),
            "ended_at": now_iso(),
            "user": user_query,
            "status": "answered" if "error" not in agent_final_text else "provider_error",
            "assistant_text": agent_final_text,
            "tool_events": all_tool_events,
        }
        st.session_state.transcript["turns"].append(turn_record)
        
        try:
            write_transcript(st.session_state.transcript_path, st.session_state.transcript)
            st.toast(f"💾 Saved transcript: {st.session_state.transcript_path.name}", icon="💾")
        except Exception as e:
            st.error(f"Error saving transcript: {e}")
