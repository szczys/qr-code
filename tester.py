testVersion = 7
tabooDict = {}
tabooDict.update(getFinderDict(testVersion))
tabooDict.update(getAlignmentDict(testVersion,tabooDict))
tabooDict.update(getSeparatorDict(testVersion))
tabooDict.update(getTimingDict(testVersion,tabooDict))
tabooDict.update(getFormatDict(testVersion,'101010101010101'))
tabooDict.update(getVersionDict(testVersion,'111111111111111111'))
grid = fillListFromDict(getEmptyGrid(testVersion),tabooDict)
grid = applyMask(grid,tabooDict,7)
genQrImage(grid)
