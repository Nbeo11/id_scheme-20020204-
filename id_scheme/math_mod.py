import requests

big_primes_headers = {
	"authority": "big-primes.ue.r.appspot.com",
	"accept": "application/json, text/javascript, */*; q=0.01",
	"accept-language": "en-US,en;q=0.9,vi;q=0.8,ja;q=0.7",
	"dnt": "1",
	"origin": "https://bigprimes.org",
	"referer": "https://bigprimes.org/",
	"sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": '"Windows"',
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "cross-site",
	"sec-gpc": "1",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}


def generate_primes(digits, nums):
	response_json = requests.get(
		"https://big-primes.ue.r.appspot.com/primes",
		params={"digits": str(digits), "numPrimes": str(nums)},
		headers=big_primes_headers
	).json()
	return [*map(int, response_json["Primes"])]


def get_prime_factors(n):
	cookies = {
		'PHPSESSID': '9945aa5a23bcf95d146edc73694e7213',
		'SL_G_WPT_TO': 'vi',
		'SL_GWPT_Show_Hide_tmp': '1',
		'SL_wptGlobTipTmp': '1',
	}
	headers = {
		'authority': 'www.dcode.fr',
		'accept': 'application/json, text/javascript, */*; q=0.01',
		'accept-language': 'en-US,en;q=0.9,vi;q=0.8,ja;q=0.7',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'dnt': '1',
		'origin': 'https://www.dcode.fr',
		'referer': 'https://www.dcode.fr/prime-factors-decomposition',
		'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'sec-gpc': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
		'x-requested-with': 'XMLHttpRequest',
	}
	data = {
		'tool': 'prime-factors-decomposition',
		'number': str(n),
	}

	response_json = requests.post('https://www.dcode.fr/api/', cookies=cookies, headers=headers, data=data).json()
	return [
		int(u[:u.find("<sup>") if u.find("<sup>") != -1 else None])
		for u in response_json["results"].split(" × ")
	]


def get_primitive_root(n, lower_bound=1):
	alpha = 2
	p_list = get_prime_factors(n - 1)
	while True:
		if alpha >= lower_bound and all(pow_mod(alpha, (n - 1) // pi, n) != 1 for pi in p_list):
			return alpha

		alpha = generate_primes(len(str(n)) - 1, 1)[0]


def mul_mod(a, b, mod):
	a %= mod
	b %= mod
	return (a * b) % mod


def pow_mod(base, pwr, mod):
	if pwr < 0:
		return pow_mod(inverse_mod(base, mod), -pwr, mod)

	res = 1
	t = base % mod
	while pwr > 0:
		if pwr & 1:
			res = (res * t) % mod

		t = (t * t) % mod
		pwr >>= 1

	return res


def extended_euclide(a, b):
	if b == 0:
		return a, 0, 1

	x1, x2, y1, y2 = 0, 1, 1, 0
	while b > 0:
		q, r = divmod(a, b)
		a, b = b, r
		x1, x2 = x2 - q * x1, x1
		y1, y2 = y2 - q * y1, y1

	return a, x2, y2


def inverse_mod(x, mod):
	g, _, y = extended_euclide(mod, x)
	return y if g == 1 else None


def str_to_base26(s, mod=None):
	res = 0
	for c in s:
		ord_c = ord(c.upper()) - 65
		if 0 <= ord_c < 26:
			res = res * 26 + ord_c

		if mod is not None:
			res %= mod

	return res
