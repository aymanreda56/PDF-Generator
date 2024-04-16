import re

def reverse_arabic_text(arabicText):
    '''
        this function just takes an arabic sentence, splits it by spaces, then reverses each word.
        this is because tkinter does not support RTL rendering of arabic text.
    '''
    tokens = re.split(r' ',arabicText[::-1])
    print(tokens)
    tokens.reverse()
    return ' '.join(tokens)



testText = r"أيمن محمد رضا"

print(reverse_arabic_text(testText))