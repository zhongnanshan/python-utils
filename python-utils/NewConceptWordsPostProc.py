import re, random, time, os, urllib, shelve, shutil
from urllib import error, request
from bs4 import BeautifulSoup
from pathlib import Path

class WordVoice():
    
    def __init__(self):
        first_dir = 'D:/Backup/english/voice_from_Macmillan'
        second_dir = 'D:/Backup/english/voice'
        fp = Path(first_dir)
        sp = Path(second_dir)
        self.first_voice = {x.name.split('_')[0] : x for x in fp.iterdir() if not x.is_dir()}
        db_file = os.path.join(second_dir, 'db_file')
        if os.path.exists(db_file):
            self.second_voice = shelve.open(db_file)
        else:
            sp_subdir = [x for x in sp.iterdir() if x.is_dir()]
            second_voice_dict_list = [{x.name : x for x in subdir.iterdir() if not x.is_dir()} for subdir in sp_subdir]
            self.second_voice = dict()
            for dd in second_voice_dict_list:
                for key, val in zip(dd.keys(), dd.values()):
                    self.second_voice[key.split('.')[0]] = val
            #with shelve.open(db_file) as db:
            #    for key, val in zip(self.second_voice.keys(), self.second_voice.values()):
            #        db[key] = val

    def get_voice(self, word):
        if word in self.first_voice.keys():
            return self.first_voice[word]
        elif word in self.second_voice.keys():
            return self.second_voice[word]
        else:
            return None


def post_proc(fileName):
    words = []
    word_voice = WordVoice()
    with open(fileName, 'r', encoding='utf-8') as fd:
        lines = fd.readlines()
        for line in lines:
            linelist = re.split(r'\t+', line)
            words.append((linelist, len(linelist)))
            print('{0},{1}'.format(linelist[0],len(linelist)))    
    word_filter_dict = dict()
    word_voice_dir = os.path.join(os.getcwd(), fileName.split('.')[0]+'_New')
    if not os.path.exists(word_voice_dir):
        os.mkdir(word_voice_dir)
    with open(fileName.split('.')[0]+'_New.txt', 'w', encoding='utf-8') as fd:
        lines = []
        for word in words:
            word_src = word[0][0]
            word_id = word_src.replace(' ', '_') + '_nnc1'
            word_voice_file = word_voice.get_voice(word_src)
            if word_src in word_filter_dict.keys():
                word_filter_dict[word_src].append(word_filter_dict[word_src][-1] + 1)
            else:
                word_filter_dict[word_src] = [1]
            word_id = word_id + '_' + str(word_filter_dict[word_src][-1])
            if word[1] == 2:
                word_pro = '[]'
                word_exp = word[0][1].rstrip('\n')
                if word_voice_file:
                    lines.append(word_id+'\t'+word_src+'\t'+word_pro+'\t'+word_exp+'\t[sound:'+word_voice_file.name+']\n')
                    shutil.copy(str(word_voice_file), word_voice_dir)
                else:
                    lines.append(word_id+'\t'+word_src+'\t'+word_pro+'\t'+word_exp+'\t[sound:]\n')
            elif word[1] == 3:
                word_pro = word[0][1]
                word_exp = word[0][2].rstrip('\n')
                if word_voice_file:
                    lines.append(word_id+'\t'+word_src+'\t'+word_pro+'\t'+word_exp+'\t[sound:'+word_voice_file.name+']\n')
                    shutil.copy(str(word_voice_file), word_voice_dir)
                else:
                    lines.append(word_id+'\t'+word_src+'\t'+word_pro+'\t'+word_exp+'\t[sound:]\n')
        fd.writelines(lines)

post_proc('NewConceptEnglish1NE.txt')

def get_words(file_name):
    words = set()
    with open(file_name, 'r', encoding='utf-8') as fd:
        lines = fd.readlines();
        for line in lines:
            line_list = re.split(r'\t+', line)
            words.add(line_list[0])
            #print(line_list[0])
    return words

#words = ['coat']

def get_web(word):
    root_addr = 'https://www.macmillandictionary.com/dictionary/british/'
    word_addr = root_addr + word + '_1'
    with request.urlopen(word_addr) as f:
        data = f.read()
        with open(word+'_web.html', 'w', encoding='utf-8') as fd:
            fd.write(data.decode('utf-8'))

#get_web(words[0])

def get_rand_sec(start, end):
    r = random.random()
    d = end - start
    return start + d * r

#print(get_rand_sec(0.5,3.0))

def get_res_dir():
    return os.path.join(os.getcwd(), 'words_pronu')

def parse_web(html):
    soup = BeautifulSoup(html, 'lxml')
    tt = soup.find_all('img')
    for t in tt:
        if t.has_attr('data-src-mp3'):
            mp3_file = t.attrs['data-src-mp3']
            mp3_name = mp3_file.split('/')[-1]
            mp3_full = os.path.join(get_res_dir(), mp3_name)
            request.urlretrieve(mp3_file, mp3_full)
            print(mp3_name)

def parse_web_test(web_file):
    with open(web_file, 'r', encoding='utf-8') as fd:
        html = fd.read()
        parse_web(html)

#parse_web_test('coat_web.html')

def shutdown_computer():
    os.system('shutdown /p /f')

def exist_word_res(word):
    p = Path(get_res_dir())
    words = [x.name.split('_')[0] for x in p.iterdir() if not x.is_dir()]
    return word in words

#print(exist_word_res('what'))

def main():
    words = get_words('NewConceptEnglish1NE_New.txt')
    for word in words:
        if exist_word_res(word):
            print('exist ' + word + '!\n')
            continue
        print('get ' + word + ' :')
        root_addr = 'https://www.macmillandictionary.com/dictionary/british/'
        try:
            word_addr = root_addr + word
            f = urllib.request.urlopen(word_addr, timeout=5)
        except urllib.error.URLError:
            time.sleep(get_rand_sec(0.5, 1))
            word_addr = root_addr + word + '_1'
            f = urllib.request.urlopen(word_addr, timeout=5)
        except:
            time.sleep(get_rand_sec(0.5, 1))
            word_addr = root_addr + word + '_2'
            f = urllib.request.urlopen(word_addr, timeout=5)
        finally:
            time.sleep(get_rand_sec(0.5, 1))
            data = f.read().decode('utf-8')
            parse_web(data)
            print('process ' + word_addr + '\n')
        time.sleep(get_rand_sec(1, 4))
    #shutdown_computer()

#main()
print('Good')