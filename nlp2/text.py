import re
import math

punctuations = r"[．﹑︰〈〉─《﹖﹣﹂﹁﹔！？｡。＂＃＄％＆＇（）＊＋，﹐－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.．!\"#$%&()*+,\-.\:;<=>?@\[\]\\\/^_`{|}~]+"
httplink = r"(https|http)[:\/0-9a-zA-Z.?=&;]*"
unused = r":.+:|<br>|\\n|\(\w+\)|\[.+\]"


def clean_all(string):
    return clean_unused_tag(clean_httplink(clean_htmlelement(string)))


def clean_unused_tag(string):
    p = re.compile(unused)
    return p.sub(' ', string.strip()).strip()


def clean_htmlelement(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data.strip()).strip()


def clean_httplink(string):
    p = re.compile(httplink)
    return p.sub(' ', string.strip()).strip()


def split_lines_by_punc(lines, max_len=50):
    sentences = []
    for line in lines:
        line = full2half(line.strip())
        for sentence in filter(None, re.split(punctuations, line)):
            sentence = sentence.strip()
            if len(sentence) > 0 and len(split_sentence_to_array(sentence)) < max_len:
                sentences.append(sentence)
    return sentences


def split_sentence_to_ngram(sentence, max_len=15):
    ngrams = []
    regex = r"[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]"
    path = re.findall(regex, sentence, re.UNICODE)
    for i in range(len(path)):
        for j in range(1, min(len(path) + 1, max_len)):
            if i + j <= len(path):
                ngrams.append(join_words_to_sentence([subPath for subPath in path[i:i + j]]))
    return ngrams


def split_sentence_to_ngram_in_part(sentence, max_len=15):
    ngrams = []
    regex = r"[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]"
    path = re.findall(regex, sentence, re.UNICODE)
    for i in range(len(path)):
        part = []
        for j in range(1, min(len(path) + 1, max_len)):
            if i + j <= len(path):
                part.append(join_words_to_sentence([subPath for subPath in path[i:i + j]]))

        ngrams.append(part)
    return ngrams


def split_text_in_all_comb(sentence):
    result = []
    for i in range(len(sentence)):
        ipart = "".join(sentence[:i + 1])
        irest = sentence[i + 1:]
        if len(irest) > len(ipart):
            for j in split_text_in_all_comb(irest):
                result.append((ipart + " " + j).rstrip())
        else:
            result.append((ipart + " " + join_words_to_sentence(irest)).rstrip())
    return result


def split_sentence_to_array(sentence, merge_non_eng=False):
    if merge_non_eng:
        regex = r"[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]+" + "|" + punctuations
    else:
        regex = r"[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]" + "|" + punctuations
    path = re.findall(regex, sentence, re.UNICODE)
    return path


def join_words_to_sentence(array):
    return ''.join([subPath + (' ' if is_all_english(str(array)) else '') for subPath in array]).strip()


def passage_into_chunk(text, length):
    lines = (i.strip() for i in text.splitlines())
    result = []
    chunk = ''
    for line in lines:
        chunk += (line + " ")
        if len(chunk) > length:
            result.append(chunk)
            chunk = ''
    if len(chunk) > 0:
        result.append(chunk)
    return result


def is_all_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def is_contain_number(s):
    return bool(re.search(r'[0-9]+', s))


def is_contain_english(s):
    return bool(re.search(r'[a-zA-Z]+', s))


def is_list_contain_string(f_str, f_list):
    return any(s in f_str for s in f_list) or any(f_str in s for s in f_list)


def full2half(s):
    n = []
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)


def half2full(s):
    n = []
    for char in s:
        num = ord(char)
        if num == 320:
            num = 0x3000
        elif 0x21 <= num <= 0x7E:
            num += 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)


def sliding_windows_larger_step(a, slide=128):
    for i in range(math.ceil(len(a) / slide) + 1):
        move = int(i * slide / 2)
        if len(a[move:move + slide]) > 0:
            yield a[move:move + slide]


def sliding_windows(a, slide=128):
    for i in range(int(len(a) / slide) + 1):
        if len(a[i * slide:i * slide + slide]) > 0:
            yield a[i * slide:i * slide + slide]


def list_in_windows(list, windows):
    if windows > len(list):
        return [list]
    iter_range = (len(list) - windows + 1)
    jump = int(iter_range / 2)
    return [list[x:x + windows] for x in range(0, iter_range, jump)]
