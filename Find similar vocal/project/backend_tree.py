# implemented by Kaze

from typing import List
from wavefile import WaveFile

class Data:
	def __init__(self, raw_data: WaveFile):
		self.dimension = len(raw_data.features)
		self.content = raw_data.features
		self.location = raw_data.location
	
	def __eq__(self, other):
		if self.dimension != other.dimension: return False
		for i in range(self.dimension):
			if self.content[i] != other.content[i]: return False
		return True
	
	def get_key(self, layer_id: int) -> list:
		key = []
		for i in range(self.dimension):
			new_index = (layer_id + i) % self.dimension
			key.append(self.content[new_index])
		return key

def compare_data(data1: Data, data2: Data, layer_id: int) -> int:
	assert (data1.dimension == data2.dimension)

	for i in range(data1.dimension):
		new_index = (layer_id + i) % data1.dimension
		if data1.content[new_index] < data2.content[new_index]: return -1
		if data1.content[new_index] > data2.content[new_index]: return +1
	return 0

def distance(data1: Data, data2: Data, metric: int = 2):
	assert (data1.dimension == data2.dimension)

	result = 0
	for i in range(data1.dimension):
		result += abs(data1.content[i] - data2.content[i]) ** metric
	return result

def raw_distance(data1: List, data2: List, metric: int = 2):
	assert (len(data1) == len(data2))

	result, length = 0, len(data1)
	for i in range(length):
		result += abs(data1[i] - data2[i]) ** metric
	return result

def distance_to_slice(data: Data, cut_layer: tuple, metric: int = 2):
	assert(0 <= cut_layer[0] < data.dimension)
	
	return abs(data.content[cut_layer[0]] - cut_layer[1]) ** metric

class KDNode:
	def __init__(self, data: Data, left_child = None, right_child = None, layer_id: int = 0):
		self.data: Data = data
		self.left: KDNode = left_child
		self.right: KDNode = right_child
		self.cut_layer: tuple = (layer_id % data.dimension, data.content[layer_id % data.dimension])

class KDTree:
	def __init__(self, data_list: List[WaveFile]):
		assert (len(data_list) > 0)
		lengths = [len(x.features) for x in data_list]
		assert (min(lengths) == max(lengths))

		refined_list = [Data(x) for x in data_list]

		self.dimension: int = lengths[0]
		self.root: KDNode = self.build_tree(refined_list)
	
	def build_tree(self, data_list: List[Data], layer_id: int=0) -> KDNode:
		data_list.sort(key = lambda x: x.get_key(layer_id))

		# print('Building with layer {} for list {}'.format(layer_id, [x.content for x in data_list]))
		if len(data_list) == 0:
			# print('Result node: data = {}, cut = {}, left = {}, right = {}'.format(None, None, None, None))
			return None

		median_index = len(data_list) // 2

		node = KDNode(data = data_list[median_index],
						left_child = self.build_tree(data_list[:median_index], layer_id+1), 
						right_child = self.build_tree(data_list[median_index+1:], layer_id+1), 
						layer_id = layer_id)
		# print('Result node: data = {}, cut = {}, left = {}, right = {}'.format(node.data.content, node.cut_slice, node.left, node.right))
		return node
	
	def search(self, data: WaveFile, tolerance: float = 0.0):
		data = Data(data)
		assert (data.dimension == self.dimension)

		current_best = [None, float("inf")]
	
		def traverse(data: Data, node: KDNode):
			if node is None: return
			# print('Accessing node with data {} and children: {}-{}, target: {}'.format(node.data.content, node.left, node.right, data.content))

			direction = compare_data(data, node.data, node.cut_layer[0])

			current_dist = distance(data, node.data)

			if current_dist < current_best[1]:
				current_best[0] = node
				current_best[1] = current_dist
			
			if current_best[1] == 0: return

			if direction < 0:
				traverse(data, node.left)
				if distance_to_slice(data, node.cut_layer) < (1.0 - tolerance) * current_best[1]:
					traverse(data, node.right)
			else:
				traverse(data, node.right)
				if distance_to_slice(data, node.cut_layer) < (1.0 - tolerance) * current_best[1]:
					traverse(data, node.left)

		traverse(data, self.root)
		return current_best
	
	def k_search(self, data: WaveFile, k: int = 3, tolerance: float = 0.0):
		data = Data(data)
		assert (data.dimension == self.dimension)

		bests = [[None, float("inf")]]
	
		def traverse(data: Data, node: KDNode):
			if node is None: return
			# print('Accessing node with data {} and children: {}-{}, target: {}'.format(node.data.content, node.left, node.right, data.content))

			direction = compare_data(data, node.data, node.cut_layer[0])

			current_dist = distance(data, node.data)

			for index in range(len(bests)):
				if current_dist < bests[index][1]:
					bests.insert(index, [node, current_dist])
					break
			else: bests.append([node, current_dist])

			while len(bests) > k: bests.pop()

			if direction < 0:
				traverse(data, node.left)
				if distance_to_slice(data, node.cut_layer) < (1.0 - tolerance) * bests[-1][1]:
					traverse(data, node.right)
			else:
				traverse(data, node.right)
				if distance_to_slice(data, node.cut_layer) < (1.0 - tolerance) * bests[-1][1]:
					traverse(data, node.left)

		traverse(data, self.root)
		return bests