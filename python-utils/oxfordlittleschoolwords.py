import re, os

def create_words1a5b_file():
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

    with open('data\\words1a5b.txt', 'w', encoding='utf-8') as fd:
        fd.writelines([word.strip(' ')+'\n' for word in words_1a5b])

def main():
    create_1a5b_file()

main()