################################################################
# File Path    : /analyse.py
# Project Name : x265_option_compare
# Author       : zzyy21
# Create Time  : 2021-03-24 22:24:37
# Modifed by   : zzyy21
# Last Modify  : 2021-04-26 23:19:12
# Description  : Compare the encoding settings of x265 video
#                clip with the x265 default encoding settings
# Revision     : v0.1: First draft
################################################################

import string
import re

class Option:
    # int num
    # string name
    # bool paramType
    # string defaultValue

    def __init__(self, num, name, paramType, defaultValue):
        self.num = int(num)
        self.name = name
        self.paramType = bool(int(paramType))
        if self.paramType:
            self.defaultValue = bool(int(defaultValue))
        else:
            try:
                self.defaultValue = float(defaultValue)
            except:
                self.defaultValue = defaultValue

    def ReturnName(self):
        return self.name

class EncodingSetting:
    # string inStr
    # string name
    # string value
    # int matchedNum
    # bool paramType
    # string defaultValue
    # bool isDefault

    def __init__(self, inStr):
        self.inStr = inStr

        equal = inStr.find('=')
        if equal != -1 :
            self.name = inStr[ :equal]
            self.value = inStr[equal + 1: ]
        elif inStr[0:3] == "no-" :
            self.name = inStr[3: ]
            self.value = False
        else:
            self.name = inStr
            self.value = True

    def CheckOption(self, optionNum, optionParamType, optionDefaultValue):
        self.matchedNum = optionNum
        self.paramType = optionParamType
        self.optionDefaultValue = optionDefaultValue
        if self.paramType:
            self.value = bool(int(self.value))
        else:
            try:
                self.value = float(self.value)
            except:
                self.value = self.value
        self.isDefault = self.optionDefaultValue == self.value

    def OptionNotFound(self):
        self.matchedNum = -1
        self.paramType = False
        self.optionDefaultValue = "N/A"
        self.isDefault = False

    def ReturnName(self):
        return self.name

    def ReturnMatchedNum(self):
        return self.matchedNum

def main():
    optionList = []
    optionStrFile = open("x265_default.txt", "r")
    for optionStr in optionStrFile:
        optionParams = optionStr.split('\t')
        optionList.append(Option(optionParams[0], optionParams[1], optionParams[2], optionParams[3]))
    optionList.sort(key=Option.ReturnName)

    encodingSettingList = []
    mediaInfoFile = open("mediainfo.txt", "r", encoding="utf-16-le")
    isVideoTrack = False
    for line in mediaInfoFile.readlines():
        line = line.strip()
        if isVideoTrack :
            matchEncoder = re.match(r"Writing library *: ", line)
            if matchEncoder :
                encoder = line[matchEncoder.end(): ]
                print("Encoder:    %s" % encoder)
                continue

            matchSettings = re.match(r"Encoding settings *: ", line)
            if matchSettings :
                encodingSettingStrList = line[matchSettings.end(): ].split(" / ")
                for encodingSettingStr in encodingSettingStrList :
                    encodingSettingList.append(EncodingSetting(encodingSettingStr))
                continue

        if re.match(r"^Video.*", line) :
            isVideoTrack = True
            continue
        if re.match(r"^(Audio|Text|Menu).*", line) :
            isVideoTrack = False
            continue
    encodingSettingList.sort(key=EncodingSetting.ReturnName)

    i = 0
    j = 0
    while ((i < len(optionList)) and (j < len(encodingSettingList))):
        if optionList[i].name < encodingSettingList[j].name:
            i += 1
        elif optionList[i].name > encodingSettingList[j].name:
            encodingSettingList[j].OptionNotFound()
            j += 1
        else:
            encodingSettingList[j].CheckOption(optionList[i].num, optionList[i].paramType, optionList[i].defaultValue)
            j += 1

    encodingSettingList.sort(key=EncodingSetting.ReturnMatchedNum)

    for encodingSetting in encodingSettingList:
        if not(encodingSetting.isDefault):
            if encodingSetting.paramType:
                if encodingSetting.value:
                    print("--%s (Default: --no-%s)" % (encodingSetting.name, encodingSetting.name))
                else:
                    print("--no-%s (Default: --%s)" % (encodingSetting.name, encodingSetting.name))
            else:
                print("--%s=%s (Default: %s)" % (encodingSetting.name, encodingSetting.value, encodingSetting.optionDefaultValue))

if __name__ == "__main__" :
    main()
