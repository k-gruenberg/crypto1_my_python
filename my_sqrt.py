def my_sqrt(u, p):
	"""
	Compute sqrt(u) (mod p).

	===== Examples: =====

	sage: sage: my_sqrt(5, 12)                                                                                                                                                           
	Error in my_sqrt(): p=12 is not prime!

	sage: sage: my_sqrt(5, 11)                                                                                                                                                           
	p % 4 == 3 => using simple formula...
	p % 4 == 3 => sqrt(u=5) = power_mod(u, (p+1)//4, p) = power_mod(5, (11+1)//4, 11) = 4
	4

	sage: my_sqrt(14, 17)                                                                                                                                                                
	Error in my_sqrt(): u=14 has no square root mod p=17 according to Sage: sqrt(Zmod(p)(u)) = sqrt(Zmod(17)(14)) = sqrt14
	
	sage: my_sqrt(15, 17)                                                                                                                                                                
	p % 4 == 1 => using complex formula (the Tonelli–Shanks algorithm)...
	Found N=3 which is a non-square in GF(p=17).
	Wrote p-1 as 2^h * (2*t+1): 16 = p-1 = 2^h * (2*t+1) = 2^4 * (2*0+1) = 16
	Continuing with the Tonelli–Shanks algorithm as described on en.wikipedia.org:
		n = u = 15, Q = 2*t+1 = 2*0+1 = 1, S = h = 4, z = non_square_N = 3
		M = S = 4, c = z^Q = 3^1 = 3, t = n^Q = 15^1 = 15, R = n^((Q+1)//2) = 15^((1+1)//2) = 15

	[1] Tonelli–Shanks algo: Found least i such that t^2^i = 15^2^i = 1: i=3
	[1] Tonelli–Shanks algo: b = c^2^(M-i-1) = 3^2^(4-3-1) = 3
	[1] Tonelli–Shanks algo: M = i = 3, c = b^2 = 3^2 = 9
	[1] Tonelli–Shanks algo: t = t*b^2 = 15 * 9 = 16
	[1] Tonelli–Shanks algo: R = R*b = 15 * 3 = 11

	[2] Tonelli–Shanks algo: Found least i such that t^2^i = 16^2^i = 1: i=1
	[2] Tonelli–Shanks algo: b = c^2^(M-i-1) = 9^2^(3-1-1) = 13
	[2] Tonelli–Shanks algo: M = i = 1, c = b^2 = 13^2 = 16
	[2] Tonelli–Shanks algo: t = t*b^2 = 16 * 16 = 1
	[2] Tonelli–Shanks algo: R = R*b = 11 * 13 = 7

	[3] Tonelli–Shanks algo: If t = 1, return r = R = 7
	7
	sage: 7^2 % 17                                                                                                                                                                       
	15
	"""

	if not is_prime(p):
		print(f"Error in my_sqrt(): p={p} is not prime!")
		return None
	elif sqrt(Zmod(p)(u)) not in ZZ:
		print(f"Error in my_sqrt(): u={u} has no square root mod p={p} according to Sage: sqrt(Zmod(p)(u)) = sqrt(Zmod({p})({u})) = {sqrt(Zmod(p)(u))}")
		return None

	square_root_of_u = None

	if p % 4 == 3:
		print("p % 4 == 3 => using simple formula...")

		square_root_of_u = power_mod(u, (p+1)//4, p)
		print(f"p % 4 == 3 => sqrt(u={u}) = power_mod(u, (p+1)//4, p) = power_mod({u}, ({p}+1)//4, {p}) = {square_root_of_u}")
	elif p % 4 == 1:
		print("p % 4 == 1 => using complex formula (the Tonelli–Shanks algorithm)...")

		# (1) and (2) is the part of the Tonelli–Shanks algorithm that the lecture and Wikipedia agree on:

		# (1) Find a number N thats not a square in GF(p):
		non_square_N = 1
		while jacobi_symbol(non_square_N, p) != -1:
			non_square_N += 1
		print(f"Found N={non_square_N} which is a non-square in GF(p={p}).")

		# (2) Write p-1 as 2^h * (2*t+1):
		p_1_factorization = factor(p-1)
		h = p_1_factorization[0][1]
		t = (((p-1) // (2**h)) - 1) // 2
		assert(p-1 == (2**h) * (2*t+1))
		print(f"Wrote p-1 as 2^h * (2*t+1): {p-1} = p-1 = 2^h * (2*t+1) = 2^{h} * (2*{t}+1) = {(2**h) * (2*t+1)}")

		# This is how the rest was described in the CRYPTO1 lecture but it does not work...:
		"""
		# (3) Find an f such that (N^(2*t+1))^f == u^(2*t+1):
		f = 1
		while power_mod(N, (2*t+1)*f, p) != power_mod(u, 2*t+1, p):
			f += 1
		print(f"Found f={f} such that (N^(2*t+1))^f == u^(2*t+1), i.e. {N**(2*t+1)}^f == {u ** (2*t+1)}")

		# (4) Compute sqrt:
		square_root_of_u = power_mod(N, (2*t+1) * (f//2), p) * power_mod(u, -t, p)
		print(f"sqrt(u={u}) = N^((2*t+1) * (f//2)) * u^(-t) = {N}^((2*{t}+1) * ({f}//2)) * {u}^(-{t}) = {square_root_of_u}")
		"""

		# This is how the rest of the Tonelli–Shanks algorithm is described on
		#   https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm:
		print("Continuing with the Tonelli–Shanks algorithm as described on en.wikipedia.org:")
		n = u
		Q = 2*t+1
		S = h
		z = non_square_N
		print(f"\tn = u = {n}, Q = 2*t+1 = 2*{t}+1 = {Q}, S = h = {S}, z = non_square_N = {z}")

		M = S
		c = power_mod(z, Q, p)
		t = power_mod(n, Q, p)
		R = power_mod(n, (Q+1)//2, p)
		print(f"\tM = S = {M}, c = z^Q = {z}^{Q} = {c}, t = n^Q = {n}^{Q} = {t}, R = n^((Q+1)//2) = {n}^(({Q}+1)//2) = {R}")

		print("")

		iteration_counter = 0
		while True:  # "Loop:"
			iteration_counter += 1

			if t == 0:
				square_root_of_u = 0  # "If t = 0, return r = 0"
				print(f"[{iteration_counter}] Tonelli–Shanks algo: If t = 0, return r = 0")
				break
			elif t == 1:
				square_root_of_u = R  # "If t = 1, return r = R"
				print(f"[{iteration_counter}] Tonelli–Shanks algo: If t = 1, return r = R = {R}")
				break
			else:
				# "Otherwise, use repeated squaring to find the least i,
				#  0 < i < M, such that t^2^i = 1":
				i = 1
				while power_mod(t, power_mod(2, i, p), p) != 1:
					i += 1
				print(f"[{iteration_counter}] Tonelli–Shanks algo: Found least i such that t^2^i = {t}^2^i = 1: i={i}")
				print(f"[{iteration_counter}] Tonelli–Shanks algo: b = c^2^(M-i-1) = {c}^2^({M}-{i}-1) = {power_mod(c, power_mod(2, M - i - 1, p), p)}")
				b = power_mod(c, power_mod(2, M - i - 1, p), p)
				M = i
				c = power_mod(b, 2, p)
				print(f"[{iteration_counter}] Tonelli–Shanks algo: M = i = {M}, c = b^2 = {b}^2 = {c}")
				print(f"[{iteration_counter}] Tonelli–Shanks algo: t = t*b^2 = {t} * {b}^2 = {t} * {power_mod(b, 2, p)} = {t * power_mod(b, 2, p) % p}")
				t = t * power_mod(b, 2, p) % p
				print(f"[{iteration_counter}] Tonelli–Shanks algo: R = R*b = {R} * {b} = {R*b % p}")
				R = R*b % p

			print("")
	else:
		print(f"Error in my_sqrt(): p={p} is not prime: p % 4 == {p % 4}")
		square_root_of_u = None

	if square_root_of_u is not None:
		assert(power_mod(square_root_of_u, 2, p) == u)
	return square_root_of_u
