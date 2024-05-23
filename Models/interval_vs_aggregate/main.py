# interval vs aggregate

import typer
import numpy as np
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

app = typer.Typer()


@app.command()
def run(max_days: int, prob_failure: float = 1e-3):
    simulate(max_days, prob_failure)


def simulate(max_days: int, prob_failure: float = 1e-3):
    print(f"Simulating for {max_days} with {prob_failure=}")
    now = datetime.utcnow()
    time = now

    values, V1, V2 = [], [], []
    dt_secs = 30
    while time < now + timedelta(days=max_days):
        time += timedelta(seconds=dt_secs)
        v = random.randint(1, dt_secs // 2)
        values.append((time, v))
        if random.random() >= prob_failure:
            if len(values) > 1:
                V1.append((time, values[-2][1] + v))
            else:
                V1.append((time, v))
            V2.append((time, v))
        else:
            V2.append((time, V2[-1][1]))

    plot(values, V1, V2)


def plot(values, V1, V2):
    (x, y) = zip(*values)
    plt.plot(x, np.cumsum(y), "-x", label="real", alpha=0.5)
    (x, y) = zip(*V1)
    plt.plot(x, np.cumsum(y), '-o', label="aggregate", alpha=0.5)
    (x, y) = zip(*V2)
    plt.plot(x, np.cumsum(y), "-c", label="interval", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    app()
