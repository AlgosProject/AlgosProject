from flask import session, redirect, url_for


def check_session():
    if session.get('logged_in'):
        return False
    return redirect(url_for("login_form.login_form"))
