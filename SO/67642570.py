import pygame.midi


def print_devices():
    for n in range(pygame.midi.get_count()):
        print(n, pygame.midi.get_device_info(n))


def readInput(input_device):

    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            print(event)
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            print(data[2])

            if data[1] == 36 and 40 and 43 and 46:  # not working
                print("chord = Cmaj7")
            else:
                print(data[2])


if __name__ == "__main__":
    pygame.midi.init()
    print_devices()
    my_input = pygame.midi.Input(1)
    readInput(my_input)
