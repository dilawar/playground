import numpy as np
import pyaudio

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                     channels=1,
                     rate=16000,
                     output=True,
                     )

import matplotlib.pyplot as plt
buf = np.uint8(np.loadtxt('./data.txt', delimiter=',')).tobytes()
string = ''.join([chr(x) for x in buf])
print('===============')
print(string)

quit()
print(len(buf))
data = np.frombuffer(buf, dtype=np.float16)
data = data / 2**16
#  print(data)
#  plt.plot(data)
#  plt.show()

# Assuming you have a numpy array called samples
#  data = samples.astype(np.float32).tostring()
stream.write(data.astype(np.float32).tostring())

