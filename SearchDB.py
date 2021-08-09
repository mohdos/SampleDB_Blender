import PyPDF2
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import glob

def get_text_from_pdf(filename):
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    if text != "":
       text = text
    else:
       text = textract.process(filename, method='tesseract', language='eng')
    
    return text


def search_key_in_text(text, key):
    tokens = word_tokenize(text)
    punctuation = ['(',')',';',':','[',']',',']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and  not word in punctuation]
    
    NUM_WORDS_BEFORE = 30
    NUM_WORDS_AFTER = 30
    for i in range(len(keywords)):
        keyword = keywords[i]
        if keyword == key:
            min_index = i - NUM_WORDS_BEFORE if (i - NUM_WORDS_BEFORE) >= 0 else 0
            max_index = i + NUM_WORDS_AFTER if (i + NUM_WORDS_AFTER) < len(keywords) else len(keywords) - 1
            return " ".join(keywords[min_index: max_index])

    return ""

def searchInPDF_folder(folder, key):
    
    for filename in glob.glob(folder + "/*"):
        original_text = get_text_from_pdf(filename=filename)
        result_text = search_key_in_text(original_text, key)
        if result_text != "":
            returned_dict = {}
            returned_dict["title"] = filename.split("/")[-1]
            returned_dict["content"] = result_text
            return returned_dict
    
    return None
    
    
