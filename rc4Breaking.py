import csv

# Known values

message = ''
key = ''

print('Message is -> ' + message + '\nKey is -> ' + key)
print('===============')

# Initialize frequency vector #

freqHistogram = []
for i in range(0, 255):
    freqHistogram.append(0)

# Guessing message #
with open('./messageFile.csv', mode='r') as file:
    fileReader = csv.DictReader(file)
    for row in fileReader:
        for mValue in range(0, 255):
            keyStream = mValue ^ int(row['Cypher'], 16)
            expectedValue = (int(row['IV'][-2:], 16) + 2) % 255
            if keyStream == expectedValue:
                freqHistogram[mValue] += 1

maxFreq = max(freqHistogram)
mesGuess = freqHistogram.index(maxFreq)
print('m[0]: ' + chr(mesGuess) + ' with freq. ' + str(maxFreq))
# print(str(chr(mesGuess) == message))  # If we know the message #
print('===============')

# Guessing key #

keyGuess = []
iv = 3  # Initial value of the first IV when guessing the key #
incrementX = 6  # Initial increment using the 'second fact: x + 6 + k[0]', it will increment when changing the IV #
kPos = 0

with open('./keyfile.csv', mode='r') as file:
    fileReader = csv.DictReader(file)
    for row in fileReader:
        if row['IV'] == ('X0'.join('{:02X}'.format(iv)) + 'FF00'):
            freqHistogram = []
            for i in range(0, 255):
                freqHistogram.append(0)

        for kValue in range(0, 255):
            keyStream = mesGuess ^ int(row['Cypher'], 16)
            expectedValue = (int(row['IV'][-2:], 16) + incrementX + kValue) % 255  # Second fact #
            if keyStream == expectedValue:
                freqHistogram[kValue] += 1

        if row['IV'] == ('X0'.join('{:02X}'.format(iv)) + 'FFFF'):
            maxFreq = max(freqHistogram)
            freq = sorted(freqHistogram, key=int, reverse=True)  # Try
            kGuess = freqHistogram.index(maxFreq)
            keyGuess.append(kGuess)
            print('k[' + str(kPos) + ']: 0x' + ''.join('{:02X}'.format(kGuess)) + ' with freq. ' + str(maxFreq))
            # print(str(kGuess == int(key[kPos * 2: kPos * 2 + 2], 16))) # If we know the key #

            iv += 1
            incrementX += iv + kGuess
            kPos += 1

# Final output #

print('===============')
keyRecovered = ''.join('{:02x}'.format(i) for i in keyGuess)
if key == '':
    print('Key guess: ' + keyRecovered)
elif key == keyRecovered:
    print('Key recovered: ' + key + '==' + keyRecovered)
else:
    print('Key can not be recovered: ' + key + '!=' + keyRecovered)
print('===============')
