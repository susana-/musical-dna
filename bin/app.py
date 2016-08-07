import web
from music21 import *
import pygame
import cStringIO

urls = (
  '/musical-dna', 'Index',
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

# For the music21 Upper Part, we automate the note creation procedure
data1 = [('g4', 'quarter'), ('a4', 'half'), ('b4', 'quarter'), ('c#5', 'whole'),('g4', 'quarter'), ('a4', 'half'), ('b4', 'quarter'), ('c#5', 'whole'),('g4', 'quarter'), ('a4', 'half'), ('b4', 'quarter'), ('c#5', 'whole')]
data2 = [('d5', 'whole'),('g4', 'quarter'), ('a4', 'half'), ('b4', 'quarter'), ('c#5', 'whole'),('g4', 'quarter'), ('a4', 'half'), ('b4', 'quarter'), ('c#5', 'whole')]
data = [data1, data2]
partUpper = stream.Part()
def makeUpperPart(data):
    for mData in data:
        m = stream.Measure()
        for pitchName, durType in mData:
            n = note.Note(pitchName)
            n.duration.type = durType
            m.append(n)
        partUpper.append(m)
makeUpperPart(data)    

# Now, we can add both Part objects into a music21 Score object.  

sCadence = stream.Score()
sCadence.insert(0, partUpper)

# Now, let's play the MIDI of the sCadence Score [from memory, ie no file  write necessary] using pygame

# for music21 <= v.1.2:
if hasattr(sCadence, 'midiFile'):
   sCadence_mf = sCadence.midiFile
else: # for >= v.1.3:
   sCadence_mf = midi.translate.streamToMidiFile(sCadence)

sCadence_mStr = sCadence_mf.writestr()
sCadence_mStrFile = cStringIO.StringIO(sCadence_mStr)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)

def play_dna(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

class Index(object):
    def GET(self):
        return render.hello_form()

    def POST(self):
        form = web.input(name="")
        greeting = "%s" % (form.name)   
    	play_dna(sCadence_mStrFile)
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()
