# Encoder-and-Decoder
This script works in 4 modes: 1) ** encode ** 2) ** decode ** 3) ** read ** 4) ** hack **

** 1) Encode **: Requires an input file / link (** - input_file, --input_url **) and an output file (** - output_file **), if there is no input or output - an exception is thrown.
You can specify the parameters: ** - cipher ** - ciphers of caesar, vigenere, vernam (caesar, vigenere, vernam). For shivrs of Caesar and Vigenère, the keys are required ** - key ** (number / string), for vernam the key is not specified, but the file ** - random_file ** is specified, in which the encoder text will be written. The language is also indicated ** - language (eng, rus) ** by default the language is English.

** 2) Decode **: Reverse operation to Encode, same arguments

** 3) Read **: Requires ** - output_file ** and ** - input_file / - input_url **. In this mode, the script reads the text and remembers the probabilities and words from the text. You can use the data.txt file to generate a file for cracking

** 4) Hack **: Hack. You need to specify ** - input_file --output_file, --AnalyzedDataFile ** - the last contains data on the frequencies of letters and words in normal text. Hacking determines the language of the text and breaks it by Caesar, then by the visionary (Coincidence indices). The best outcome is selected.

# Example of using commands:

** python3 encode.py encode --cipher = 'caesar' --key = '2' --output_file = 'f.out' **

** python3 encode.py read --input_file = 'f.in' --output_file = 'f.out' **

** python3 hack --AnalyzedDataFile = 'data.in' **

See the examples file for examples of results.


#Notes
If you do not specify a file for input and output, everything will be done via ** sys.stdin / sys.stdout **. The file encrypted with the Vigenère cipher will be compressed using ** pickle **, the data used for cracking is also compressed (** read ** mode)
All constants were taken from Wikipedia as recommended for normal texts (in English / Russian)
