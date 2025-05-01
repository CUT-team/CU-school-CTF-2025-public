# eavesdropili-on-spyonini | hard | forensics

## Хинт 
Первый и главный шаг рещения - понять, что наш агент начал атаку ReVoLTE, именно поэтому после перехвата трафика он позвонил Шпионини Голубини.
Хинты также были в самом трафике: можно было увидеть http запросы на сайты про ReVoLTE или поск в гугле этой атаки.
Дальше дело за меньшим (большим) - закончить атаку.

## Коротко по теории:

eNodeB отрправляет K_ASME ключ на телефон, из него вычиляется K_eNB, который сплитится на три части, одной из которых будет K_UPenc - это число выступает ключом для шифрования пакетом (в SNOW 3G например). 

[SIM (K)]
  -> [CK, IK] from AKA
  -> [K_eNB] = KDF(K_ASME, eNB ID)
     K_eNB is splitted into:
    - K_RRCenc — RRC signaling encryption (low-level communication)
    - K_RRCint — RRC integrity protection (anti-spoofing and anti-replay) 
    - K_UPenc - usertraffic encryption (e.g., voice, data)

SNOW3G.init(key=K_UPenc, IV=IV)
IV = COUNT || BEARER || DIRECTION || 26 zero bits

## Так проходит подключения

1. [eNodeB <-> UE]: Establish Radio Bearer (using same key K)
    - Radio connection secured using K_UPenc (derived from K_eNB)
2. [UE -> SIP Proxy]: SIP INVITE
    - Start call setup over SIP (encrypted transport if available)
3. [SIP Proxy -> UE]: SIP 200 OK
    - Remote party accepts the call
4. [UE -> SIP Proxy]: SIP ACK
    - Confirm call establishmeny
5. [UE <-> UE]: RTP Voice Stream 1 (SNOW 3G encrypted)
    - Voice traffic flows using SNOW 3G encryption (keystream based on K_UPenc)
6. [Call Ended]
    - Normal behavior: New K should be negotiated
    - Vulnerable behavior: Key reuse (bug)
7. [eNodeB <-> UE]: (BUG) Reuse old Radio Bearer Key (K)
    - Radio Bearer *reuses* the old K_eNB → K_UPenc
8. [UE -> SIP Proxy]: SIP INVITE (second call)
    - New SIP call starts
9. [SIP Proxy -> UE]: SIP 200 OK
    - Call accepted
10. [UE -> SIP Proxy]: SIP ACK
    - Call confirmed
11. [UE <-> UE]: RTP Voice Stream 2 (SNOW 3G  encrypted)
    - Second voice session, but encrypted with the **same** keystream

## Вулна

Уязвимость ReVoLTE возникает на последнем этапе подключения - при создании нового соединения должен производиться повторный обмен ключами, но некоторые операторы игнорируют это правило при небольшой разнице во времени между звонками.

И отсюда идея:  
SNOW3G.init(key=K_UPenc, IV=IV)
IV = COUNT || BEARER || DIRECTION || 26 zero bits

Count сбивается в ноль при новом соединении, bearer остается таким же, как и direction.
И как мы выяснили, K_UPenc остается неизменным.

SNOW 3G - потоковый шифр -> мы уже можем сделать вывод о том, в каких пакетах потоки совпадают.

Пусть у нас есть два зашифрованных пакета с совпадаюшими keystream, и мы знаем информация второго пакета.
E(A) = A xor keystream
E(B) = B xor keystream

## A = E(A) xor E(B) xor B
Таким методом мы и будем декриптить информацию.

## Теперь к декрипту
В реальной версии общения пакеты бы выглядели вот так.
Ether - IP - UDP - GTP-U - PDCP -> encrpted[ROHC - RTP - AMR-WB]

Чтобы таск был решаемым, пакеты были усечены ETHER - IP - UDP  RTP - AMR-WB  и шифровался толко payload. 

Нам нужно найти SSRС стримов шпионини, по времени (да по условию задания) очевидно, что было два звонка, можем просто найти сопадающий IP - это и будут те потоки сообщений, которые нам нужно будет спарситься. (А еще у Гоолубини MAC адрес APPLE - так что хакаем мажоров выходит)

Все что было дальше можно найти в [solve.py]

shpionini-answer.amr - это записанный второй звонок (сторона Шпионини)
Нужно было правильно разбить .amr файл на фреймы.

Достать соответсвующие фреймы из pcap, это SSRC = 0x9017b177 и SSRC = 0x13376060 (ставьте лайк если нашли aboba внути pcap)

Осталось только проксорить и упаковать результат в amr file. Перевести в wav и послушать!