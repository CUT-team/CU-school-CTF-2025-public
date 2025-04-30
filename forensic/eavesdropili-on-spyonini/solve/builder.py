import random
import struct
from scapy.all import Ether, UDP, IP, Raw

def construct_invite_packet(devices, call_config):
    # SIP INVITE with AMR-WB (VoLTE standard)
    sip_invite = (
        f"INVITE sip:+79123456789@{devices['p_cscf']['ip']} SIP/2.0\r\n"
        f"Via: SIP/2.0/UDP {devices['ue']['ip']}:{devices['ue']['sip_port']};branch=z9hG4bK{call_config['branch']}\r\n"
        f"Route: <sip:pcscf.ims.mnc001.mcc250.3gppnetwork.org;lr>\r\n"
        f"Max-Forwards: 70\r\n"
        f"From: <sip:+79123456789@{devices['p_cscf']['ip']}>;tag=543212\r\n"
        f"To: <sip:+79120000000@{devices['p_cscf']['ip']}>\r\n"
        f"Call-ID: {call_config['call_id']}\r\n"
        f"CSeq: {call_config['cseq']} INVITE\r\n"
        f"Contact: <sip:{devices['ue']['ip']}:{devices['ue']['sip_port']};transport=udp>\r\n"
        f"Content-Type: application/sdp\r\n"
        f"Content-Length: 200\r\n\r\n"
        f"v=0\r\n"
        f"o=- {random.randint(1,10**9)} {random.randint(1,10**9)} IN IP4 {devices['ue']['ip']}\r\n"
        f"s=-\r\n"
        f"c=IN IP4 {devices['ue']['ip']}\r\n"
        f"t=0 0\r\n"
        f"m=audio {devices['ue']['rtp_port']} RTP/AVP {call_config['codec']['payload_type']}\r\n"
        f"a=rtpmap:{call_config['codec']['payload_type']} {call_config['codec']['type']}/{call_config['codec']['clock_rate']}\r\n"
        f"a=fmtp:{call_config['codec']['payload_type']} mode-change-capability=2;max-red=220\r\n"
        f"a=sendrecv\r\n"
    )
    return Ether(src=devices["ue"]["mac"], dst=devices["p_cscf"]["mac"])/IP(src=devices['ue']['ip'], dst=devices['p_cscf']['ip'])/UDP(sport=devices['ue']['sip_port'], dport=devices['p_cscf']['sip_port'])/Raw(load=sip_invite)

def construct_ok_packet(devices, call_config):
    # SIP 200 OK response
    sip_ok = (
        f"SIP/2.0 200 OK\r\n"
        f"Via: SIP/2.0/UDP {devices['ue']['ip']}:{devices['ue']['sip_port']};branch=z9hG4bK{call_config['branch']}\r\n"
        f"Record-Route: <sip:pcscf.ims.mnc001.mcc250.3gppnetwork.org;lr>\r\n"
        f"From: <sip:+79123456789@ims.mnc001.mcc250.3gppnetwork.org>;tag=54321\r\n"
        f"To: <sip:+79120000000@ims.mnc001.mcc250.3gppnetwork.org>;tag=67890\r\n"
        f"Call-ID: {call_config['call_id']}\r\n"
        f"CSeq: {call_config['cseq'] + 1} INVITE\r\n"
        f"Contact: <sip:+79120000000@ims.mnc001.mcc250.3gppnetwork.org>\r\n"
        f"Content-Type: application/sdp\r\n"
        f"Content-Length: 200\r\n\r\n"
        f"v=0\r\n"
        f"o=- 123456789 987654321 IN IP4 {devices['p_cscf']['ip']}\r\n"
        f"s=-\r\n"
        f"c=IN IP4 {devices['p_cscf']['ip']}\r\n"
        f"t=0 0\r\n"
        f"m=audio {devices['p_cscf']['rtp_port']} RTP/AVP {call_config['codec']['payload_type']}\r\n"
        f"a=rtpmap:{call_config['codec']['payload_type']} {call_config['codec']['type']}/{call_config['codec']['clock_rate']}\r\n"
        f"a=fmtp:{call_config['codec']['payload_type']} mode-set=0,1,2;mode-change-period=2\r\n"
        f"a=sendrecv\r\n"
    )
    return Ether(src=devices["p_cscf"]["mac"], dst=devices["ue"]["mac"])/IP(src=devices['p_cscf']['ip'], dst=devices['ue']['ip'])/UDP(sport=devices['p_cscf']['sip_port'], dport=devices['ue']['sip_port'])/Raw(load=sip_ok)

def construct_ack_packet(devices, call_config):
    # SIP ACK
    sip_ack = (
        f"ACK sip:+79120000000@{devices['p_cscf']['domain']} SIP/2.0\r\n"
        f"Via: SIP/2.0/UDP {devices['ue']['ip']}:{devices['ue']['sip_port']};branch=z9hG4bK{call_config['branch']}\r\n"
        f"Route: <sip:pcscf.{devices['p_cscf']['domain']};lr>\r\n"
        f"From: <sip:+79123456789@{devices['p_cscf']['domain']}>;tag=54321\r\n"
        f"To: <sip:+79120000000@{devices['p_cscf']['domain']}>;tag=67890\r\n"
        f"Call-ID: {call_config['call_id']}\r\n"
        f"CSeq: {call_config['cseq'] + 2} ACK\r\n"
        f"Content-Length: 0\r\n\r\n"
    )
    return Ether(src=devices['ue']['mac'], dst=devices['p_cscf']['mac'])/IP(src=devices['ue']['ip'], dst=devices['p_cscf']['ip'])/UDP(sport=devices['ue']['sip_port'], dport=devices['p_cscf']['sip_port'])/Raw(load=sip_ack)

def construct_bye_packet(devices, call_config):
    # SIP BYE
    sip_bye = (
        f"BYE sip:+79120000000@{devices['p_cscf']['domain']} SIP/2.0\r\n"
        f"Via: SIP/2.0/UDP {devices['ue']['ip']}:{devices['ue']['sip_port']};branch=z9hG4bK{call_config['branch']}\r\n"
        f"From: <sip:+79123456789@{devices['p_cscf']['domain']}>;tag=54321\r\n"
        f"To: <sip:+79120000000@{devices['p_cscf']['domain']}>;tag=67890\r\n"
        f"Call-ID: {call_config['call_id']}\r\n"
        f"CSeq: {call_config['cseq'] + 3} BYE\r\n"
        f"Content-Length: 0\r\n\r\n"
    )
    return Ether(src=devices['ue']['mac'], dst=devices['p_cscf']['mac'])/IP(src=devices['ue']['ip'], dst=devices['p_cscf']['ip'])/UDP(sport=devices['ue']['sip_port'], dport=devices['p_cscf']['sip_port'])/Raw(load=sip_bye)

def construct_bye_ok_packet(devices, call_config):
    # SIP 200 OK (BYE reponse)
    sip_ok = (
        f"SIP/2.0 200 OK\r\n"
        f"Via: SIP/2.0/UDP {devices['ue']['ip']}:{devices['ue']['sip_port']};branch=z9hG4bK{call_config['branch']}\r\n"
        f"From: <sip:+79123456789@{devices['p_cscf']['domain']}>;tag=54321\r\n"
        f"To: <sip:+79120000000@{devices['p_cscf']['domain']}>;tag=67890\r\n"
        f"Call-ID: {call_config['call_id']}\r\n"
        f"CSeq: {call_config['cseq'] + 4} BYE\r\n"
        f"Content-Length: 0\r\n\r\n"
    )
    return Ether(src=devices['p_cscf']['mac'], dst=devices['ue']['mac'])/IP(src=devices['p_cscf']['ip'], dst=devices['ue']['ip'])/UDP(sport=devices['p_cscf']['sip_port'], dport=devices['ue']['sip_port'])/Raw(load=sip_ok)

def rtp_packet(payload, seq, timestamp, ssrc):
    version = 2 << 6
    pt = 96 & 0x7F
    header = struct.pack("!BBHII", version, pt, seq, timestamp, ssrc)
    return header + payload

def make_rtp_pkt(src_ip, dst_ip, src_port, dst_port, payload, seq, timestamp, ssrc, pkt_time):
    pkt = rtp_packet(payload, seq, timestamp, ssrc)
    ether = Ether()/IP(src=src_ip, dst=dst_ip)/UDP(sport=src_port, dport=dst_port)/Raw(load=pkt)
    ether.time = pkt_time
    return ether
