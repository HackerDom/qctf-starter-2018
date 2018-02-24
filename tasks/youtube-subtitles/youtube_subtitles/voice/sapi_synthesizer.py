import tts.sapi


engine = tts.sapi.Sapi()
for name in engine.get_voice_names():
    if 'English' in name:
        engine.set_voice(name)
        break
engine.set_rate(-2)


def create_recording(filename, text):
    engine.create_recording(filename, text)
