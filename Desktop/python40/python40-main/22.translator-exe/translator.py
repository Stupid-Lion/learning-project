import googletrans
import tkinter
from tkinter import ttk
import tkinter.font
from gtts import gTTS
from playsound import playsound
import os



def clear_text(event):
    if text_widget1.get("1.0",tkinter.END).strip() == "번역할 문장을 입력하세요.":
        text_widget1.delete("1.0",tkinter.END)
    

def translate_text():
    tranlator = googletrans.Translator()
    input_text = text_widget1.get("1.0",tkinter.END).strip()
    if not input_text:
        return
    select_lang = lang_combobox.get()
    dest_lang = lang_mapping.get(select_lang,'en')
    result = tranlator.translate(input_text,dest=dest_lang,src='auto')
    text_widget2.config(state="normal")
    text_widget2.delete("1.0",tkinter.END)
    text_widget2.insert(tkinter.END, result.text)
    text_widget2.config(state="disabled")
    
def tts_text():
    save_path = r"C:\Users\USER\Documents\translated.mp3"
    if  os.path.exists(save_path):
        os.remove(save_path)
    get_text = text_widget2.get("1.0",tkinter.END)
    select_lang2 = lang_combobox.get()
    dest_lang2 = lang_mapping.get(select_lang2,'en')
    tts = gTTS(text=get_text,lang=dest_lang2)
    tts.save(save_path)
    playsound(save_path)


window=tkinter.Tk()

titlefont = tkinter.font.Font(size=16,weight="bold")

window.title("번역기")
window.geometry("800x200+500+300")
window.resizable(False,False)
window.configure(bg="#f0f0f0") 

tras_button = tkinter.Button(window, overrelief="solid",text="번역하기",width=30,command=translate_text)
tts_button = tkinter.Button(window, overrelief="solid",text="듣기",width=15,command=tts_text)
text_widget1 = tkinter.Text(window, height=10, width=50,)
text_widget1.insert("1.0","번역할 문장을 입력하세요.")
text_widget1.bind("<FocusIn>",clear_text)
text_widget2 = tkinter.Text(window, height=10, width=50, state="disabled")

lang_mapping = {
    '영어': 'en',
    '한국어': 'ko',
    '일본어': 'ja',
    '스페인어': 'es',
    '프랑스어': 'fr',
    '독일어': 'de',
    '중국어': 'zh-CN'
}
lang_option = list(lang_mapping.keys())
lang_label = tkinter.Label(window,text="번역할 언어")
lang_combobox = ttk.Combobox(window, values=lang_option,state="readonly",width=15)
lang_combobox.set('영어')

text_widget1.pack(side="left",padx=10,pady=10)
text_widget2.pack(side="right",padx=10,pady=10)
tras_button.pack(pady=5)
tts_button.pack(pady=5)
lang_combobox.pack(pady=5)
window.mainloop()