from dashapp import app, FIGS
import webbrowser

def main():
    url = 'http://127.0.0.1:8050/'
    webbrowser.open(url)
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
