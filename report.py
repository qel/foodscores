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
    return datetime.datetime.strptime(s, '%m/%d/%Y').date()

locationList = []
with open(dat_file, 'r') as dat:
    locationList = json.load(dat)

print('-' * 95)
print('Worst inspections:')
print('-' * 95)

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
    print('{0:>2}. {1:<40} {2:<25} {3} : {4} : {5:>3}'.format(i, loc[NAME], loc[ADDRESS], loc[ZIP], inspection[DATE], inspection[SCORE]))
    if i == 30:
        break

print('-' * 95)
print('Worst TWO inspections:')
print('-' * 95)

worstList = []
for i, location in enumerate(locationList):
    if len(location[INSPECTIONS]) < 2:
        continue
    bottomTwo = sorted(location[INSPECTIONS], key=lambda x: x[SCORE])[2:]
    averageScore = sum(float(score) for date, score in bottomTwo) / 2
    worstList.append({
        LOCATION: i,
        SCORE: averageScore,
        INSPECTIONS: bottomTwo
    })

worstList = sorted(worstList, key=lambda x: x[SCORE])

for i, worst in enumerate(worstList):
    loc = locationList[worst[LOCATION]]
    print('{0:>2}. {1:<40} {2:<25} {3} : {5:>3} bottom two avg'.format(i, loc[NAME], loc[ADDRESS], loc[ZIP], worst[SCORE]))
    for inspection in worst[INSPECTIONS]:
        print(' ' * 60, '{4} : {5:>3}'.format(inspection[DATE], inspection[SCORE]))
    if i == 10:
        break
