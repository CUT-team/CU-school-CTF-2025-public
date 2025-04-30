import random
import hashlib
import time
from builder import *
from scapy.all import Ether, IP, UDP, Raw, rdpcap, PcapWriter
from snow3G import SNOW
import copy


def random_uint32():
    return random.getrandbits(32)

def read_amr_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Header(6 байт для AMR-NB)
    if data.startswith(b'#!AMR\n') or data.startswith(b'#!AMR-WB\n'):
        data = data[6:]

    frames = []
    pos = 0
    while pos < len(data):
        frame_header = data[pos]
        frame_type = (frame_header >> 3) & 0x0F
        
        frame_sizes_nb = [12, 13, 15, 17, 19, 20, 26, 31, 5, 0, 0, 0, 0, 0, 0, 0]
        frame_size = frame_sizes_nb[frame_type] if frame_type < len(frame_sizes_nb) else 0
        
        if frame_size == 0 or pos + 1 + frame_size > len(data):
            break
            
        frames.append(data[pos:pos+1+frame_size])
        pos += 1 + frame_size
    
    return frames

devices = {
    "ue1": {
        "mac": "dc:a9:04:12:34:56", # iPhone
        "ip": "10.100.1.14", # UE1 (caller in call 1, callee in call 2)
        "sip_port": 5060,
        "rtp_port": 40000
    },
    "ue2": {
        "mac": "78:44:76:65:43:21", # Samsung
        "ip": "10.100.1.27", # UE2 (callee in call 1)
        "sip_port": 5060,
        "rtp_port": 40002
    },
    "ue3": {
        "mac": "00:16:3e:6b:5f:1a", # Generic Android
        "ip": "10.100.1.33", # UE3 (caller in call 2)
        "sip_port": 5060,
        "rtp_port": 40004
    },
    "p_cscf": {
        "mac": "00:50:56:aa:bb:cc", # virtualized P-CSCF VMware
        "ip": "10.100.1.2",
        "sip_port": 5060,
        "rtp_port": 40006,
        "domain": "ims.mnc001.mcc250.3gppnetwork.org"
    }
}

# VoLTE Call Configurations
call_1_config = {
    "ssrc": {
        "caller": 0x13376060, # UE1 SSRC for first call
        "callee": 0xab0bacc0 # UE2 SSRC for first call
    },
    "codec": {
        "type": "AMR-NB",
        "payload_type": 96,
        "clock_rate": 8000
    },
    "call_id": f"{random.randint(1, 10**6)}@ims.mnc001.mcc250.3gppnetwork.org",
    "cseq": 1,
    "branch": hashlib.sha1(f"call1-{time.time()}".encode()).hexdigest()[:8]
}

call_2_config = {
    "ssrc": {
        "caller": 0x411ac5e7, # UE3 SSRC for second call
        "callee": 0x9017b177 # UE1 SSRC for second call (UE1 now callee)
    },
    "codec": {
        "type": "AMR-NB",
        "payload_type": 96,
        "clock_rate": 8000
    },
    "call_id": f"{random.randint(1, 10**6)}@ims.mnc001.mcc250.3gppnetwork.org",
    "cseq": 1,
    "branch": hashlib.sha1(f"call2-{time.time()}".encode()).hexdigest()[:8]
}

        
salt_pkts = rdpcap('salt.pcap')[3:]

base_time = salt_pkts[0].time

start_offset = 1.0
rtp_time = base_time + start_offset

spy_frames = read_amr_file('file-wav/victim-call-1.amr')
basa_frames = read_amr_file('file-wav/abonent.amr')

writer = PcapWriter('test.pcap', append=False, sync=True)

# Buildim RTP stream
seq_callee = 1
seq_caller = 1

key = [731536269, 2380087669]

key_others = [1234567, 987654323]

timestamp = 0

sip_invite_pkt = construct_invite_packet(devices={"ue": devices["ue1"], "p_cscf": devices["p_cscf"]}, call_config=call_1_config)
sip_ok_pkt = construct_ok_packet(devices={"ue": devices["ue1"], "p_cscf": devices["p_cscf"]}, call_config=call_1_config)
sip_ack_pkt = construct_ack_packet(devices={"ue": devices["ue1"], "p_cscf": devices["p_cscf"]}, call_config=call_1_config)

call_pkts = [sip_invite_pkt, sip_ok_pkt, sip_ack_pkt]

for pkt in call_pkts:
    pkt.time = rtp_time + random.uniform(-0.0002, 0.0002)
    rtp_time += 0.005
base_interval = 0.02

for i in range(max(len(spy_frames), len(basa_frames))):
    if i < len(spy_frames):
        key_tmp = key + [i+1]
    
        cipher = SNOW(key_tmp)
        
        ciphered_frame = bytearray(spy_frames[i])
        cipher.Encrypt(ciphered_frame)
        
        
        call_pkts.append(make_rtp_pkt(src_ip=devices["ue1"]["ip"], dst_ip=devices["ue2"]["ip"], 
                                      src_port=devices["ue1"]["rtp_port"], dst_port=devices["ue2"]["rtp_port"],
                                      payload=ciphered_frame, seq=seq_caller, timestamp=timestamp, 
                                      ssrc=call_1_config["ssrc"]["caller"], pkt_time=rtp_time))
        seq_caller += 1
        timestamp += 160
        rtp_time += base_interval + random.uniform(-0.005, 0.005)
    
    if i < len(basa_frames):
        key_tmps = key_others + [i+1]
        
        cipher = SNOW(key_tmp)
        ciphered_frame = bytearray(basa_frames[i])
        
        cipher.Encrypt(ciphered_frame)
        
        call_pkts.append(make_rtp_pkt(src_ip=devices["ue2"]["ip"], dst_ip=devices["ue1"]["ip"], 
                                        src_port=devices["ue2"]["rtp_port"], dst_port=devices["ue1"]["rtp_port"],
                                        payload=ciphered_frame, seq=seq_callee, timestamp=timestamp, 
                                        ssrc=call_1_config["ssrc"]["callee"], pkt_time=rtp_time))
 
        seq_callee += 1
        timestamp += 160
        rtp_time += base_interval + random.uniform(-0.005, 0.005)

cseq = 1

mixed = []

for i in range(len(salt_pkts)):
    if IP in salt_pkts[i]:
        if salt_pkts[i][IP].src == "10.245.74.92":
            salt_pkts[i][IP].src = "10.100.1.52"
        if salt_pkts[i][IP].dst == "10.245.74.92":
            salt_pkts[i][IP].dst = "10.100.1.52"


start, end = 11, 178
for i in range(start, end + 1):
    pkt = salt_pkts[i].copy()
    if hasattr(pkt, 'time'):
        pkt.time += 16
    salt_pkts.append(pkt)

curr_len = len(salt_pkts)
for i in range(curr_len):
    pkt = salt_pkts[i].copy()
    if hasattr(pkt, 'time'):
        pkt.time += 34
    salt_pkts.append(pkt)


first_salt_chunk = 49
i = 0
salt_curr = first_salt_chunk

mixed.extend(salt_pkts)


while i < len(call_pkts):
    mixed.append(call_pkts[i])
    i += 1
    prob = random.randint(0, 11)
    if prob <= 9:
        salt_size = random.randint(1, 10)
        for j in range(salt_size):
            if salt_curr < len(salt_pkts):
                mixed.append(salt_pkts[salt_curr])
                salt_curr += 1
    
sip_bye_pkt = construct_bye_packet(devices={"ue": devices["ue1"], "p_cscf": devices["p_cscf"]}, call_config=call_1_config)

sip_bye_pkt.time = rtp_time + 0.1
mixed.append(sip_bye_pkt)

# SIP 200 OK на BYE
cseq += 1


sip_ok_bye_pkt = construct_bye_ok_packet(devices={"ue": devices["ue1"], "p_cscf": devices["p_cscf"]}, call_config=call_1_config)

sip_ok_bye_pkt.time = rtp_time + 0.15
mixed.append(sip_ok_bye_pkt)

# Пауза перед атакующим вызовом
rtp_time += 4.3

# Атакующий вызов (используем тот же SSRC, что и в основном вызове)

sip_attack_invite_pkt = construct_invite_packet(devices={"ue": devices["ue3"], "p_cscf": devices["p_cscf"]}, call_config=call_2_config)
sip_attack_invite_pkt.time = rtp_time
mixed.append(sip_attack_invite_pkt)
rtp_time += 0.109120

# SIP 200 OK на атакующий вызов
sip_attack_ok_pkt = construct_ok_packet(devices={"ue": devices["ue3"], "p_cscf": devices["p_cscf"]}, call_config=call_2_config)
sip_attack_ok_pkt.time = rtp_time
mixed.append(sip_attack_ok_pkt)
rtp_time += 0.1

# SIP ACK от хакеруна
sip_attack_ack_pkt = construct_ack_packet(devices={"ue": devices["ue3"], "p_cscf": devices["p_cscf"]}, call_config=call_2_config)
sip_attack_ack_pkt.time = rtp_time
mixed.append(sip_attack_ack_pkt)
rtp_time += 0.1

# атакующий вызов
attack_frames = read_amr_file('file-wav/attacker-call.amr')
victim_frames = read_amr_file('file-wav/victim-call-2.amr')

caller_seq = 1
callee_seq = 1
attack_timestamp = 0 
key_attack = [63274536, 87623465]

for j in range(max(len(attack_frames), len(victim_frames))):
    if j < len(attack_frames):
        key_tmp = key_attack + [j+1]
        cipher = SNOW(key_tmp)
        ciphered_frame = bytearray(attack_frames[j])
        cipher.Encrypt(ciphered_frame)
        
        mixed.append(make_rtp_pkt(src_ip=devices["ue3"]["ip"], dst_ip=devices["ue1"]["ip"], 
                                    src_port=devices["ue3"]["rtp_port"], dst_port=devices["ue1"]["rtp_port"],
                                    payload=ciphered_frame, seq=caller_seq, timestamp=timestamp, 
                                    ssrc=call_2_config["ssrc"]["caller"], pkt_time=rtp_time))
        attack_timestamp += 160
        caller_seq += 1
        rtp_time += base_interval + random.uniform(-0.005, 0.005)
    if j < len(victim_frames):
        key_tmp = key + [j+1]
        cipher = SNOW(key_tmp)
        ciphered_frame = bytearray(victim_frames[j])
        
        cipher.Encrypt(ciphered_frame)
        
        mixed.append(make_rtp_pkt(src_ip=devices["ue1"]["ip"], dst_ip=devices["ue3"]["ip"], 
                                    src_port=devices["ue1"]["rtp_port"], dst_port=devices["ue3"]["rtp_port"],
                                    payload=ciphered_frame, seq=callee_seq, timestamp=timestamp, 
                                    ssrc=call_2_config["ssrc"]["callee"], pkt_time=rtp_time))
        attack_timestamp += 160
        callee_seq += 1
        rtp_time += base_interval + random.uniform(-0.005, 0.005)

# Завершение атакующего вызова
sip_attack_bye_pkt = construct_bye_packet(devices={"ue": devices["ue3"], "p_cscf": devices["p_cscf"]}, call_config=call_2_config)
sip_attack_bye_pkt.time = rtp_time + 0.1
mixed.append(sip_attack_bye_pkt)

# SIP 200 OK на BYE от хакера
sip_attack_bye_pkt = construct_bye_packet(devices={"ue": devices["ue3"], "p_cscf": devices["p_cscf"]}, call_config=call_2_config)
sip_attack_bye_pkt.time = rtp_time + 0.15
mixed.append(sip_attack_bye_pkt)

# Добавляем оставшиеся salt-пакеты
while salt_curr < len(salt_pkts):
    mixed.append(salt_pkts[salt_curr])
    salt_curr += 1

mixed.sort(key=lambda pkt: pkt.time)

for pkt in mixed:
    writer.write(pkt)

writer.close()
print("PCAP generated: test.pcap")

