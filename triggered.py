import random
import glob

def triggered(pics):
    selection = random.randint(1,pics)
    return glob.glob('triggered/' + str(selection) + 'g.*')[0]
