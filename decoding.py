def decode(message_file):
    with open(message_file, 'r') as file:
        lines = file.readlines()

    number_word_dict = {}
    for line in lines:
        number, word = line.split()
        number_word_dict[int(number)] = word

    max_number = max(number_word_dict.keys())

    def is_end_of_line(number, max_number):
        count = 0
        for i in range(1, max_number + 1):
            count += i
            if number == count:
                return True
        return False

    message_words = [number_word_dict[n] for n in sorted(number_word_dict) if is_end_of_line(n, max_number)]
    print(' '.join(message_words))

decode('test.txt')
