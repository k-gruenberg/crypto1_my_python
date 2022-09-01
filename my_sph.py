def dlog(g, order, h, recursionDepth=0):  # ToDo: recursionDepth 
	"""
	Given a generator `g` that generates a group of order `order`
	and h=g^x, return x, i.e. solve the DLP -- using SPH and brute force.
	"""

	if is_prime(order):  # ord(G) is prime:
		# Use brute force:
		for x in range(0, order):
			if g**x == h:
				print("\t" * recursionDepth + f"[0] dlog(g={g}, order={order}, h={h}) = {x} (using brute force)")
				return x
		return None
	elif len(factor(order)) == 1:  # ord(G) = p^e with p prime and e>1:
		# Use SPH [2]:
		p, e = factor(order)[0]
		assert(order == p ** e)
		print("\t" * recursionDepth + f"[2] ===== ord(G) = p^e with p={p} and e={e} =====")

		x_0 = dlog(g=g**(p**(e-1)), order=p, h=h**(p**(e-1)), recursionDepth=recursionDepth+1)
		print("\t" * recursionDepth + f"[2] x_0 = dlog(g=g**(p**(e-1))={g**(p**(e-1))}, order=p={p}, h=h**(p**(e-1))={(p**(e-1))}) = {x_0} (using recursive call)")

		x_1_plus_x_2_p_etc = dlog(g=g**p, order=p**(e-1), h=h*g**(-x_0), recursionDepth=recursionDepth+1)
		print("\t" * recursionDepth + f"[2] x_1_plus_x_2_p_etc = dlog(g=g**p={g**p}, order=p**(e-1)={p**(e-1)}, h=h*g**(-x_0)={h*g**(-x_0)}) = {x_1_plus_x_2_p_etc} (using recursive call)")

		return (x_0 + p * x_1_plus_x_2_p_etc) % order
	else:  # ord(G) = a * b with gcd(a, b) == 1:
		# Use SPH [1]:
		# Pull out the first prime power as a and use the rest as b:
		a = factor(order)[0][0] ** factor(order)[0][1]
		b = order / a
		assert(gcd(a, b) == 1)
		print("\t" * recursionDepth + f"[1] ===== ord(G) = a * b with a={a} and b={b} =====")

		x_a = dlog(g=g**b, order=a, h=h**b, recursionDepth=recursionDepth+1)
		print("\t" * recursionDepth + f"[1] x_a = dlog(g=g**b={g**b}, order=a={a}, h=h**b={h**b}) = {x_a} (using recursive call)")
		x_b = dlog(g=g**a, order=b, h=h**a, recursionDepth=recursionDepth+1)
		print("\t" * recursionDepth + f"[1] x_b = dlog(g=g**a={g**a}, order=b={b}, h=h**a={h**a}) = {x_b} (using recursive call)")

		_one, u, v = xgcd(a, b)  # (extended Euclidean algorithm)
		assert(u*a + v*b == _one)
		assert(_one == 1)
		print("\t" * recursionDepth + f"[1] Found u = {u} and v = {v} with u*a + v*b == 1 with Euclid")

		x = (u * a * x_b + v * b * x_a) % order
		print("\t" * recursionDepth + f"[1] Computed dlog(g={g}, order={order}, h={h}) = x = {x} (using SPH [1])")
		return x


def dlogZp(p, h, Z = IntegerModRing(p), g = Z.multiplicative_generator()):
	# for example: p = 5839037, g = 2 and h = g**2769541
	# should return: 2769541
	answer = dlog(g=g, order=p-1, h=h)
	assert(h == g**answer)
	return answer

"""
sage: load("/Users/kendrick/Documents/SS2022/Kryptologie_1_CRYPTO1/Python_Ueb_mit_meinen_Kommentaren/my_sph.py")                                                                                                                                                                                                                                                    
sage:                                                                                                                                                                                
sage: dlogZp(p = 5839037, h = g**2769541)                                                                                                                                            
[1] ===== ord(G) = a * b with a=4 and b=1459759 =====
	[2] ===== ord(G) = p^e with p=2 and e=2 =====
		[0] dlog(g=5839036, order=2, h=5839036) = 1 (using brute force)
	[2] x_0 = dlog(g=g**(p**(e-1))=5839036, order=p=2, h=h**(p**(e-1))=2) = 1 (using recursive call)
		[0] dlog(g=5839036, order=2, h=1) = 0 (using brute force)
	[2] x_1_plus_x_2_p_etc = dlog(g=g**p=5839036, order=p**(e-1)=2, h=h*g**(-x_0)=1) = 0 (using recursive call)
[1] x_a = dlog(g=g**b=1902746, order=a=4, h=h**b=1902746) = 1 (using recursive call)
	[1] ===== ord(G) = a * b with a=49 and b=29791 =====
		[2] ===== ord(G) = p^e with p=7 and e=2 =====
			[0] dlog(g=4745330, order=7, h=4688678) = 5 (using brute force)
		[2] x_0 = dlog(g=g**(p**(e-1))=4745330, order=p=7, h=h**(p**(e-1))=7) = 5 (using recursive call)
			[0] dlog(g=4745330, order=7, h=4745330) = 1 (using brute force)
		[2] x_1_plus_x_2_p_etc = dlog(g=g**p=4745330, order=p**(e-1)=7, h=h*g**(-x_0)=4745330) = 1 (using recursive call)
	[1] x_a = dlog(g=g**b=2270366, order=a=49, h=h**b=631894) = 12 (using recursive call)
		[2] ===== ord(G) = p^e with p=31 and e=3 =====
			[0] dlog(g=3213846, order=31, h=3213846) = 1 (using brute force)
		[2] x_0 = dlog(g=g**(p**(e-1))=3213846, order=p=31, h=h**(p**(e-1))=961) = 1 (using recursive call)
			[2] ===== ord(G) = p^e with p=31 and e=2 =====
				[0] dlog(g=3213846, order=31, h=1455982) = 29 (using brute force)
			[2] x_0 = dlog(g=g**(p**(e-1))=3213846, order=p=31, h=h**(p**(e-1))=31) = 29 (using recursive call)
				[0] dlog(g=3213846, order=31, h=1455982) = 29 (using brute force)
			[2] x_1_plus_x_2_p_etc = dlog(g=g**p=3213846, order=p**(e-1)=31, h=h*g**(-x_0)=1455982) = 29 (using recursive call)
		[2] x_1_plus_x_2_p_etc = dlog(g=g**p=4420568, order=p**(e-1)=961, h=h*g**(-x_0)=4358289) = 928 (using recursive call)
	[1] x_b = dlog(g=g**a=3860916, order=b=29791, h=h**a=4193828) = 28769 (using recursive call)
	[1] Found u = 608 and v = -1 with u*a + v*b == 1 with Euclid
	[1] Computed dlog(g=16, order=1459759, h=3334389) = x = 1309782 (using SPH [1])
[1] x_b = dlog(g=g**a=16, order=b=1459759, h=h**a=3334389) = 1309782 (using recursive call)
[1] Found u = 364940 and v = -1 with u*a + v*b == 1 with Euclid
[1] Computed dlog(g=2, order=5839036, h=5066826) = x = 2769541 (using SPH [1])
2769541
"""
