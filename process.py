def decodeSutom(message):
    i = 0
    for c in message:
        if c == "🟥":
            break
        i += 1
    decodedMessage = message[i:]

    i = 0
    for c in decodedMessage:
        #if c != "🟥" and c != "🟦" and c != "🟡" and c != "\n":
        #    break
        if c == "\n" and decodedMessage[i + 1] == "\n":
            break
        i += 1
    sutomCode = decodedMessage[:i]
    return sutomCode

def verifySutom(sutomCode):
    for c in sutomCode:
        if c != "🟥" and c != "🟦" and c != "🟡" and c != "\n":
            return False

    lines = sutomCode.splitlines()
    try:
        numberLetter = len(lines[0])
    except IndexError:
        return False
    numberOfLines = len(lines)
    if numberOfLines > 6:
        return False
    actualLine = 0
    for line in sutomCode.splitlines():
        actualLine += 1
        nextNumberLetter = len(line)
        if numberLetter != nextNumberLetter:
            return False
        if "🟦" not in line and "🟡" not in line:
            if actualLine != numberOfLines:
                return False

    return True

def scoreSutom(sutomCode):
    score = 6
    for line in sutomCode.splitlines():
        if "🟦" not in line and "🟡" not in line:
            return score
        score -= 1
    return 0