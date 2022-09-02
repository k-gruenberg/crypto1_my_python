# pollard_rho

def f(x, N):  # (Parameter N von mir ergänzt, schlechter Stil...)
	return (x**2 + 1) % N
    
def factor_pollard_rho(N = 71125773902563, s0=1000000, x0=1, y0=1):  # (Parameter N von mir ergänzt, schlechter Stil...)
    """
    Faktorisiere mit Pollard-Rho in O(p^0.5) = O(N^0.25) anstatt
    in O(N^0.5) wie mit Brute-Force:

    Laufe dazu mit x_i und y_i zufällig durch Z_n bis eine Kollision modulo p
    auftritt, d.h. bis x_i === y_i (mod p)
    => p | (x_i - y_i)
    => ggT(x_i - y_i, N) = p.   Q.E.D.

    Beispiele:

    sage: factor_pollard_rho()                                                                                                                                                           
    Faktorisiere N=71125773902563 mithilfe von Pollard-Rho, beginne bei x0=1 und y0=1:
    divisor 8383757 found in 2347 steps; with x=46251308021363, y=15832388358151 and gcd(x-y, N) = gcd(30418919663212, 71125773902563) = 8383757
    8383757

    sage: factor_pollard_rho(12)                                                                                                                                                         
    Faktorisiere N=12 mithilfe von Pollard-Rho, beginne bei x0=1 und y0=1:
    divisor 3 found in 2 steps; with x=2, y=5 and gcd(x-y, N) = gcd(-3, 12) = 3
    3

    sage: factor_pollard_rho(11*17)                                                                                                                                                      
    Faktorisiere N=187 mithilfe von Pollard-Rho, beginne bei x0=1 und y0=1:
    divisor 11 found in 5 steps; with x=116, y=39 and gcd(x-y, N) = gcd(77, 187) = 11
    11

    sage: factor_pollard_rho(next_prime(1000)*next_prime(5000))                                                                                                                          
    Faktorisiere N=5048027 mithilfe von Pollard-Rho, beginne bei x0=1 und y0=1:
    divisor 1009 found in 50 steps; with x=391491, y=2131007 and gcd(x-y, N) = gcd(-1739516, 5048027) = 1009
    1009
    """

    x = x0  # initial x_i = x_0
    y = y0  # initial y_i = y_0

    print(f"Faktorisiere N={N} mithilfe von Pollard-Rho, beginne bei x0={x0} und y0={y0}:") # (von mir ergänzt)

    for s in range(1,s0):
        t = gcd(x-y, N)  # Berechne den ggT(x_i - y_i, N) und erhalte einen (trivialen oder nicht-trivialen) Teiler von N.
        if t > 1 and t < N:  # Juhu, habe mit gcd(x-y, N) einen nicht-trivialen(!) Teiler von N gefunden:
            print(f'divisor {t} found in {s} steps; with x={x}, y={y} and gcd(x-y, N) = gcd({x-y}, {N}) = {gcd(x-y, N)}')  # (von mir ergänzt)
            return t  # "return t" ist doch wohl deutlich schöner als "break"...
        x = f(x, N)        # Laufe mit x_i zufällig weiter
        y = f(f(y, N), N)  # Laufe mit y_i zufällig weiter

    # Von mir ergänzt:
    print(f'No divisor found in {s0-1} steps')
    return None
