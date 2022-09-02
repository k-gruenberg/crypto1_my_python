# "Das ist also das, was ich vergessen habe" / "Ich gebe Ihnen das mit":
# Rechne dlog in Körper aus und teste:

q = 31609549  # eine Primzahl: is_prime(31609549) == True
Eq = EllipticCurve(GF(q), [0,-1])  # E_{0, -1} = {(x,y) in GF(q)^2 | y^2 = x^3 - 1}
# => Ich nehme mal an, diese Kurve hat einen geringen Einbettungsgrad (MOV-Attack, s.u.)...

# Drei Punkte P, Q und T auf dieser EC (P und Q "zufällig wählen und hoffen, dass gut ist"):
P = Eq(( 5049972 , 14242076 , 1))
Q = Eq((16545731 , 18354147 , 1))  # = ein Vielfaches von P, finde den Faktor x mit Q == x*P heraus, s.u. ...
T = Eq((30571290 , 10731231 , 1))
print(T.order() == 541)  # Punkt hat Ordnung 541  # gibt tatsächlich "True" aus!

# Dieser untere Teil wirft leider einen Fehler...:
#   AttributeError: 'int' object has no attribute 'test_bit'
# Beim manuellen Einfügen in die Sage Shell funktioniert es seltsamerweise...

# "erzähle Ihnen nicht, wie man die Weil-Pairing ausrechnet" => in SageMath geschenkt
g = P.weil_pairing(T,541)  # g == 30391587  # => die Weil-Paarung ist eine Zahl
h = Q.weil_pairing(T,541)  # h == 10935566
x = discrete_log(h,g,541)  # x == 213  # x = dlog_g(h)  # discrete_log(a, base, ord = order of base or None, ...) ?! # Example: discrete_log(Zmod(17)(15), Zmod(17)(2)) == 5
print(x * P == Q)  # True  # x * P ist (16545731 : 18354147 : 1) sprich Q

"""
Angenommen, es gilt x * P == Q und wir suchen x:
w(P, T)^x == w(x*P, T) == w(Q, T)
=> x = dlog_{w(P,T)}(w(Q,T))
Hier ist g=w(P,T) und h=w(Q,T), wir können also beides ausrechnen und
müssen dann nur den diskreten Logarithmus für diese beiden Zahlen ausrechnen
und erhalten x. 
"""

"""
Vgl. MOV-Angriff / genau dasselbe: Gegeben: x*P; Gesucht: x

   w(x*P, Q) = w(P, Q)^x           | Bilinearität der Weil-Paarung!
=> x = dlog_{w(P, Q)} (w(x*P, Q))
"""
