from pydub import AudioSegment

flag = "cuctf{k4zhd4y4_d3vch0nk4_h0ch3t_t4nc3v4t_s_t0b0y_ee37830c02}"

combined_audio = AudioSegment.from_mp3("start.mp3")
for letter in flag:
    for digit in bin(ord(letter))[2:].zfill(8):
        if digit == "0":
            audio = AudioSegment.from_mp3("zero.mp3")
        else:
            audio = AudioSegment.from_mp3("one.mp3")
        combined_audio += audio
    print(letter)
combined_audio += AudioSegment.from_mp3("end.mp3")
combined_audio.export("sigmaboy.mp3", format="mp3")
