# FieldMedic
# FieldMedic

**Offline Open-Weight AI Decision Support for Disaster Response**

FieldMedic is a disaster-response decision-support prototype built around a locally running open-weight AI model.

In disaster environments, internet connectivity and access to medical infrastructure may be limited or unavailable. FieldMedic is designed to help responders organize patient observations, identify dangerous findings, retrieve relevant offline reference material, and generate a structured assessment without requiring cloud-based AI inference.

> FieldMedic is a prototype and is not a medical device. It does not provide confirmed diagnoses and should not replace emergency medical services, trained medical professionals, or established emergency-response protocols.

---

## The Problem

During disasters, responders may face:

- Limited or nonexistent internet access
- Overwhelmed medical infrastructure
- Large numbers of patients
- Limited personnel
- Limited time for patient assessment
- Difficulty accessing reference material

Many modern AI applications depend entirely on cloud infrastructure.

FieldMedic takes a different approach:

**The core AI system runs locally.**

This means the primary FieldMedic analysis pipeline can continue operating without cloud AI inference.

---

## What FieldMedic Does

A responder enters information such as:

- Age
- Symptoms and observations
- Heart rate
- Respiratory rate
- Blood pressure
- Oxygen saturation
- Visible injuries
- Altered mental status
- Severe or uncontrolled bleeding
- Additional observations

FieldMedic then combines several components:

1. Deterministic safety checks
2. Offline reference retrieval
3. Local open-weight AI analysis
4. Structured assessment generation
5. Web-based interface
6. Optional Telegram mobile interface
7. Optional voice output

The resulting assessment can include:

- Suggested triage priority
- Danger signs
- Possible concerns
- Observations to check next
- Recommended escalation
- Reasoning
- Offline references used
- System limitations

---

# Architecture

```text
                 FieldMedic
                     |
           +---------+---------+
           |                   |
      Streamlit Web        Telegram
        Interface             Bot
           |                   |
           +---------+---------+
                     |
                     v
              Safety Engine
                     |
                     v
          Offline Reference Search
                     |
                     v
             Local AI Model
               via Ollama
                     |
                     v
          Structured Assessment
                     |
          +----------+----------+
          |                     |
       Website              Telegram
          |
       Optional
    ElevenLabs Voice
