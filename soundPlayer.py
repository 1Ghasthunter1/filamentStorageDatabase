from playsound import playsound
import qrMaker
def playChime():
	currentLoc = qrMaker.getCurrentPath()
	playsound(f'{currentLoc}/sounds/qrChime.wav')
