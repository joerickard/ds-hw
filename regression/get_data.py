
from pollster import Pollster

from csv import DictWriter

pollster = Pollster()

kFIELDS = ['YEAR', 'NAME', 'MOE', 'SUBPOP', 'SUBPOPID', 'CHOICE', 'PARTY', 'VALUE', 'OBS', 'STATE']

if __name__ == "__main__":
    o = DictWriter(open("data.csv", 'w'), kFIELDS)
    o.writeheader()
    for year in [2012, 2016]:
        line = {}
        line['YEAR'] = year
        entry = pollster.charts(topic='%i-president' % year)
        for chart in entry:
            for poll in chart.polls():
                for question in poll.questions:
                    line['NAME'] = question['name']
                    line['STATE'] = question['state']
                    subpop_id = 0
                    for subpop in question['subpopulations']:
                        subpop_id += 1
                        line['SUBPOPID'] = subpop_id
                        line['SUBPOP'] = subpop['name']
                        line['MOE'] = subpop['margin_of_error']
                        line['OBS'] = subpop['observations']
                        for res in subpop['responses']:
                            line['CHOICE'] = res['choice']
                            line['VALUE'] = res['value']
                            line['PARTY'] = res['party']
                            o.writerow(line)
                        
                        
