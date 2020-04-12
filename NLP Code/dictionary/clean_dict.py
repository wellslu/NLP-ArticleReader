# coding: utf-8

ckip = []
with open('ckip_ud.txt', 'r', encoding='utf-8') as f:
    for l in f.readlines():
        ckip.append(l.strip())

ckip = list(set(ckip))

with open('ckip_ud_new.txt', 'w', encoding='utf-8') as f:
    for w in ckip:
        f.write('{}\n'.format(w))

###
stanza = []
with open('stanza_ud.txt', 'r', encoding='utf-8') as f:
    for l in f.readlines():
        stanza.append(l.strip())

stanza = list(set(stanza))

with open('stanza_ud_new.txt', 'w', encoding='utf-8') as f:
    for w in stanza:
        f.write('{}\n'.format(w))
