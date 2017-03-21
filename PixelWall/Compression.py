import Core

def toLinearfromRaw(data):
    indicator = 1;replacement = 2;new = [[], [], []];
    for channel in range(0, len(data)):
        temporary = []
        lastPoint = None
        for point in range(0, len(data[channel])):
            if lastPoint != data[channel][point]:
                if len(temporary) <= 3:
                    if len(temporary) != 0:
                        for i in temporary:
                            if i == indicator:
                                new[channel].append(replacement)
                            else:
                                new[channel].append(i)
                else:
                    if len(temporary) > 255:
                        for i in range(1, (len(temporary)-1)//254):
                            new[channel].append(indicator)
                            new[channel].append(temporary[0])
                            new[channel].append(254)
                        new[channel].append(indicator)
                        new[channel].append(temporary[0])
                        new[channel].append((len(temporary)-1)%254)
                    else:
                        new[channel].append(indicator)
                        new[channel].append(temporary[0])
                        new[channel].append(len(temporary)-1)
                lastPoint = data[channel][point]
                temporary = [data[channel][point]]
            else:
                if data[channel][point] == indicator:
                    temporary.append(replacement)
                else:
                    temporary.append(data[channel][point])

        if len(temporary) > 255:
            for i in range(1, (len(temporary)-1)//254):
                new[channel].append(indicator)
                new[channel].append(temporary[0])
                new[channel].append(254)
            new[channel].append(indicator)
            new[channel].append(temporary[0])
            new[channel].append((len(temporary)-1)%254)
        elif len(temporary) > 0:
            new[channel].append(indicator)
            new[channel].append(temporary[0])
            new[channel].append(len(temporary)-1)
        else:
            if lastPoint == indicator:
                new[channel].append(replacement)
            else:
                new[channel].append(lastPoint)
    return new

def toRawfromLinear(data):
    indicator = 1;
    new = [[], [], []]
    cnt = -1
    for i in data:
        locked = None
        cnt +=1
        for x in range(0, len(i)):
            if i[x] == indicator:
                if x + 2 <= len(i):
                    #[Indicator][Value][Count]
                    for r in range(0, i[x+2]+1):
                        new[cnt].append(i[x+1])#new value
                    locked = x+2;
                else:
                    Core.UtilPrint.compose("!", "UDN", __name__, "found indicator byte at unintended position please check you indicator bytes")
            elif x <= locked:
                pass
                #to be ignored, because theese are the indicator and value bytes
            else:
                new[cnt].append(i[x])
    return new

def toLinearfromTransport(data):
    data = bytearray(data);
    Ldat = len(data);
    #Structure:
    #[Compression (0,1,2)][EXTRA+6]
    #[Lengtha1][lengtha2][Lengthb1][lengthb2][lengthc1][lengthc2]
    #totalLength = 255*Lengthxa[0-255] + Lengthxb[0-255]|| MAX: 65280bytes length*3 + 7
    totalLengthR = int(ldat[0]) * 254 + int(ldat[1])
    totalLengthG = int(ldat[2]) * 254 + int(ldat[3])
    totalLengthB = int(ldat[4]) * 254 + int(ldat[5])
    if Ldat != (totalLengthR + totalLengthG + totalLengthB+6):
        Core.UtilPrint.compose("!", self.__class__, __name__, "failed to decode. The lengths do not match. The packet will be ignored.")
        return False

    newdata = [[], [], []]
    newdata[0] = data[7:7+totalLengthR]
    newdata[1] = data[totalLengthR+7+1:totalLengthG+7+totalLengthR]
    newdata[2] = data[totalLengthG+7+totalLengthR+1:totalLengthG+7+totalLengthR+totalLengthB]
    return newdata


def toTransportfromLinear(data):
    lenR = len(data[0])
    lenG = len(data[1])
    lenB = len(data[2])
    header = bytearray([lenR//254, lenR%254, lenG//254, lenG%254, lenB//254, lenB%254])
    if type(data[0]) == list:
        R = bytearray(data[0])

    if type(data[1]) == list:
        G = bytearray(data[1])

    if type(data[2]) == list:
        B = bytearray(data[2])

    return (header + R + G + B)
