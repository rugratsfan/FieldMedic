import os
from io import BytesIO

from dotenv import load_dotenv

load_dotenv()


def voice_is_available():
    return bool(
        os.getenv("ELEVENLABS_API_KEY")
    )


def create_voice_audio(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is missing from .env"
        )

    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(
        api_key=api_key
    )

    audio_iterator = client.text_to_speech.convert(
        voice_id=os.getenv(
            "ELEVENLABS_VOICE_ID",
            "JBFqnCBsd6RMkjVDRZzb"
        ),
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        text=text
    )

    audio_bytes = b"".join(audio_iterator)

    return BytesIO(audio_bytes)