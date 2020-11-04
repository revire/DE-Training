import os
import logging
logging.basicConfig(level=logging.INFO)



DIRECTORY = 'out'


if __name__ == '__main__':
    logging.info('Running container')
    print("Working directory: {}".format(os.getcwd()))
    print(os.listdir())
    print('hello hello')
    # with open(os.path.join(DIRECTORY, 'test.txt'), 'w') as output_file:
    #     output_file.write('is anybody home?')

    with open(os.path.join(DIRECTORY, 'test.txt'), 'w') as output_file:
        output_file.write('is anybody home?')
    print(os.listdir())
    print('Done')

