import ollama
from pydantic import BaseModel, Field

from safety import run_safety_checks
from references import search_references, format_references


class Assessment(BaseModel):
    triage_priority: str
    summary: str

    danger_signs: list[str] = Field(default_factory=list)
    possible_concerns: list[str] = Field(default_factory=list)
    next_checks: list[str] = Field(default_factory=list)

    recommended_action: str
    reasoning: str

    reference_sources: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


SYSTEM_PROMPT = """
You are FieldMedic, a disaster-response decision-support prototype.

You organize information supplied by a responder. You do not diagnose,
prescribe, replace emergency services, or replace trained medical judgment.

Rules:

1. Never state that the patient definitely has a disease or injury.
2. Use the phrase "possible concern" instead of "diagnosis."
3. Do not invent vital signs, observations, treatments, medications,
   references, dosages, or patient history.
4. Clearly state when information is missing.
5. If deterministic safety checks require IMMEDIATE priority, do not lower it.
6. Only cite sources supplied in the local-reference section.
7. If no useful reference is supplied, leave reference_sources empty.
8. Recommended actions should focus on seeking qualified emergency assistance
   and following the responder's approved protocol.
9. Do not give medication doses.
10. Return only the requested structured response.
"""


def parse_systolic_pressure(blood_pressure):
    if not blood_pressure:
        return None

    try:
        return int(
            str(blood_pressure).strip().split("/")[0]
        )
    except (ValueError, IndexError, AttributeError):
        return None


def analyze_patient(patient):
    systolic_pressure = parse_systolic_pressure(
        patient.get("blood_pressure", "")
    )

    safety = run_safety_checks(
        heart_rate=patient.get("heart_rate"),
        respiratory_rate=patient.get("respiratory_rate"),
        systolic_pressure=systolic_pressure,
        oxygen=patient.get("oxygen"),
        altered_mental_status=patient.get(
            "altered_mental_status",
            False
        ),
        uncontrolled_bleeding=patient.get(
            "uncontrolled_bleeding",
            False
        )
    )

    search_text = " ".join([
        str(patient.get("symptoms", "")),
        str(patient.get("injuries", "")),
        str(patient.get("notes", ""))
    ])

    reference_matches = search_references(search_text)

    reference_context = format_references(
        reference_matches
    )

    if safety["force_immediate"]:
        forced_priority = "IMMEDIATE"
    else:
        forced_priority = (
            "Not forced by the demonstration safety layer"
        )

    prompt = f"""
PATIENT INFORMATION

Age: {patient.get("age")}
Symptoms: {patient.get("symptoms")}
Heart rate: {patient.get("heart_rate")} bpm
Respiratory rate: {patient.get("respiratory_rate")}
Blood pressure: {patient.get("blood_pressure")}
Oxygen saturation: {patient.get("oxygen")}%
Visible injuries: {patient.get("injuries")}
Additional notes: {patient.get("notes")}
Altered mental status reported:
{patient.get("altered_mental_status")}
Uncontrolled bleeding reported:
{patient.get("uncontrolled_bleeding")}

DETERMINISTIC SAFETY RESULTS

Required minimum priority: {forced_priority}
Safety findings: {safety["danger_signs"]}

LOCAL REFERENCE MATERIAL

{reference_context}

Produce a concise assessment.

Allowed triage_priority values:
IMMEDIATE
URGENT
DELAYED
MINOR
INSUFFICIENT INFORMATION
"""

    response = ollama.generate(
        model="gemma4",
        prompt=prompt,
        format=Assessment.model_json_schema(),
    )

    if not response or not response.get("response"):
        return {
            "triage_priority": "INSUFFICIENT INFORMATION",
            "summary": "Unable to generate an assessment.",
            "danger_signs": [],
            "possible_concerns": [],
            "next_checks": [],
            "recommended_action": "Seek qualified emergency assistance and follow the responder's approved protocol.",
            "reasoning": "The model did not return a usable assessment.",
            "reference_sources": [],
            "limitations": [
                "The assessment could not be generated from the available information."
            ],
        }

    raw = response["response"]
    parsed = Assessment.model_validate_json(raw)
    if parsed.reference_sources:
        pass

    return parsed.model_dump()