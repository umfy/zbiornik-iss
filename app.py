from flask import Flask, render_template, request, redirect
import numpy as np
import skfuzzy.control as ctrl

app = Flask(__name__)


@app.route('/')
def redirect_base():
    return redirect("/base")


@app.route('/base', methods=['POST', 'GET'])
def base():
    ts = [0.,  0.5,  1.,  1.5,  2.,  2.5,  3.,  3.5,  4.,  4.5,  5.,
          5.5,  6.,  6.5,  7.,  7.5,  8.,  8.5,  9.,  9.5, 10.]
    hs = [0., 0.25, 0.475, 0.69053988, 0.89899051,
          1.10158296, 1.2991048, 1.49211566, 1.5, 1.5,
          1.5, 1.5, 1.5, 1.5, 1.5,
          1.5, 1.5, 1.5, 1.5, 1.5,
          1.5]
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
          0.48077279, 0.57383901, 0.66626379, 0.7581013, 0.84939439,
          0.93682198, 0.99241894, 1.01762747, 1.02353819, 1.02071358,
          1.01585168, 1.01197816, 1.00979351, 1.00895025, 1.00886004,
          1.00905675, 1.00927918, 1.0094281, 1.0094949, 1.00950527,
          1.0094878, 1.00946208, 1.00943777, 1.00941773, 1.00940145,
          1.00938747, 1.00937446, 1.00936166, 1.00934871, 1.00933557,
          1.00932229, 1.00930893, 1.00929557, 1.00928223, 1.00926891,
          1.00925563, 1.00924237, 1.00922913, 1.00921591, 1.00920271,
          1.00918953, 1.00917637, 1.00916322, 1.0091501, 1.00913699,
          1.0091239, 1.00911083, 1.00909778, 1.00908475, 1.00907174,
          1.00905874, 1.00904577, 1.00903281, 1.00901987, 1.00900695,
          1.00899405, 1.00898117, 1.0089683, 1.00895545, 1.00894263,
          1.00892982, 1.00891703, 1.00890425, 1.0088915, 1.00887876,
          1.00886604, 1.00885334, 1.00884066, 1.008828, 1.00881535,
          1.00880273, 1.00879012, 1.00877753, 1.00876495, 1.0087524,
          1.00873986, 1.00872734, 1.00871484, 1.00870236, 1.00868989,
          1.00867745, 1.00866502, 1.0086526, 1.00864021, 1.00862783,
          1.00861548, 1.00860313, 1.00859081, 1.00857851, 1.00856622,
          1.00855395, 1.00854169, 1.00852946, 1.00851724, 1.00850504,
          1.00849286]
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
    hs = [0., 0.1, 0.19683772, 0.29240108, 0.38699367,
          0.48077279, 0.57383901, 0.66626379, 0.7581013, 0.84939439,
          0.94017814, 1.00910252, 0.99905711, 0.99114261, 1.00097396,
          0.99096909, 1.00282833, 0.9928142, 0.99984458, 0.99020706,
          1.00389201, 0.99387257, 0.9982221, 0.99254535, 0.99714517,
          0.99396564, 0.99239907, 0.99785252, 0.99292614, 0.99571128,
          0.99621462, 0.99604606, 0.99599711, 0.99636957, 0.99584547,
          0.99540881, 0.99628326, 0.9958598, 0.99563976, 0.99647749,
          0.99558237, 0.99487547, 0.99640354, 0.99554199, 0.99502145,
          0.99664833, 0.99516949, 0.99403331, 0.99657901, 0.99508644,
          0.99412592, 0.9968738, 0.9946383, 0.99293278, 0.99677341,
          0.99458186, 0.99313168, 0.99710738, 0.99411248, 0.99207507,
          0.99718079, 0.99384357, 0.99267747, 0.99841904, 0.99215365,
          0.9981556, 0.99247507, 0.9970843, 0.99404405, 0.99212263,
          0.99739106, 0.99354894, 0.99365447, 0.99979836, 0.99027771,
          1.00370579, 0.99368728, 0.99850158, 0.99211858, 0.99839822,
          0.99213656, 0.99812979, 0.99250932, 0.99697444, 0.99421086,
          0.99225114, 0.99712126, 0.99395585, 0.99235343, 0.99783035,
          0.99295243, 0.99561928, 0.99636562, 0.99576751, 0.99534117,
          0.99640928, 0.9956327, 0.99509728, 0.99650004, 0.99542947,
          0.99466651]
    hmax = 0
    universe_scale = 1
    mnoznik = 10
    universe = np.linspace(-universe_scale, universe_scale, 5)
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

        mnoznik = float(request.form['mnoznik'])
        universe_scale = float(request.form['skala'])

        kp = float(request.form['kp'])
        kd = float(request.form['kd'])

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

            # Kp
            sim.input['error'] = kp * e
            # Kd
            sim.input['delta'] = kd * (e_next - e)/dt
            sim.compute()
            Qd = mnoznik * sim.output['output']
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
        return render_template('fuzzy.html', max=hmax + 1, labels=ts, values=hs, b=b, A=A, Qd=Qd, Qmax=Qmax, dt=dt, tf=tf, hz=hz, hmax=hmax, universe_scale=universe_scale, mnoznik=mnoznik, kp=kp, kd=kd)
    else:
        # GET aka first load
        return render_template('fuzzy.html', max=hmax + 1, labels=ts, values=hs)


if __name__ == '__main__':
    app.run(debug=True)
