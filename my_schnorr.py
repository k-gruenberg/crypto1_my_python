"""
The Schnorr signature scheme, based on Elliptic Curves.

Example:

sage: load("/Users/kendrick/Documents/SS2022/Kryptologie_1_CRYPTO1/Python_Ueb_mit_meinen_Kommentaren/crypto1_my_python/my_schnorr.py")                                               
                                                                                                                                                                               
sage: alice_private_key_dA, alice_public_key_PA = my_schnorr_generate_key_pair()                                                                                                     
                                                                                                                                                                               
sage: alice_private_key_dA, alice_public_key_PA                                                                                                                                      
(100, (11 : 18 : 1))
                                                                                                                                                                               
sage: message_m = 10                                                                                                                                                                 
                                                                                                                                                                            
sage: signature_r, signature_s = my_schnorr_sign(alice_private_key_dA, message_m)                                                                                                    
Signing [1]: Q = (x_Q, y_Q) = (8, 16) = k * G = 8 * (6 : 7 : 1) (k random, G public)
Signing [2]: r = hash((message_m, x_Q)) % order_n = hash((10, 8)) % 13 = 5680612697361088710 % 13 = 2
Signing [3]: s = k - r*dA % order_n = (8 - 2 * 100) % 13 = (8 - 200) % 13 = 3
Computed signature as (r, s) = (2, 3)

sage: my_schnorr_verify_signature(alice_public_key_PA, message_m, (signature_r, signature_s))                                                                                        
Verifying signature (r, s) = (2, 3)...
Computed point Q_ = (x_Q_, y_Q_) = (8, 16) = s*G + r*PA = 3 * (6 : 7 : 1) + 2 * (11 : 18 : 1) = (0 : 9 : 1) + (8 : 3 : 1)
Verifying whether r == hash((message_m, x_Q_)) % order_n, i.e. whether 2 == hash((10, 8)) % 13, i.e. whether 2 == 5680612697361088710 % 13:
True

sage: my_schnorr_verify_signature(alice_public_key_PA, 11, (signature_r, signature_s))                                                                                               
Verifying signature (r, s) = (2, 3)...
Computed point Q_ = (x_Q_, y_Q_) = (8, 16) = s*G + r*PA = 3 * (6 : 7 : 1) + 2 * (11 : 18 : 1) = (0 : 9 : 1) + (8 : 3 : 1)
Verifying whether r == hash((message_m, x_Q_)) % order_n, i.e. whether 2 == hash((11, 8)) % 13, i.e. whether 2 == -2915982724384074854 % 13:
False

sage: my_schnorr_verify_signature(alice_public_key_PA, message_m, (signature_r+1, signature_s))                                                                                      
Verifying signature (r, s) = (3, 3)...
Computed point Q_ = (x_Q_, y_Q_) = (11, 1) = s*G + r*PA = 3 * (6 : 7 : 1) + 3 * (11 : 18 : 1) = (0 : 9 : 1) + (6 : 7 : 1)
Verifying whether r == hash((message_m, x_Q_)) % order_n, i.e. whether 3 == hash((10, 11)) % 13, i.e. whether 3 == 2402105395517694403 % 13:
False

sage: my_schnorr_verify_signature(alice_public_key_PA, message_m, (signature_r, signature_s+1))                                                                                      
Verifying signature (r, s) = (2, 4)...
Computed point Q_ = (x_Q_, y_Q_) = (11, 18) = s*G + r*PA = 4 * (6 : 7 : 1) + 2 * (11 : 18 : 1) = (11 : 1 : 1) + (8 : 3 : 1)
Verifying whether r == hash((message_m, x_Q_)) % order_n, i.e. whether 2 == hash((10, 11)) % 13, i.e. whether 2 == 2402105395517694403 % 13:
False
"""


DEFAULT_EC = EllipticCurve(GF(19), [3,5])
DEFAULT_G = DEFAULT_EC(6, 7, 1)  # order = 13 (which is prime!)


def my_schnorr_generate_key_pair(public_point_G = DEFAULT_G, alice_private_key_dA = None):  # works exactly the same way as in Elgamal scheme
	if alice_private_key_dA is None: alice_private_key_dA = ZZ(Zmod(1000).random_element())  # dA
	alice_public_key_PA = alice_private_key_dA * public_point_G  # PA = dA * G
	return alice_private_key_dA, alice_public_key_PA


def my_schnorr_sign(alice_private_key_dA, message_m, public_point_G = DEFAULT_G, order_n = None, random_k = None):
	if order_n is None: order_n = public_point_G.order()
	
	# [1]: Wähle zufällig k aus [1, n-1] und berechne den temporären/Ephemeral-Schlüssel Q = k*G = (x_Q, y_Q)
	if random_k is None: random_k = 1 + ZZ(Zmod(order_n-1).random_element())
	point_Q = random_k * public_point_G
	x_Q, y_Q = point_Q.xy()  # temporärer/Ephemeral-Schlüssel
	print(f"Signing [1]: Q = (x_Q, y_Q) = ({x_Q}, {y_Q}) = k * G = {random_k} * {public_point_G} (k random, G public)")
	
	# [2]: r = Hash(m || x_Q) mod n
	r = hash((message_m, x_Q)) % order_n
	print(f"Signing [2]: r = hash((message_m, x_Q)) % order_n = hash(({message_m}, {x_Q})) % {order_n} = {hash((message_m, x_Q))} % {order_n} = {r}")

	# [3]: s = k - r*dA mod n
	s = (random_k - r*alice_private_key_dA) % order_n
	print(f"Signing [3]: s = k - r*dA % order_n = ({random_k} - {r} * {alice_private_key_dA}) % {order_n} = ({random_k} - {r*alice_private_key_dA}) % {order_n} = {s}")

	# Return Alice's signature:
	print(f"Computed signature as (r, s) = ({r}, {s})")
	return r, s


def my_schnorr_verify_signature(alice_public_key_PA, message_m, signature, public_point_G = DEFAULT_G, order_n = None):
	if order_n is None: order_n = public_point_G.order()

	r, s = signature
	print(f"Verifying signature (r, s) = ({r}, {s})...")
	point_Q_ = s * public_point_G + r * alice_public_key_PA  # Q_ = s*G + r*PA = (s + r*dA) * G = k*G
	x_Q_, y_Q_ = point_Q_.xy()
	print(f"Computed point Q_ = (x_Q_, y_Q_) = ({x_Q_}, {y_Q_}) = s*G + r*PA = {s} * {public_point_G} + {r} * {alice_public_key_PA} = {s * public_point_G} + {r * alice_public_key_PA}")
	print(f"Verifying whether r == hash((message_m, x_Q_)) % order_n, i.e. whether {r} == hash(({message_m}, {x_Q_})) % {order_n}, i.e. whether {r} == {hash((message_m, x_Q_))} % {order_n}:")
	return r == hash((message_m, x_Q_)) % order_n
