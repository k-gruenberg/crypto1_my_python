def xgcd3(a, b, c):
	gcd1, u_, v_ = xgcd(a,b)
	gcd2, k, w = xgcd(gcd1, c)
	gcd2, u, v, w = gcd2, k*u_, k*v_, w
	assert(gcd2 == gcd(a, gcd(b, c)) and gcd2 == u*a + v*b + w*c)
	return gcd2, u, v, w
