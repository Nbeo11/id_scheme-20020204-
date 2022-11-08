import random

from math_mod import *
from identification_scheme import *


class OkamotoProver(Prover):
	def __init__(self, info):
		super().__init__(info)

	def _create_private_key(self, id_scheme):
		a1 = random.randint(0, id_scheme.q - 1)  # input_number("\tA: Input `a1` = ")
		a2 = random.randint(0, id_scheme.q - 1)  # input_number("\tA: Input `a2` = ")
		print("A: a1 =", a1)
		print("A: a2 =", a2)
		return a1, a2

	def _create_public_key(self, id_scheme):
		a1, a2 = self._get_private_key()
		return mul_mod(
			pow_mod(id_scheme.alpha1, -a1, id_scheme.p),
			pow_mod(id_scheme.alpha2, -a2, id_scheme.p),
			id_scheme.p
		)

	def create_gamma(self, id_scheme, k1, k2):
		return mul_mod(
			pow_mod(id_scheme.alpha1, k1, id_scheme.p),
			pow_mod(id_scheme.alpha2, k2, id_scheme.p),
			id_scheme.p
		)

	def create_y(self, id_scheme, c, k1, k2):
		a1, a2 = self._get_private_key()
		return ((k1 + a1 * c) % id_scheme.q, (k2 + a2 * c) % id_scheme.q)


class Okamoto:
	def __init__(self, prover_info):
		self.p = generate_primes(30, 1)[0]
		p1_prime_fact = get_prime_factors(self.p - 1)
		self.q = p1_prime_fact[-1]
		self.t = random.randint(1, self.q.bit_length() - 1)
		p_primitive_root1 = get_primitive_root(self.p)
		min2 = random.randint(p_primitive_root1+1, self.p-1)
		p_primitive_root2 = get_primitive_root(self.p, min2)
		self.alpha1 = pow_mod(p_primitive_root1, (self.p-1) // self.q, self.p)
		self.alpha2 = pow_mod(p_primitive_root2, (self.p-1) // self.q, self.p)

		print("p =", self.p)
		print("q =", self.q)
		print("t =", self.t)
		print("alpha1 =", self.alpha1)
		print("alpha2 =", self.alpha2)

		self.trusted_authority = TrustedAuthority()
		self.prover = OkamotoProver(prover_info)
		self.prover.set_private_key_from_arguments(self)
		self.prover.set_public_key_from_arguments(self)
		self.prover.set_certificate_from_trusted_authority(self.trusted_authority)
		print(self.do_verify())

	def do_verify(self) -> bool:
		cert_a = self.prover.get_certificate()
		v = self.prover.get_public_key()
		print("A: v =", v)

		if not self.trusted_authority.verify_certificate(cert_a):
			return False

		k1 = random.randint(0, self.q - 1)  # input_number("\tA: Input `k1` = ")
		k2 = random.randint(0, self.q - 1)  # input_number("\tA: Input `k2` = ")
		print("A: k1 =", k1)
		print("A: k2 =", k2)

		gamma = self.prover.create_gamma(self, k1, k2)
		c = self.verifier_generate_c()
		y = self.prover.create_y(self, c, k1, k2)
		print("A: x =", gamma)
		print("B: c =", c)
		print("A: y =", y)
		return self.verifier_check_value(gamma, v, c, y)

	def verifier_generate_c(self):
		return random.randint(1, (1 << self.t))

	def verifier_check_value(self, gamma, v, c, y):
		y1, y2 = y
		temp = mul_mod(
			pow_mod(self.alpha1, y1, self.p),
			pow_mod(self.alpha2, y2, self.p),
			self.p
		)
		return gamma % self.p == mul_mod(
			temp,
			pow_mod(v, c, self.p),
			self.p
		)


if __name__ == '__main__':
	scheme = Okamoto("yourname")
