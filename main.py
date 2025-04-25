import streamlit as st
from google import genai

# Set your Gemini API key
API_KEY = "API_KEY"

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Define the insurance knowledge base as a large string
knowledge_base = """
Insurance Policies Knowledge Base:

1. Health Insurance:
   - Covers medical expenses for illnesses, injuries, and hospitalizations.
   - Coverage options: Individual, Family Floater, Critical Illness, Maternity.
   - Premiums depend on age, health condition, sum insured, and coverage type.
   - Claim process: Notify insurer, submit hospital bills and documents, get claim approval and reimbursement.

2. Life Insurance:
   - Provides financial protection to beneficiaries in case of policyholder's death.
   - Types: Term Life, Whole Life, Endowment, Unit Linked Insurance Plans (ULIPs).
   - Premiums depend on age, sum assured, policy term, and health status.
   - Claim process: Submit claim form, death certificate, policy documents; insurer processes and pays out.

3. Auto Insurance:
   - Covers damages to vehicles and third-party liabilities.
   - Types: Comprehensive, Third-party, Own Damage.
   - Premiums depend on vehicle type, age, location, and coverage.
   - Claim process: Inform insurer, file FIR (if needed), submit documents, get vehicle inspected, claim settled.

4. Home Insurance:
   - Protects home structure and contents against risks like fire, theft, natural disasters.
   - Coverage options: Structure, Contents, Comprehensive.
   - Premiums depend on property value, location, and coverage.
   - Claim process: Notify insurer, submit proof of loss, documents, and get claim processed.

General:
- Premium: The amount paid periodically to keep the policy active.
- Coverage: The protection provided under the policy.
- Exclusions: Events or conditions not covered by the policy.
- Claim: The process to request payment or compensation as per policy terms.

For more details or specific queries, ask about the type of insurance, coverage, premiums, or claim process.
"""

st.title("Insurance Assistant Chatbot 🛡️")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Chat input box
if prompt := st.chat_input("Ask me anything about insurance policies..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Construct the prompt for the LLM
    system_prompt = (
        "You are an expert insurance assistant. Use the provided knowledge base to answer customer queries about insurance policies, "
        "coverage options, premiums, and claim processes. Be clear, concise, and helpful."
    )
    full_prompt = f"{system_prompt}\n\nKnowledge Base:\n{knowledge_base}\n\nUser Query: {prompt}"

    # Get Gemini response
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[full_prompt]
    )
    bot_reply = response.text

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
