import random

from math_mod import *
from identification_scheme import *


class SchnorrProver(Prover):
	def __init__(self, info):
		super().__init__(info)

	def _create_private_key(self, id_scheme):
		a = random.randint(0, id_scheme.q - 1)  # input_number("\tA: Input `a` = ")
		print("A: a =", a)
		return a

	def _create_public_key(self, id_scheme):
		a = self._get_private_key()
		return pow_mod(id_scheme.alpha, -a, id_scheme.p)

	def create_gamma(self, id_scheme, k):
		return pow_mod(id_scheme.alpha, k, id_scheme.p)

	def create_y(self, id_scheme, c, k):
		a = self._get_private_key()
		return (k + a * c) % id_scheme.q


class Schnorr:
	def __init__(self, prover_info):
		self.p = generate_primes(30, 1)[0]
		p1_prime_fact = get_prime_factors(self.p - 1)
		self.q = p1_prime_fact[-1]
		self.t = random.randint(1, self.q.bit_length() - 1)
		p_primitive_root = get_primitive_root(self.p)
		self.alpha = pow_mod(p_primitive_root, (self.p-1) // self.q, self.p)

		print("p =", self.p)
		print("q =", self.q)
		print("t =", self.t)
		print("alpha =", self.alpha)

		self.trusted_authority = TrustedAuthority()
		self.prover = SchnorrProver(prover_info)
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

		k = random.randint(0, self.q - 1)  # input_number("\tA: Input `k` = ")
		print("A: k =", k)
		gamma = self.prover.create_gamma(self, k)
		c = self.verifier_generate_c()
		y = self.prover.create_y(self, c, k)
		print("A: x =", gamma)
		print("B: c =", c)
		print("A: y =", y)
		return self.verifier_check_value(gamma, v, c, y)

	def verifier_generate_c(self):
		return random.randint(1, (1 << self.t))

	def verifier_check_value(self, gamma, v, c, y):
		return gamma % self.p == mul_mod(
			pow_mod(self.alpha, y, self.p),
			pow_mod(v, c, self.p),
			self.p
		)


if __name__ == '__main__':
	scheme = Schnorr("ngan")
