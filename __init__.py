from anki.hooks import addHook
import os.path
import json
import re

import urllib.parse
import urllib.request    

from aqt.qt import * 
from aqt import mw


def yieldFurigana(motKanji):  # return motKanji with furigana added to the string
    try:
        urllib.request.urlretrieve("https://jisho.org/word/" + urllib.parse.quote(motKanji), "tempo.txt")

    except Exception as e:
        print("Error 404")
        return motKanji
        
    with open('tempo.txt') as f:
        L = f.readlines()[574:575]

    hiragana = "".join(re.findall('(?<=i">)[^</spa]*', L[0]))
    furigana = "<ruby>{0}<rt>{1}</rt></ruby>".format(motKanji, hiragana)
    return furigana


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def addFurigana(editor):
    selection = editor.web.selectedText()
    if not selection:
        return
    editor.web.eval(
        "document.execCommand('insertHTML', false, %s);"
        % json.dumps(yieldFurigana(selection)))


def setupEditorButtonsFilter(buttons, editor):
    key = QKeySequence(gc('Key_insert_furigana'))
    keyStr = key.toString(QKeySequence.NativeText)
    if gc('Key_insert_furigana'):
        b = editor.addButton(
            os.path.join(os.path.dirname(__file__), "icons", "furigana.png"),
            "button_add_furigana",
            addFurigana,
            tip="Insert furigana".format(keyStr),
            keys=gc('Key_insert_furigana')
            )
        buttons.append(b)
    return buttons


addHook("setupEditorButtons", setupEditorButtonsFilter)
