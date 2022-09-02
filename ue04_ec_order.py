def find_non_square(p):
    """
    Finde ein Nicht-Quadrat modulo p.

    Finde ein zufälliges Element 1 <= r < p sodass
    weder 0 === r (mod p)
    noch ein x existiert mit x^2 === r (mod p).

    Letztlich nur eine "Kapselung" vom Jacobi-Symbol.
    """
    r = 1
    while jacobi_symbol(r, p) != -1:
        # Jacobi-Symbol(a, p prim) = Legendre-Symbol(a, p muss prim)
        #    = 1  wenn a ein quadratischer Rest modulo p ist (d.h. es existiert ein x mit x^2 === a (mod p))
        #    = -1 wenn a ein quadratischer Nichtrest modulo p ist
        #    = 0  wenn p ein Teiler von a ist (d.h. 0 === a (mod p))
        r = ZZ.random_element(1, p)
    return r


def square_root_mod(u, p):  # wissen: p ist ungerade
    """
    Algorithmus, der eine (! man beachte, dass in Z_p Wurzeln nicht eindeutig sein müssen!) Wurzel findet.
    Wie man Wurzeln in GF(p) findet, wurde gegen Ende in 2022-05-18_VL04.pdf beschrieben! (NICHT auf meinen Cheat Sheets!!!):

    Da p prim ist, muss entweder p === 1 oder p === 3 (mod 4) gelten:

    * Schön ist es, wenn p === 3 (mod 4) (könnte man hier auch vorher prüfen), denn dann gilt ganz einfach:
    sqrt(u) = u ^ ((p+1) / 4)
    Denn: [u ^ ((p+1) / 4)] ^ 2 = u ^ ((p+1) / 2) = sqrt(u) ^ (p+1) = sqrt(u)^(p-1) * sqrt(u)^2 = sqrt(u)^2 = u   Q.E.D.

    * Wenn p === 1 (mod 4) ist das Verfahren komplizierter, siehe unten bzw. 2022-05-18_VL04.pdf.
      Mir scheint hier jedoch ein Implementierungs-Fehler vorzuliegen, da z.B.
      square_root_mod(13, 17) == 16
      aber
      (16^2) % 17 == 1.

      Genauso gilt:
      square_root_mod(15, 17) gibt entweder 2, 8, 9 oder 15 zurück.
      Die tatsächlichen Wurzeln von 15 sind aber 7 und 10.

      Sage hat das Wurzel-Ziehen in Z_p aber auch bereits eingebaut:

      sage: sqrt(Zmod(17)(15))                                                                                                                                                             
      7
      sage:                                                                                                                                                                                
      sage: sqrt(Zmod(17)(13))                                                                                                                                                             
      8
      sage: 8^2 % 17                                                                                                                                                                       
      13

      Aber Achtung:

      sage: sqrt(Zmod(17)(10))                                                                                                                                                             
      sqrt10
    """

    # Check added by the dumb me:
    if u == 0:
        return 0  # sqrt(0) = 0
    elif jacobi_symbol(u, p) != 1:
        print(f"Cannot compute square root of u={u} in GF({p}) because u={u} is not a square in GF({p})!")
        return None

    # Zerlege p-1 = 2**h * m, m ungerade:
    lst = list(factor(p - 1))  # lst = Die Faktorisierung von p-1
    h = lst[0][1]  # h = Die Potenz des kleinstes Primfaktors von p-1 (hier die Potenz von 2)
    m = (p - 1) // (2 ** h)  # (m ist ungerade.)

    # Finde ein Nicht-Quadrat N in GF(p): Finde eine zufällige Zahl N, für die kein x existiert mit x^2 === N (mod p) (auch nicht 0):
    N = find_non_square(p)

    u1 = power_mod(u, m, p) # u1 = u^m (mod p)  # effizienter als (u**m) % p
    N1 = power_mod(N, m, p) # N1 = N^m (mod p)  # effizienter als (N**m) % p
    
    # find ell such that N1**ell = u1
    ell = log(Mod(u1, p), Mod(N1, p))  # ell = log_N1(u1)  # !!! ACHTUNG: log(32, 2) == 5 !!!  # "Theorie sagt: ell ist gerade"
    w = u1 ** (ell // 2)  # w = u1 ** (ell // 2)

    hh = power_mod(u, -(m - 1) // 2, p)  # hh = u ^ [-(m - 1) // 2] (mod p)
    s = w * hh % p  # s = (w * hh) % p  # "*" scheint stärker zu binden als "%" !!
    return s  # "die Wurzel aus u"


def find_point(a, b, p):
    """
    "Find-Point-Algorithmus".

    Finde einen Punkt auf der elliptischen Kurve mit den Parametern a und b:
    E_{a,b} = {(x,y) in Z_p^2 | y^2 = x^3 + ax + b}.

    Wähle dazu einfach solange ein zufälliges x aus Z_p,
    bis x^3 + ax + b ein Quadrat in Z_p ist! (völlig einleuchtend!)
    """

    ## find point on E_{a,b}
    while True:
        x = ZZ.random_element(p)  # Nehme ein zufälliges x.
        yp = x * (x * x + a) + b  # yp = x^3 + ax + b
        if jacobi_symbol(yp, p) == -1: # Wenn yp kein Quadrat ist, muss ich mir was anderes suchen!
            continue
        y = square_root_mod(yp, p) # **Wenn** yp ein Quadrat ist, gebe x=x (das zufällige) und y=sqrt(yp) zurück.
        break
    return x, y


def example_order(a, b, seed):
    """
    Finde die Ordnung eines (zufälligen) Punktes auf der EC E_{a,b}
    (über dem Körper Z_p wobei p = next_prime(seed)),
    die im Hasse-Weyl-Intervall liegt und erhalte damit
    eine **SCHÄTZUNG** für die Ordnung der Kurve!
    """

    p = next_prime(seed)

    x, y = find_point(a, b, p) # zufälliger Punkt auf der EC E_{a,b}

    print(f'x={x}, y={y}')

    E = EllipticCurve(GF(p), [a, b])  # Die EC E_{a,b} über dem Körper Z_p = GF(p)
    Q = E(x, y)

    ## 2*sqrt(p) for the Hasse-Weil bound
    t = ceil(2.0*sqrt(p*1.0))

    print(f't={t}')
    
    # try to find point of order
    # in the Hasse-Weil interval
    R = (p+1-t)*Q  # (p+1-t) ist die **minimale** Ordnung der Kurve nach Hasse-Weyl!
    od = 0
    for i in range(2*t):
        if R == E(0,1,0):  # "Wenn ich bei dem Einselement angekommen bin..."
            od = i
            break
        else:
            R = R + Q  # "Addiere Punkt Q immer weiter dazu."
    o1 = p + 1 - t + od  # Geschätzte Ordnung der Kurve E_{a,b}.
    print(f'estimated order o1 = {o1}')
    print(f'o1*Q = {o1*Q}')
    print(f'true order of E: {E.order()}')
