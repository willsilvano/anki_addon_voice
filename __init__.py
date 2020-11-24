import uuid
import os
import random
import requests
from anki.hooks import addHook
from aqt.utils import showInfo, showWarning
from aqt.sound import play
from aqt.editor import Editor


# cross out the currently selected text


def getWatsonVoice(editor, voice='random'):

    text = editor.web.selectedText()
    if not text:
        showInfo("Selecione o texto!")
        return

    if voice == 'random':
        voice = random.choice(['Allison', 'Lisa', 'Michael', 'Olivia'])

    url = 'https://text-to-speech-demo.ng.bluemix.net/api/v3/synthesize?voice=en-US_{}V3Voice&download=true&accept=audio%2Fmp3&text={}'.format(
        voice, text)

    try:
        response = requests.get(url, timeout=10)
    except:
        showWarning("Ocorreu um erro, tente novamente!")
        return

    hash = uuid.uuid4().hex
    file = "english-{}.mp3".format(hash)
    file_path = os.path.join(".", file)

    with open(file_path, mode='wb') as localfile:
        localfile.write(response.content)

    text = "[sound:{}]".format(file)
    editor.web.eval("wrap('',' {}')".format(text))
    play(file_path)


def getAllisonVoice(editor):
    getWatsonVoice(editor, 'Allison')


def getMichaelVoice(editor):
    getWatsonVoice(editor, 'Michael')


def getLisaVoice(editor):
    getWatsonVoice(editor, 'Lisa')


def getOliviaVoice(editor):
    getWatsonVoice(editor, 'Olivia')


def addWatsonButton(buttons, editor):
    editor._links['allison_voice'] = getAllisonVoice
    editor._links['michael_voice'] = getMichaelVoice
    editor._links['lisa_voice'] = getLisaVoice
    editor._links['olivia_voice'] = getOliviaVoice

    buttons += [editor._addButton(
        "/home/willian/.local/share/Anki2/addons21/watson_speak/voice.png",
        "allison_voice",
        "Allison Voice")]

    buttons += [editor._addButton(
        "/home/willian/.local/share/Anki2/addons21/watson_speak/voice.png",
        "michael_voice",
        "Michael Voice")]

    buttons += [editor._addButton(
        "/home/willian/.local/share/Anki2/addons21/watson_speak/voice.png",
        "lisa_voice",
        "Lisa Voice")]

    buttons += [editor._addButton(
        "/home/willian/.local/share/Anki2/addons21/watson_speak/voice.png",
        "olivia_voice",
        "Olivia Voice")]

    return buttons


addHook("setupEditorButtons", addWatsonButton)
