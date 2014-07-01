# -*- coding: utf-8

LANG = 'english'
wordlist = open('labMTwords-%s.csv' % LANG,'r').read().split('\n')
scores = open('labMTscores-%s.csv' % LANG,'r').read().split('\n')

import nltk
from nltk.tokenize import RegexpTokenizer
TOKENIZER = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
SPECIAL_CHARS = ['.', ',', '!', '?']

def get_words(text=''):
    words = []
    pos = []
    lastpos = 0
    words = TOKENIZER.tokenize(text)
    filtered_words = []
    for word in words:
        if word in SPECIAL_CHARS or word == " ":
            pass
        else:
            new_word = word.replace(",","").replace(".","")
            new_word = new_word.replace("!","").replace("?","")
            lastpos =  text[lastpos:].find(new_word) + lastpos
            filtered_words.append(new_word)
            pos.append(lastpos)
            lastpos = lastpos + len(new_word)
    return filtered_words, pos

def hi(s, ws=None):

    if not ws:
        s = s.lower()
        s = s.replace('\n', ' ')
        ws, pos = get_words(s)

    df = {}
    for w in ws:
         if w in wordlist and (float(scores[wordlist.index(w)].strip())<=3 or float(scores[wordlist.index(w)].strip())>=7):
            df[w] = df.get(w,0)+1

    h = 0.
    f = 0
    for k in df.keys():
        h = h + df[k]*float(scores[wordlist.index(k)].strip())
        f = f + df[k]

    if f>0:
        return h/f
    else:
        return None

def hgraph(s, window):

    import matplotlib.pyplot as plt

    text = s.lower()
    text = text.replace('\n', ' ')
    ws, pos = get_words(text)

    i = 0
    h = []

    maxhi = 0
    minhi = 9999999999999999
    maxi = 0
    mini = 0

    while(i+window<=len(ws)):

        whi = hi('',ws[i:i+window])

        if whi:
            if whi > maxhi:
                maxhi = whi
                maxi = i
            if whi < minhi:
                minhi= whi
                mini= i
            h.append(whi)

        i = i + 1

    h.append(hi('',ws[i:]))

    # this helps figuring out if a small window is meaningful
    print "Max score sequence:", maxhi
    print s[pos[maxi]:pos[maxi+window]+len(ws[maxi+window])]
    print
    print "Min score sequence:", minhi
    print s[pos[mini]:pos[mini+window]+len(ws[mini+window])]

    plt.plot(h)
    plt.show()

if __name__ == "__main__":

    s1 = '''Shiny Happy People (...)
'''

    s2 = '''Losing My Religion (...)
'''

    s3 = '''Stop Crying Your Heart Out (...)
'''

    print hi(s1)
    print hi(s2)
    print hi(s3)
    hgraph(s3,20)
