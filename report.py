import json
import datetime

dat_file = 'data.json'
NAME = 'name'
ADDRESS = 'address'
SUITE = 'suite'
ZIP = 'zip'
INSPECTIONS = 'inspections'
LOCATION = 'location'
DATE = 'inspected'
SCORE = 'score'

def parse_date(s):
    if type(s) is str:
        return datetime.datetime.strptime(s, '%m/%d/%Y').date()
    if type(s) is datetime.date:
        return s
    print('What are you doing trying to parse', type(s), 'to a date?')
    quit()

locationList = []
with open(dat_file, 'r') as dat:
    locationList = json.load(dat)

print('-' * 79)
print('Worst inspections:')
print('-' * 79)

inspectionList = []
for i, location in enumerate(locationList):
    for inspection in location[INSPECTIONS]:
        inspectionList.append({
            LOCATION: i,
            DATE: parse_date(inspection[DATE]),
            SCORE: inspection[SCORE]
        })

inspectionList = sorted(inspectionList, key=lambda x: x[SCORE])

for i, inspection in enumerate(inspectionList):
    loc = locationList[inspection[LOCATION]]
    if i < 100:
        print('{0:>2}. {1:<35.35} {2:<24.24} {3}:{4:>3}'.format(i, loc[NAME], loc[ADDRESS], inspection[DATE], inspection[SCORE]))
    else:
        print('{0:>2}.{1:<35.35} {2:<24.24} {3}:{4:>3}'.format(i, loc[NAME], loc[ADDRESS], inspection[DATE], inspection[SCORE]))
    if i == 500:
        break

print('-' * 79)
print('Worst NATIONAL CHAINS:')
print('-' * 79)

chains = [
    'GRANDY',
    'ELEVEN',
    'SONIC',
    'TORCHY',
    'DENNY',
    'FUDDRUCKER',
    'CHICK-FIL',
    'SHELL',
    'DICKEY',
    'CABANA',
    'WAFFLE HOUSE',
    'JACK IN',
    '7-11',
    'DAIRY QUEEN',
    'MCDONALDS',
    'CHURCH',
    'TEXACO',
    'KROGER',
    'CHEDDAR',
    'HYATT',
    'ZENNA',
    'VILLAGE BURGER'
]

inspectionList = [x for x in inspectionList if locationList[x[LOCATION]][NAME].str.contains('')]

for i, inspection in enumerate(inspectionList):
    loc = locationList[inspection[LOCATION]]
    if i < 100:
        print('{0:>2}. {1:<35.35} {2:<24.24} {3}:{4:>3}'.format(i, loc[NAME], loc[ADDRESS], inspection[DATE], inspection[SCORE]))
    else:
        print('{0:>2}.{1:<35.35} {2:<24.24} {3}:{4:>3}'.format(i, loc[NAME], loc[ADDRESS], inspection[DATE], inspection[SCORE]))
    if i == 500:
        break

print('-' * 79)
print('Worst TWO inspections:')
print('-' * 79)

def worst_average(num, listLen, useZero=False):
    worstList = []
    for i, location in enumerate(locationList):
        if len(location[INSPECTIONS]) < num:
            continue
        bottomTwo = sorted(location[INSPECTIONS], key=lambda x: x[SCORE])[:num]
        for inspection in bottomTwo:
            inspection[DATE] = parse_date(inspection[DATE])
        bottomTwo = sorted(bottomTwo, key=lambda x: x[DATE])
        averageScore = sum([insp[SCORE] for insp in bottomTwo]) / num
        worstList.append({
            LOCATION: i,
            SCORE: averageScore,
            INSPECTIONS: bottomTwo
        })

    worstList = sorted(worstList, key=lambda x: x[SCORE])

    for i, worst in enumerate(worstList):
        idx = i + 1
        if useZero:
            idx = i
        loc = locationList[worst[LOCATION]]
        print('{0:>2}. {1:<35.35} {2:<24.24}   avg = {3:>4.5}'.format(idx, loc[NAME], loc[ADDRESS], worst[SCORE]))
        for inspection in worst[INSPECTIONS]:
            print(' ' * 64, '{0}:{1:>3}'.format(inspection[DATE], inspection[SCORE]))
        if i + 1 == listLen:
            break

worst_average(2, 21, useZero=True)

print('-' * 79)
print('Worst THREE inspections:')
print('-' * 79)

worst_average(3, 11, useZero=True)

print('-' * 79)
print('Worst FOUR inspections:')
print('-' * 79)

worst_average(4, 5)

print('-' * 79)
print('Worst FIVE inspections:')
print('-' * 79)

worst_average(5, 5)

print('-' * 79)
print('Worst SIX inspections:')
print('-' * 79)

worst_average(6, 8)

print('-' * 79)
print('Worst SEVEN inspections:')
print('-' * 79)

worst_average(7, 4)

print('-' * 79)
print('Worst EIGHT inspections:')
print('-' * 79)

worst_average(8, 4)

print('-' * 79)
print('Worst NINE inspections:')
print('-' * 79)

worst_average(9, 8)

print('-' * 79)
print('Worst TEN inspections:')
print('-' * 79)

worst_average(10, 4)

print('-' * 79)
print('Worst TWELVE inspections:')
print('-' * 79)

worst_average(12, 2)
