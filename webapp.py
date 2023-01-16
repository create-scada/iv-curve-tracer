from microdot import Microdot

def create_webapp(iv_curve_tracer):
    
    app = Microdot()

    @app.route('/')
    def index(request):
        return 'Hello, world!'

    @app.route('/run')
    def run(request):
        
        results = iv_curve_tracer.run()

        with open('num.txt') as f:
            num = f.read()
            num = num.strip()
            num = int(num)
            num += 1

        try:

            with open('num.txt', 'w') as f:
                f.write(str(num))

            with open(f'/data/reading{num}.csv', 'w') as fp:

                fp.write('Voltage, Current\n')

                for (voltage, current) in results:
                    line = f'{voltage},{current}\n'
                    fp.write(line)

                fp.flush()
        except Exception as e:

            print(e)
            time.sleep(3)

        else:

            led.value(True)
            time.sleep(3)

        return 'Complete'

    return app
