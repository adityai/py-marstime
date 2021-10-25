import time
import math

DEBUG = None

def a_days_since_j2000_epoch(millis):
    if DEBUG:
        print("A-1 millis = ", millis)

    # Julian Date
    JDUT = 2440587.5 + (millis / (8.64 * 10**7))
    if DEBUG:
        print("A-2 JDUT = ", JDUT)

    # Time offset from J2000 epoch
    # This step is optional; we only need to make this calculation if the date is before Jan. 1, 1972. 
    # Determine the elapsed time in Julian centuries since 12:00 on Jan. 1, 2000
    # T = (JDUT - 2451545.0) / 36525 # Optional for dates before Jan 1, 1972
    T = 0
    if DEBUG:
        print("A-3 T = ", T)

    # UTC to TT conversion
    # The formula applied for dates prior to Jan. 1, 1972, is similar to AM2000, eq. 27, 
    # but has been revised and includes additional terms:
    TT_minus_UTC = 64.184 + 59 * T - 51.2 * T**2 - 67.1 * T**3 - 16.4 * T**4
    if DEBUG:
        print("A-4 TT - UTC = ", TT_minus_UTC)

    # Julian Date TT
    JDTT = JDUT + (TT_minus_UTC / 86400)
    if DEBUG:
        print("A-5 JDTT = ", JDTT)

    # time offset from J2000 epoch (TT)
    DELTA_T_J2000 = JDTT - 2451545.0
    if DEBUG:
        print("A-6 DELTA_T_J2000 = ", DELTA_T_J2000)

    return DELTA_T_J2000, JDTT

def determine_perturbers(DELTA_T_J2000):
    Ai = [0.0071, 0.0057, 0.0039, 0.0037, 0.0021, 0.0020, 0.0018]
    Ti = [2.2353, 2.7543, 1.1177, 15.7866, 2.1354, 2.4694, 32.8493]
    Qi = [49.409, 168.173, 191.837, 21.736, 15.704, 95.528, 49.095]
    PBS = 0
    for i in range(7):
        PBSi = Ai[i] * math.cos(math.radians((0.985626 * DELTA_T_J2000 / Ti[i]) + Qi[i]))
        PBS = PBS + PBSi
    return PBS

def b_mars_parameters_of_date(DELTA_T_J2000):
    # Mars mean anomaly
    M = 19.3871 + (0.52402073 * DELTA_T_J2000)
    if DEBUG:
        print("B-1 M = ", M)

    # angle of Fiction Mean Sun
    alfaFMS = 270.3871 + 0.524038496 * DELTA_T_J2000
    if DEBUG:
        print("B-2 αFMS = ", alfaFMS)

    # perturbers
    PBS = determine_perturbers(DELTA_T_J2000)
    if DEBUG:
        print("B-3 PBS = ", PBS)

    # Equation of center
    V_minus_M = (10.691 + 3.0 * (10**(-7)) * DELTA_T_J2000) * math.sin(math.radians(M)) + 0.623 * math.sin(math.radians(2 * M)) + 0.050 * math.sin(math.radians(3 * M)) + 0.005 * math.sin(math.radians(4 * M)) + 0.0005 * math.sin(math.radians(5 * M)) + PBS
    if DEBUG:
        print("B-4 v - M = ", V_minus_M)

    # areocentric solar longitude
    Ls = alfaFMS + (V_minus_M)
    if DEBUG:
        print("B-5 Ls = ", Ls)

    return Ls, V_minus_M

def c_mars_time(Ls, V_minus_M, JDTT, LAMBDA):
    # Equation of Time
    EOT = 2.861 * math.sin(math.radians(2 * Ls)) - 0.071 * math.sin(math.radians(4 * Ls)) + 0.002 * math.sin(math.radians(6 * Ls)) - V_minus_M
    if DEBUG:
        print("C-1 EOT = ", EOT)

    # Mean Solar Time at Mars's prime meridian, i.e., Airy Mean Time
    MST = ( 24 * ( ((JDTT - 2451549.5) / 1.0274912517) + 44796.0 - 0.0009626 ) ) % 24
    if DEBUG:
        print("C-2 MST = ", MST)

    # Local Mean Solar Time
    LMST = ( MST - LAMBDA * (24 / 360) ) % 24 
    # or LMST = ( MST - lambda (1 / 15) ) % 24
    if DEBUG:
        print("C-3 LMST = ", LMST)

    # Local True Solar Time
    LTST = LMST + EOT * (24 / 360) 
    # or LTST = LMST + EOT * (1 / 15)
    if DEBUG:
        print("C-4 LTST = ", LTST)

    # Subsolar longitude
    # Note: The formula published is Λs = MST (360° / 24 h) + EOT + 180° = MST (15° / h) + EOT + 180°, but a (- 180) gave the right answer
    LAMBDAs = (MST * (360 / 24)) + EOT - 180
    if DEBUG:
        print("C-5 Λs = ", LAMBDAs)

    return MST, LMST, LTST, LAMBDAs

def generate_time_string(decimal_time):
    hours = int(decimal_time)
    if DEBUG:
        print("Hours = ", hours)
    minutes = (decimal_time - hours) * 60
    if DEBUG:
        print("Minutes = ", int(minutes))
    seconds = (minutes - int(minutes)) * 60
    if DEBUG:
        print("Seconds = ", int(seconds))
    time_string = str(hours) + ":" + str(int(minutes)) + ":" + str(int(seconds))
    if (hours > 0):
        sign = decimal_time / hours
        if sign < 0:
            time_string = "-" + time_string
    return time_string

def main(millis, LAMBDA):
    DELTA_T_J2000, JDTT = a_days_since_j2000_epoch(millis)
    if DEBUG:
        print("A = ", DELTA_T_J2000)
    Ls, V_minus_M = b_mars_parameters_of_date(DELTA_T_J2000)
    if DEBUG:
        print("B = ", Ls)

    MST, LMST, LTST, LAMBDAs = c_mars_time(Ls, V_minus_M, JDTT, LAMBDA)
    print("Mean Solar Time at Mars's prime meridian (MST) = ", generate_time_string(MST))
    print("Local Mean Solar Time (LMST) = ", generate_time_string(LMST))
    print("Local True Solar Time (LTST) = ", generate_time_string(LTST))

## Marstime from current earth time: 
# main(time.time_ns() // 1_000_000)

## lambda is the Mars latitude. 0 implies that the location is on the Mars prime meridian.
# LAMBDA = 0
## Near Coincident Earth and Mars Times
# main(947116800000, 0)

# MER-A Spirit Landing
LAMBDA_Spirit_Landing = 184.702
main(1073137591000, LAMBDA_Spirit_Landing)
