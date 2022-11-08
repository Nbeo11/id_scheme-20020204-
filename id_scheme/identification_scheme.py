import random


def input_number(prompt="", check_num_func=None):
	while True:
		try:
			x = int(input(prompt))
			if check_num_func is None or check_num_func(x):
				return x
		except ValueError:
			continue


def input_number_array(array_length, prompt=""):
	result = []
	while len(result) < array_length:
		try:
			result += [*map(int, input(prompt).split())]
		except ValueError:
			continue

	return result[:array_length]


def random_array(array_length: int, min_val: int, max_val: int, is_unique=False):
	result = []
	while len(result) < array_length:
		next_value = random.randint(min_val, max_val)
		result.append(next_value)

	return result


class TrustedAuthority:
	def __init__(self):
		pass

	def hash_data(self, identity, public_key):
		return hash((identity, public_key))

	def _sign(self, identity, public_key):
		return hash(identity) + hash(public_key)

	def create_certificate(self, identify, public_key):
		signature = self._sign(identify, public_key)
		return identify, public_key, signature

	def verify_certificate(self, certificate) -> bool:
		identity, public_key, signature = certificate
		return True


class Prover:
	def __init__(self, info):
		self.__info = info
		self.__private_key = None
		self.__public_key = None
		self.__certificate = None

	def _get_private_key(self):
		return self.__private_key

	def set_private_key_from_arguments(self, id_scheme):
		self.__private_key = self._create_private_key(id_scheme)

	def _create_private_key(self, id_scheme):
		pass

	def get_public_key(self):
		return self.__public_key

	def set_public_key_from_arguments(self, id_scheme, *args):
		self.__public_key = self._create_public_key(id_scheme, *args)

	def _create_public_key(self, id_scheme, *args):
		pass

	def create_gamma(self, id_scheme, *args):
		pass

	def create_y(self, id_scheme, c, *args):
		pass

	def get_certificate(self):
		return self.__certificate

	def set_certificate_from_trusted_authority(self, trusted_authority):
		self.__certificate = trusted_authority.create_certificate(repr(self.__info), self.__public_key)
