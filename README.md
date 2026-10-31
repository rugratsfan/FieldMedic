# FieldMedic

**Offline Open-Weight AI Decision Support for Disaster Response**

FieldMedic is a disaster-response decision-support prototype built around a locally running open-weight AI model.

During disasters, internet connectivity and access to normal medical infrastructure may become limited or unavailable. FieldMedic explores how local AI can help responders organize patient observations, identify dangerous findings, retrieve relevant offline reference material, and generate structured assessments without relying on cloud-based AI inference.

> **Important:** FieldMedic is a competition and educational prototype. It is not a medical device, does not provide confirmed diagnoses, and must not replace emergency medical services, trained medical professionals, or established emergency-response protocols.

---

# The Problem

Disaster environments can involve:

- Limited or nonexistent internet access
- Overwhelmed medical infrastructure
- Large numbers of patients
- Limited personnel
- Limited time for patient assessment
- Difficulty accessing reference material
- Limited access to cloud-based AI systems

Many modern AI applications rely completely on cloud infrastructure.

FieldMedic takes a different approach:

> **The core AI analysis runs locally.**

---

# What FieldMedic Does

A responder enters patient observations such as:

- Age
- Symptoms
- Heart rate
- Respiratory rate
- Blood pressure
- Oxygen saturation
- Visible injuries
- Altered mental status
- Severe or uncontrolled bleeding
- Additional observations

FieldMedic then combines:

1. Deterministic safety checks
2. Offline reference retrieval
3. Local open-weight AI analysis
4. Structured assessment generation
5. A Streamlit web interface
6. An optional Telegram mobile interface
7. Optional ElevenLabs voice output

FieldMedic can return:

- Suggested triage priority
- Danger signs
- Possible concerns
- Observations to check next
- Recommended escalation
- Reasoning
- Offline references used
- System limitations

---

# Why Open-Weight AI?

The AI is not an additional feature added on top of FieldMedic.

It is a central component of the application.

FieldMedic uses a Gemma model running locally through Ollama.

The model helps:

- Organize responder observations
- Interpret supplied patient context
- Identify possible concerns
- Generate structured output
- Explain why observations may be important
- Incorporate retrieved local reference material

The deterministic safety system remains separate from the language model so selected critical findings do not depend exclusively on generative AI.

---

# Architecture

```text
                       FieldMedic
                           |
               +-----------+-----------+
               |                       |
        Streamlit Website          Telegram Bot
               |                       |
               +-----------+-----------+
                           |
                           v
                  Deterministic
                   Safety Layer
                           |
                           v
                    Local Offline
                 Reference Retrieval
                           |
                           v
                      Gemma Model
                     through Ollama
                           |
                           v
                  Structured Assessment
                           |
               +-----------+-----------+
               |                       |
            Website                  Telegram
               |
               v
      Optional ElevenLabs Voice
```

---

# Core Features

## Local AI Inference

FieldMedic runs the configured Gemma model locally through Ollama.

Core patient analysis therefore does not require a cloud AI inference API.

---

## Deterministic Safety Layer

Before generative AI results are presented, FieldMedic checks selected reported measurements and observations using normal Python logic.

The prototype can flag observations such as:

- Reported severe or uncontrolled bleeding
- Altered mental status
- Very low systolic blood pressure
- Very low oxygen saturation
- Extremely high or low heart rate
- Extremely high or low respiratory rate

For selected high-risk findings, the deterministic system can force escalation regardless of what the language model generates.

This means the architecture is:

```text
Patient Observations
        |
        v
Deterministic Safety Checks
        |
        v
Offline Reference Search
        |
        v
Local Gemma Model
        |
        v
Structured Assessment
```

This safety layer is a prototype and does not constitute a validated clinical triage algorithm.

---

# Offline Reference Retrieval

FieldMedic includes a simple offline reference-retrieval system.

Reference files are stored inside:

```text
references/
```

For example:

```text
references/
|
+-- README.txt
+-- start_triage_reference.txt
```

FieldMedic searches these local files for material related to the observations entered by the responder.

Relevant content is then supplied to the local model as additional context.

This gives FieldMedic a basic local Retrieval-Augmented Generation, or RAG, pipeline:

```text
Patient Information
        |
        v
Local Search
        |
        v
Relevant References
        |
        v
Gemma
        |
        v
Assessment
```

Reference material should come from authoritative sources and include the title, publisher, version/date, and original source.

Do not redistribute copyrighted or restricted reference material without permission.

---

# Streamlit Web Interface

The main FieldMedic interface is built with Streamlit.

It allows the responder to enter patient observations and receive a structured result containing:

```text
Suggested Priority
Danger Signs
Possible Concerns
Check Next
Recommended Escalation
Reasoning
Offline References
Limitations
```

The Streamlit application can run locally on the same computer as FieldMedic.

---

# Telegram Interface

FieldMedic includes an optional Telegram bot.

This allows a user to send structured observations from a phone when network connectivity is available.

Example:

```text
/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy and confused; injuries=deep leg wound; altered=yes; bleeding=yes
```

The Telegram interface connects to the same FieldMedic analysis pipeline.

## Important Privacy Limitation

Telegram itself requires internet connectivity.

Therefore:

```text
Gemma inference             LOCAL
Ollama                      LOCAL
Safety checks               LOCAL
Reference retrieval         LOCAL
Local Streamlit interface   LOCAL

Telegram                    CONNECTED
ElevenLabs                  CONNECTED
```

Do not claim that the entire Telegram workflow is offline.

Do not transmit real personally identifiable patient information through the demonstration Telegram bot.

---

# Optional Voice Output

FieldMedic can optionally use ElevenLabs to turn limited assessment information into speech.

For example:

```text
Suggested priority: IMMEDIATE.
Recommended escalation: ...
```

This feature may be useful for hands-free interaction.

However, ElevenLabs is an external connected service.

Voice is optional and is not required for the core FieldMedic system.

---

# Technology Stack

FieldMedic uses:

- Python
- Gemma
- Ollama
- Streamlit
- Pydantic
- python-telegram-bot
- python-dotenv
- ElevenLabs, optional

---

# Project Structure

```text
FieldMedic/
|
+-- app.py
+-- ai.py
+-- safety.py
+-- references.py
+-- voice.py
+-- telegram_bot.py
+-- requirements.txt
+-- README.md
+-- .env
+-- .gitignore
|
+-- references/
    |
    +-- README.txt
    +-- start_triage_reference.txt
```

## File Responsibilities

### `app.py`

Runs the Streamlit web application.

### `ai.py`

Communicates with the locally running Gemma model and builds the structured FieldMedic assessment.

### `safety.py`

Contains deterministic safety checks.

### `references.py`

Searches the offline reference library.

### `telegram_bot.py`

Provides the optional Telegram mobile interface.

### `voice.py`

Provides optional ElevenLabs speech generation.

### `.env`

Contains API tokens and secrets.

**Never upload `.env` to GitHub.**

---

# Complete Installation Guide

The following instructions assume a new user is setting up FieldMedic on Windows.

---

## Step 1: Install Python

Install a recent Python 3 version.

During installation on Windows, enable:

```text
Add Python to PATH
```

Open PowerShell and confirm:

```powershell
python --version
```

A Python version number should appear.

---

# Step 2: Install Git

Install Git if you intend to clone FieldMedic from GitHub.

Confirm:

```powershell
git --version
```

---

# Step 3: Install Ollama

Install Ollama.

After installation, restart PowerShell or VS Code if necessary.

Confirm:

```powershell
ollama --version
```

---

# Step 4: Download Gemma

FieldMedic requires the Ollama model specified inside `ai.py`.

For the current configuration:

```powershell
ollama pull gemma4
```

The model download may be relatively large and may take some time.

Verify your installed Ollama models:

```powershell
ollama list
```

Make sure you see the model that FieldMedic is configured to use.

Test it:

```powershell
ollama run gemma4
```

Enter:

```text
Hello
```

If Gemma generates a response, local inference is working.

Exit the interactive session with:

```text
/bye
```

---

# Step 5: Download FieldMedic

Clone the repository:

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then enter the project:

```powershell
cd FieldMedic
```

Alternatively:

1. Open the GitHub repository.
2. Select **Code**.
3. Select **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted FieldMedic directory in VS Code.

## Windows Recommendation

Use a short directory such as:

```text
C:\FieldMedic
```

instead of:

```text
C:\Users\YourName\OneDrive - Organization\Documents\FieldMedic
```

A shorter path can avoid Windows path-length problems with deeply nested Python packages.

---

# Step 6: Open the Project in VS Code

Open VS Code.

Select:

```text
File -> Open Folder
```

Open:

```text
C:\FieldMedic
```

Then select:

```text
Terminal -> New Terminal
```

---

# Step 7: Create a Virtual Environment

Run:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If Windows reports that script execution is disabled, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

You should eventually see something similar to:

```text
(.venv) PS C:\FieldMedic>
```

Do not type:

```text
(.venv) PS C:\FieldMedic>
```

yourself.

That is PowerShell's prompt.

---

# Step 8: Upgrade pip

Run:

```powershell
python -m pip install --upgrade pip
```

---

# Step 9: Install Dependencies

Run:

```powershell
pip install -r requirements.txt
```

A typical FieldMedic `requirements.txt` contains:

```text
streamlit
ollama
pydantic
python-dotenv
python-telegram-bot
elevenlabs
```

If you are not using ElevenLabs, the voice integration can remain disabled.

The core FieldMedic analysis does not depend on ElevenLabs.

---

# Step 10: Check Offline References

Make sure this directory exists:

```text
FieldMedic\references\
```

and contains your local reference material.

For example:

```text
references/
|
+-- README.txt
+-- start_triage_reference.txt
```

The reference library is part of FieldMedic's offline retrieval system.

---

# Step 11: Check for Python Syntax Errors

Before starting the application, run:

```powershell
python -m py_compile app.py ai.py safety.py references.py telegram_bot.py
```

If the command returns to the normal PowerShell prompt without displaying anything, Python did not detect a syntax error in those files.

---

# Running FieldMedic

## Step 12: Start the Website

Make sure the virtual environment is active:

```text
(.venv)
```

Then run:

```powershell
streamlit run app.py
```

Streamlit should open your browser.

If it does not, look for an address similar to:

```text
http://localhost:8501
```

Open that address manually.

Keep the terminal open while FieldMedic is running.

To stop Streamlit:

```text
Ctrl + C
```

---

# Telegram Setup

Telegram is optional.

Skip this section if you only want to run the web interface.

---

## Step 13: Create a Telegram Bot

Open Telegram.

Find the official BotFather account.

Send:

```text
/newbot
```

Follow the prompts to choose:

1. A bot display name
2. A unique bot username

BotFather will provide a bot token.

Treat this token like a password.

Do not post it on GitHub.

---

# Step 14: Create `.env`

Create:

```text
.env
```

inside your main FieldMedic directory.

Add:

```text
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
```

For optional ElevenLabs support:

```text
ELEVENLABS_API_KEY=YOUR_ELEVENLABS_KEY
ELEVENLABS_VOICE_ID=YOUR_VOICE_ID
```

Do not place spaces around `=`.

---

# Step 15: Protect Your Secrets

Your `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
*.mp3
```

Before uploading the repository, run:

```powershell
git status
```

Verify that:

```text
.env
```

does **not** appear in the files being committed.

If a Telegram or ElevenLabs token is accidentally published, revoke it and create a new token.

---

# Step 16: Start the Telegram Bot

Keep your Streamlit terminal running.

Open a **second VS Code terminal**.

If necessary:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Start Telegram:

```powershell
python telegram_bot.py
```

You should see:

```text
FieldMedic Telegram bot is running.
Press Ctrl+C to stop it.
```

Leave this terminal running.

---

# Step 17: Test Telegram

Open your bot from your phone or Telegram desktop.

Send:

```text
/start
```

Then test using synthetic data:

```text
/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy and confused; injuries=deep leg wound; altered=yes; bleeding=yes
```

FieldMedic should send the observations through the local analysis pipeline and return a structured assessment.

---

# Optional ElevenLabs Setup

If you want spoken assessment summaries:

1. Obtain an ElevenLabs API key.
2. Put it in `.env`.

```text
ELEVENLABS_API_KEY=YOUR_API_KEY
```

If required:

```text
ELEVENLABS_VOICE_ID=YOUR_VOICE_ID
```

Restart Streamlit after modifying `.env`.

Stop Streamlit:

```text
Ctrl + C
```

Restart:

```powershell
streamlit run app.py
```

Voice requires internet connectivity.

The core FieldMedic analysis does not.

---

# Starting FieldMedic After Initial Installation

You do not need to repeat the entire installation process every time.

Normally, you only need the following.

## Terminal 1: Website

```powershell
cd C:\FieldMedic
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Terminal 2: Telegram

```powershell
cd C:\FieldMedic
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
python telegram_bot.py
```

Ollama must also be installed and available.

Verify with:

```powershell
ollama list
```

---

# Demonstration Cases

Use synthetic patient data only.

## Case 1: Lower-Risk Synthetic Case

```text
Age:
20

Symptoms:
Awake, alert, mild pain in left hand

Heart Rate:
78

Respiratory Rate:
16

Blood Pressure:
118/76

Oxygen Saturation:
99%

Visible Injuries:
Small superficial scrape on left hand

Altered Mental Status:
No

Uncontrolled Bleeding:
No
```

Telegram:

```text
/analyze age=20; hr=78; rr=16; bp=118/76; o2=99; symptoms=awake and alert with mild pain in left hand; injuries=small superficial scrape on left hand; altered=no; bleeding=no
```

The purpose of this case is to show that FieldMedic does not automatically treat every submitted patient as a critical emergency.

---

## Case 2: Critical Synthetic Trauma Case

```text
Age:
22

Symptoms:
Dizzy, pale, confused, and becoming less responsive

Heart Rate:
128

Respiratory Rate:
28

Blood Pressure:
85/55

Oxygen Saturation:
94%

Visible Injuries:
Deep leg wound with significant bleeding

Altered Mental Status:
Yes

Uncontrolled Bleeding:
Yes
```

Telegram:

```text
/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy, pale, confused, and becoming less responsive; injuries=deep leg wound with significant bleeding; altered=yes; bleeding=yes
```

This synthetic example exercises several FieldMedic safety checks simultaneously.

---

# Complete Demonstration Setup

A complete demonstration can use three terminals/components:

```text
                    FieldMedic Demo

                         Ollama
                           |
                         Gemma
                           |
                 FieldMedic Backend
                      /         \
                     /           \
            Streamlit             Telegram
            Website                 Bot
               |                     |
             Laptop                 Phone
```

### Before presenting

Check Ollama:

```powershell
ollama list
```

Start Streamlit:

```powershell
streamlit run app.py
```

Start Telegram in another terminal:

```powershell
python telegram_bot.py
```

Then test:

```text
Website -> Synthetic Case 1
Website -> Synthetic Case 2
Telegram -> /start
Telegram -> Synthetic Case 2
```

---

# Troubleshooting

## Python Is Not Recognized

If:

```text
python is not recognized
```

appears, reinstall Python and enable:

```text
Add Python to PATH
```

during installation.

---

## Ollama Is Not Recognized

Restart VS Code or PowerShell after installing Ollama.

Then:

```powershell
ollama --version
```

---

## Model Not Found

If you see:

```text
model 'gemma4' not found
```

check:

```powershell
ollama list
```

If Gemma is missing:

```powershell
ollama pull gemma4
```

The model name configured inside `ai.py` must exactly match an installed Ollama model.

---

# PowerShell Says Scripts Are Disabled

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

This changes the policy only for the current PowerShell process.

---

# Telegram Token Is Missing

Check that:

```text
.env
```

exists directly inside the FieldMedic project directory.

It needs:

```text
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
```

Then restart:

```powershell
python telegram_bot.py
```

---

# Telegram Works but Analysis Fails

First test Ollama:

```powershell
ollama list
```

Then test Gemma directly:

```powershell
ollama run gemma4
```

If Gemma works directly but FieldMedic does not, check the model configured inside:

```text
ai.py
```

It must match the name displayed by:

```powershell
ollama list
```

---

# Windows Path-Length Error

If a dependency produces a Windows long-path error, the project path may be too long.

Instead of:

```text
C:\Users\Username\OneDrive - Organization\Documents\FieldMedic
```

move the project to:

```text
C:\FieldMedic
```

Delete the old `.venv`, create a new one, activate it, and reinstall dependencies:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# Streamlit Is Already Running

Stop the existing instance by clicking its terminal and pressing:

```text
Ctrl + C
```

Then restart:

```powershell
streamlit run app.py
```

---

# Privacy

FieldMedic contains both local and connected components.

## Local

```text
Gemma inference
Ollama
Python safety engine
Offline reference retrieval
Local Streamlit interface
```

## Connected

```text
Telegram
ElevenLabs
```

The correct description is:

> FieldMedic's core AI inference, deterministic safety system, and reference retrieval can run locally while Telegram and ElevenLabs provide optional connected interfaces.

Do not enter personally identifiable healthcare information into the demonstration system.

---

# Limitations

FieldMedic is an experimental educational and competition prototype.

It:

- Is not a medical device
- Is not clinically validated
- Does not provide confirmed diagnoses
- Should not autonomously make treatment decisions
- Should not replace trained responders
- Should not replace emergency medical services
- Can produce incorrect AI-generated information
- Depends on the accuracy of information supplied by the user
- Depends on the quality of its local reference library
- Has not been validated for real-world clinical deployment

FieldMedic should currently be evaluated as a demonstration of:

- Local open-weight AI
- Deterministic safety logic
- Retrieval-Augmented Generation
- Structured AI output
- Offline-first system design
- Disaster-response human-computer interaction

---

# Future Improvements

Potential future work includes:

- Vector-based offline RAG
- Larger authoritative reference libraries
- Fully offline speech-to-text
- Fully offline text-to-speech
- Multilingual responder support
- Dedicated offline mobile application
- Reassessment tracking
- Multiple-patient incident dashboard
- Resource availability tracking
- Patient handoff reports
- Offline mesh networking
- Model uncertainty visualization
- Evaluation against standardized synthetic scenarios
- Formal review by emergency medicine professionals
- Formal review by disaster-response professionals

---

# Setup Checklist

Before running FieldMedic, confirm:

- [ ] Python is installed
- [ ] Git is installed if cloning the repository
- [ ] Ollama is installed
- [ ] Gemma is downloaded
- [ ] `ollama list` displays the correct model
- [ ] The FieldMedic repository is downloaded
- [ ] `.venv` has been created
- [ ] `.venv` is activated
- [ ] Python dependencies are installed
- [ ] `references/` exists
- [ ] Offline reference files are present
- [ ] `ai.py` specifies the correct Ollama model
- [ ] Streamlit launches successfully
- [ ] `.env` is excluded from Git
- [ ] Telegram token is configured if using Telegram
- [ ] Telegram `/start` works
- [ ] Telegram `/analyze` works
- [ ] ElevenLabs is configured only if voice is desired
- [ ] Synthetic cases have been tested

---

# Why FieldMedic?

Most AI applications assume there will always be connectivity.

Disasters cannot make that assumption.

FieldMedic explores a different question:

> **What if useful AI decision support could remain available when the network and normal infrastructure are not?**

By combining local open-weight AI, deterministic safety checks, offline reference retrieval, and responder-focused interfaces, FieldMedic explores how useful AI capabilities might remain accessible in infrastructure-constrained environments.

---

# Disclaimer

**FieldMedic is an educational and competition prototype only.**

It is not intended for clinical use, diagnosis, treatment, autonomous triage, or autonomous medical decision-making.

Never delay or replace professional emergency medical care based on FieldMedic output.

For real emergencies, contact the appropriate emergency services and follow established local emergency-response protocols.
