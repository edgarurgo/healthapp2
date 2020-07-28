import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.core.window import Window
from datetime import datetime

kivy.config.Config.set('graphics', 'resizable',False)     #used for screen size
currentuser = {'id':'99', 'username':'default', 'name':'default','last':'default','email':'default','password':'default'}
userdata = ('username','name','last','email','password')
today = datetime.today().strftime('%Y-%m-%d')

class WindowManager(ScreenManager):
    manager_name = StringProperty('None')
    manager_last = StringProperty('None')

class LogInWindow(Screen):
    username = StringProperty(None)
    password = StringProperty(None)

    def validate_user(self,**kwargs):
        global currentuser
        self.username = self.ids.first_text.text
        self.password = self.ids.second_text.text

        # In this part of the code the username and password will be verified against the database
        if self.username == '' or self.password == '':
            self.ids.first_label.text = '[color=ff0000]Both fields are required to continue[/color]'
        else:
            self.ids.first_label.text = ''
            try:
                sqlcnx = sqlite3.connect('healthapp.db')
                sqlcursor = sqlcnx.cursor()
                print('Successfully Connected to DB')
            except sqlite3.Error as error:
                print('Error while connecting to sqlite', error)
                self.ids.first_label.text = '[color=ff0000]Error while connecting to DB[/color]'
            finally:
                if sqlcnx:
                    try:
                        sqlcursor.execute('SELECT * FROM users WHERE username = ?;', (self.username,))
                        queryresult = sqlcursor.fetchall()

                        for item in queryresult:
                            x = 0
                            for i in item:
                                currentuser[userdata[x]] = i
                                x += 1
                        if queryresult == []:
                            self.ids.first_label.text = '[color=ff0000]Username does not exist[/color]'
                        elif currentuser['password'] != self.password:
                            self.ids.first_label.text = '[color=ff0000]Password is incorrect[/color]'
                        else:
                            self.ids.first_text.text = ''
                            self.ids.second_text.text = ''
                            self.manager.manager_name = currentuser['name'].capitalize()
                            self.manager.manager_last = currentuser['last'].capitalize()
                            self.manager.transition.direction = "left"
                            self.manager.current = 'windowmain'

                        sqlcursor.close()
                        sqlcnx.close()
                    except sqlite3.Error as error:
                        print('Error while query:', error)
                        qlcursor.close()
                        sqlcnx.close()

class NewUserWindow(Screen):
    def create_newuser(self):
        newusername = self.ids.newusername.text
        newname = self.ids.newname.text
        newlast = self.ids.newlast.text
        newemail = self.ids.newemail.text
        newpassword = self.ids.newpassword.text
        newrepassword = self.ids.newrepassword.text

        if newusername == '' or newname == '' or newlast == '' or newemail == '' \
                or newpassword == '' or newrepassword == '':
            self.ids.newuserstatus.text = '[color=ff0000]All fields are required to Continue[/color]'

        else:
            if newpassword != newrepassword:
                self.ids.newuserstatus.text = '[color=ff0000]Mismatch in Password, Try again[/color]'
            else:
                try:
                    sqlcnx = sqlite3.connect('Healthapp.db')
                    sqlcursor = sqlcnx.cursor()
                    print('Successfully connected to database')
                except sqlite3.Error as error:
                    print('Error while connecting to sqlite:', error)
                    self.ids.newuserstatus.text = '[color=ff0000]Error while doing Query[/color]'
                finally:
                    if sqlcnx:
                        try:
                            sqlcursor.execute('SELECT name FROM users WHERE username = ?;', (newusername,))
                            searchresult = sqlcursor.fetchall()

                            if searchresult == []:
                                newuserdata = (newusername, newname, newlast, newemail, newpassword)
                                sqlcursor.execute('INSERT INTO users(username, name, last, email, password) VALUES (?, ?, ?, ?, ?);', newuserdata)
                                sqlcnx.commit()
                                self.ids.newuserstatus.text = '[color=00ff00]New User Created[/color]'
                                sqlcursor.close()
                                sqlcnx.close()
                                self.ids.newusername.text = ''
                                self.ids.newname.text = ''
                                self.ids.newlast.text = ''
                                self.ids.newemail.text = ''
                                self.ids.newpassword.text = ''
                                self.ids.newrepassword.text = ''

                            else:
                                self.ids.newuserstatus.text = '[color=ff0000]Username already exists[/color]'
                                sqlcursor.close()
                                sqlcnx.close()

                        except sqlite3.Error as error:
                            print('Error while INSERTING data:', error)
                            sqlcursor.close()
                            sqlcnx.close()

class MainWindow(Screen):
    def update_currentuser(self):
        global today
        todaystart = str(today) + ' 00:00:01'
        todayend = str(today) + ' 23:59:59'
        print(todaystart)
        print(todayend)
        calories = 0
        try:
            sqlcnx = sqlite3.connect('Healthapp.db')
            sqlcursor = sqlcnx.cursor()
            print('Successfully connected to database')
        except sqlite3.Error as error:
            print('Error while connecting to database:', error)
            self.ids.status_temp.text = 'Error while connecting to DB'
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute("SELECT calories FROM consumption WHERE date BETWEEN ? AND ? ;", (todaystart, todayend))

                    for cal in sqlcursor:
                        calories += cal[0]

                    self.ids.current_calories.text = str(calories)

                    sqlcursor.close()
                    sqlcnx.close()

                except sqlite3.Error as error:
                    print ('Error while doint query:', error)
                    self.ids.status_temp.text = 'Error while doing query'
                    sqlcursor.close()
                    sqlcnx.close()

class MealWindow_egg(Screen):
    def inserteggmeal(self):
        meal = 'egg sandwich'
        calories = 408
        try:
            sqlcnx = sqlite3.connect('Healthapp.db')
            sqlcursor = sqlcnx.cursor()
        except sqlite3.Error as error:
            print ('Error while connecting to database:', error)
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (?,?,?);', (currentuser['username'], meal, calories))
                    sqlcnx.commit()
                    sqlcursor.close()
                    sqlcnx.close()
                    self.ids.eggstatus.text = '[color=00ff00]Meal Added[/color]'
                except sqlite3.Error as error:
                    print('Error while doing INSERT:', error)
                    sqlcursor.close()
                    sqlcnx.close()

class MealWindow_oat(Screen):
    def insertoatmeal(self):
        meal = 'overnight oats'
        calories = 483
        try:
            sqlcnx = sqlite3.connect('Healthappdb')
            sqlcursor = sqlcnx.cursor()
        except sqlite3.Error as error:
            print('Error while connecting to database:', error)
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (?, ?, ?);', (currentuser['username'], meal, calories))
                    sqlcnx.commit()
                    sqlcursor.close()
                    sqlcnx.close()
                    self.ids.oatstatus.text = '[color=00ff00]Meal Added[/color]'
                except sqlite3.Error as error:
                    print('Error while doing INSERT:', error)
                    sqlcursor.close()
                    sqlcnx.close()

class MealWindow_rice(Screen):
    def insertricemeal(self):
        meal = 'beans with rice'
        calories = 265
        try:
            sqlcnx = sqlite3.connect('Healthapp.db')
            sqlcursor = sqlcnx.cursor()
        except sqlite3.Error as error:
            print('Error while connecting to database:', error)
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (?, ?, ?);', (currentuser['username'], meal, calories))
                    sqlcnx.commit()
                    sqlcursor.close()
                    sqlcnx.close()
                    self.ids.ricestatus.text = '[color=00ff00]Meal Added[/color]'
                except sqlite3 as error:
                    print('Error while doing INSERT:', error)
                    sqlcursor.close()
                    sqlcnx.close()

class MealWindow_tuna(Screen):
    def inserttunameal(self):
        meal = 'tuna salad'
        calories = 375
        try:
            sqlcnx = sqlite3.connect('Healthapp.db')
            sqlcursor = sqlcnx.cursor()
        except sqlite3.Error as error:
            print('Error while connecting to database:', error)
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (?, ?, ?);', (currentuser['username'], meal, calories))
                    sqlcnx.commit()
                    sqlcursor.close()
                    sqlcnx.close()
                    self.ids.tunastatus.text = '[color=00ff00]Meal Added[/color]'
                except sqlite3.Error as error:
                    print('Error while doing INSERT:', error)
                    sqlcursor.close()
                    sqlcnx.close()

class MealWindow_galleta(Screen):
    def insertgalletameal(self):
        meal = 'galleta lenteja'
        calories = 130
        try:
            sqlcnx = sqlite3.connect('Healthapp.db')
            sqlcursor = sqlcnx.cursor()
        except sqlite3.Error as error:
            print('Error while connecting to database:', error)
        finally:
            if sqlcnx:
                try:
                    sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (? ,? ,?);', (currentuser['username'], meal, calories))
                    sqlcnx.commit()
                    sqlcursor.close()
                    sqlcnx.close()
                    self.ids.galletastatus.text = '[color=00ff00]Meal Added[/color]'
                except sqlite3.Error as error:
                    print('Error while doing INSERT:', error)
                    sqlcursor.close()
                    sqlcnx.close()

class AddNewMealWindow(Screen):
    def insert_newmeal(self):
        if self.ids.newmealname.text == '' or self.ids.newmealcalories.text == '':
            self.ids.newmealstatus.text = '[color=ff0000]Both fields are required to continue[/color]'
        else:
            try:
                sqlcnx = sqlite3.connect('Healthapp.db')
                sqlcursor = sqlcnx.cursor()
            except sqlite3.Error as error:
                print('Error while connecting to database', error)
                self.ids.newmealstatus.text = '[color=ff0000]Connection error[/color]'
            finally:
                if sqlcnx:
                    try:
                        sqlcursor.execute('INSERT INTO consumption (username, foodname, calories) VALUES (?, ?, ?);',(currentuser['username'], self.ids.newmealname.text, self.ids.newmealcalories.text))
                        sqlcnx.commit()
                        sqlcursor.close()
                        sqlcnx.close()
                        self.ids.newmealstatus.text = '[color:00ff00]Added Successfully[/color]'
                    except sqlite3.Error as error:
                        print('Error while INSERT:', error)
                        self.ids.newmealstatus.text = 'Error while INSERT'
                        sqlcursor.close()
                        sqlcnx.close()

kv = Builder.load_file('health.kv')

class HealthApp(App):
    def build(self):
        Window.size = (450, 800)
        return kv

if __name__ == "__main__":
    HealthApp().run()

