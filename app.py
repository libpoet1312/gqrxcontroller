from flask import Flask, render_template, request, redirect
from telnet import TelnetClient

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = ''

MODULATIONS = ['FM', 'AM', 'NFM', 'WFM_ST', 'WFM_ST_OIRT', 'WFM']

telnet_client = TelnetClient()


@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'GET':
        return render_template('index.html', active=telnet_client.client)
    else:
        connect_to_server = request.form['connect']
        if connect_to_server == '1':
            telnet_client.connect()
            return redirect('/control')
        else:
            telnet_client.close()
            return ''


@app.route('/control', methods=['GET', 'POST'])
async def control():
    if not telnet_client.client:
        return redirect('/')

    if not telnet_client.client:
        freq = None
        mod = None
    else:
        freq = await telnet_client.get_freq()
        mod = await telnet_client.get_mod()

    if request.method == 'POST':
        (new_mod, new_freq) = (request.form.get('mod', None), request.form.get('freq', None))
        if new_mod != mod:
            res = await telnet_client.send('M', new_mod)
            if '0' in res:
                print('mod ok')
                mod = new_mod
            else:
                print('freq error')
        if new_freq != freq:
            res = await telnet_client.send('F', new_freq)
            if '0' in res:
                print('freq ok')
                freq = new_freq
            else:
                print('mod error')

    return render_template('control.html', active=telnet_client.client, mods=MODULATIONS, freq=freq, mod=mod)


if __name__ == '__main__':
    app.run(
        debug=True,
    )
