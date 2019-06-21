solutions16 = {
    '1': ['ORGANISATION', 'ORGANIZATION'],
    '2': ['FUCK', 'CUNT']
    }

solutions17 = {
    '1': ['ORGANISATION', 'ORGANIZATION'],
    '2': ['FUCK', 'CUNT']
    }

solutions18 = {
    '1': ['ORGANISATION', 'ORGANIZATION'],
    '2': ['FUCK', 'CUNT']
    }

solutions19 = {
    '1': ['ORGANISATION', 'ORGANIZATION'],
    '2': ['FUCK', 'CUNT']
    }


def check(year, question, answer):
    print(year, int(question))
    if year == "2016":
        x = solutions16[question]
    if year == "2017":
        x = solutions17[question]
    if year == "2018":
        x = solutions18[question]
    if year == "2019":
        x = solutions19[question]

    print(x)
    for i in range(len(x)):
        if answer == x[i]:
            return "correct"
    return "wrong"
