from flask import Flask, render_template, request, redirect
import numpy as np
import skfuzzy.control as ctrl

app = Flask(__name__)


@app.route('/base', methods=['POST', 'GET'])
def base():
    ts = [0.,  0.5,  1.,  1.5,  2.,  2.5,  3.,  3.5,  4.,  4.5,  5.,
          5.5,  6.,  6.5,  7.,  7.5,  8.,  8.5,  9.,  9.5, 10.]
    hs = [0., 0.125, 0.23232233, 0.33322242, 0.42935971,
          0.52159693, 0.6104861, 0.6964193, 0.77969343, 0.8605433,
          0.93916056, 1., 1., 1., 1.,
          1., 1., 1., 1., 1.,
          1.]
    hmax = 0
    if request.method == 'POST':
        b = float(request.form['wspolczynnik_wyplywu'])
        A = float(request.form['pole_dna'])
        Qd = float(request.form['wplyw'])
        dt = float(request.form['krok_symulacji'])
        tf = float(request.form['czas_symulacji'])

        h = 0
        t = 0
        ts = []
        hs = []
        i = 0
        hmax = float(request.form['wysokosc_zbiornika'])
        while t <= tf:
            ts.append(t)
            hs.append(h)

            # Q Output -- Wypływ ze zbiornika
            QO = b * pow(h, 0.5)
            # R.Różnicowe
            h = (Qd-QO)*dt/A + h
            # Przelewanie się zbiornika
            if h > hmax:
                h = hmax

            i = i + 1
            t = t + dt
        return render_template('base.html', max=hmax + 1, labels=ts, values=hs, b=b, A=A, Qd=Qd,  dt=dt, tf=tf, hmax=hmax)
    else:
        # GET aka first load
        return render_template('base.html', max=hmax + 1, labels=ts, values=hs)


@app.route('/pid', methods=['POST', 'GET'])
def pid():
    ts = [0.,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.,
          1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2.,  2.1,
          2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3.,  3.1,  3.2,
          3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4.,  4.1,  4.2,  4.3,
          4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5.,  5.1,  5.2,  5.3,  5.4,
          5.5,  5.6,  5.7,  5.8,  5.9,  6.,  6.1,  6.2,  6.3,  6.4,  6.5,
          6.6,  6.7,  6.8,  6.9,  7.,  7.1,  7.2,  7.3,  7.4,  7.5,  7.6,
          7.7,  7.8,  7.9,  8.,  8.1,  8.2,  8.3,  8.4,  8.5,  8.6,  8.7,
          8.8,  8.9,  9.,  9.1,  9.2,  9.3,  9.4,  9.5,  9.6,  9.7,  9.8,
          9.9, 10.]
    hs = [0., 0.1, 0.19683772, 0.29240108, 0.38699367,
          0.48077279, 0.57383901, 0.66626379, 0.75748958, 0.83908665,
          0.90695215, 0.95996616, 0.99890324, 1.02559814, 1.04234285,
          1.05148049, 1.05515666, 1.05518932, 1.05302278, 1.04973649,
          1.04608595, 1.04255884, 1.03943489, 1.036842, 1.03480474,
          1.03328344, 1.03220391, 1.0314786, 1.03102049, 1.03075148,
          1.03060637, 1.03053414, 1.03049719, 1.03046966, 1.03043525,
          1.03038494, 1.03031499, 1.03022516, 1.03011731, 1.02999442,
          1.02985981, 1.02971669, 1.02956788, 1.02941572, 1.02926199,
          1.02910799, 1.0289546, 1.02880236, 1.02865155, 1.02850227,
          1.02835451, 1.02820816, 1.02806313, 1.02791927, 1.02777647,
          1.02763461, 1.02749362, 1.02735342, 1.02721396, 1.02707522,
          1.02693717, 1.0267998, 1.0266631, 1.02652708, 1.02639172,
          1.02625703, 1.02612302, 1.02598967, 1.02585701, 1.02572501,
          1.02559369, 1.02546303, 1.02533304, 1.02520372, 1.02507506,
          1.02494705, 1.0248197, 1.024693, 1.02456695, 1.02444154,
          1.02431678, 1.02419265, 1.02406915, 1.02394628, 1.02382405,
          1.02370243, 1.02358144, 1.02346106, 1.0233413, 1.02322215,
          1.02310361, 1.02298567, 1.02286833, 1.0227516, 1.02263546,
          1.02251991, 1.02240495, 1.02229058, 1.02217679, 1.02206359,
          1.02195096]
    hmax = 0
    if request.method == 'POST':
        b = float(request.form['wspolczynnik_wyplywu'])
        A = float(request.form['pole_dna'])
        Qd = 0
        Qmax = float(request.form['wplyw_max'])
        dt = float(request.form['krok_symulacji'])
        tf = float(request.form['czas_symulacji'])
        hz = float(request.form['wysokosc_zadana'])
        hmax = float(request.form['wysokosc_zbiornika'])

        ts = []
        hs = []
        h = 0
        t = 0
        i = 0
        e = hz - h
        I = 0
        # Nastawy <ekperymentalne>

        Kp = float(request.form['kp'])
        Ki = float(request.form['ki'])
        Kd = float(request.form['kd'])

        while t <= tf:
            ts.append(t)
            hs.append(h)

            e_next = hz - h
            # pid
            P = Kp*e
            I = I + Ki*e*dt
            D = Kd*(e_next - e)/dt

            Qd = Qd + P + I + D
            if Qd < 0:
                Qd = 0
            elif Qd > Qmax:
                Qd = Qmax

            # Q Output -- Wypływ ze zbiornika
            QO = b * pow(h, 0.5)
            # R.Różnicowe
            h = (Qd-QO)*dt/A + h

            # Przelewanie się zbiornika
            if h > hmax:
                h = hmax
            elif h < 0:
                h = 0

            i = i + 1
            t = t + dt
            e = e_next
        return render_template('pid.html', max=hmax + 1, labels=ts, values=hs, b=b, A=A, Qd=Qd, Qmax=Qmax, dt=dt, tf=tf, hz=hz, hmax=hmax, kp=Kp, ki=Ki, kd=Kd)
    else:
        # GET aka first load
        return render_template('pid.html', max=hmax + 1, labels=ts, values=hs)


@app.route('/fuzzy', methods=['POST', 'GET'])
def fuzzy():
    ts = [0.,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.,
          1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2.,  2.1,
          2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3.,  3.1,  3.2,
          3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4.,  4.1,  4.2,  4.3,
          4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5.,  5.1,  5.2,  5.3,  5.4,
          5.5,  5.6,  5.7,  5.8,  5.9,  6.,  6.1,  6.2,  6.3,  6.4,  6.5,
          6.6,  6.7,  6.8,  6.9,  7.,  7.1,  7.2,  7.3,  7.4,  7.5,  7.6,
          7.7,  7.8,  7.9,  8.,  8.1,  8.2,  8.3,  8.4,  8.5,  8.6,  8.7,
          8.8,  8.9,  9.,  9.1,  9.2,  9.3,  9.4,  9.5,  9.6,  9.7,  9.8,
          9.9, 10.]
    hs = [0., 0.1, 0.09683772, 0.19372585, 0.18932442,
          0.28497327, 0.27963499, 0.37434693, 0.36822854, 0.46216036,
          0.45536212, 0.54861407, 0.54120722, 0.63385054, 0.62588907,
          0.71797775, 0.7095044, 0.80108119, 0.79213087, 0.8832307,
          0.87383267, 0.95080424, 0.94105332, 1.00572578, 0.99569719,
          1.05675546, 1.0464756, 1.06769873, 1.05736578, 1.07095004,
          1.06060137, 1.07197171, 1.06161811, 1.07229791, 1.06194272,
          1.07240257, 1.06204688, 1.0724362, 1.06208035, 1.07244701,
          1.06209111, 1.07245049, 1.06209457, 1.07245161, 1.06209569,
          1.07245197, 1.06209604, 1.07245209, 1.06209616, 1.07245212,
          1.0620962, 1.07245214, 1.06209621, 1.07245214, 1.06209621,
          1.07245214, 1.06209621, 1.07245214, 1.06209621, 1.07245214,
          1.06209621, 1.07245214, 1.06209621, 1.07245214, 1.06209621,
          1.07245214, 1.06209621, 1.07245214, 1.06209621, 1.07245214,
          1.06209621, 1.07245214, 1.06209621, 1.07245214, 1.06209621,
          1.07245214, 1.06209621, 1.07245214, 1.06209621, 1.07245214,
          1.06209621, 1.07245214, 1.06209621, 1.07245214, 1.06209621,
          1.07245214, 1.06209621, 1.07245214, 1.06209621, 1.07245214,
          1.06209621, 1.07245214, 1.06209621, 1.07245214, 1.06209621,
          1.07245214, 1.06209621, 1.07245214, 1.06209621, 1.07245214,
          1.06209621]
    hmax = 0
    universe = np.linspace(-2, 2, 5)
    error = ctrl.Antecedent(universe, 'error')
    delta = ctrl.Antecedent(universe, 'delta')
    output = ctrl.Consequent(universe, 'output')
    names = ['nb', 'ns', 'ze', 'ps', 'pb']
    error.automf(names=names)
    delta.automf(names=names)
    output.automf(names=names)

    rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
                                  (error['ns'] & delta['nb']) |
                                  (error['nb'] & delta['ns'])),
                      consequent=output['nb'], label='rule nb')

    rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
                                  (error['nb'] & delta['ps']) |
                                  (error['ns'] & delta['ns']) |
                                  (error['ns'] & delta['ze']) |
                                  (error['ze'] & delta['ns']) |
                                  (error['ze'] & delta['nb']) |
                                  (error['ps'] & delta['nb'])),
                      consequent=output['ns'], label='rule ns')

    rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
                                  (error['ns'] & delta['ps']) |
                                  (error['ze'] & delta['ze']) |
                                  (error['ps'] & delta['ns']) |
                                  (error['pb'] & delta['nb'])),
                      consequent=output['ze'], label='rule ze')

    rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
                                  (error['ze'] & delta['pb']) |
                                  (error['ze'] & delta['ps']) |
                                  (error['ps'] & delta['ps']) |
                                  (error['ps'] & delta['ze']) |
                                  (error['pb'] & delta['ze']) |
                                  (error['pb'] & delta['ns'])),
                      consequent=output['ps'], label='rule ps')

    rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
                                  (error['pb'] & delta['pb']) |
                                  (error['pb'] & delta['ps'])),
                      consequent=output['pb'], label='rule pb')

    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])
    sim = ctrl.ControlSystemSimulation(system)

    if request.method == 'POST':
        b = float(request.form['wspolczynnik_wyplywu'])
        A = float(request.form['pole_dna'])
        Qd = 0
        Qmax = float(request.form['wplyw_max'])
        dt = float(request.form['krok_symulacji'])
        tf = float(request.form['czas_symulacji'])
        hz = float(request.form['wysokosc_zadana'])
        hmax = float(request.form['wysokosc_zbiornika'])

        h = 0
        t = 0
        ts = []
        hs = []
        i = 0
        e = hz - h

        while t <= tf:
            ts.append(t)
            hs.append(h)
            e_next = hz - h

            sim.input['error'] = e
            sim.input['delta'] = (e_next - e)/dt
            sim.compute()
            Qd = 10 * sim.output['output']
            # print(Qd)
            if Qd < 0:
                Qd = 0
            elif Qd > Qmax:
                Qd = Qmax

            # Q Output -- Wypływ ze zbiornika
            QO = b * pow(h, 0.5)
            # R.Różnicowe
            h = (Qd-QO)*dt/A + h

            # Przelewanie się zbiornika
            if h > hmax:
                h = hmax
            if h < 0:
                h = 0

            i = i + 1
            t = t + dt
            e = e_next
        return render_template('fuzzy.html', max=hmax + 1, labels=ts, values=hs, b=b, A=A, Qd=Qd, Qmax=Qmax, dt=dt, tf=tf, hz=hz, hmax=hmax)
    else:
        # GET aka first load
        return render_template('fuzzy.html', max=hmax + 1, labels=ts, values=hs)


if __name__ == '__main__':
    app.run(debug=True)
