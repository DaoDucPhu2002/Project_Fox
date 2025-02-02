# input File Pins and File PinsLong => output File PinsShort
import os
path_pins = 'pins'
path_pins_long = 'pins_long'


def CheckShortPins(PinsFile, PinsLongFile, PinsShortFile):
    Pins = []
    PinsLong = []
    PinsShort = []
    with open(PinsFile, 'r') as f:
        for line in f:
            if not line.startswith('!'):
                Pins.append(line.strip())
    print("Read file Pins done!!!!")
    with open(PinsLongFile, 'r') as f:
        for line in f:
            # bo qua dau !
            if not line.startswith('!'):
                PinsLong.append(line.strip())
    print("Read file PinsLong done!!!!")
    for pin in Pins:
        if pin not in PinsLong:
            PinsShort.append(pin)
    # create file PinsShort
    if os.path.exists(PinsShortFile):
        open(PinsShortFile, 'w').close()
    print("Creating file PinsShort....")
    with open(PinsShortFile, 'w') as f:
        for pin in PinsShort:
            f.write(pin + '\n')
    print("Done!!!!")


CheckShortPins('pins', 'pins_long', 'pins_shorts')
