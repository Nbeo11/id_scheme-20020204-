import random
from math import gcd

from math_mod import *
from identification_scheme import *


class GuillouQuisquaterProver(Prover):
	def __init__(self, info):
		super().__init__(info)

	def _create_private_key(self, id_scheme):
		# u = input_number("A: Input `u` = ", lambda _u: gcd(_u, id_scheme.n) == 1)
		while True:
			u = random.randint(0, id_scheme.n - 1)
			if gcd(u, id_scheme.n) == 1:
				break

		print("A: u =", u)
		return u

	def _create_public_key(self, id_scheme):
		u = self._get_private_key()
		return pow_mod(inverse_mod(u, id_scheme.n), id_scheme.b, id_scheme.n)

	def create_gamma(self, id_scheme, k):
		return pow_mod(k, id_scheme.b, id_scheme.n)

	def create_y(self, id_scheme, c, k):
		u = self._get_private_key()
		return mul_mod(k, pow_mod(u, c, id_scheme.n), id_scheme.n)


class GuillouQuisquater:
	def __init__(self, prover_info):
		self.__p, self.__q = generate_primes(30, 2)
		self.n = self.__p * self.__q
		self.b = generate_primes(13, 1)[0]  # ~2^40

		print("p =", self.__p)
		print("q =", self.__q)
		print("n =", self.n)
		print("b =", self.b)

		self.trusted_authority = TrustedAuthority()
		self.prover = GuillouQuisquaterProver(prover_info)
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

		k = random.randint(0, self.n - 1)  # input_number("\tA: Input `k` = ")
		print("A: k =", k)

		gamma = self.prover.create_gamma(self, k)
		c = self.verifier_generate_c()
		y = self.prover.create_y(self, c, k)
		print("A: x =", gamma)
		print("B: c =", c)
		print("A: y =", y)
		return self.verifier_check_value(gamma, v, c, y)

	def verifier_generate_c(self):
		return random.randint(1, self.b - 1)

	def verifier_check_value(self, gamma, v, c, y):
		return gamma % self.n == mul_mod(
			pow_mod(y, self.b, self.n),
			pow_mod(v, c, self.n),
			self.n
		)


if __name__ == '__main__':
	scheme = GuillouQuisquater("yourname")
