import asyncio
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from ai import analyze_patient


# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------

DISCLAIMER = (
    "PROTOTYPE ONLY: FieldMedic is not a medical device, "
    "does not provide confirmed diagnoses, and does not "
    "replace emergency services or trained medical judgment. "
    "Do not send names, addresses, dates of birth, medical "
    "record numbers, phone numbers, or other identifying "
    "patient information through Telegram."
)


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

def yes_value(value):
    if value is None:
        return False

    return value.strip().lower() in {
        "yes",
        "y",
        "true",
        "1"
    }


def optional_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------
# PARSE TELEGRAM INPUT
# ---------------------------------------------------

def parse_case(text):
    fields = {}

    for part in text.split(";"):
        if "=" not in part:
            continue

        key, value = part.split("=", 1)

        key = key.strip().lower()
        value = value.strip()

        fields[key] = value

    required = [
        "age",
        "hr",
        "rr",
        "bp",
        "o2",
        "symptoms"
    ]

    missing = [
        key
        for key in required
        if not fields.get(key)
    ]

    if missing:
        raise ValueError(
            "Missing fields: " + ", ".join(missing)
        )

    patient = {
        "age": optional_integer(fields.get("age")),
        "heart_rate": optional_integer(fields.get("hr")),
        "respiratory_rate": optional_integer(fields.get("rr")),
        "blood_pressure": fields.get("bp", ""),
        "oxygen": optional_integer(fields.get("o2")),
        "symptoms": fields.get("symptoms", ""),
        "injuries": fields.get("injuries", ""),
        "notes": fields.get("notes", ""),
        "altered_mental_status": yes_value(
            fields.get("altered", "no")
        ),
        "uncontrolled_bleeding": yes_value(
            fields.get("bleeding", "no")
        )
    }

    return patient


# ---------------------------------------------------
# FORMAT AI RESPONSE
# ---------------------------------------------------

def format_assessment(result):
    # Support Pydantic objects
    if hasattr(result, "model_dump"):
        result = result.model_dump()

    if not isinstance(result, dict):
        raise TypeError(
            "analyze_patient() returned an unsupported result type."
        )

    danger_signs = "\n".join(
        f"- {item}"
        for item in result.get("danger_signs", [])
    )

    if not danger_signs:
        danger_signs = (
            "- None identified from the entered information"
        )

    possible_concerns = "\n".join(
        f"- {item}"
        for item in result.get("possible_concerns", [])
    )

    if not possible_concerns:
        possible_concerns = "- Insufficient information"

    next_checks = "\n".join(
        f"- {item}"
        for item in result.get("next_checks", [])
    )

    if not next_checks:
        next_checks = "- Follow approved responder protocol"

    references = "\n".join(
        f"- {item}"
        for item in result.get("reference_sources", [])
    )

    if not references:
        references = "- No local reference used"

    limitations = "\n".join(
        f"- {item}"
        for item in result.get("limitations", [])
    )

    if not limitations:
        limitations = "- Prototype output only"

    priority = result.get(
        "triage_priority",
        "UNKNOWN"
    )

    summary = result.get(
        "summary",
        "No summary available."
    )

    recommended_action = result.get(
        "recommended_action",
        "Follow approved emergency-response protocol."
    )

    reasoning = result.get(
        "reasoning",
        "No reasoning available."
    )

    message = f"""
FIELD MEDIC ASSESSMENT

SUGGESTED PRIORITY:
{priority}

SUMMARY:
{summary}

DANGER SIGNS:
{danger_signs}

POSSIBLE CONCERNS:
{possible_concerns}

CHECK NEXT:
{next_checks}

RECOMMENDED ESCALATION:
{recommended_action}

REASONING:
{reasoning}

OFFLINE REFERENCES:
{references}

LIMITATIONS:
{limitations}

{DISCLAIMER}
"""

    return message.strip()


# ---------------------------------------------------
# /START COMMAND
# ---------------------------------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = f"""
FieldMedic Demo Bot

Local AI disaster-response decision-support prototype.

{DISCLAIMER}

To analyze a synthetic demonstration case, use:

/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy and confused; injuries=deep leg wound; altered=yes; bleeding=yes

AVAILABLE COMMANDS

/start
/help
/analyze
"""

    if update.message:
        await update.message.reply_text(
            message.strip()
        )


# ---------------------------------------------------
# /HELP COMMAND
# ---------------------------------------------------

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = """
FIELD MEDIC HELP

Use the /analyze command followed by patient observations.

Required fields:

age = age
hr = heart rate
rr = respiratory rate
bp = blood pressure
o2 = oxygen saturation
symptoms = reported symptoms

Optional fields:

injuries = visible injuries
notes = other observations
altered = yes/no
bleeding = yes/no

EXAMPLE:

/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy and confused; injuries=deep leg wound; altered=yes; bleeding=yes

Do not enter personally identifying patient information.
"""

    if update.message:
        await update.message.reply_text(
            message.strip()
        )


# ---------------------------------------------------
# /ANALYZE COMMAND
# ---------------------------------------------------

async def analyze_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    command_text = " ".join(
        context.args
    ).strip()

    if not command_text:
        await update.message.reply_text(
            "No patient information was entered.\n\n"
            "Example:\n\n"
            "/analyze age=22; hr=128; rr=28; "
            "bp=85/55; o2=94; "
            "symptoms=dizzy and confused; "
            "injuries=deep leg wound; "
            "altered=yes; bleeding=yes"
        )
        return

    status_message = await update.message.reply_text(
        "FieldMedic is running local safety checks "
        "and AI analysis..."
    )

    try:
        patient = parse_case(
            command_text
        )

        result = await asyncio.to_thread(
            analyze_patient,
            patient
        )

        final_message = format_assessment(
            result
        )

        if len(final_message) > 3900:
            final_message = (
                final_message[:3800]
                + "\n\nOutput shortened for Telegram."
            )

        await status_message.edit_text(
            final_message
        )

    except ValueError as error:
        await status_message.edit_text(
            "INPUT PROBLEM\n\n"
            f"{error}\n\n"
            "Example:\n\n"
            "/analyze age=22; hr=128; rr=28; "
            "bp=85/55; o2=94; "
            "symptoms=dizzy and confused; "
            "injuries=deep leg wound; "
            "altered=yes; bleeding=yes"
        )

    except Exception as error:
        await status_message.edit_text(
            "FieldMedic could not complete the analysis.\n\n"
            f"Technical error: {error}"
        )


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():
    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing.\n"
            "Add it to C:\\FieldMedic\\.env"
        )

    application = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    application.add_handler(
        CommandHandler(
            "analyze",
            analyze_command
        )
    )

    print("FieldMedic Telegram bot is running.")
    print("Press Ctrl+C to stop it.")

    application.run_polling()


# ---------------------------------------------------
# START PROGRAM
# ---------------------------------------------------

if __name__ == "__main__":
    main()