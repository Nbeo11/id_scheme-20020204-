import random

from math_mod import *
from identification_scheme import *


class FeigeFiatShamirProver(Prover):
	def __init__(self, info):
		super().__init__(info)

	def _create_private_key(self, id_scheme):
		# s = input_number_array(id_scheme.k, "A: Input `s` = ")
		s = tuple(random_array(id_scheme.k, 1, id_scheme.n - 1, True))
		print("A: s =", s)
		return s

	def _create_public_key(self, id_scheme, b):
		s = self._get_private_key()
		return tuple(
			mul_mod(1 if b[i] == 0 else -1, inverse_mod(s[i] ** 2, id_scheme.n), id_scheme.n)
			for i in range(id_scheme.k)
		)

	def create_gamma(self, id_scheme, r, b):
		return mul_mod(1 if b == 0 else -1, r ** 2, id_scheme.n)

	def create_y(self, id_scheme, c, r, *_):
		s = self._get_private_key()
		result = r
		for i in range(id_scheme.k):
			result = mul_mod(result, 1 if c[i] == 0 else s[i], id_scheme.n)

		return result


class FeigeFiatShamir:
	def __init__(self, prover_info, query_number=1):
		while True:
			p, q = generate_primes(30, 2)
			if p % 4 == 3 and q % 4 == 3:
				break

		self.__p, self.__q = p, q
		self.n = self.__p * self.__q
		self.k = random.randint(1, 5)

		print("p =", self.__p)
		print("q =", self.__q)
		print("n =", self.n)
		print("k =", self.k)

		self.trusted_authority = TrustedAuthority()
		self.prover = FeigeFiatShamirProver(prover_info)
		# b = input_number_array(self.k, "A: Input `b` = ")
		b = tuple(random_array(self.k, 0, 1))
		print("A: b =", b)
		self.prover.set_private_key_from_arguments(self)
		self.prover.set_public_key_from_arguments(self, b)
		self.prover.set_certificate_from_trusted_authority(self.trusted_authority)
		print(self.do_verify())

	def do_verify(self, query_number=1) -> bool:
		cert_a = self.prover.get_certificate()
		v = self.prover.get_public_key()
		print("A: v =", v)

		if not self.trusted_authority.verify_certificate(cert_a):
			return False

		query_id = 0
		while query_id < query_number:
			query_id += 1
			print("query #{}".format(query_id))

			r = random.randint(1, self.n - 1)  # input_number("\tA: Input `r` = ")
			b = random.randint(0, 1)  # input_number("\tA: Input `b` = ")
			print("A: r =", r)
			print("A: b =", b)

			gamma = self.prover.create_gamma(self, r, b)
			c = self.verifier_generate_c()
			y = self.prover.create_y(self, c, r)
			print("A: x =", gamma)
			print("B: c =", c)
			print("A: y =", y)
			if not self.verifier_check_value(gamma, v, c, y):
				return False

		return True

	def verifier_generate_c(self):
		return tuple(random_array(self.k, 0, 1))

	def verifier_check_value(self, gamma, v, c, y):
		z = y ** 2
		for i in range(self.k):
			z = mul_mod(z, 1 if c[i] == 0 else v[i], self.n)

		return z != 0 and (gamma % self.n == z or (gamma + z) % self.n == 0)


if __name__ == '__main__':
	scheme = FeigeFiatShamir("yourname")
