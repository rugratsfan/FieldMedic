import streamlit as st

from ai import analyze_patient
from voice import voice_is_available, create_voice_audio


st.set_page_config(
    page_title="FieldMedic",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 FieldMedic")

st.caption(
    "Offline open-weight AI decision-support prototype "
    "for disaster-response demonstrations"
)

st.error(
    "Competition prototype only. Not a medical device, diagnosis service, "
    "or replacement for emergency services or trained medical judgment."
)

st.info(
    "Do not enter names, addresses, dates of birth, medical-record numbers, "
    "phone numbers, or other identifying patient information."
)

st.divider()

left, right = st.columns(2)

with left:
    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=20
    )

    symptoms = st.text_area(
        "Symptoms and observations",
        placeholder="Example: dizzy, pale, confused..."
    )

    injuries = st.text_area(
        "Visible injuries",
        placeholder="Describe only what was observed."
    )

    notes = st.text_area(
        "Additional notes",
        placeholder="Relevant non-identifying observations"
    )

with right:
    heart_rate = st.number_input(
        "Heart rate",
        min_value=0,
        max_value=250,
        value=80
    )

    respiratory_rate = st.number_input(
        "Respiratory rate",
        min_value=0,
        max_value=80,
        value=16
    )

    blood_pressure = st.text_input(
        "Blood pressure",
        placeholder="Example: 120/80"
    )

    oxygen = st.number_input(
        "Oxygen saturation",
        min_value=0,
        max_value=100,
        value=98
    )

    altered_mental_status = st.checkbox(
        "Confusion, unresponsiveness, or altered mental status reported"
    )

    uncontrolled_bleeding = st.checkbox(
        "Uncontrolled or severe bleeding reported"
    )

st.divider()

if st.button("Analyze Patient", type="primary"):
    patient = {
        "age": age,
        "symptoms": symptoms,
        "heart_rate": heart_rate,
        "respiratory_rate": respiratory_rate,
        "blood_pressure": blood_pressure,
        "oxygen": oxygen,
        "injuries": injuries,
        "notes": notes,
        "altered_mental_status": altered_mental_status,
        "uncontrolled_bleeding": uncontrolled_bleeding
    }

    try:
        with st.spinner(
            "Running safety checks and local AI analysis..."
        ):
            result = analyze_patient(patient)

        st.session_state["assessment"] = result

    except Exception as error:
        st.error(
            f"FieldMedic could not complete the assessment: {error}"
        )


if "assessment" in st.session_state:
    result = st.session_state["assessment"]

    st.header("Assessment")

    priority_colors = {
        "IMMEDIATE": "🔴",
        "URGENT": "🟠",
        "DELAYED": "🟡",
        "MINOR": "🟢",
        "INSUFFICIENT INFORMATION": "⚪"
    }

    icon = priority_colors.get(
        result.triage_priority,
        "⚪"
    )

    st.subheader(
        f"{icon} Suggested priority: {result.triage_priority}"
    )

    st.write(result.summary)

    column1, column2 = st.columns(2)

    with column1:
        st.subheader("⚠️ Danger signs")

        if result.danger_signs:
            for item in result.danger_signs:
                st.write(f"• {item}")
        else:
            st.write(
                "No danger sign was identified from the entered information."
            )

        st.subheader("Possible concerns")

        for item in result.possible_concerns:
            st.write(f"• {item}")

    with column2:
        st.subheader("Check next")

        for item in result.next_checks:
            st.write(f"• {item}")

        st.subheader("Recommended escalation")

        st.write(result.recommended_action)

    st.subheader("Reasoning")
    st.write(result.reasoning)

    st.subheader("Offline references used")

    if result.reference_sources:
        for source in result.reference_sources:
            st.write(f"• {source}")
    else:
        st.write("No local reference was used.")

    with st.expander("Limitations"):
        for limitation in result.limitations:
            st.write(f"• {limitation}")

    voice_text = (
        f"Suggested priority: {result.triage_priority}. "
        f"Recommended escalation: {result.recommended_action}"
    )

    if voice_is_available():
        st.warning(
            "Voice mode uses an external service. "
            "Only the priority and escalation text will be sent."
        )

        if st.button("🔊 Generate spoken summary"):
            try:
                audio = create_voice_audio(voice_text)

                st.audio(
                    audio,
                    format="audio/mp3"
                )
            except Exception as error:
                st.error(
                    f"Voice generation failed: {error}"
                )
    else:
        st.caption(
            "Add ELEVENLABS_API_KEY to .env to enable spoken summaries."
        )