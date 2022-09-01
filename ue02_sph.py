p = 5839037  # p prim
Z = IntegerModRing(p) # Ring Z_p
g = Z.multiplicative_generator()  # g generiert multiplikative (zyklische) Gruppe der Ordnung p-1: ord(<g>) = p-1 (mit p=5839037)
print(f'g={g}')
h = g**2769541  # ein öffentlicher Diffie-Hellman-"Schlüssel"; wir wollen x=2769541 suchen/"knacken", gegeben öff. g und h=g**x (DLP)
pm1 = factor(p-1)
# => faktorisiere die Gruppenordung ord(G) = ord(<g>) = ord({1=g^0=g^(p-1), ..., g^(p-2)}) = p-1 => denn hier setzt SPH an!!
#    => 1=g^(p-1) gilt, da Element hoch Gruppenordnung immer =1 ist!
# 2^2 * 7^2 * 31^3

# Die naive Brute-Force-Implementierung des diskreten Logarithmus:
# We define the 'simple' dlog
def dlog(gg, hh, s):
    for i in range(1,s):
        if gg**i == hh:
            return i
    return 0   

# Silver-Pohlig-Hellman reduziert das DLP in einer Gruppe der Ordnung p[1]^e[1] * p[2]^e[2] * ...
# [1] zunächst auf das DLP in den Gruppen der Ordnung p[1]^e[1], p[2]^e[2], ...
# [2] und dann auf das DLP in den Gruppen der Ordnung p[1], p[2], ...
# Also hier
# [1] zunächst auf das DLP in den Gruppen der Ordnung 2^2, 7^2 und 31^3
# [2] und dann auf das DLP in den Gruppen der Ordnung 2, 7 und 31

# Schritt/Part [1] (1. Teil): Finde x_a, x_b und (hier) x_c:

## determine DL in 2^2
## solve g2**x2 = h2
g2=g**(7**2 * 31**3)
h2=h**(7**2 * 31**3)
x2 = dlog(g2,h2,4)  # (auf Cheat Sheet x_a mit (g^b)^x_a = h^b in Gruppe der Ordnung a = 2^2)

## determine DL in 7^2
## solve g7**x7 = h7
g7=g**(2**2 * 31**3)
h7=h**(2**2 * 31**3)
x7 = dlog(g7,h7,7**2)  # (auf Cheat Sheet x_b mit (g^a)^x_b = h^a in Gruppe der Ordnung b = 7^2)


## determine DL in 31^3
## solve g31**x31 = h31
g31=g**(2**2 * 7**2)
h31=h**(2**2 * 7**2)
x31 = dlog(g31,h31,31**3)

print(f'x2={x2}, x7={x7}, x31={x31}')

# Schritt/Part [1] (2. Teil): Finde mit Euklid (hier anderweitig bestimmt... ("uninteressant")) u, v und (hier) w, sodass
#   u*b*c + v*a*c + w*a*b == 1
#   Dies it die verallgemeinerte Form von u*a + v*b == 1 im Falle von nur 2 Faktoren a und b: ord(G) = a*b
#
# In Sage lässt sich dies wie mit der Funktion `xgcd()` lösen (für 2 Faktoren):
#   xgcd(11,13) == (1, 6, -5)  |  bedeutet, dass 1 = 6*11 + (-5)*13 = 66 - 65
#
# Für 3 Faktoren (meine eigene Funktion!!!):
# sage: xgcd3(b*c, a*c, a*b)
# (1, -1, 12, 152)
#
# Und für mehrere Faktoren (code takes about 2 minutes to execute...):
#
# sage: var("u v w")
# sage: a = 2**2                                                                                                                                                                       
# sage: b = 7**2                                                                                                                                                                       
# sage: c = 31**3 
# sage: for u in range(-200,200): 
# ....:     for v in range(-200,200): 
# ....:         for w in range(-200,200): 
# ....:             if u*b*c + v*a*c + w*a*b == 1: 
# ....:                 print(f"u={u}, v={v}, w={w}")
# ....:                 break
#
# u=-13, v=159, w=152
# u=-9, v=110, w=152
# u=-5, v=61, w=152
#  u=-1, v=12, w=152
# u=3, v=-37, w=152
# u=7, v=-86, w=152
# u=11, v=-135, w=152
# u=15, v=-184, w=152
#
"""
for u in range(-200,200): 
    for v in range(-200,200): 
        for w in range(-200,200): 
            if u*b*c + v*a*c + w*a*b == 1: 
                print(f"u={u}, v={v}, w={w}")
                break
"""

n2 =  7**2 * 31**3
n7 =  2**2 * 31**3
n31 = 2**2 *  7**2

## compute u, v, w such that u*n2 + v*n7 + w*n31 = 1
## u=-1, v=12, w=152 (result of Euclid => zusammensetzen!!!)
print(f'-n2 + 12*n7 +152*n31 = {-n2 + 12*n7 +152*n31}')

# Schritt/Part [1] (3. Teil): Setze die Lösung x zusammen: x = u*a*x_b + v*b*x_a
# Hier mit 3 Faktoren: x = u*b*c*x_a + v*a*c*x_b + w*a*b*x_c

## compose x2, x7, x31 to obtain dlog_g(h)
dl = (-n2*x2 + 12*n7*x7 +152*n31*x31)%(p-1)

# Schritt/Part [1] (4. Teil): Gebe Ergebnis aus und überprüfe die Korrektheit durch Potenzieren:

print(f'dlog_g(h) = {dl}')
print(f'check: {g**dl} == {h}')

print('===========================')




# Nun noch einmal beispielhalt Schritt/Part [2] (was wir eben noch naiv/brute-force-mäßig mit dlog() bestimmt haben):
#   Primzahlpotenzen:
#   ord(G) = p^e

## reduction for 31^3
## solve g31^x = h^31  in cyclic group of order 31**3 = 29791
## x = x_0 + x_1 * 31 + x_2 * 31**2
#    (x ist der gesuchte Wert mit g31^x = h^31 (in der Gruppe von Ordnung 31^3), hier in Basis p=31 geschrieben)

## first solve g31^(31^2 * x_0) = h31^(31^2)
#    enspricht auf Cheat Sheet: h^p^(e-1) = (g^p^(e-1))^x_0 * 1 # x_0 in Ordnung p "leicht" bestimmbar
 
g310 = g31**(31**2)
h310 = h31**(31**2)
x310 = dlog(g310, h310, 31) # x_0  # => habe soeben x_0 in Ordnung p "leicht" bestimmt!

# Und weiter gehts in Ordnung 31^2:

## solve now: (g31^31)^x_1 = h31 * g31^(-x310)  # enspricht auf Cheat Sheet: h*g^-x_0 = (g^p)^(x_1 + x_2*p + ...) ?!?!?!

g311 = (g31**31)**31
h311 = (h31 * g31**(-x310))**31
x311 = dlog(g311,h311,31) # x_1

## solve now g31^(31^2 * x_2) = h31 * g31^(-x310) * g31^(-x311*31)
g312 = g311
x312 = dlog(g312, h31*g31**(-x310)*g31**(-x311 * 31), 31)

# Habe nun x mit g31^x = h^31 in der Basis p=31 bestimmt, setze zusammen und printe:

## compute the dlog, should be 28796
print(f'{(x310 + 31*x311 + 31**2 * x312)%(p-1)} == 28769')

