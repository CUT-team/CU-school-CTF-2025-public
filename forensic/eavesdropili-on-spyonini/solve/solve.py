from scapy.all import *
import struct
import os

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

def extract_amr(pcap_file, target_ssrc):
    packets = rdpcap(pcap_file)
    amr_frames = []
    
    for pkt in packets:
        if UDP in pkt and Raw in pkt:
            payload = bytes(pkt[Raw].load)
            
            if len(payload) >= 12 and (payload[0] & 0xC0) == 0x80:  # RTP header
                
                pkt_ssrc = struct.unpack('!I', payload[8:12])[0]
                if pkt_ssrc != target_ssrc:
                    continue
                
                if len(payload) >= 13:
                    # AMR payload header (1 byte)
                    amr_payload_header = payload[12]
                    frame_type = amr_payload_header & 0x0F
                    
                    
                    if  len(payload) >= 13:
                        amr_frame =  payload[12:]
                        amr_frames.append(amr_frame)
    
    return amr_frames


target_ssrc_1 = 0x13376060
target_ssrc_2 = 0x9017b177

victim_frames_1 = extract_amr('sniffed.pcap', target_ssrc=target_ssrc_1)
victim_frames_2 = extract_amr('sniffed.pcap', target_ssrc=target_ssrc_2)

orig_frames = read_amr_file('file-wav/victim-call-2.amr')


print(f"Captured frames (call 1): {len(victim_frames_1)}")
print(f"Captured frames (call 2): {len(orig_frames)}")
print(f"Captured frames (orig call 2): {len(victim_frames_2)}")

res_frames = []

for i in range(min(len(orig_frames), len(victim_frames_1), len(victim_frames_2))):
    tmp = b''
    for j in range(min(len(orig_frames[i]), len(victim_frames_1[i]), len(victim_frames_2[i]))):
        byte = orig_frames[i][j] ^ victim_frames_1[i][j] ^ victim_frames_2[i][j]
        tmp += bytes([byte])
    
    res_frames.append(tmp)

# making the file
with open('call.amr', 'wb') as f:
    f.write(b'#!AMR\n') # AMR header
    for frame in res_frames:
        
        f.write(frame)

try:
    os.system('ffmpeg -i call.amr call.wav')
except Exception as e:
    print(e)
    
# huray