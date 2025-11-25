from flask import Blueprint
from app.views.VoicetoText import render_voice_page

web = Blueprint("web", __name__)

@web.get("/voice")
def voice_page():
    return render_voice_page()
