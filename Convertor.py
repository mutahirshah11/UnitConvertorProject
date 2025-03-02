import streamlit as st
from transformers import pipeline
import re

# Conversion Factors
conversion_factors = {
    "kilometer": 1000,
    "meter": 1,
    "centimeter": 0.01,
    "millimeter": 0.001,
    "micrometer": 1e-6,
    "nanometer": 1e-9,
    "mile": 1609.34,
    "yard": 0.9144,
    "foot": 0.3048,
    "inch": 0.0254,
    "nautical mile": 1852,
}

# Multiple names for each unit
aliases = {
    "kilometer": {"Km", "km", "Kilometer", "Kilometers", "kilometers"},
    "meter": {"m", "Meter", "meters"},
    "centimeter": {"cm", "Centimeter", "centimeters"},
    "millimeter": {"mm", "Millimeter", "millimeters"},
    "micrometer": {"µm", "Micrometer", "micrometers"},
    "nanometer": {"nm", "Nanometer", "nanometers"},
    "mile": {"Mile", "miles"},
    "yard": {"Yard", "yards"},
    "foot": {"ft", "Foot", "feet"},
    "inch": {"in", "Inch", "inches"},
    "nautical mile": {"NM", "Nautical Mile", "nautical miles"},
}

# Sidebar for Navigation
st.sidebar.markdown("## 🔀 Select Mode")
mode = st.sidebar.radio("Choose Converter", ["Manual Unit Converter", "AI Unit Converter"])

# Sidebar for Theme Selection
st.sidebar.markdown("## 🎨 Theme Selection")
theme = st.sidebar.radio("Choose Theme", ["Light Mode", "Dark Mode"])

# Apply Dark Mode Styling
if theme == "Dark Mode":
    st.markdown("""
        <style>
            body, .stApp { background-color: #1E1E1E; color: white; }
            .stTextInput label, .stFileUploader label, .stCheckbox label, .stSelectbox label, .stRadio label, .stNumberInput label {
                color: white !important;
            }
            .stDownloadButton button, .stButton>button {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #2B2B2B !important;
                color: white !important;
            }
            section[data-testid="stSidebar"] * {
                color: white !important;
            }
            h1, h3 {
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Title
heading_color = "white" if theme == "Dark Mode" else "black"
subheading_color = "lightgray" if theme == "Dark Mode" else "gray"

st.markdown(
    f"<h1 style='text-align: center; color: #4CAF50;'>📣 <span style='color: {heading_color};'>ConvertX</span> - Effortless Conversions, Limitless Possibilities</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h3 style='text-align: center; color: {subheading_color};'>Converting Units with <span style='color: blue;'>ConvertX</span> is now Easy 😎</h3>",
    unsafe_allow_html=True
)

st.divider()

# Conversion Function
def convert_length(value, from_unit, to_unit):
    meters = value * conversion_factors[from_unit]
    return meters / conversion_factors[to_unit]

# Function to get the standard unit name from aliases
def get_standard_unit(unit):
    unit = unit.lower()
    for standard, alias_set in aliases.items():
        if unit in alias_set:
            return standard  # Return the correct unit name
    return unit  # Return as-is if no alias found

# Updated AI Chatbot Input Function
def process_user_input(user_input):
    match = re.search(r"(\d+(\.\d+)?)\s*(\w+)\s*to\s*(\w+)", user_input, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        from_unit = get_standard_unit(match.group(3))  # Convert alias to standard name
        to_unit = get_standard_unit(match.group(4))    # Convert alias to standard name
        
        if from_unit in conversion_factors and to_unit in conversion_factors:
            result = convert_length(value, from_unit, to_unit)
            return f"✅ {value} {from_unit} is equal to **{result:.5f} {to_unit}**"
        return "⚠️ Sorry, I couldn't find these units. Try again!"
    return "⚠️ Please ask like: 'Convert 10 feet to inches'"

# Manual Unit Converter
if mode == "Manual Unit Converter":
    st.markdown("### 🔢 Enter Value to Convert")
    value = st.number_input("Enter Value:", min_value=0.0, format="%.5f")
    
    st.markdown("### 📏 Select Units")
    units = list(conversion_factors.keys())
    col1, col2 = st.columns(2)
    
    with col1:
        from_units = st.selectbox("From Unit", units)
    with col2:
        to_units = st.selectbox("To Unit", units)
    
    st.divider()
    
    if st.button("✅ Convert"):
        if from_units and to_units:
            result = convert_length(value, from_units, to_units)
            st.success(f"✅ {value} {from_units} is equal to **{result:.5f} {to_units}**")
        else:
            st.warning("⚠️ Please select both units!")

# AI Unit Converter
elif mode == "AI Unit Converter":
    st.title("🤖 AI Unit Converter Chatbot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("Ask me: 'Convert 10 meters to feet'")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = process_user_input(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
