#!/usr/bin/python

"""
Element speller.

Input a word (or words) and see it spelled with chemical elements!
"""

from __future__ import print_function
import itertools
import sys

class Element(object):
	def __init__(self, number, symbol, name):
		self.name = name
		self.number = number
		self.symbol = symbol

	def __repr__(self):
		return '({0}, {1}, {2})'.format(self.number, self.symbol, self.name)

	def __str__(self):
		return '({0}, {1}, {2})'.format(self.number, self.symbol, self.name)


def generate_combinations(sum_):
	combinations = []

	combo = [1 for i in range(sum_)]

	combinations.append(list(combo))

	while combo.count(1) > 1:
		combo.remove(1)
		combo.remove(1)
		combo.append(2)

		combinations.append(list(combo))

	return combinations


def generate_permutations(values):
	permutations = []

	for permutation in itertools.permutations(values):
		if permutation not in permutations:
			permutations.append(permutation)

	return permutations


def get_possible_solutions(target):
	length = len(target)

	permutations = []

	combinations = generate_combinations(length)

	for combination in combinations:
		permutations.extend(generate_permutations(combination))

	return permutations


def main(target):
	raw_elements = read_elements()

	elements = {element.symbol.lower(): element for element in raw_elements}

	spell(target.lower(), elements)


def output(elements):
	for element in elements:
		print('{:<2}  '.format(element.symbol), end='')

	print()

	for element in elements:
		print('{:<3} '.format(element.number), end='')

	print()

	for element in elements:
		print('----', end='')

	print()

	max_length = max([len(element.name) for element in elements])

	for i in range(max_length):
		for element in elements:
			if len(element.name) > i:
				print(element.name[i] + '   ', end='')
			else:
				print('    ', end='')

		print()


def read_elements():
	elements = []

	with open('elements.tsv') as f:
		for row in f.readlines():
			values = row.split()

			elements.append(Element(values[0], values[1], values[2]))

	return elements


def spell(target, elements):
	chosen_elements = []

	solutions = []
	possible_solutions = get_possible_solutions(target)

	for possible_solution in possible_solutions:
		chosen_elements = []
		start = 0

		try:
			for group in possible_solution:
				end = start + group

				attempt = target[start:end]

				chosen_elements.append(elements[attempt])

				start = end
		except LookupError as e:
			pass
		else:
			solutions.append(chosen_elements)

	if not solutions:
		print('No solutions possible. Sorry.')
	elif len(solutions) == 1:
		output(solutions[0])
	else:
		for i, solution in enumerate(solutions):
			if i > 0:
				print('==============================')

			output(solution)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Requires an argument. Pass the word to spell.')
		sys.exit()

	main(sys.argv[1])