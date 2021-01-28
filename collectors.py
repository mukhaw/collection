
import tkinter as tk
from tkinter import Menu,ttk
import sqlite3
from tkinter import messagebox
from lxml import ElementInclude
import xml.etree.ElementTree as xml
import webbrowser as wb
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root=root
        self.init_main()
        self.db = db
        self.xml_list=[]
        self.view_records()

    def init_main(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Точно хотите уйти?((", command=self.onExit)
        findMenu = Menu(menubar)
        findMenu.add_command(label="Найти марки каких стран содержатся в коллекции", command = self.doc_1)
        findMenu.add_command(label="Найти в каких местах коллекции находятся марки указанной серии",command = self.doc_2)
        findMenu.add_command(label="Найти названия коллекций и количество страниц в каждой коллекции", command = self.doc_3)
        findMenu.add_command(label="Найти марка какой страны и какой серии находится "
                                   "в указанном месте коллекции место в коллекции", command = self.doc_4)
        corrMenu=Menu(menubar)
        corrMenu.add_command(label="Страну",command=self.open_dialog_for_corr)
        corrMenu.add_command(label="Коллекцию", command=self.open_dialog_for_corr_col)
        corrMenu.add_command(label="Серию", command=self.open_dialog_for_corr_ser)
        corrMenu.add_command(label="Место", command=self.open_dialog_for_corr_pl)
        corrMenu.add_command(label="Количество", command=self.open_dialog_for_corr_q)

        renameMenu = Menu(menubar)
        renameMenu.add_command(label = "Коллекцию",command=self.rename_col)
        renameMenu.add_command(label = "Серию", command = self.rename_ser)
        menubar.add_cascade(label="Добавить новую марку",command=self.open_dialog_for_add)
        menubar.add_cascade(label="Изменить",menu = corrMenu)
        menubar.add_cascade(label="Удалить",command=self.delete_records)
        menubar.add_cascade(label="Найти",menu=findMenu)
        menubar.add_cascade(label="Сформировать xml", command = self.create_xml)
        menubar.add_cascade(label="Выйти", command=self.onExit,menu=fileMenu)
        menubar.add_cascade(label="Переименовать", menu=renameMenu)

        self.tree = ttk.Treeview(self, columns=('marks name', 'country', 'collection', 'series', 'place','quantity'),
                                 height=20, show='headings')
        self.tree.column("marks name", stretch=tk.NO, minwidth=100, width=200)
        self.tree.column("country", stretch=tk.NO, minwidth=50, width=100)
        self.tree.column("collection", stretch=tk.NO, minwidth=50, width=100)
        self.tree.column("series", stretch=tk.NO, minwidth=30, width=100)
        self.tree.column("place", stretch=tk.NO, minwidth=30, width=50)
        self.tree.column("quantity",stretch=tk.NO, minwidth=30, width=100)

        self.tree.heading("marks name", text='Номер марки')
        self.tree.heading("country", text='Страна')
        self.tree.heading("collection", text='Коллекция')
        self.tree.heading("series", text='Серия')
        self.tree.heading("place", text='Место')
        self.tree.heading("quantity", text='Количество')


        self.tree.pack()

    def records(self,marks_name,country,collection,series,place,quantity):
        self.db.c.execute("""SELECT place from marks where collection=?""",(collection.title(),))
        pl_list = self.db.c.fetchall()
        pl_list2 =[]
        for i in range(len(pl_list)):
            pl_list2.append(pl_list[i][0])


        if not marks_name.isdigit()or not place.isdigit()or not quantity.isdigit()  or not country.isalpha() or not collection.isalpha() or not series.isalpha():
            messagebox.showinfo("Ошибка", "Неверные данные в полях "
                                          "В поле номер марки, место в коллекции, количество страниц в коллекции"
                                          "должны быть только цифры, в остальных полях только буквы(Желательно связный текст)")

        else:
            self.db.insert_data(marks_name, country.title(), collection.title(), series.title(), place, quantity)
            self.view_records()
            self.db.insert_col(collection.title(),quantity)



    def update_record1(self,country):
        if not country.isalpha() or country.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute(
                '''UPDATE marks SET country=? WHERE marks_name=?''',
                (country.title(), self.tree.set(self.tree.selection()[0], '#1')))
            self.db.conn.commit()
            self.view_records()




    def update_record_col(self,column_name):
        if not column_name.isalpha() or column_name.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute(
                '''UPDATE marks SET collection=? WHERE marks_name=?''',
                (column_name.title(), self.tree.set(self.tree.selection()[0], '#1')))
            self.db.conn.commit()
            self.view_records()



    def update_record_ser(self,column_name):

        if not column_name.isalpha() or column_name.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute(
                '''UPDATE marks SET series=? WHERE marks_name=?''',
                (column_name.title(), self.tree.set(self.tree.selection()[0], '#1')))
            self.db.conn.commit()
            self.view_records()

    def update_record_pl(self, column_name):

        if not column_name.isdigit():
                    messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
         self.db.c.execute(
                        '''UPDATE marks SET place=? WHERE marks_name=?''',
                        (column_name.title(), self.tree.set(self.tree.selection()[0], '#1')))
         self.db.conn.commit()
         self.view_records()

    def update_record_q(self, column_name):

        if not column_name.isdigit():
                    messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
         self.db.c.execute(
                        '''UPDATE marks SET quantity=? WHERE marks_name=?''',
                        (column_name.title(), self.tree.set(self.tree.selection()[0], '#1')))
         self.db.conn.commit()
         self.view_records()
    def find_country(self,collection):
        if not collection.isalpha():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute('''SELECT country FROM marks WHERE collection=?''',(collection.title(),))
            messagebox.showinfo("Страны", set(self.db.c.fetchall()))

    def find_place(self,collection,series):
        if not collection.isalpha() or not series.isalpha():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute('''SELECT place FROM marks WHERE collection=? AND series=?''', (collection.title(),series.title()))
            messagebox.showinfo("Место", set(self.db.c.fetchall()))

    def find_country_and_series(self,collection,place):
        if not collection.isalpha() or not place.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute('''SELECT country,series FROM marks WHERE collection=? AND place=?''', (collection.title(),place))
            messagebox.showinfo("Страна и серия", set(self.db.c.fetchall()))
    def rename_collection(self,collection, collection_1):
        if not collection.isalpha() or collection.isdigit() or not collection_1.isalpha() or collection_1.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute(
                '''UPDATE collection1 SET collection=? WHERE collection=?''',
                (collection_1.title(), collection.title()),)
            self.db.c.execute('''UPDATE marks SET collection=? WHERE collection=?''',(collection_1.title(), collection.title(),))
            self.db.conn.commit()
            self.view_records()
    def rename_series(self,series,series_1):
        if not series.isalpha() or series.isdigit() or not series_1.isalpha() or series_1.isdigit():
            messagebox.showinfo("Ошибка", "Неверные данные ")
        else:
            self.db.c.execute(
                '''UPDATE series SET series=? WHERE series=?''',
                (series_1.title(), series.title()),)
            self.db.c.execute('''UPDATE marks SET series=? WHERE series=?''',(series_1.title(), series.title(),))
            self.db.conn.commit()
            self.view_records()


    def view_records(self):
        self.db.c.execute('''SELECT * FROM marks''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]



    def onExit(self):
        self.quit()

    def open_dialog_for_add(self):
        ADD()
    def open_dialog_for_corr(self):
        Update()
    def open_dialog_for_corr_col(self):
        Update1()
    def open_dialog_for_corr_ser(self):
        Update2()
    def open_dialog_for_corr_pl(self):
        Update3()
    def open_dialog_for_corr_q(self):
        Update4()
    def doc_1(self):
        For_collection()
    def doc_2(self):
        For_place()
    def doc_3(self):
            self.db.c.execute('''SELECT collection, quantity FROM marks''')
            messagebox.showinfo("Коллекции и количество", set(self.db.c.fetchall()))
    def doc_4(self):
        For_series()

    def rename_col(self):
        for_coll()

    def rename_ser(self):
        for_ser()
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM marks WHERE marks_name=?''', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    def create_xml(self):
        self.db.c.execute('''SELECT * FROM marks''')
        self.xml_list = self.db.c.fetchall()
        root = xml.Element("Marks_for_collector")

        for row in range(len(self.xml_list)):
            appt = xml.Element("mark", id=str(self.xml_list[row][0]))
            root.append(appt)
            country = xml.SubElement(appt, "country")
            country.text = self.xml_list[row][1]

            collection = xml.SubElement(appt, "collection")
            collection.text = self.xml_list[row][2]

            series = xml.SubElement(appt, "series")
            series.text = self.xml_list[row][3]

            place = xml.SubElement(appt, "place")
            place.text = str(self.xml_list[row][4])

            quantity = xml.SubElement(appt, "quantity")
            quantity.text = str(self.xml_list[row][5])

        tree = xml.ElementTree(root)
        open("marks.xml", "w")
        tree.write("marks.xml")
        wb.open("C:\\Users\\mi\\PycharmProjects\\oop_lab2\\marks.xml",new=2)


class ADD(tk.Toplevel):
            def __init__(self):
                super().__init__(root)
                self.init_child()
                self.view = app

            def init_child(self):
                self.title('Добавить данные')
                self.geometry('400x300+400+300')
                self.resizable(False, False)

                label_marks_name = tk.Label(self, text='Номер марки:')
                label_marks_name.place(x=50, y=50)
                label_country = tk.Label(self, text='Страна:')
                label_country.place(x=50, y=80)
                label_collection = tk.Label(self, text='Коллекция:')
                label_collection.place(x=50, y=110)
                label_series = tk.Label(self, text='Серия:')
                label_series.place(x=50, y=140)
                label_place = tk.Label(self, text='Место:')
                label_place.place(x=50, y=170)
                label_quantity= tk.Label(self, text='Колисечтво страниц в коллекции:')
                label_quantity.place(x=50, y=210)


                self.entry_marks_name = ttk.Entry(self)
                self.entry_marks_name.place(x=250, y=50)

                self.entry_country = ttk.Entry(self)
                self.entry_country.place(x=250, y=80)

                self.entry_collection = ttk.Entry(self)
                self.entry_collection.place(x=250, y=110)

                self.entry_series = ttk.Entry(self)
                self.entry_series.place(x=250, y=140)

                self.entry_place = ttk.Entry(self)
                self.entry_place.place(x=250, y=170)

                self.entry_quantity = ttk.Entry(self)
                self.entry_quantity.place(x=250, y=210)

                btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
                btn_cancel.place(x=130, y=240)

                self.btn_ok = ttk.Button(self, text='Добавить')
                self.btn_ok.place(x=50, y=240)

                self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_marks_name.get(),
                                                                          self.entry_country.get(),
                                                                          self.entry_collection.get(),
                                                                          self.entry_series.get(),
                                                                          self.entry_place.get(),
                                                                          self.entry_quantity.get()))



                self.grab_set()
                self.focus_set()

class Update(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('200x100+400+300')

        #label_country = tk.Label(self, text='Номер марки:')
        #label_country.place(x=10, y=20)
        label_country = tk.Label(self, text='Страна:')
        label_country.place(x=10, y=20)

        #self.entry_marks_name = ttk.Entry(self)
        #self.entry_marks_name.place(x=60, y=20)
        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=60, y=20)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=10, y=50)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record1(self.entry_country.get()))

class Update1(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('220x90+400+300')

        label_country = tk.Label(self, text='Коллекция:')
        label_country.place(x=10, y=20)


        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=10, y=50)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record_col(self.entry_country.get()))

class Update2(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('220x90+400+300')

        label_country = tk.Label(self, text='Серия:')
        label_country.place(x=10, y=20)


        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=10, y=50)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record_ser(self.entry_country.get()))

class Update3(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('220x90+400+300')

        label_country = tk.Label(self, text='Место:')
        label_country.place(x=10, y=20)


        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=10, y=50)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record_pl(self.entry_country.get()))

class Update4(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('220x90+400+300')

        label_country = tk.Label(self, text='Количество:')
        label_country.place(x=10, y=20)


        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=10, y=50)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record_q(self.entry_country.get()))

class For_collection(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Найти марки каких стран содержатся в коллекции')
        self.geometry('320x90+400+300')

        label_country = tk.Label(self, text='Коллекция:')
        label_country.place(x=10, y=20)


        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)

        btn_pdf = ttk.Button(self, text='Узнать')
        btn_pdf.place(x=10, y=50)
        btn_pdf.bind('<Button-1>', lambda event: self.view.find_country(self.entry_country.get()))

class for_coll(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Переименовать коллекцию')
        self.geometry('320x110+400+300')

        label_country = tk.Label(self, text='Переименовать коллекцию в :')
        label_country.place(x=10, y=20)

        label_series = tk.Label(self, text='Коллекцию:')
        label_series.place(x=10, y=50)

        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=180, y=20)

        self.entry_series = ttk.Entry(self)
        self.entry_series.place(x=180, y=50)

        btn_pdf = ttk.Button(self, text='Переименовать')
        btn_pdf.place(x=10, y=80)
        btn_pdf.bind('<Button-1>', lambda event: self.view.rename_collection(self.entry_country.get(),self.entry_series.get()))

class for_ser(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Переименовать коллекцию')
        self.geometry('320x110+400+300')

        label_country = tk.Label(self, text='Переименовать серию в :')
        label_country.place(x=10, y=20)

        label_series = tk.Label(self, text='Серию:')
        label_series.place(x=10, y=50)

        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=180, y=20)

        self.entry_series = ttk.Entry(self)
        self.entry_series.place(x=180, y=50)

        btn_pdf = ttk.Button(self, text='Переименовать')
        btn_pdf.place(x=10, y=80)
        btn_pdf.bind('<Button-1>', lambda event: self.view.rename_series(self.entry_country.get(),self.entry_series.get()))

class For_place(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Найти в каких местах коллекции находятся марки указанной серии')
        self.geometry('300x110+400+300')

        label_country = tk.Label(self, text='Коллекция:')
        label_country.place(x=10, y=20)

        label_series = tk.Label(self, text='Серия:')
        label_series.place(x=10, y=50)

        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)
        self.entry_series = ttk.Entry(self)
        self.entry_series.place(x=80, y=50)

        btn_pdf = ttk.Button(self, text='Узнать')
        btn_pdf.place(x=10, y=80)
        btn_pdf.bind('<Button-1>', lambda event: self.view.find_place(self.entry_country.get(),self.entry_series.get()))

class For_series(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
    def init_edit(self):
        self.title('Найти в каких местах коллекции находятся марки указанной серии')
        self.geometry('300x110+400+300')

        label_country = tk.Label(self, text='Коллекция:')
        label_country.place(x=10, y=20)

        label_series = tk.Label(self, text='Место:')
        label_series.place(x=10, y=50)

        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=80, y=20)
        self.entry_series = ttk.Entry(self)
        self.entry_series.place(x=80, y=50)

        btn_pdf = ttk.Button(self, text='Узнать')
        btn_pdf.place(x=10, y=80)
        btn_pdf.bind('<Button-1>', lambda event: self.view.find_country_and_series(self.entry_country.get(),self.entry_series.get()))

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('marks.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS marks ( ID integer primary key,marks_name text, country text, collection text, series text,place integer,quantity integer)''')
        self.conn.commit()
    def insert_data(self,marks_name,country,collection,series,place,quantity):
        self.c.execute(
            """INSERT INTO marks(marks_name,country,collection,series,place,quantity) VALUES(?,?,?,?,?,?)""",(marks_name,country,collection,series,place,quantity)
        )
        self.conn.commit()
    def insert_col(self,collection,quantity):
        self.c.execute("""insert into collection1(collection,quantity)  values(?,?)""", (collection, quantity))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Марки")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()






