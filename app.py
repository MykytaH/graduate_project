from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
@app.route('/result', methods=['POST'])
def result():

    n1, n2, n3, n4 = 0, 0, 0, 0
    v1, v2, v3, v4 = 10, 10, 10, 10
    N1, N2, N3, N4 = 1.5, 2, 3.5, 1.5


    mixer_status = (
        "rest",
        "mixes",
    )
    mixing_t = 1000
    mixture_q = 0
    status = mixer_status[0]
    dt = 0
    lines = []

    while dt < 100:

        w1 = np.random.normal(0.1, 0.01)
        w2 = np.random.normal(0.2, 0.02)
        w3 = np.random.normal(0.3, 0.03)
        w4 = np.random.normal(0.1, 0.01)
        t = np.random.exponential(4)
        nu1 = np.random.randint(3, 7)
        nu2 = np.random.randint(0.5, 3)
        nu3 = np.random.randint(0.5, 5)

        if n1 < v1:
            n1 += w1 * t
        if n2 < v2:
            n2 += w2 * t
        if n3 < v3:
            n3 += w3 * t
        if n4 < v4:
            n4 += w4 * t

        if n1 >= N1 and n2 >= N2 and n3 >= N3 and n4 >= N4 and status == mixer_status[0]:
            n1 -= N1
            n2 -= N2
            n3 -= N3
            n4 -= N4
            status = mixer_status[1]
            mixing_t = t + dt

        if mixing_t <= dt:
            status = mixer_status[0]
            mixture_q = (N1 + nu1 * N2 / 100 + nu2 * N3 / 100 + nu3 * N4 / 100) / (N1 + N2 + N3 + N4) * 100

        dt += 1

        protocol = {"dt": dt,
                    "n1": round(n1, 2),
                    "n2": round(n2, 2),
                    "n3": round(n3, 2),
                    "n4": round(n4, 2),
                    "status": status,
                    "mixture_q": round(mixture_q, 1)}
        lines.append(protocol)
    return render_template('launch.html', lines=lines)


if __name__ == '__main__':
    app.run(debug=True)
