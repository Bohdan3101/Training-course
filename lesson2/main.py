import PyPDF2
from gtts import gTTS

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def text_to_audio(text, audio_path):
    tts = gTTS(text=text, lang='uk')
    tts.save(audio_path)

def pdf_to_audio(pdf_path, audio_path):
    text = pdf_to_text(pdf_path)
    text_to_audio(text, audio_path)
    print(f"PDF файл '{pdf_path}' успішно перетворено в аудіофайл '{audio_path}'")

if __name__ == "__main__":
    pdf_path = input("Введіть шлях до pdf: ").strip()
    audio_path = input("Введіть шлях для збереження аудіо: ").strip()
    pdf_to_audio(pdf_path, audio_path)

