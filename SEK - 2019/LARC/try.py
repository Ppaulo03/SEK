import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('sample.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))

logger.addHandler(file_handler)

def add(x,y):
    return x+y

def subtract(x,y):
    return x-y

def mutiply(x,y):
    return x*y

def division(x,y):
    return x/y

num1 = 10
num2 = 5

add_result = add(num1,num2)
logger.debug('Add: {} + {} = {}'.format(num1,num2,add_result))

sub_result = subtract(num1,num2)
logger.debug('Sub: {} - {} = {}'.format(num1,num2,sub_result))

mut_result = mutiply(num1,num2)
logger.debug('Mut: {} * {} = {}'.format(num1,num2,mut_result))

divid_result = division(num1,num2)
logger.debug('Div: {} / {} = {}'.format(num1,num2,divid_result))
