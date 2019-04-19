
def writeToFile(data):
    f = open('debug.txt', 'w')
    f.write(data)
    f.close

def openURL(url):
    print(url)
    import webbrowser
    webbrowser.open(url)
