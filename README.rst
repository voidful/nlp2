🔨 nlp2 🔧
========

Tools for NLP using Python

This repertory used to handle file io and string cleaning/parsing

Usage
-----

Install:

::

    pip install nlp2

Before using :

::

    from nlp2 import *

Features
========

File Handling
~~~~~~~~~~~~~

get\_folders\_form\_dir(path)
-----------------------------

Arguments - ``path(String)`` : getting all folders under this path
(string) Returns - ``path(String)(generator)`` : path of folders under
arguments path ## get\_files\_from\_dir(path) Arguments -
``path(String)`` : getting all files under this path (string) Returns -
``path(String)(generator)`` : path of files under arguments path ##
read\_dir\_files\_into\_lines(path) Arguments - ``path(String)`` :
getting all files line by lines under this path (string) Returns -
``line(String)(generator)`` : files line under arguments path ##
read\_files\_into\_lines(path) Arguments - ``path(String)`` : getting
content in input file path (string) Returns -
``path(String)(generator)`` : file line under arguments path

String cleaning/parsing
~~~~~~~~~~~~~~~~~~~~~~~

lines\_into\_sentence(lines)
----------------------------

Arguments - ``lines(Array(String))`` : lines array Returns -
``path(String)(generator)`` : split all line base on punctuations ##
split\_sentence\_to\_ngram(text) Arguments - ``path(String)`` : sentence
to ngram

Returns - ``ngrams(Array)`` : ngrams array

Examples

::

    split_sentence_to_ngram("加州旅館")
    return ['加','加州',"加州旅","加州旅館","州","州旅","州旅館","旅","旅館","館"]

split\_sentence\_to\_ngram\_inpart(text)
----------------------------------------

| Arguments - ``path(String)`` : sentence to ngram Returns -
``path(String)(generator)`` : multiple ngrams array in different start
character
| Examples

::

    split_sentence_to_ngram("加州旅館")
    return [['加','加州',"加州旅","加州旅館"],["州","州旅","州旅館"],["旅","旅館"],["館"]]

spilt\_text\_to\_combine\_ways(text)
------------------------------------

Arguments - ``text(String)`` : input text Returns -
``path(String)(generator)`` : all of the text combines ways Examples

::

    spilt_text_to_combine_ways("加州旅館")
    return ['加 州 旅 館', '加 州 旅館', '加 州旅 館', '加 州旅館', '加州 旅館', '加州旅 館', '加州旅館']

spilt\_sentence\_to\_array(sentence)
------------------------------------

Arguments - ``sentence(String)`` : input text Returns -
``sentencearray(Array)`` : sentence array ## is\_all\_english(text)
Arguments - ``text(String)`` : input text Returns - ``result(Boolean)``
: whether the text is all English or not ## is\_contain\_number(text)
Arguments - ``text(String)`` : input text Returns - ``result(Boolean)``
: whether the text contain number or not ## is\_contain\_english(text)
Arguments - ``text(String)`` : input text Returns - ``result(Boolean)``
: whether the text contain english or not ## full2half(text) Arguments -
``string(String)`` : input string which needs turn to half Returns -
``(String)`` : a half-string ## half2full(text) Arguments -
``text(String)`` : input string which needs turn to full Returns -
``(String)`` : a full-string
