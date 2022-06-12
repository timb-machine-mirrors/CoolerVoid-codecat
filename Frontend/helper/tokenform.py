from wtforms.csrf.core import CSRF
from hashlib import sha512
import datetime
import os

class Ice_CSRF(CSRF):
    def deadspread_2minutes(self, min):
       second=min
       if second & 1:
           return min
       else:
           t=datetime.datetime.now() - datetime.timedelta(minutes=2)
           return t.minute

    def cmp_token_range_5min(self, input_token):
        now = datetime.datetime.now()
        time_list=[]
        count=5
        while count != -1:
            time_list.append(datetime.datetime.now() - datetime.timedelta(minutes=count))
            count-=1
        for time2test in time_list:
            token = str(sha512((os.environ['CODECAT_CSRF_KEY'] + self.csrf_context+ str(time2test.minute)+str(time2test.hour)).encode('utf-8')).hexdigest()) 
            if token == input_token:
                return True
        return False


    def setup_form(self, form):
        self.csrf_context = form.meta.csrf_context
        return super(Ice_CSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token):
        now = datetime.datetime.now()
        #minutes=str(self.deadspread_2minutes(now.minute)
        token = sha512((os.environ['CODECAT_CSRF_KEY'] + self.csrf_context+ str(now.minute)+str(now.hour)).encode('utf-8')).hexdigest()
        return token

    def validate_csrf_token(self, form, field):
        if self.cmp_token_range_5min(str(field.data)) == False:
            #if field.data != field.current_token:
            raise ValueError('Invalid CSRF')
