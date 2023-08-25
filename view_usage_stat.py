from Tkinter import Tk
import tkFileDialog
import ttk
import sqlite3
import os
import csv

class UsageStatUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.dbpath   = 'C:/' # <------ path to save database file. same as in "LayoutTool/scriptUsage.py"
        self.dbfile   = 'layouttool_script_usage.db'
        self.order    = 'id'
        self.suborder = 'script'
        self.colums   = ('id', 'timestamp', 'user', 'script', 'runfrom', 'filename')

        self.title('Layout Statistic')
        self.geometry('800x600+500+300')

        app_frm = ttk.Frame(self)
        app_frm.pack(fill='both', expand=True, padx=10, pady=10)

        # create functions widget
        self.func_frm = ttk.Frame(app_frm)
        self.func_frm.pack(fill='x')
        ttk.Label(self.func_frm, text='Month:').pack(side='left')
        self.month_ls_cmb = ttk.Combobox(self.func_frm, width=10)
        self.month_ls_cmb.pack(side='left', pady = 10, padx=5)
        ttk.Label(self.func_frm, text='Year:').pack(side='left')
        self.year_ls_cmb = ttk.Combobox(self.func_frm, width=10)
        self.year_ls_cmb.pack(side='left', pady = 10, padx=5)

        self.export_btn = ttk.Button(self.func_frm, text='Export CSV', 
                                     width = 15, command=self.exportCsv)
        self.export_btn.pack(side='right', pady = 10)
        self.sel_count_l = ttk.Label(self.func_frm, text='Selected rows: 0')
        self.sel_count_l.pack(side='right', padx=(5,15))
        self.subsort_cmb = ttk.Combobox(self.func_frm, width=10)
        self.subsort_cmb.pack(side='right', pady = 10, padx=5)
        ttk.Label(self.func_frm, text='Subsort:').pack(side='right')
        self.sort_cmb = ttk.Combobox(self.func_frm, width=10)
        self.sort_cmb.pack(side='right', pady = 10, padx=5)
        ttk.Label(self.func_frm, text='Sort:').pack(side='right')

        # create table widget
        self.table_frm = ttk.Frame(app_frm)
        self.table_frm.pack(fill='both', expand=True)
        col_w    = 70
        col_ls   = ('ID', 'Date/Time', 'User', 'Script', 'Run From', 'File')
        col_w_ls = [0, 70, 30, 100, 10, 200]
        self.scl_table = ttk.Scrollbar(self.table_frm)
        self.scl_table.pack(side='right', fill='y')
        self.table = ttk.Treeview(self.table_frm, column=col_ls, show='headings', 
                                  selectmode='extended', yscrollcommand=self.scl_table.set)
        self.table.pack(fill='both', expand=True)

        for i in range(6):
            self.table.column('{}'.format(i), width=col_w_ls[i])
            self.table.heading('{}'.format(i), text=col_ls[i], command=self.generateTable)

        self.month_ls_cmb.bind('<<ComboboxSelected>>', self.generateTable)
        self.year_ls_cmb.bind('<<ComboboxSelected>>', self.generateTable)
        self.subsort_cmb.bind('<<ComboboxSelected>>', self.generateTable)
        self.table.bind('<<TreeviewSelect>>', self.showSelectedCount)

        self.refresh()


    def refresh(self):
        con = sqlite3.connect(self.dbpath + self.dbfile)
        cursor = con.cursor()
        cursor.execute("""SELECT DISTINCT strftime('%m', timestamp) as month 
                          FROM script_usage ORDER by month """)
        month_ls_raw = cursor.fetchall()
        month_ls = [i[0] for i in month_ls_raw]
        month_ls.insert(0, 'All')
        cursor.execute("""SELECT DISTINCT strftime('%Y', timestamp) as month 
                          FROM script_usage ORDER by month """)
        year_ls_raw = cursor.fetchall()
        year_ls = [i[0] for i in year_ls_raw]
        year_ls.insert(0, 'All')
        cursor.close()
        con.close()
        self.month_ls_cmb['values'] = month_ls
        self.month_ls_cmb.current(month_ls.index('All'))
        self.year_ls_cmb['values'] = year_ls
        self.year_ls_cmb.current(year_ls.index('All'))
        self.sort_cmb['values'] = self.colums
        self.sort_cmb.current(3)
        self.subsort_cmb['values'] = self.colums
        self.subsort_cmb.current(4)
        self.generateTable()


    def getTableData(self):
        month         = self.month_ls_cmb.get()
        year          = self.year_ls_cmb.get()
        self.order    = self.sort_cmb.get()
        self.suborder = self.subsort_cmb.get()
        con = sqlite3.connect(self.dbpath + self.dbfile)
        cursor = con.cursor()
        if month == 'All' and year == 'All':
            sqlcmd = """SELECT * FROM script_usage ORDER by {}, {}
                     """.format(self.order, self.suborder)
        elif month == 'All' and year != 'All':
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%Y', timestamp) = '{}' 
                        ORDER by {}, {}
                     """.format(year, self.order, self.suborder)
        elif month != 'All' and year == 'All':
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%m', timestamp) = '{}' 
                        ORDER by {}, {}
                     """.format(month, self.order, self.suborder)
        else:
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%m-%Y', timestamp) = '{}-{}' 
                        ORDER by {}, {}
                     """.format(month, year, self.order, self.suborder)
        cursor.execute(sqlcmd)
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return data


    def generateTable(self, *args):
        self.table.delete(*self.table.get_children())
        for i in self.getTableData():
            self.table.insert(parent = '', index='end', iid=i[0]
                ,values=(i[0], i[1], i[2], i[3], i[4], i[5]))


    def exportCsv(self, *args):
        data     = self.getTableData()
        month    = self.month_ls_cmb.get()
        year     = self.year_ls_cmb.get()
        homedir  = os.path.expanduser('~')
        savepath = homedir + '/Documents'
        savename = 'layouttool_usage_{}-{}'.format(month, year)
        csvfile  = tkFileDialog.asksaveasfilename(
            initialdir=savepath, initialfile = savename, 
            filetypes=([('CSV','*.csv')]), defaultextension='.csv')
        if csvfile:
            with open(csvfile, 'wb') as f:
                csv_writer = csv.writer(f)
                column_names = ('ID', 'Date/Time', 'User', 'Script', 'Run From', 'File')
                csv_writer.writerow(column_names)
                csv_writer.writerows(data)


    def showSelectedCount(self, *args):
        sel = len(self.table.selection())
        self.sel_count_l.config(text = 'Selected rows: {}'.format(sel))


UsageStatUI().mainloop()