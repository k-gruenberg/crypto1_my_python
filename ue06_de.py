## Given e and d, we can factor n:
# Dabei gilt: n = p*q
#             d = e^-1 (mod phi(n))  mit phi(n) = (p-1)*(q-1)

n = 89256619835203  # factor(89256619835203): 5454557 * 16363679
# we know e and d
e = 2**16-1
d = 61973647357383  # Probe: Zmod(5454556 * 16363678)(2**16-1)^(-1) == 61973647357383   (ergibt True)
# e*d - 1 = k*phi(n) even  # ist gerade, da phi(n)=(p-1)*(q-1) und sowohl (p-1) als auch (q-1) gerade
# e*d - 1 = 2**h * m 
h = 3
m = 507680372445761863
# Probe: 2^3 * 507680372445761863 == (2**16-1)*61973647357383 - 1   (ergibt True)


# Wir haben nun e*d - 1 als 2^h * m dargestellt (mit h=3 und m groß).
# Bestimme nun einen Faktor (p oder q) wie folgt (vgl. Mail vom 31.08.2022):
#   (1) Rate eine Nachricht a.
#   (2) Rechne x0 = a^m (mod n) sodass a^m (mod n) not in [+1,-1] und a^(2m) (mod n) == 1.
#   (3) Dann ist x0 eine "exotische" (d.h. nicht-triviale) Lösung von 0 == x^2 - 1 == (x-1)*(x+1).
#   (4) Daraus folgt, dass p = ggT(x-1, n) und q = ggT(x+1, n).
#
# Hinweis: Damit a^(2m) (mod n) == 1 gilt, sollte 2*m phi(n) teilen, daher die
#          Voraussetzung, dass e und d und damit k*phi(n) bekannt. (ich denke so passt es)


# guess a
a = 29  # (1) Rate eine Nachricht a.
x0 = power_mod(a, m, n)  # x0 = (a^m) % n  # (2) Rechne x0 = a^m (mod n) sodass a^m (mod n) not in [+1,-1] und a^(2m) (mod n) == 1.
assert(x0 not in [1, -1, n-1])  # (von mir ergänzt)
x1 = x0**2 % n  # x = (x0^2) %n
print(x1 == 1)  # print(...) or assert(...) was missing here!!
print(gcd(x0-1, n))  # ggT(x0-1, n)  # (3) und (4).
