import serial
import time

buffer = bytes()
msg_in_bytes = bytearray()
s = serial.Serial("COM3", 115200)

while True:
    # print(s.in_waiting)
    if s.in_waiting:
        buffer = s.read()
        if buffer == bytes(b'\x0f'):
            if s.read(3) == bytes(b'\x0f\x0f\x0f'):
                rpm = msg_in_bytes[0:4]
                rpm_int = int.from_bytes(rpm, 'little')
                crc = msg_in_bytes[4:8]
                crc_int = int.from_bytes(crc, 'little')
                eol = msg_in_bytes[8:12]
                print("RPM IN BYTES: ", rpm, "\t\t RPM IN INT: ", rpm_int)
                print("CRC IN BYTES: ", crc, "\t\t CRC IN INT: ", crc_int)
                print("END OF THE MESSAGE")
                msg_in_bytes.clear()
                # time.sleep(1)
        else:
            msg_in_bytes += bytearray(buffer)
