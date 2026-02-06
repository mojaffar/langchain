import requests
import streamlit as st


def get_groq_response(input_text, language="Hindi"):
    json_body = {
        "input": {
            "language": language,
            "text": input_text
        },
        "config": {},
        "kwargs": {}
    }
    try:
        resp = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}


## Streamlit app
st.title("LLM Application Using LCEL")

languages = [
    "Hindi",
    "Spanish",
    "German",
    "French",
    "Urdu",
    "Arabic",
    "Chinese",
    "Pashto",
    "English",
]

selected_lang = st.selectbox("Select target language", languages, index=0)

input_text = st.text_input(f"Enter the text you want to translate to {selected_lang}")

if st.button("Translate"):
    if not input_text:
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Calling server..."):
            result = get_groq_response(input_text, language=selected_lang)

        if isinstance(result, dict) and "error" in result:
            st.error(result["error"])
        else:
            # Prefer showing only the main output text if available
            output_text = None
            if isinstance(result, dict):
                # common shape: {"output": "...", "metadata": {...}}
                if "output" in result:
                    output_text = result["output"]
                # nested shape: {"result": {"output": "..."}}
                elif "result" in result and isinstance(result["result"], dict) and "output" in result["result"]:
                    output_text = result["result"]["output"]

            if output_text is not None:
                st.subheader("Output")
                st.write(output_text)
            else:
                # fallback: show full JSON or raw result
                st.subheader("Response (raw)")
                try:
                    st.json(result)
                except Exception:
                    st.write(result)