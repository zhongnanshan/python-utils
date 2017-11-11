import re, os

def main():
    words1a3bfile = os.path.join(os.getcwd(), 'data\\牛津小学英语1A_3B.txt')
    words1a5bfile = os.path.join(os.getcwd(), 'data\\牛津小学英语1A_5B.txt')

    words_1a3b = []
    with open(words1a3bfile, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            wordlist = re.split(r'\t+', line)
            words_1a3b.append(wordlist[0])
            print(wordlist[0])

    words_1a5b = []
    with open(words1a5bfile, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            wordlist = re.split(r'\t+', line)
            words_1a5b.append(wordlist[0])
            print(wordlist[0])

main()