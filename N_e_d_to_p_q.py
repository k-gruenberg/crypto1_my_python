def N_e_d_to_p_q(N, e, d):
	k = math.ceil((e*d - 1) / N)
	print(f"k = math.ceil((e*d - 1) / N) = math.ceil(({e}*{d} - 1) / {N}) = math.ceil({(e*d - 1) / N}) = {k}")

	print(f"Finde nun ein i sodass (d*e-1)/(k+i) in ZZ d.h. {d*e-1}/({k}+i) in ZZ")
	for i in range(0,1000000000): 
		if (d*e-1)/(k+i) in ZZ: 
			print(f"i = {i} erfüllt (d*e-1)/(k+i) in ZZ, denn ({d}*{e}-1)/({k}+{i}) = {d*e-1}/{k+i} = {(d*e-1)/(k+i)} in ZZ")
			phi_N = (d*e-1)/(k+i)
			print(f"phi(N) = (d*e-1)/(k+i) = ({d}*{e}-1)/({k}+{i}) = {d*e-1}/{k+i} = {phi_N}")
			var("x")
			print(f"p und q sind die Lösungen von [x**2 - (N-phi_N+1)*x + N == 0] d.h. [x**2 - ({N}-{phi_N}+1)*x + {N} == 0]")
			return solve([x**2 - (N-phi_N+1)*x + N == 0], x)


# sage: N_e_d_to_p_q(N=38749709,e=10988423,d=36153251)                                                                                                                                                      
# i = 3332
# [x == 5347, x == 7247]
#
# By the way gilt:
# 3332 ~= 10252135*((5347*7247)/(5346*7246)-1)
# i    ~= k * ( (p*q)/((p-1)*(q-1)) - 1)

# sage: N_e_d_to_p_q(N=143,e=7,d=103)                                                                                                                                                  
# i = 0
# [x == 13, x == 11]
