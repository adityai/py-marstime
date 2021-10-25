import time
import math

def a_days_since_j2000_epoch(millis):
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

    # time offset from J2000 epoch (TT)
    DELTA_T_J2000 = JDTT - 2451545.0
    print("A-6 DELTA_T_J2000 = ", DELTA_T_J2000)

    return DELTA_T_J2000

def determine_perturbers(DELTA_T_J2000):
    Ai = [0.0071, 0.0057, 0.0039, 0.0037, 0.0021, 0.0020, 0.0018]
    Ti = [2.2353, 2.7543, 1.1177, 15.7866, 2.1354, 2.4694, 32.8493]
    Qi = [49.409, 168.173, 191.837, 21.736, 15.704, 95.528, 49.095]
    PBS = 0
    for i in range(7):
        PBSi = Ai[i] * math.cos(math.radians((0.985626 * DELTA_T_J2000 / Ti[i]) + Qi[i]))
        PBS = PBS + PBSi
    # TODO: Fix this method
    return PBS

def determine_equation_of_center(DELTA_T_J2000, M, PBS):
    V_minus_M = (10.691 + 3.0 * (10**(-7)) * DELTA_T_J2000) * math.sin(math.radians(M)) + 0.623 * math.sin(math.radians(2 * M)) + 0.050 * math.sin(math.radians(3 * M)) + 0.005 * math.sin(math.radians(4 * M)) + 0.0005 * math.sin(math.radians(5 * M)) + PBS
    return V_minus_M

def b_mars_parameters_of_date(DELTA_T_J2000):
    # Mars mean anomaly
    M = 19.3871 + (0.52402073 * DELTA_T_J2000)
    print("B-1 M = ", M)

    # angle of Fiction Mean Sun
    alfaFMS = 270.3871 + 0.524038496 * DELTA_T_J2000
    print("B-2 αFMS = ", alfaFMS)

    # perturbers
    PBS = determine_perturbers(DELTA_T_J2000)
    print("B-3 PBS = ", PBS)

    # Equation of center
    V_minus_M = determine_equation_of_center(DELTA_T_J2000, M, PBS)
    print("B-4 v - M = ", V_minus_M)

    # areocentric solar longitude
    Ls = alfaFMS + (V_minus_M)
    print("B-5 Ls = ", Ls)

    return Ls

A = a_days_since_j2000_epoch(947116800000)
print("A = ", A)
B = b_mars_parameters_of_date(A)
print("B = ", B)

# Marstime from current earth time: 
# a_days_since_j2000_epoch(time.time_ns() // 1_000_000)


