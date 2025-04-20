# Astro-Vars: AI-Powered Astrological Partner Analysis

![Astro-Vars Logo](https://img.shields.io/badge/AstroVars-Astrology%20AI-9467bd)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Astro-Vars is a sophisticated astrological analysis tool that leverages AI to provide personalized partner compatibility insights. By analyzing your birth chart using Google's Gemma 3 1B model, Astro-Vars delivers professional-grade interpretations about ideal partner traits.

## 🌟 Features

- **Full Birth Chart Calculation**: Generate a complete natal chart with Sun, Moon, Ascendant, all planets, and houses
- **AI-Powered Interpretation**: Detailed partner trait analysis using Google's Gemma 3 LLM
- **Comprehensive Astrological Insights**: Analysis based on planetary positions, houses, elements, modalities, and aspects
- **Smart Location Detection**: Automatic timezone adjustment based on geolocation
- **Beautiful Streamlit Interface**: User-friendly UI for entering birth details
- **Detailed Logging**: All AI interactions are logged for reference and improvement

## 📋 Requirements

- Python 3.10+
- Hugging Face API token (for accessing the Gemma 3 model)
- Internet connection (for geocoding and model downloads)

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/astrovars.git
   cd astrovars
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Hugging Face token:
   ```bash
   export HF_TOKEN=your_huggingface_token_here
   # On Windows: set HF_TOKEN=your_huggingface_token_here
   ```

## 💫 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Enter your birth details in the form:
   - Name
   - Gender
   - Place of birth (for geocoding)
   - Date and time of birth

3. Submit the form to receive your personalized astrological partner analysis!

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Google's Gemma 3 1B instruction-tuned model
- **Astrological Calculations**: Flatlib
- **Geocoding**: Geopy with Nominatim
- **Timezone Management**: Timezonefinder, pytz

## 🔑 API Keys

To use this application, you'll need:

- A [Hugging Face Token](https://huggingface.co/settings/tokens) with access to the Gemma 3 model

## 📚 Project Structure

- `app.py`: Main Streamlit application
- `astrology.py`: Natal chart calculation functions
- `llm_handler.py`: AI model integration for interpretations
- `llm_utils.py`: Utilities for model management
- `timezone_utils.py`: Handling timezone conversions
- `prompt_engine.py`: Templates for AI prompts

## 📜 License

MIT

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
