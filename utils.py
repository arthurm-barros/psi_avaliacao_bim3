from flask import session, redirect, url_for

def proteger_com_login(callback):
    def wrapper(*args, **kwargs):
        if 'usuario_id' in session:
            return callback(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return wrapper