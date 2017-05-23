import random

def triggered(pics):
    selection = random.randint(1,pics)
    return "/triggered/" + str(selection) + "g.*"
