from collections import Counter

def read_and_filter_input_file(file_name):
    file = open(file_name, "r")
    normal_text = ''
    for c in file.read():
        if c == c.lower():
            c = c.upper()
        if 'A' <= c and c <= 'Z':
            normal_text += c
    file.close()
    return normal_text


def crypt_text(normal_text, key, output_file_name):
    global letter_to_number
    global number_to_letter
    cryptotext = ''
    m = len(key)
    for i in range(len(normal_text)):
        cryptotext += number_to_letter[(letter_to_number[normal_text[i]] + letter_to_number[key[i % m]]) % 26]

    output_file = open(output_file_name, "w")
    output_file.write(cryptotext)
    output_file.close()
    return cryptotext


def decrypt_text(cryptotext,  key, output_file_name):
    global letter_to_number
    global number_to_letter
    decryption = ''
    m = len(key)
    for i in range(len(cryptotext)):
        decryption += number_to_letter[(letter_to_number[cryptotext[i]] - letter_to_number[key[i % m]]) % 26]

    output_file = open(output_file_name,"w")
    output_file.write(decryption)
    output_file.close()
    return decryption


def IC(alpha):
    index = 0.0
    frequencies = Counter(alpha)
    length = len(alpha)
    for i in frequencies:
        index += (float(frequencies[i]) / length) * (float(frequencies[i] - 1) / (length - 1))
    return index


def compute_key_length(cryptotext):
    best_mean = 0
    best_key_length = 0
    best_ic_array = []
    key_length = 0
    tries = 0
    for i in range(1000):
        ic_array = list()
        key_length += 1
        tries += 1

        for j in range(key_length):
            ic_array.append(IC(cryptotext[j::key_length]))
        mean = sum(ic_array) / len(ic_array)

        if abs(mean - 0.065) < abs(best_mean - 0.065):
            tries = 0
            best_mean = mean
            best_key_length = key_length
            best_ic_array = ic_array

        #if key_length < 9:
        #    print([round(number, 4) for number in ic_array])

        if tries == 50:
            print('FINAL VALUES IN IC_ARRAY:', [round(i, 4) for i in best_ic_array])
            break

    return best_key_length

def SHIFT(text, offset):
    result = ''
    for c in text:
        if chr(ord(c) + offset) > 'Z':
            c = chr((ord(c) + offset) % (ord('Z') + 1) + ord('A'))
        else:
            c = chr(ord(c) + offset)
        result += c
    return result

def MIC_2b(beta):
    english_frequencies = {
    'A': 8.55,
    'K': 0.81,
    'U': 2.68,
    'B':  1.60,
    'L': 4.21,
    'V': 1.06,
    'C': 3.16,
    'M': 2.53,
    'W': 1.83,
    'D': 3.87,
    'N': 7.17,
    'X': 0.19,
    'E': 12.10,
    'O': 7.47,
    'Y': 1.72,
    'F': 2.18,
    'P': 2.07,
    'Z': 0.11,
    'G': 2.09,
    'Q': 0.10,
    'H': 4.96,
    'R': 6.33,
    'I': 7.33,
    'S': 6.73,
    'J': 0.22,
    'T': 8.94,
    }
    length_beta = len(beta)
    frequencies_beta = Counter(beta)
    result = 0.0
    for i in english_frequencies:
        result += english_frequencies[i] / 100 * (float(frequencies_beta[i])/ length_beta)
    return result

def compute_key(cryptotext,key_length):
    key=''
    for j in range(key_length):
        shift_offset = -1
        best_shift_offset = -1
        best_mic = 0
        while(shift_offset<26):
            shift_offset += 1
            mic = MIC_2b(SHIFT(cryptotext[j::key_length],shift_offset))
            if abs(0.065 - best_mic) > abs(0.065 - mic):
                best_mic = mic
                best_shift_offset = shift_offset
        c = chr((26 - best_shift_offset) % 26 + ord('A')) #+ord(A) to have it between A and Z
        print('key[',j,'] = ', c)
        key += c
    return key

def get_atomic_key(key):
    divisors = []
    key_length = len(key)
    for i in range(2, int(key_length / 2 + 1)):
        if key_length % i == 0:
            divisors.append(i)
    divisors.append(key_length)
    for d in divisors:
        if key[:d] * int(key_length / d) == key:
            return key[:d]

letter_to_number = {}
number_to_letter = {}

for i in range(26):
    letter_to_number[chr(ord('A') + i)] = i
    number_to_letter[i] = chr(ord('A') + i)

key = "AAAAAAABAAAAAAAA"

plain_text = read_and_filter_input_file('input.txt')
cryptotext = crypt_text(plain_text, key, 'encryption.txt')

key_length = compute_key_length(cryptotext)

print('KEY LENGTH: ', key_length)
found_key = compute_key(cryptotext,key_length)
print('KEY: ',found_key)
decrypt_text(cryptotext,found_key,'decryption.txt')
atomic_key = get_atomic_key(found_key)
print('ATOMIC KEY: ',atomic_key)
print('Press any key to exit...')
input()
