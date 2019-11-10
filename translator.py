
from translate import Translator

def hardTrans(text,lang):
    #translator = Translator(to_lang = lang)
    #print('translating..')
    #return translator.translate(text)
    return ''

try:
    f = open('trans.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
except FileNotFoundError:
    lines = []
# "cat|de:katze"



phrases = []
answers = []

for i in range(0,len(lines)):
    phrases.append(lines[i].partition(':')[0])
    answers.append(lines[i].partition(':')[2].rstrip())

def trans(text,lang):
    phrase = text + '|' + lang
    
    if phrase in phrases:
        i = phrases.index(phrase)
        return answers[i]
    
    ans = hardTrans(text,lang)
    
    f = open('trans.txt','a', encoding='utf-8')
    
    f.write(phrase + ':' + ans + '\n')
    phrases.append(phrase)
    answers.append(ans)
    f.close()
    
    return ans