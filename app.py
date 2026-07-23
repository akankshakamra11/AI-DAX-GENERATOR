from pathlib import Path
import re

import streamlit as st
from dotenv import load_dotenv

from gemini_service import GeminiService

load_dotenv()

st.set_page_config(
    page_title="AI DAX Generator",
    page_icon="📊",
    layout="wide",
)

SCHEMA_FILE = Path("powerbi_schema.txt")


def load_schema() -> str:
    if not SCHEMA_FILE.exists():
        return ""
    return SCHEMA_FILE.read_text(encoding="utf-8").strip()


def extract_dax(response: str) -> str:
    match = re.search(
        r"```(?:dax)?\s*(.*?)```",
        response,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1).strip() if match else response.strip()


st.title("📊 AI DAX Generator")
st.caption("Generate paste-ready DAX using the saved Power BI model schema.")

schema = load_schema()

if not schema:
    st.error("powerbi_schema.txt is missing or empty.")
    st.stop()

with st.expander("View model schema"):
    st.code(schema, language="text")

object_type = st.selectbox(
    "Create",
    ["Measure", "Calculated Column", "Calculated Table"],
)

object_name = st.text_input(
    "Measure or object name",
    placeholder="Example: Total Sales",
)

requirement = st.text_area(
    "What should the DAX calculate?",
    height=180,
    placeholder=(
        "Example: Calculate total sales after discount, including shipping cost."
    ),
)

expected_result = st.text_input(
    "Expected result or test case — optional",
    placeholder="Example: Return total sales for the selected region and date range.",
)

if st.button("Generate DAX", type="primary", use_container_width=True):
    if not requirement.strip():
        st.warning("Enter the DAX requirement.")
        st.stop()

    prompt = f"""
You are a senior Microsoft Power BI DAX developer.

Create one Power BI {object_type}.

OBJECT NAME
{object_name or "Choose a clear name"}

BUSINESS REQUIREMENT
{requirement}

POWER BI MODEL SCHEMA
Use only the tables, columns, relationships, and business rules below.

{schema}

EXPECTED RESULT OR TEST CASE
{expected_result or "Not provided"}

MANDATORY RULES
1. Never invent table names, column names, measures, or relationships.
2. Use only model objects available in the supplied schema.
3. Preserve Power BI filter context unless explicitly asked otherwise.
4. Use readable VAR blocks for complex calculations.
5. Use DIVIDE instead of the / operator for ratios.
6. Use COALESCE where zero is preferable to BLANK.
7. State missing information clearly.
8. Return paste-ready DAX without placeholders.

Return exactly these sections:

## DAX
```dax
Complete paste-ready DAX
```

## Explanation
Briefly explain the logic and filter-context behaviour.

## Assumptions
State assumptions or write "None".

## Validation
Explain how to verify the result in Power BI.
""".strip()

    try:
        with st.spinner("Generating DAX..."):
            response = GeminiService().generate(prompt)

        dax = extract_dax(response)

        st.subheader("Generated DAX")
        st.code(dax, language="dax")

        st.download_button(
            "Download DAX",
            dax,
            file_name="generated_dax.txt",
            mime="text/plain",
            use_container_width=True,
        )

        with st.expander("Explanation and validation"):
            st.markdown(response)

    except Exception as exc:
        st.error(f"DAX generation failed: {exc}")
