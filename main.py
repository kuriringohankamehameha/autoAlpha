#!/usr/bin/env python

import autoalpha

#Main Program
def main():
	price_volume_data = ['open', 'close', 'high', 'low', 'vwap', 'volume', 'returns', 'adv20', 'sharesout', 'cap', 'split', 'dividend', 'market', 'country', 'exchange', 'sector', 'industry', 'subindustry']
	alpha_instance = autoalpha.AlphaGenerator("Chrome", "cache.txt")
	alpha_instance.setupDrivers()
	alpha_instance.assign_values_to_param_set(price_volume_data)
	alpha_instance.simulate_alphas()
	alpha_instance.close_object("cache.txt")

if __name__ == '__main__':
	main()