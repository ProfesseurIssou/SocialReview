from datetime import date, timedelta
import numpy as np

def reputationAlgorithm (reports):
    numbers = []
    dateSommes = [[]]
    for report in reports :
        found = False
        for dataSomme in dateSommes:
            if date.__eq__(dateSomme[0], report.report_date) :
                dateSomme[1] = dateSomme[1] + 1
                found = True
        if not found:
            dateSommes.append([report.report_date, 1])

    dateSommes = sorted(dateSommes, key=lambda x: x[0])
    dateSommesTotal =  [dateSommes[0]]
    for dateSomme in dateSommes:
        datePlusOne = dateSommesTotal[-1][0] + timedelta(days=1)
        if dateSomme[0] == datePlusOne :
            dateSommesTotal.append(dateSomme)
        else :
            dateSommesTotal.append([datePlusOne, 0])

    lastDate = dateSommesTotal[-1][0]
    timeDelta =  date.today() - lastDate
    if timeDelta > timedelta(days=0):
        for index in range(timeDelta.days) :
            dateSommesTotal.append([lastDate + timeDelta(days = index+1), 0])

    for dateSomme in dateSommesTotal:
        numbers.append(dateSomme[1])
    
    j = len(numbers)
    numerator = sum(np.log10(numbers[i]) * (j - (i + 1)) for i in range(j))
    denominator = sum(numbers)
    
    return numerator / denominator if denominator != 0 else None