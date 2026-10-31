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
# Complete Setup Guide
 
The following instructions explain how to set up FieldMedic from a fresh computer.
 
---
 
## 1. Install Python
 
FieldMedic requires Python.
 
Download and install Python from:
 
https://www.python.org/downloads/
 
During installation on Windows, make sure you check:
 
```text
Add Python to PATH

After installation, open PowerShell and verify:

PowerShell
python --version

You should see a Python version number.

2. Install Git

Download Git from:

https://git-scm.com/downloads


After installation, verify:

```powershell
git --version

3. Install Ollama

FieldMedic uses Ollama to run the open-weight AI model locally.

Download Ollama from:

https://ollama.com/download


Confirm the installation:

```powershell
ollama --version


If the command is not recognized, restart your terminal or computer after installing Ollama.

4. Download the AI Model

FieldMedic is configured to use Gemma through Ollama.

Run:

PowerShell
ollama pull gemma4

This may take several minutes depending on your internet speed and computer.

After the download completes, verify the model:

PowerShell
ollama list
 

You should see gemma4 in the list.

Test the model:

PowerShell
ollama run gemma4

Enter:

Plain Text
Hello

If the model responds, Ollama is working.

Exit with:

Plain Text
/bye

IMPORTANT:

The model name in ai.py must exactly match the model installed in Ollama.

For example:

Python
model="gemma4"

If you change models, change this value in ai.py as well.

5. Download FieldMedic

Clone the repository:

PowerShell
git clone YOUR_GITHUB_REPOSITORY_URL

Then:

PowerShell
cd FieldMedic

Alternatively, download the repository as a ZIP file from GitHub and extract it.

On Windows, a short folder path is recommended:

Plain Text
C:\FieldMedic

This can help avoid Windows path-length problems with some Python packages.

6. Create the Virtual Environment

From inside the FieldMedic folder:

PowerShell
python -m venv .venv

Activate it:

PowerShell
.venv\Scripts\Activate.ps1

If Windows reports:

Plain Text
running scripts is disabled on this system

run:

PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then try again:

PowerShell
.venv\Scripts\Activate.ps1

Once activated, the terminal should look similar to:

Plain Text
(.venv) PS C:\FieldMedic>

Do not type the:

Plain Text
(.venv) PS C:\FieldMedic>

portion yourself. PowerShell displays it automatically.

7. Upgrade pip

Run:

PowerShell
python -m pip install --upgrade pip
8. Install FieldMedic Dependencies

Run:

PowerShell
pip install -r requirements.txt

The project uses packages including:

Plain Text
streamlit
ollama
pydantic
python-dotenv
python-telegram-bot
elevenlabs

If ElevenLabs causes an installation problem and you do not need voice output, it can be removed temporarily because voice is not required for the core FieldMedic system.

9. Check the Offline Reference Library

Make sure the project contains:

Plain Text
FieldMedic/
|
+-- references/
|
+-- start_triage_reference.txt

FieldMedic searches this directory for offline reference material.

Additional reference files can be placed here as .txt files.

Only use authoritative reference material that you are legally allowed to store and redistribute.

10. Check the Python Files

Before starting FieldMedic, you can check for basic syntax errors:

PowerShell
python -m py_compile app.py ai.py safety.py references.py telegram_bot.py

If this command displays nothing, the files passed Python's syntax check.

If Python shows an error, fix that error before proceeding.

Running the Website
11. Start FieldMedic

Make sure your terminal begins with:

Plain Text
(.venv)

Then run:

PowerShell
streamlit run app.py

Your browser should open automatically.

If it does not, Streamlit will display an address similar to:

Plain Text
http://localhost:8501

Open that address in your browser.

Keep the terminal open while using FieldMedic.

To stop the application, click the terminal and press:

Plain Text
Ctrl + C
Telegram Setup

Telegram support is optional.

The main FieldMedic website does not require Telegram.

12. Create a Telegram Bot

Open Telegram and search for:

Plain Text
@BotFather

Send:

Plain Text
/newbot

Follow the instructions.

BotFather will ask you for:

A display name
A unique bot username

The username normally ends in:

Plain Text
bot

For example:

Plain Text
FieldMedicDemoBot

BotFather will then provide a bot token.

Treat this token like a password.

DO NOT upload it to GitHub.

13. Create .env

Inside the main FieldMedic folder create:

Plain Text
.env

Add:

Plain Text
TELEGRAM_BOT_TOKEN=PASTE_YOUR_TOKEN_HERE

If using ElevenLabs, you can also add:

Plain Text
ELEVENLABS_API_KEY=PASTE_YOUR_KEY_HERE
ELEVENLABS_VOICE_ID=YOUR_VOICE_ID

Example folder structure:

Plain Text
FieldMedic/
|
+-- app.py
+-- ai.py
+-- safety.py
+-- references.py
+-- telegram_bot.py
+-- voice.py
+-- requirements.txt
+-- .env
+-- .gitignore
|
+-- references/
+-- start_triage_reference.txt

Never include spaces around the = in .env.

14. Protect API Keys

Make sure .gitignore contains:

Plain Text
.env
.venv/
__pycache__/
*.pyc
*.mp3

Before pushing to GitHub, run:

PowerShell
git status

Make sure .env DOES NOT appear in the files being committed.

If a Telegram or ElevenLabs key is accidentally uploaded publicly, revoke it immediately and generate a new one.

Running the Telegram Bot
15. Open a Second Terminal

Keep Streamlit running in the first terminal.

Open another terminal in VS Code.

Activate the virtual environment again:

PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:

PowerShell
.venv\Scripts\Activate.ps1

Run:

PowerShell
python telegram_bot.py

You should see:

Plain Text
FieldMedic Telegram bot is running.
Press Ctrl+C to stop it.

Leave this terminal running.

16. Connect to the Bot

Open your bot in Telegram.

Send:

Plain Text
/start

The bot should return FieldMedic instructions.

Then try a synthetic example:

Plain Text
/analyze age=22; hr=128; rr=28; bp=85/55; o2=94; symptoms=dizzy and confused; injuries=deep leg wound; altered=yes; bleeding=yes

Do not enter real personally identifying patient information into Telegram.

Telegram is an online interface even though FieldMedic's AI inference runs locally.

Optional ElevenLabs Voice Setup

FieldMedic can optionally generate a spoken version of limited assessment information.

Create an ElevenLabs account and obtain an API key.

Add it to .env:

Plain Text
ELEVENLABS_API_KEY=YOUR_API_KEY

If required by your version of voice.py, also provide:

Plain Text
ELEVENLABS_VOICE_ID=YOUR_VOICE_ID

Restart Streamlit after changing .env:

Plain Text
Ctrl + C

Then:

PowerShell
streamlit run app.py

Voice functionality requires internet connectivity.

The core FieldMedic AI does not require ElevenLabs.

Starting the Full FieldMedic System

After the initial installation, you do not need to repeat all of the setup steps every time.

Normally, starting FieldMedic requires the following:

Terminal 1 - Website
PowerShell
cd C:\FieldMedic
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
streamlit run app.py
 
Terminal 2 - Telegram Bot
PowerShell
cd C:\FieldMedic
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
python telegram_bot.py

Ollama must also be installed and available on the computer.

Verify with:

PowerShell
ollama list
Quick System Test

Before a demonstration, test FieldMedic with synthetic data.

Example 1 - Lower-Risk Case
Plain Text
Age: 20
Heart Rate: 78
Respiratory Rate: 16
Blood Pressure: 118/76
Oxygen: 99
 
Symptoms:
Awake and alert with mild left-hand pain.
 
Injuries:
Small superficial scrape on left hand.
 
Altered Mental Status:
No
 
Uncontrolled Bleeding:
No
Example 2 - Critical Synthetic Case
Plain Text
Age: 22
Heart Rate: 128
Respiratory Rate: 28
Blood Pressure: 85/55
Oxygen: 94
 
Symptoms:
Dizzy, pale, confused, and becoming less responsive.
 
Injuries:
Deep leg wound with significant bleeding.
 
Altered Mental Status:
Yes
 
Uncontrolled Bleeding:
Yes

These cases are fictional and intended only to test the software.

Troubleshooting
python is not recognized

Reinstall Python and make sure:

Plain Text
Add Python to PATH

is selected during installation.

ollama is not recognized

Install Ollama and restart PowerShell or VS Code.

Then test:

PowerShell
ollama --version
Model Not Found

If you see:

Plain Text
model 'gemma4' not found

run:

PowerShell
ollama pull gemma4

Verify:

PowerShell
ollama list

The name inside ai.py must match the installed Ollama model.

PowerShell Blocks .venv

Run:

PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:

PowerShell
.venv\Scripts\Activate.ps1
Telegram Token Missing

Check that:

Plain Text
.env
 

exists in the main FieldMedic directory.

It should contain:

Plain Text
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
 

Then restart:

PowerShell
python telegram_bot.py
Telegram Works but AI Analysis Fails

First verify Ollama:

PowerShell
ollama list

Then test the model directly:

PowerShell
ollama run gemma4

If the model works directly but FieldMedic does not, verify that ai.py uses the exact same model name.

Streamlit Port Is Already Being Used

First stop any older Streamlit terminal with:

Plain Text
Ctrl + C

Then restart:

PowerShell
streamlit run app.py
Important Privacy Information

The FieldMedic architecture contains both local and connected components.

LOCAL:

Plain Text
Gemma inference
Ollama
Safety checks
Offline reference retrieval
Local Streamlit interface

CONNECTED:

Plain Text
Telegram
ElevenLabs

Therefore, do not claim that the entire FieldMedic system is offline when using Telegram or ElevenLabs.

A more accurate description is:

FieldMedic's core AI inference, safety system, and reference retrieval can operate locally, while Telegram and ElevenLabs are optional connected interfaces.
