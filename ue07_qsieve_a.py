N = 71125773902563

# QS
# Das Quadratische Sieb
# (die zweitschnellste bekannte Faktorisierungsmethode, nach dem Zahlkörpersieb und vor der EC-Faktorisierung):

def is_smooth(B, x):
    """
    Ist x B-glatt?!
    (D.h. sind alle Primteiler von x <= B?!)
    """
    xl = list(factor(x))
    return xl[-1][0] <= B  # Ist der größte Primteiler von x <= B?!
    

def construct_smooth(N, B, g):
    """
    Konstruiere B-glatte t_i^2 - N,
    angefangen bei t_0 = ceil(sqrt(N)) (wird hier aber de facto ignoriert, also eig. angefangen bei t_1)
    und dann t_i = t_{i-1} + 1 (bis hin zu t_{g-1}).
    Gebe zwei Listen zurück:
    [t_i^2 - N | i], [t_i | i]
    """
    t0 = ceil(sqrt(N))
    ret = []
    tees = []
    for i in range(1,g):
        z = (t0+i)**2 - N
        if is_smooth(B,z):
            ret.append(z)
            tees.append(t0+i)
    return ret, tees
    
            
def construct_lgs(smooth, factor_basis):
    """
    Konstruiere das folgende LGS (über Z_2):

    y_0 * e_0,j + ... + y_k * e_k,j === 0 (mod 2) für 0 <= j <= k

    (e's fest (die Exponenten aus der Faktorisierung der glatten Zahlen), y's gesucht)
    """
    ret = []
    for z in smooth:
        zl = list(factor(z))
        v = [0] * len(factor_basis)
        for p, e in zl:
            idx = factor_basis.index(p)
            v[idx] = e
        ret.append(v)
    return ret


def quadratic_sieve(N, B, g, r=0):
    """
    Nutze das Verfahren des Quadratischen Siebs, um N zu faktorisieren.
    Nutze dazu B-glatte Zahlen (probiere dazu g-1 Zahlen aus).

    In Übung aufgreufen als: quadratic_sieve(N, 10000, 10000, 0) => 8483759

    Ein weiteres Beispiel von mir:
    
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=100, g=10000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=100, g=20000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=100, g=30000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=100, g=40000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=100, g=50000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=200, g=50000) == 1
    quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=150, g=50000) == 1009
    """

    smooth, tees = construct_smooth(N, B, g)  # Konstruiere B-glatte t_i^2 - N.
    factor_basis = prime_range(B+1)  # Die Faktorbasis = alle Primzahlen <= B
    print(f'{len(smooth)} smooth numbers on a factor basis of {len(factor_basis)} primes:')
    print(f"=> Smooth numbers: {smooth}")  # (von mir ergänzt)
    print(f"=> Factor basis: {factor_basis}")  # (von mir ergänzt)
    pre_lgs = construct_lgs(smooth, factor_basis)  # Konstruiere LGS: y_0 * e_0,j + ... + y_k * e_k,j === 0 (mod 2) für 0 <= j <= k
    print("===== LGS über ZZ (hier als Matrix ausgegeben) (y_0 * e_0,j + ... + y_k * e_k,j soll gerade sein, für 0 <= j <= k und e_i den Exponenten der glatten Zahlen): =====")
    print(Matrix(ZZ, pre_lgs))
    M = Matrix(GF(2), pre_lgs)  # Schreibe das LGS als Matrix und übetrage es in GF(2).
    print("===== LGS über GF(2) als Matrix (y_0 * e_0,j + ... + y_k * e_k,j === 0 (mod 2) für 0 <= j <= k und e_i den Exponenten der glatten Zahlen): =====")
    print(M)
    sol = M.left_kernel()  # Löse das LGS (da alle Gleichungen === 0 sind, entspricht das der Bestimmung des Kerns der Matrix)
    print("===== Lösung/en des LGS über GF(2) (Kern der obigen Matrix): =====")
    print(sol)
    rows = sol.basis_matrix().rows()
    print("===== Lösung/en des LGS als Zeilen: =====")
    print(rows)
    if len(rows) == 0:
        print('LGS has only trivial solution.')
        return
    if r >= len(rows):
        print('No more rows.')
        return
    row = rows[r]
    y = sqrt(prod([smooth[i]**ZZ(row[i]) for i in range(len(smooth))]))  # y == T == sqrt((t_0^2 - N)^y_0 * ... * (t_k^2 - N)^y_k) # prod() = product!!!
    x = prod([tees[i]**ZZ(row[i]) for i in range(len(smooth))])  # x == S == t_0 ^ y_0 * ... * t_k ^ y_k
    print(f"Ein Faktor von N: gcd(x-y,N) = gcd({x}-{y},{N}) = gcd({x-y},{N}) = {gcd(x-y,N)}")
    assert(N % gcd(x-y,N) == 0)  # (Überprüfe, dass tatsächlich ein Faktor. Eigentlich klar per Definition des gcd().)
    return gcd(x-y,N)
    
"""
sage: quadratic_sieve(N=next_prime(1000) * next_prime(5000), B=150, g=50000)                                                                                                         
39 smooth numbers on a factor basis of 35 primes:
=> Smooth numbers: [41509, 154934, 246574, 260389, 334373, 339014, 764894, 1629029, 2301494, 2630414, 3933982, 6958198, 7639817, 7761214, 11386889, 15500062, 27396389, 56088734, 60303029, 62783669, 66625129, 75072374, 80514473, 102302294, 150427934, 202600073, 232450894, 295905077, 305451614, 433812574, 468231998, 494072254, 679140622, 702777998, 766069334, 809540654, 875498249, 1157284622, 1636255142]
=> Factor basis: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]  # alle Primzahlen <= B
===== LGS über ZZ (hier als Matrix ausgegeben) (y_0 * e_0,j + ... + y_k * e_k,j soll gerade sein, für 0 <= j <= k und e_i den Exponenten der glatten Zahlen): =====
[0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0]  # denn factor(41509) = 13 * 31 * 103
[1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]  # denn factor(154934) = 2 * 13 * 59 * 101
...
[1 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0]  # denn factor(1636255142) = 2 * 41^2 * 59 * 73 * 113
===== LGS über GF(2) als Matrix (y_0 * e_0,j + ... + y_k * e_k,j === 0 (mod 2) für 0 <= j <= k und e_i den Exponenten der glatten Zahlen): =====
[0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0]  # selbiges wie oben für factor(41509)
[1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]  # selbiges wie oben für factor(154934)
...
[1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0]  # die "2" aus factor(1636255142) wurde hier zur "0" (da nun in GF(2)), da uns nur wichtig ist, ob Exponent gerade oder ungerade ist (wir wollen ja ein Quadrat T^2 (hier y^2) erzeugen)
===== Lösung/en des LGS über GF(2) (Kern der obigen Matrix): =====
Vector space of degree 39 and dimension 27 over Finite Field of size 2
Basis matrix:
27 x 39 dense matrix over Finite Field of size 2
===== Lösung/en des LGS als Zeilen: =====
[(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, ...
Ein Faktor von N: gcd(x-y,N)
= gcd(19755635698077496443990418016181600-1732232898794945545106369552765864,5048027)
= gcd(18023402799282550898884048463415736,5048027)
= 1009
1009
"""
