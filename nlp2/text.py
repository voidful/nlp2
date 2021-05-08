import re

punctuations = r"[¥•＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·'℃°•·．﹑︰〈〉─《﹖﹣﹂﹁﹔！？｡。＂＃＄％＆＇（）＊＋，﹐－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.．!\"#$%&()*+,\-.\:;<=>?@\[\]\\\/^_`{|}~]"
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
    sentence = "".join(
        (char if char.isalpha() or char == " " else " " + char + " ") for char in sentence)  # separate punctuation
    if merge_non_eng:
        regex = r"[0-9]|[a-zA-Z]+\'*[a-z]*|[\w]+|[^ ]"
    else:
        regex = r"[0-9]|[a-zA-Z]+\'*[a-z]*|[\w]|[^ ]"
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


def sliding_windows(seq, slide=128, append_seq=[]):
    windows_list = []
    slide_pos = []
    seq_length = len(seq)
    windows_min_size = min(slide, seq_length)
    for i in range(int(seq_length / slide) + 1):
        for end in [min(i * slide + slide, seq_length),
                    min(i * slide + slide - int(slide / 2), seq_length)]:
            start = max(0, end - slide)
            slide_seq = seq[start:end] + append_seq
            if len(
                    slide_seq) >= windows_min_size and slide_seq not in windows_list:  # avoid adding same list repeatedly
                windows_list.append(slide_seq)
                slide_pos.append([start, end])
    return windows_list, slide_pos
