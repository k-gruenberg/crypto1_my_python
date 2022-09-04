"""
The Elgamal asymmetric encryption scheme, based on Elliptic Curves.

Example:

sage: load("/Users/kendrick/Documents/SS2022/Kryptologie_1_CRYPTO1/Python_Ueb_mit_meinen_Kommentaren/crypto1_my_python/my_elgamal.py")                                               
                                                                                                                                                                             
sage: alice_private_key_tA, alice_public_key_A = my_elgamal_generate_key_pair()                                                                                                      
                                                                                                                                                                              
sage: alice_private_key_tA, alice_public_key_A                                                                                                                                       
(862, (11 : 1 : 1))
                                                                                                                                                                              
sage: DEFAULT_G                                                                                                                                                                      
(6 : 7 : 1)

sage: alice_private_key_tA * DEFAULT_G                                                                                                                                               
(11 : 1 : 1)
                                                                                                                                                                        
sage: DEFAULT_EC.points()                                                                                                                                                            
[(0 : 1 : 0), (0 : 9 : 1), (0 : 10 : 1), (1 : 3 : 1), (1 : 16 : 1), (2 : 0 : 1), (4 : 9 : 1), (4 : 10 : 1), (6 : 7 : 1), (6 : 12 : 1), (8 : 3 : 1), (8 : 16 : 1), (9 : 1 : 1), (9 : 18 : 1), (10 : 3 : 1), (10 : 16 : 1), (11 : 1 : 1), (11 : 18 : 1), (14 : 6 : 1), (14 : 13 : 1), (15 : 9 : 1), (15 : 10 : 1), (16 : 8 : 1), (16 : 11 : 1), (18 : 1 : 1), (18 : 18 : 1)]                                                                                                                                                                               

sage: my_elgamal_encrypt(alice_public_key_A, DEFAULT_EC(14, 13, 1))                                                                                                                  
Chose r=2, returning ciphertext (r*G, N+r*A) = (2 * (6 : 7 : 1), (14 : 13 : 1) + 2 * (11 : 1 : 1)):
((18 : 1 : 1), (2 : 0 : 1))
                                                                                                                                                                               
sage: my_elgamal_decrypt(alice_private_key_tA, (DEFAULT_EC(18, 1, 1), DEFAULT_EC(2, 0, 1)))                                                                                          
Decrypting (r*G, N+r*A) = ((18 : 1 : 1), (2 : 0 : 1)) as N = (N+r*A) - t_A * (r*G) = (2 : 0 : 1) - 862 * (18 : 1 : 1) = (14 : 13 : 1).
(14 : 13 : 1)
"""


#DEFAULT_EC = EllipticCurve(GF(17), [0,-1])
#DEFAULT_G = DEFAULT_EC(7, 6, 1)  # order = 18 (Achtung!!!: Eigentlich sollte die Ordnung prim sein, wegen SPH !!!!!)
# Beispiel mit Prim-Ordnung wäre z.B.:
DEFAULT_EC = EllipticCurve(GF(19), [3,5])
DEFAULT_G = DEFAULT_EC(6, 7, 1)  # order = 13 (which is prime!)


def my_elgamal_generate_key_pair(public_point_G = DEFAULT_G, alice_private_key_tA = None):
	if alice_private_key_tA is None: alice_private_key_tA = ZZ(Zmod(1000).random_element())
	alice_public_key_A = alice_private_key_tA * public_point_G
	return alice_private_key_tA, alice_public_key_A


def my_elgamal_encrypt(alice_public_key_A, bobs_message_N, public_point_G = DEFAULT_G, order_q = None, r = None):
	if order_q is None: order_q = public_point_G.order()  # ord(G) = q
	if r is None: r = 2 + ZZ(Zmod(order_q-3).random_element())  # a random number r with 2 <= r <= q-2

	print(f"Chose r={r}, returning ciphertext (r*G, N+r*A) = ({r} * {public_point_G}, {bobs_message_N} + {r} * {alice_public_key_A}):")
	return r * public_point_G, bobs_message_N + r * alice_public_key_A  # (r*G, N+r*A)


def my_elgamal_decrypt(alice_private_key_tA, bobs_encrypted_message):
	r_times_G, N_plus_r_times_A = bobs_encrypted_message
	print(f"Decrypting (r*G, N+r*A) = ({r_times_G}, {N_plus_r_times_A}) as N = (N+r*A) - t_A * (r*G) = {N_plus_r_times_A} - {alice_private_key_tA} * {r_times_G} = {N_plus_r_times_A - alice_private_key_tA * r_times_G}.")
	return N_plus_r_times_A - alice_private_key_tA * r_times_G
