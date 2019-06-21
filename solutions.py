solutions16 = {
    '1': ['GERMANY'],
    '2': ['TELLES'],
    '3': ['SELENA'],
    '4': ['NORTON'],
    '5': ['VENETIAN'],
    '6': ['KAPLINSKY'],
    '7': ['BOWIE', 'DAVID BOWIE'],
    '8': ['ARGO'],
    '9': ['SOVEREIGNTY'],
    '10': ['AMINO'],
    '11': ['VANNA', 'VANNA WHITE'],
    '12': ['FROZEN']
    }

solutions17 = {
    '1': ['JOLT'],
    '2': ['ORGANISATION', 'ORGANIZATION'],
    '3': ['CHECK'],
    '4': ['DRACULA', 'NOSFERATU'],
    '5': ['PRISM'],
    '6': ['DAHSHUR', 'CAIRO', 'EGYPT', 'DASHUR'],
    '7': ['BONDS', 'BARRY BONDS', 'WILLIE MAYS'],
    '8': ['DRAGON']
    }

solutions18 = {
    '1': ['ARCHITECTURE'],
    '2': ['MEIROWITZ'],
    '3': ['COINAGE'],
    '4': ['WELCOME'],
    '5': ['OCEAN'],
    '6': ['SNAKE EYES'],
    '7': ['ATHLETICISM'],
    '8': ['EXPECTATIONS']
    }

solutions19 = {
    '1': ['FINANCIER'],
    '2': ['VILNIUS'],
    '3': ['BEHIND'],
    '4': ['SPORADIC'],
    '5': ['CONTRAST'],
    '6': ['RAINCOAT'],
    '7': ['THIRTY'],
    '8': ['DECADE'],
    '9': ['MARSHALL', 'ROB MARSHALL'],
    '10': ['MONOCHROME', 'CUNT'],
    '11': ['COLUMNS']
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
