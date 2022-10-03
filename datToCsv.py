import os
import pandas as pd

### Convert .dat files to .csv files ###

files_to_convert = './first'
csv_dir = './csvFiles'

cd_files = sorted(os.listdir(files_to_convert))

for i in range(len(cd_files)):
    name = cd_files[i]
    nameFile = name[:-4]+'.csv'
    data = pd.read_csv(files_to_convert + '\\' + cd_files[i], sep=' ', header=None)
    data.dropna(inplace=True)
    data.to_csv(csv_dir + '\\' + nameFile, index=False)

###-----------------------------------------###

### Merge .csv files from bytes_03FFxx.csv to bytes_0FFF.csv ###

df = pd.concat(map(pd.read_csv, ['./csvFiles/bytes_03FFxx.csv',
                                 './csvFiles/bytes_04FFxx.csv',
                                 './csvFiles/bytes_05FFxx.csv',
                                 './csvFiles/bytes_06FFxx.csv',
                                 './csvFiles/bytes_07FFxx.csv',
                                 './csvFiles/bytes_08FFxx.csv',
                                 './csvFiles/bytes_09FFxx.csv',
                                 './csvFiles/bytes_0AFFxx.csv',
                                 './csvFiles/bytes_0BFFxx.csv',
                                 './csvFiles/bytes_0CFFxx.csv',
                                 './csvFiles/bytes_0DFFxx.csv',
                                 './csvFiles/bytes_0EFFxx.csv',
                                 './csvFiles/bytes_0FFFxx.csv']))

df.to_csv('./csvFiles/filesMerged.csv', index=False)

###-----------------------------------------###

### Add headers to final .csv files ###

key = pd.read_csv('./csvFiles/filesMerged.csv')
key.rename({'0': 'IV', '1': 'Cypher'}, axis=1, inplace=True)
key.to_csv('./keyfile.csv', index=False)

message = pd.read_csv('./csvFiles/bytes_01FFxx.csv')
message.rename({'0': 'IV', '1': 'Cypher'}, axis=1, inplace=True)
message.to_csv('./messageFile.csv', index=False)

###-----------------------------------------###