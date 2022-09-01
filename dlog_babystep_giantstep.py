def dlog_babystep_giantstep(generator_g, order_n, h):
	"""
	Berechnet ein x, sodass h = generator_g^x (d.h. löst das DLP).

	Beispiel:

	sage: Z13 = IntegerModRing(13)
	sage: Z13.multiplicative_generator()                                                                                                                                                 
    2
    sage: dlog_babystep_giantstep(generator_g=2, order_n=12, h=2**5)                                                                                                                     
    5
    sage: dlog_babystep_giantstep(generator_g=Z13.multiplicative_generator(), order_n=12, h=2**5)                                                                                        
    5
    sage: dlog_babystep_giantstep(generator_g=Z13.multiplicative_generator(), order_n=12, h=2**17)                                                                                       
    5

    sage: dlog_babystep_giantstep(generator_g=2, order_n=12, h=2**5)                                                                                                                     
	    N = ceil(sqrt(12)) = 4 where 12 = order_n
	    Giant Steps: [g^0, g^N, g^2N, ..., g^(N-1)N] = [1, 16, 256, 4096]
	    Baby Steps: [h, h*g^(-1), h*g^(-2), ..., h*g^(-N+1)] = [32, 16, 8, ..., 4] = [32, 16, 8, 4]
	    Found collision g^(u*big_N) == h*g^(-v): 2^(1*4) == 16 == 16 == 32*2^(-1)
	      => x = dlog_g(h) = u*big_N + v = 1*4 + 1 = 5
    5

	https://de.wikipedia.org/wiki/Babystep-Giantstep-Algorithmus
	"""

	big_N = math.ceil(math.sqrt(order_n))
	print(f"\tN = ceil(sqrt({order_n})) = {big_N} where {order_n} = order_n")

	giant_steps = [generator_g**(i*big_N) for i in range(0, big_N)]
	print(f"\tGiant Steps: [g^0, g^N, g^2N, ..., g^(N-1)N] = {giant_steps}")

	print(f"\tBaby Steps: [h, h*g^(-1), h*g^(-2), ..., h*g^(-N+1)] = [{h}, {h*g**(-1)}, {h*g**(-2)}, ..., {h*g**(-big_N+1)}] = {[h*g**(-v) for v in range(0, big_N)]}")
	#print(f"\tBaby Steps: [h, h*g^(-1), h*g^(-2), ..., h*g^(-N+1)] = [{h}, {h*g**(-1)}, {h*g**(-2)}, ..., {h*g**(-big_N+1)}]")  # for bigger examples: w/o duplicate computation...
	# Baby Steps:
	for v in range(0, big_N):
		baby_step = h * generator_g**(-v)
		if baby_step in giant_steps:  # found collision:
			# g^(u*big_N) == h*g^(-v) => x = dlog_g(h) = u*big_N + v
			u = giant_steps.index(baby_step)
			print(f"\tFound collision g^(u*big_N) == h*g^(-v): {g}^({u}*{big_N}) == {g**(u*big_N)} == {h*g**(-v)} == {h}*{g}^(-{v})")
			print(f"\t  => x = dlog_g(h) = u*big_N + v = {u}*{big_N} + {v} = {u*big_N + v}")
			return u*big_N + v
