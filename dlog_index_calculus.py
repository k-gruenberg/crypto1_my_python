"""
Example from Lecture: 

sage: load("/Users/kendrick/Documents/SS2022/Kryptologie_1_CRYPTO1/Python_Ueb_mit_meinen_Kommentaren/crypto1_my_python/dlog_index_calculus.py")
sage: p = 11517659
sage: Zp = IntegerModRing(p)
sage: g = Zp.multiplicative_generator()
sage: dlog_index_calculus(h=g**4776699, p=p, Zp=Zp, g=g)                                                                                         
4776699

More examples:

sage: p = 17                                                                                                                                                                         
sage: Zp = IntegerModRing(p)                                                                                                                                                         
sage: g = Zp.multiplicative_generator()
sage: dlog_index_calculus(h=g**12, p=p, Zp=Zp, g=g, B=10, o=1, n=80, t=10)                                                                                                           
12

sage: p = next_prime(5000)                                                                                                                                                           
sage: p                                                                                                                                                                              
5003
sage: Zp = IntegerModRing(p)                                                                                                                                                         
sage: g = Zp.multiplicative_generator()
sage: dlog_index_calculus(h=g**3123, p=p, Zp=Zp, g=g, B=20, o=1, n=800, t=100)                                                                                                       
3123
"""


def dlog_index_calculus(h, p, Zp = None, g = None, B=50, o=76, n=8000, t=1000):
	# the index calculus

	if Zp is None:
		Zp = IntegerModRing(p)
	if g is None:
		g = Zp.multiplicative_generator()

	# from now on: index calculus

	# compute the factor basis  # Die Faktorbasis sind all die Primzahlen, die <= B sind:
	# p_1, ... p_t <= B
	def f_base(B):
	    """
	    Die Funktion gibt eine Liste all der Primzahlen zurück, die <= B sind,
	    die sog. "Faktorbasis".
	    """
	    ret=[2]  # nötig, da 2 die einzige gerade Primzahl ist, die also nicht von der Form 2*k+1 ist!
	    for i in [2*k+1 for k in range(B//2)]:  # ("for i in range(B+1):" hätte es auch getan, aber so ist es natürlich smarter)
	        if is_prime(i):
	            ret.append(i)
	    return ret

	# when is x smooth?
	def is_smooth(x, b):
	    """
	    Testet ob die gegebene Zahl x B-glatt ist.
	    Per Definition ist das genau dann der Fall, wenn alle Primteiler von x <= B sind.
	    """
	    if x == 1:  # NEW CASE!
	    	return False  # macht keinen Sinn, führt zur Gleichung 0=0 im LGS
	    pd = prime_divisors(x)
	    return pd[len(pd)-1] <= b  # Testest, ob der größte Primteiler von x <= B ist.

	# guess B and compute the factor base
	#B = 50
	fb = f_base(B)
	print(f"Gewählt wurde: B = {B}")
	print(f"Faktorbasis: fb = [p | p prim, p <= B == {B}] = {fb}")

	# Wir haben B (durch gutes Raten) und die zu B zugehörige Faktorbasis bestimmt, nun
	# können wir das LGS aufstellen, doch dazu benötigen wir zunächst
	# f_1, ..., f_r sodass g^f_i stets B-glatt ist:

	## fb = p_1, ... p_t
	## if g^k smooth
	## g^k = p_1^e_1 * ... * p_t^e_t
	## dlog: k = e_1 * dlog(p_1) + ... + e_t * dlog(p_t)

	# linearize p_1^e_1 * ... * p_t^e_t
	# returns [e_1, ... ,e_t]
	def to_lin(u, base):
	    """
	    Stellt die gegebene Zahl `u` in/mithilfe der Faktorbasis `base` dar:

	    Beispiel:

	    sage: to_lin(u=18, base=fb)                                                                                                                                                          
	    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	    
	    da 18 = 2 * 3^2
	    """
	    lenb = len(base)
	    ret = [0 for i in range(lenb)]
	    # t = (p_i, e_i)
	    for t in list(factor(u)):
	        ret[base.index(t[0])] = t[1]
	    return ret


	# find the LGS
	def find_lgs(o, n, g=g, B=B, fb=fb):  # ("g=g, B=B, fb=fb" von mir hinzugefügt zum leichteren Testen von kleineren Beispielen)
	    """
	    Stellt das Gleichungssystem
	    f_1 = e_{1,1} * dlog_g(p_1) + ... + e_{1,t} * dlog_g(p_t)
	    ...
	    f_i = e_{i,1} * dlog_g(p_1) + ... + e_{i,t} * dlog_g(p_t)
	    ...
	    f_r = e_{r,1} * dlog_g(p_1) + ... + e_{r,t} * dlog_g(p_t)
	    auf,
	    wobei g^f_i stets B-glatt ist und o <= f_1 <= f_r <= o+n.

	    Gibt pre_b, pre_M zurück,
	    wobei pre_b = {f_i | 1 <= i <= r bzw. eigentlich sodass o <= f_i <= o+n}
	    und pre_M = die rechte Seite des obigen LGS in Matrix-Form.
	    """
	    pre_b = []
	    pre_M = []
	    for i in range(n):
	        # ZZ cast to integer
	        u = ZZ(g**(o+i))
	        if is_smooth(u, B):
	            pre_b.append(o+i)
	            pre_M.append(to_lin(u, fb))
	    return pre_b, pre_M

	# guess o, n, and try
	pre_b, pre_M = find_lgs(o=o,n=n)
	# Tatsächlich wird gelten:
	#   pre_b = [76, 77, 78, 1115, 1116, 1117, 1118, 1119, 1120, 1648, ..., 6212, 6526, 6527, 6528, 6529, 6568, 6867]
	#   und len(pre_M) == 74.

	print("LGS:")
	for i in range(0, len(pre_b)):
		print(f"f_{i+1} = {pre_b[i]} = " + " + ".join([f"{pre_M[i][t]} * dlog_g(p_{t+1})" for t in range(0, len(fb))]))

	R = IntegerModRing(p-1)

	M = Matrix(R, pre_M)
	b = vector(R, pre_b)

	# Löse nun das obige besagte LGS, um die diskreten Logarithmen dlog_g(p_i) für alle 1 <= i <= t zu erhalten:
	## the dlogs of the primes in fb
	dlogs = M.solve_right(b)
	print("Lösung des LGS:")
	print(f"dlog_g(p_j = {fb}) = {dlogs}")

	# x mit h=g^x (g und h gegeben) lässt sich nun wie folgt bestimmen:
	# (1.) Suche eine Zahl f, sodass h*g^f B-glatt ist.
	# (2.) Aus h * g^f = p_1^e_1 * ... * p_t^e_t
	#      folgt dlog_g(h) + f = e_1 * dlog_g(p_1) + ... + e_t * dlog_g(p_t)
	#      folgt dlog_g(h) = -f + e_1 * dlog_g(p_1) + ... + e_t * dlog_g(p_t)
	#      Sprich: x = dlog_g(h) = -f + e_1 * dlog_g(p_1) + ... + e_t * dlog_g(p_t)
	#      Da wir soeben die diskreten Logarithmen dlog_g(p_i) für alle 1 <= i <= t (durch Lösen eines LGS)
	#      bestimmt haben, können wir jetzt auch x bestimmen:

	# find x 
	def comp_dlog(g, h, t):
	    for i in range(t):  # "f" heißt in der Schleife nun "i": Suche eine Zahl i, sodass h*g^i B-glatt ist. 
	        u = ZZ(h*g**i)
	        # h * g^i = p_1^e_1 * ... * p_t^e_t
	        # x + i = e_1 * dlog(p_1) + ... + e_t * dlog(p_t)
	        if is_smooth(u, B):
	            print(f"Ein f gefunden, sodass h*g^f B-glatt ist: f={i} und h*g^f = {u}")
	            x = (sum([t[1]*dlogs[fb.index(t[0])] for t in factor(u)]) - i)%(p-1)
	            print(f"x = dlog_g(h) = -f + sum(e_j * dlog_g(p_j)) = -{i} + sum({[t[1]*dlogs[fb.index(t[0])] for t in factor(u)]}) = {x} (mod {p-1})")
	            return x

	x = comp_dlog(g,h,t=t)

	assert(h == g**x)  # Überprüfe.

	return x
