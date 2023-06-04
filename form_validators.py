import datetime as dt
from flask import flash, render_template

class FormValidator():
    def __init__(self, file, filename:str, prepare_date:str, finish_date:str, is_urgent:bool) -> None:
        self.file = file
        self.filename = filename
        self.prepare_date = prepare_date
        self.finish_date = finish_date
        self.is_urgent = is_urgent

    def is_empty(self, field) -> bool:
        return not bool(field)

    def is_file_format_correct(self) -> bool:
        file_format = self.filename.split('.')[-1]
        if file_format == 'xls':
            return True
        else:
            return False
        
    def is_date_correct(self, date: str) -> bool:
        dl = date.split("-")
        given_date = dt.date(int(dl[0]), int(dl[1]), int(dl[2]))
        if given_date >= dt.date.today():
            return True
        else:
            return False

    def validate_form(self) -> render_template():
        if self.is_empty(self.file):
            flash("Musisz wybrac plik do zaladowania.", 'Error')
            return render_template('home.html')

        if not self.is_file_format_correct():
            flash('Wybrany plik musi byc arkuszem Excel o formacie .xls.', 'Error')
            return render_template('home.html')
        
        if not self.is_empty(self.finish_date):
            if not self.is_date_correct(self.finish_date):
                flash('Data zakonczenia obrobki nie moze byc wczesniejsza niz dzisiaj.', 'Error')
                return render_template('home.html')

        if not self.is_empty(self.finish_date):
            if not self.is_date_correct(self.prepare_date):
                flash('Data przygotowania materialow nie moze byc wczesniejsza niz dzisiaj.' 'Error')
                return render_template('home.html')

        if self.is_empty(self.finish_date):
            flash('Plik wygenerowano bez daty zakonczenia obrobki', 'Alert')
            if self.is_empty(self.prepare_date):
                flash('Plik wygenerowano bez daty przygotowania materialu', 'Alert')
            return None