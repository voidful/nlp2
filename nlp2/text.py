import re

punctuations = r"[．﹑︰〈〉 ─《﹖﹣﹂﹁﹔！？｡。＂＃＄％＆＇（）＊＋，﹐－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.．!\"#$%&()*+,\-.\:;<=>?@\[\]\\\/^_`{|}~]+"


def lines_into_sentence(lines):
    sentences = []
    for line in lines:
        line = full2half(line.strip())
        for sentence in filter(None, re.split(punctuations, line)):
            sentence = sentence.strip()
            if len(sentence) > 0:
                sentences.append(sentence)
    return sentences


def split_sentence_to_ngram(sentence):
    ngrams = []
    regex = r"[\u4e00-\ufaff]|[0-9]+|[a-zA-Z]+\'*[a-z]*"
    path = re.findall(regex, sentence, re.UNICODE)
    for i in range(len(path)):
        for j in range(1, len(path) + 1):
            if i + j <= len(path):
                ngrams.append(join_array_to_sentence([subPath for subPath in path[i:i + j]]))
    return ngrams


def split_sentence_to_ngram_inpart(sentence):
    ngrams = []
    regex = r"[\u4e00-\ufaff]|[0-9]+|[a-zA-Z]+\'*[a-z]*"
    path = re.findall(regex, sentence, re.UNICODE)
    for i in range(len(path)):
        part = []
        for j in range(1, len(path) + 1):
            if i + j <= len(path):
                part.append(join_array_to_sentence([subPath for subPath in path[i:i + j]]))

        ngrams.append(part)
    return ngrams


def spilt_text_to_combine_ways(sentence):
    result = []
    for i in range(len(sentence)):
        ipart = "".join(sentence[:i + 1])
        irest = sentence[i + 1:]
        if len(irest) > len(ipart):
            for j in spilt_text_to_combine_ways(irest):
                result.append((ipart + " " + j).rstrip())
        else:
            result.append((ipart + " " + join_array_to_sentence(irest)).rstrip())
    return result


def spilt_sentence_to_array(sentence):
    regex = r"[\u4e00-\ufaff]|[0-9]+|[a-zA-Z]+\'*[a-z]*"
    path = re.findall(regex, sentence, re.UNICODE)
    return path


def join_array_to_sentence(array):
    return ''.join([subPath + (' ' if is_all_english(str(subPath)) else '') for subPath in array]).strip()


def is_all_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def is_contain_number(s):
    return bool(re.search(r'[0-9]+', s))


def is_contain_englis(s):
    return bool(re.search(r'[a-zA-Z]+', s))


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
        num = char(char)
        if num == 320:
            num = 0x3000
        elif 0x21 <= num <= 0x7E:
            num += 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)
