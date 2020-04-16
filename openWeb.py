import webbrowser

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

def openChrome(url):
    try:
        webbrowser.get(chrome_path).open(url)
        return True
    except:
        return False

