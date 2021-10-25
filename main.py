import time

def go(millis):
    print("A-1 millis = ", millis)

    # Julian Date
    JDUT = 2440587.5 + (millis / (8.64 * 10**7))
    print("A-2 JDUT = ", JDUT)

    # Time offset from J2000 epoch
    # This step is optional; we only need to make this calculation if the date is before Jan. 1, 1972. 
    # Determine the elapsed time in Julian centuries since 12:00 on Jan. 1, 2000
    # T = (JDUT - 2451545.0) / 36525 # Optional for dates before Jan 1, 1972
    T = 0
    print("A-3 T = ", T)

    # UTC to TT conversion
    # The formula applied for dates prior to Jan. 1, 1972, is similar to AM2000, eq. 27, 
    # but has been revised and includes additional terms:
    TT_minus_UTC = 64.184 + 59 * T - 51.2 * T**2 - 67.1 * T**3 - 16.4 * T**4
    print("A-4 TT - UTC = ", TT_minus_UTC)

    # Julian Date TT
    JDTT = JDUT + (TT_minus_UTC / 86400)
    print("A-5 JDTT = ", JDTT)

# Marstime from current earth time: 
# go(time.time_ns() // 1_000_000)

go(947116800000)
