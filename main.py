from flask import Flask, render_template, request

app = Flask(__name__)

modes = ['Startup', 'Static', 'Loop', 'Automatic', 'Sound']
funcs = ['Slow Fade', 'Fast Fade', 'Strobe']


@app.route("/", methods=['GET', 'POST'])
def index():
    red = 0
    yellow = 0
    green = 0
    strobe = 0
    sensivity = 0

    if request.method == 'POST':
        print(request.form)
        if request.form.get('mode'):
            selected_mode = request.form.get('mode')
            modes.remove(selected_mode)
            modes.insert(0, selected_mode)
            if selected_mode == "Startup":
                pass
            elif selected_mode == "Static":
                red = request.form.get('red')
                yellow = request.form.get('yellow')
                green = request.form.get('green')
            elif selected_mode == "Loop":
                selected_func = request.form.get('func')
                if not selected_func:
                    selected_func = funcs[0]
                funcs.remove(selected_func)
                funcs.insert(0, selected_func)
                strobe = request.form.get('strobe')
            elif selected_mode == "Automatic":
                pass
            elif selected_mode == "Sound":
                sensivity = request.form.get('sensivity')
            return render_template('index.html', modes=modes, funcs=funcs, red=red, yellow=yellow, green=green, strobe=strobe, sensivity=sensivity)
        else:
            pass
        return render_template('index.html', modes=modes, funcs=funcs, red=red, yellow=yellow, green=green, strobe=strobe, sensivity=sensivity)
    elif request.method == 'GET':
        return render_template('index.html', modes=modes, funcs=funcs, red=red, yellow=yellow, green=green, strobe=strobe, sensivity=sensivity)

    return render_template('index.html', modes=modes, funcs=funcs, red=red, yellow=yellow, green=green, strobe=strobe,
                           sensivity=sensivity)


if __name__ == '__main__':
    app.run(port=80)
