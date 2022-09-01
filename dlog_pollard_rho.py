"""
sage: Z13 = IntegerModRing(13)
sage: Z17 = IntegerModRing(17)

sage: load("/Users/kendrick/Documents/SS2022/Kryptologie_1_CRYPTO1/Python_Ueb_mit_meinen_Kommentaren/crypto1_my_python/dlog_pollard_rho.py")

sage: dlog_pollard_rho(g=Z13.multiplicative_generator(), h=Z13.multiplicative_generator()^7, group_order=12)
    x_0 = g^u_0 * h^v_0 = 2^1 * 11^1 = 2 * 11 = 9
	f(x_i=9) = x_i*h = 9*11 = 8 (v_i++)
	f(x_i=8) = x_i*g = 8*2 = 3 (u_i++)
	f(x_i=3) = x_i*h = 3*11 = 7 (v_i++)
	f(x_i=7) = x_i*x_i = 7*7 = 10 (u_i*=2, v_i*=2)
	f(x_i=10) = x_i*x_i = 10*10 = 9 (u_i*=2, v_i*=2)                                                                      
    x_i, u_i, v_i = [(9, 1, 1), (8, 1, 2), (3, 2, 2), (7, 2, 3), (10, 4, 6), (9, 8, 12)]
    g^u_L * h^v_k == g^u_L+T * h^v_L+T  =>  x = (u_L - u_L+T) / (v_L+T - v_L) = (1 - 8) / (12 - 1) = 7
    7

sage: dlog_pollard_rho(g=Z17.multiplicative_generator(), h=Z17.multiplicative_generator()^10, group_order=16)   
    x_0 = g^u_0 * h^v_0 = 3^1 * 8^1 = 3 * 8 = 7
	f(x_i=7) = x_i*x_i = 7*7 = 15 (u_i*=2, v_i*=2)
	f(x_i=15) = x_i*h = 15*8 = 1 (v_i++)
	f(x_i=1) = x_i*x_i = 1*1 = 1 (u_i*=2, v_i*=2)                                                                    
    x_i, u_i, v_i = [(7, 1, 1), (15, 2, 2), (1, 2, 3), (1, 4, 6)]
    g^u_L * h^v_k == g^u_L+T * h^v_L+T  =>  x = (u_L - u_L+T) / (v_L+T - v_L) = (2 - 4) / (6 - 3) = 10
    10

sage: dlog_pollard_rho(g=Z17.multiplicative_generator(), h=Z17.multiplicative_generator()^11, group_order=16)                                                                        
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)

=> auch nicht für andere Werte von u_0 und v_0 !!!!!


sage: dlog_pollard_rho(g=Z17.multiplicative_generator(), h=Z17.multiplicative_generator()^12, group_order=16)
    x_0 = g^u_0 * h^v_0 = 3^1 * 4^1 = 3 * 4 = 12
	f(x_i=12) = x_i*h = 12*4 = 14 (v_i++)
	f(x_i=14) = x_i*g = 14*3 = 8 (u_i++)
	f(x_i=8) = x_i*g = 8*3 = 7 (u_i++)
	f(x_i=7) = x_i*x_i = 7*7 = 15 (u_i*=2, v_i*=2)
	f(x_i=15) = x_i*h = 15*4 = 9 (v_i++)
	f(x_i=9) = x_i*h = 9*4 = 2 (v_i++)
	f(x_i=2) = x_i*g = 2*3 = 6 (u_i++)
	f(x_i=6) = x_i*h = 6*4 = 7 (v_i++)
    x_i, u_i, v_i = [(12, 1, 1), (14, 1, 2), (8, 2, 2), (7, 3, 2), (15, 6, 4), (9, 6, 5), (2, 6, 6), (6, 7, 6), (7, 7, 7)]
    g^u_L * h^v_k == g^u_L+T * h^v_L+T  =>  x = (u_L - u_L+T) / (v_L+T - v_L) = (3 - 7) / (7 - 2) = 12
    12
"""

def pollard_f(x_i, u_i, v_i, g, h, G1, G2, G3): # returns x_i+1, u_i+1, v_i+1
	#print(f"x_i = {x_i}")
	if ZZ(x_i) in G1:
		print(f"f(x_i={x_i}) = x_i*h = {x_i}*{h} = {x_i*h} (v_i++)")
		return x_i*h, u_i, v_i+1
	elif ZZ(x_i) in G2:
		print(f"f(x_i={x_i}) = x_i*x_i = {x_i}*{x_i} = {x_i*x_i} (u_i*=2, v_i*=2)")
		return x_i*x_i, 2*u_i, 2*v_i  # i.e. x_i^2
	elif ZZ(x_i) in G3:
		print(f"f(x_i={x_i}) = x_i*g = {x_i}*{g} = {x_i*g} (u_i++)")
		return x_i*g, u_i+1, v_i
	else:
		print("Error: x_i is neither in G1 nor in G2 nor in G3!")

BIG = 100000  # (but not too big because we're doing "in" checks!!!)

def dlog_pollard_rho(g, h, group_order, u_0=1, v_0=1, G1 = range(0,BIG,3), G2 = range(1,BIG,3), G3 = range(2,BIG,3)):
	x_0 = g**u_0 * h**v_0
	print(f"x_0 = g^u_0 * h^v_0 = {g}^{u_0} * {h}^{v_0} = {g**u_0} * {h**v_0} = {g**u_0 * h**v_0}")
	x_i_u_i_v_i = [(x_0, u_0, v_0)]
	while True:
		next_x, next_u, next_v = pollard_f(x_i_u_i_v_i[-1][0], x_i_u_i_v_i[-1][1], x_i_u_i_v_i[-1][2], g=g, h=h, G1=G1, G2=G2, G3=G3)
		if next_x in [x_i for x_i, u_i, v_i in x_i_u_i_v_i]: # Found collision:
			[(u_L, v_L)] = [(u_i, v_i) for x_i, u_i, v_i in x_i_u_i_v_i if x_i == next_x]
			u_L_plus_T = next_u
			v_L_plus_T = next_v

			#print(f"g^u_L * h^v_k == g^u_L+T * h^v_L+T  =>  x = (u_L - u_L+T) / (v_L+T - v_L) = ({u_L} - {u_L_plus_T}) / ({v_L_plus_T} - {v_L})")
			x = Zmod(group_order)(u_L - u_L_plus_T) / Zmod(group_order)(v_L_plus_T - v_L)

			x_i_u_i_v_i.append((next_x, next_u, next_v))
			print(f"x_i, u_i, v_i = {x_i_u_i_v_i}")
			print(f"g^u_L * h^v_k == g^u_L+T * h^v_L+T  =>  x = (u_L - u_L+T) / (v_L+T - v_L) = ({u_L} - {u_L_plus_T}) / ({v_L_plus_T} - {v_L}) = {x}")
			return x
		else:
			x_i_u_i_v_i.append((next_x, next_u, next_v))
