

def load(path):
    try:
        f = open(path)
        lines = f.readlines()
        f.close()
        return ''.join(lines)
    except FileNotFoundError:
        return ''
    
dire = 'css'

MAIN_BUTTONS_CSS = load(dire + '/main_button.css')
EVENT_LABEL_CSS = load('css' + '/event_label.css')
CALENDAR_CSS = load(dire + '/calendar.css')
TIME_TAPE_CSS = load(dire + '/time_tape.css')
MAIN_WINDOW_CSS = load(dire + '/main_window.css')