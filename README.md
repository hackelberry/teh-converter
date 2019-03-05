    usage: teh-converter.py [-h] [-s STRATEGY] input output

    Converts midi files to our format.

    positional arguments:
    input                 input midi file
    output                output C source file

    optional arguments:
    -h, --help            show this help message and exit
    -s STRATEGY, --strategy STRATEGY
                            strategy to use when encountering unplayable notes

    Examples:
        python teh-converter.py input.midi notes.h
        python teh-converter.py input.midi notes.h --strategy closest