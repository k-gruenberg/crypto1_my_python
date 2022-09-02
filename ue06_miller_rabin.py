def miller_rabin(x, n):
    """
    Der Miller-Rabin-Primzahltest.
    Testet, ob die Zahl `n` (Voraussetzung: `n` muss ungerade sein) prim ist.

    Berechnet dazu die Liste [x^m, (x^m)^2, (x^m)^4, (x^m)^8, ..., (x^m)^(2^h)]   (wobei n-1 = 2^h * m, mit m ungerade)
    und gibt diese zurück.

    * Falls die Liste die Form [1, 1, ..., 1, 1] oder [..., n-1, 1, 1, ..., 1, 1] hat,
      dann ist `n` VERMUTLICH prim (wäre es nicht prim, wäre der Test mit Wk. >=3/4 fehlgeschlagen!).
      Formal ausgedruckt: Jede 1 in der Liste muss auf eine +1 oder eine -1 folgen.
      !!! Falls das letzte Element in der Liste != 1 ist, dann schlägt bereits der Fermat-Test fehl und `n` ist definitiv NICHT prim !!!
    * Falls nicht, dann ist `n` definitiv NICHT prim.

    Um die Gewissheit zu erhöhen, sollte der Test für mehrere Werte von `x`
    durchgeführt werden!



    https://de.wikipedia.org/wiki/Miller-Rabin-Test#Funktionsweise:

    Die Folge besteht dann also entweder nur aus Einsen,
    oder sie enthält n − 1 (was sich bei modulo-n-Rechnung für einen Wert kongruent zu −1 ergibt),
    worauf wegen (n−1)^2 ≡ 1 Einsen folgen.
    Wenn die Folge nicht diese Form hat, muss n zusammengesetzt sein.

    Man prüft, ob die Folge mit 1 beginnt oder ob n − 1 spätestens als vorletztes Element auftritt.
    Ist dies der Fall, ist n entweder prim oder eine starke Pseudoprimzahl zur Basis a,
    und es wird „möglicherweise prim“ ausgegeben.
    Ansonsten kann n nicht prim sein, und der Algorithmus gibt „zusammengesetzt“ aus.
    Man kann die Berechnung abbrechen, wenn 0 oder 1 ohne vorhergehendes n − 1 auftritt,
    denn danach kann nur noch 0 bzw. 1 kommen.



    Beispiele:

    sage: miller_rabin(10, 17)                                                                                                                                                           
    Zahl n=17 ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:
    [10, 15, 4, 16, 1]

    sage: miller_rabin(12, 17)                                                                                                                                                           
    Zahl n=17 ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:
    [12, 8, 13, 16, 1]

    sage: miller_rabin(16, 17)                                                                                                                                                           
    Zahl n=17 ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:
    [16, 1, 1, 1, 1]

    sage: miller_rabin(10, 35)                                                                                                                                                           
    Zahl n=35 kann gar nicht prim sein, da bereits der Fermat-Test fehlschlägt: x^(n-1) == 10^34 == 25 != 1 (mod n=35)
    [5, 25]

    sage: miller_rabin(34, 35)                                                                                                                                                           
    Zahl n=35 ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:
    [34, 1]

    # Carmichael-Zahl 561=3*11*17:

    sage: miller_rabin(50, 561)                                                                                                                                                          
    Zahl n=561 ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:
    [560, 1, 1, 1, 1]

    sage: miller_rabin(100, 561)                                                                                                                                                         
    Zahl n=561 kann nicht prim sein, da Liste weder mit 1 anfängt noch n−1 spätestens als vorletztes Element auftritt:
    [298, 166, 67, 1, 1]
    """

    # (0.) Von mir hinzugefügt: Führe zunächst den Fermat-Test durch:
    if power_mod(x, n-1, n) != 1:
        print(f"Zahl n={n} kann gar nicht prim sein, da bereits der Fermat-Test fehlschlägt: x^(n-1) == {x}^{n-1} == {power_mod(x, n-1, n)} != 1 (mod n={n})")

    # (1.) Teile n-1 in den geraden und ungeraden Anteil, d.h. schreibe n-1 als 2^h * m   (wobei m ungerade):
    tl = list(factor(n-1))
    h = tl[0][1]
    m = (n-1) // (2**h)  # (von mir korrigiert, denn ich denke hier sollte n-1 und nicht n stehen...)
    assert(n-1 == 2**h * m)  # (added by me)

    # (2.) Berechne die Liste [x^m, (x^m)^2, (x^m)^4, (x^m)^8, ..., (x^m)^(2^h)] (alles modulo n versteht sich, wir sind ja in Z_n\{0}):
    x0 = power_mod(x,m,n)
    x_list = [x0]  # Beginne die Liste mit [x^m] (modulo n versteht sich)
    for i in range(h):
        # Berechne durch Quadrieren des letzen Listenelements das nächste Listenelement und füge es an:
        xi = power_mod(x_list[len(x_list)-1], 2, n)
        x_list.append(xi)

    # (3.) Von mir hinzugefügt: Untersuche die Liste:
    if x_list[0] == 1 or ((n-1) in x_list and x_list.index(n-1) <= len(x_list)-2):  # len(x_list)-2 ist der Index des vorletzen Elements
        print(f"Zahl n={n} ist vermutlich prim, da Liste mit 1 anfängt oder n−1 spätestens als vorletztes Element auftritt:")
    else:
        print(f"Zahl n={n} kann nicht prim sein, da Liste weder mit 1 anfängt noch n−1 spätestens als vorletztes Element auftritt:")

    # (4.) Gebe die berechnete Liste zurück:
    return(x_list)
