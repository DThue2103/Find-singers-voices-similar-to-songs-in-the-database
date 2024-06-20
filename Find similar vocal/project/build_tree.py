import pickle
from backend_tree import KDTree

# get wavefiles from file with pickle

with open('list_wavefile.obj', 'rb') as input:
    wavefiles = pickle.load(input)
    for item in wavefiles: print('{} {}'.format(item.features, item.location))

    tree = KDTree(wavefiles)

    with open('premade_tree.obj', 'wb') as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)

    for item in wavefiles:
        output_list = tree.k_search(item)
        print('+++++++++++++++++++++++++++')
        print(item.location)
        for candidate in output_list:
            if candidate[0] is not None: print(candidate[0].data.location, item.location == candidate[0].data.location)

        print('---------------------------')