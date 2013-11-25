# Brian is a neural simulator. This script tests its capabilities of generating
# spike train.
import brian
from IPython import embed

if __name__ == "__main__":
    # Create a group of neuron which emits spikes independently according to
    # Possion processes
    grps = brian.PoissonGroup(1, rates=50*brian.Hz)
    # Attach input to these neurons
    ips = brian.PoissonInput(grps, N=1, rate=50)
    embed()
