try:
    # Python 3
    from tkinter import Tk
    from tkinter import filedialog as FileDialog
    from tkinter import ttk
except ImportError:
    # Python 2
    from Tkinter import Tk
    import tkFileDialog as FileDialog
    import ttk
import sqlite3
import os
import csv
from datetime import datetime

#### set database path in Model() first" ####

class UsageStatUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.control = Control(self)
        self.colums = self.control.dataCols

        self.title('Layout Scripts Statistic')
        self.geometry('1000x700+300+100')

        data_frm = ttk.Frame(self)
        data_frm.pack(fill='both', expand=True, padx=10, pady=10)


        # --- create input widget ---

        func_frm = ttk.Frame(data_frm)
        func_frm.pack(fill='x', pady=(0,5))
        data_l_frm = ttk.Frame(func_frm)
        data_l_frm.pack(side='left')
        ttk.Label(data_l_frm, text='Year:').grid(row=0, column=0, pady=(0,5), sticky='e')
        self.year_ls_cmb = ttk.Combobox(data_l_frm, width=10, state="readonly")
        self.year_ls_cmb.grid(row=0, column=1, padx=(0,20), pady=(0,5))
        ttk.Label(data_l_frm, text='Month:').grid(row=0, column=2, pady=(0,5), sticky='e')
        self.month_ls_cmb = ttk.Combobox(data_l_frm, width=10, state="readonly")
        self.month_ls_cmb.grid(row=0, column=3, pady=(0,5))

        ttk.Label(data_l_frm, text='Sort:').grid(row=1, column=0, sticky='e')
        self.sort_cmb = ttk.Combobox(data_l_frm, width=10, state="readonly")
        self.sort_cmb.grid(row=1, column=1, padx=(0,20))
        ttk.Label(data_l_frm, text='Subsort:').grid(row=1, column=2, sticky='e')
        self.subsort_cmb = ttk.Combobox(data_l_frm, width=10, state="readonly")
        self.subsort_cmb.grid(row=1, column=3)
        self.sel_count_l = ttk.Label(data_l_frm, text='Selected rows: 0')
        self.sel_count_l.grid(row=1, column=4, padx=20)

        data_r_frm = ttk.Frame(func_frm)
        data_r_frm.pack(side='right')
        ttk.Label(data_r_frm, text='').grid(row=0, column=0, pady=(0,5))
        exportdata_btn = ttk.Button(data_r_frm, text='Export CSV', 
                                     width = 15, command=self.control.exportDataCsv)
        exportdata_btn.grid(row=1, column=0, sticky='s')


        # --- create table widget ---

        # data table
        table_frm = ttk.Frame(data_frm)
        table_frm.pack(fill='both', expand=True)
        coldata_w_ls = [60, 150, 100, 200, 70, 300]
        coldata_s_ls = [0, 1, 1, 1, 1, 1]
        sclx_tabledata = ttk.Scrollbar(table_frm, orient='horizontal')
        sclx_tabledata.pack(side='bottom', fill='x')
        scly_tabledata = ttk.Scrollbar(table_frm)
        scly_tabledata.pack(side='right', fill='y')
        self.tabledata = ttk.Treeview(table_frm, column=self.colums, show='headings', 
                                  selectmode='extended', 
                                  xscrollcommand=sclx_tabledata.set,
                                  yscrollcommand=scly_tabledata.set)
        self.tabledata.pack(fill='both', expand=True)

        for i in range(6):
            self.tabledata.column('{}'.format(i), width=coldata_w_ls[i], stretch=coldata_s_ls[i])
            self.tabledata.heading('{}'.format(i), text=self.colums[i])

        ttk.Separator(self, orient='horizontal').pack(padx = 10, fill='x')
        
        # count table
        count_frm = ttk.Frame(self)
        count_frm.pack(fill='both', expand=True, padx=10, pady=(0,10))
        exportcount_btn = ttk.Button(count_frm, text='Export CSV', 
                                     width = 15, command=self.control.exportCountCsv)
        exportcount_btn.pack(pady=10, anchor='e')
        
        tablecount_frm = ttk.Frame(count_frm)
        tablecount_frm.pack(fill='both', expand=True)
        sclx_tablesum = ttk.Scrollbar(tablecount_frm, orient='horizontal')
        sclx_tablesum.pack(side='bottom', fill='x')
        scly_tablesum = ttk.Scrollbar(tablecount_frm)
        scly_tablesum.pack(side='right', fill='y')
        self.tablecount = ttk.Treeview(tablecount_frm, show='headings',
                                       xscrollcommand=sclx_tablesum.set,
                                       yscrollcommand=scly_tablesum.set)
        self.tablecount.pack(fill='both', expand=True)


        # --- bindings ---

        self.month_ls_cmb.bind('<<ComboboxSelected>>', self.control.generateTables)
        self.year_ls_cmb.bind('<<ComboboxSelected>>', self.control.generateTables)
        self.sort_cmb.bind('<<ComboboxSelected>>', self.control.generateTables)
        self.subsort_cmb.bind('<<ComboboxSelected>>', self.control.generateTables)
        self.tabledata.bind('<<TreeviewSelect>>', self.control.showSelectedCount)

        self.control.initialize()


class Control:
    def __init__(self, view):
        self.view = view
        self.model = Model()

        self.dataCols = ('id', 'timestamp', 'user', 'script', 'runfrom', 'filename')
        self.order    = 'id'
        self.suborder = 'script'
        self.year_ls  = list(['All'])
        self.month_ls = list(['All'])
        

    def initialize(self):
        year, month = datetime.now().strftime('%Y-%m').split('-')
        year_ls_raw, month_ls_raw = self.model.getDateLs()
        self.year_ls.extend(map(lambda x: x[0], year_ls_raw))
        self.month_ls.extend(map(lambda x: x[0], month_ls_raw))
        self.view.month_ls_cmb['values'] = self.month_ls
        self.view.month_ls_cmb.current(self.month_ls.index(month))
        self.view.year_ls_cmb['values'] = self.year_ls
        self.view.year_ls_cmb.current(self.year_ls.index(year))
        self.view.sort_cmb['values'] = self.dataCols
        self.view.sort_cmb.current(self.dataCols.index(self.order))
        self.view.subsort_cmb['values'] = self.dataCols
        self.view.subsort_cmb.current(self.dataCols.index(self.suborder))
        self.generateTables()


    def generateTables(self, *args):
        self.generateDataTable()
        self.generateCountTable()


    def getDataTable(self, *args):
        year          = self.view.year_ls_cmb.get()
        month         = self.view.month_ls_cmb.get()
        self.order    = self.view.sort_cmb.get()
        self.suborder = self.view.subsort_cmb.get()
        return self.model.getData(year, month, self.order, self.suborder)


    def generateDataTable(self, *args):
        self.view.tabledata.delete(*self.view.tabledata.get_children())
        for i in self.getDataTable():
            self.view.tabledata.insert(parent = '', index='end', iid=i[0]
                ,values=(i[0], i[1], i[2], i[3], i[4], i[5]))
            

    def getCountTable(self, *args):
        year          = self.view.year_ls_cmb.get()
        month         = self.view.month_ls_cmb.get()
        self.order    = self.view.sort_cmb.get()
        self.suborder = self.view.subsort_cmb.get()
        return self.model.getCountData(year, month, self.order, self.suborder)


    def generateCountTable(self, *args):
        self.view.tablecount.delete(*self.view.tablecount.get_children())
        colLs = [self.order]
        colLs.extend(self.model.getSuborderList(self.suborder))
        colLs.append('total')
        self.view.tablecount.configure(column=colLs)
        for i in range(len(colLs)):
            self.view.tablecount.column('{}'.format(i), width = 170 if i==0 else 50, stretch = 0)
            self.view.tablecount.heading('{}'.format(i), text=colLs[i])
        for i in self.getCountTable():
            self.view.tablecount.insert(parent = '', index='end', iid=i[0]
                ,values=(i))


    def showSelectedCount(self, *args):
        sel = len(self.view.tabledata.selection())
        self.view.sel_count_l.config(text = 'Selected rows: {}'.format(sel))


    def exportDataCsv(self, *args):
        data     = self.getDataTable()
        month    = self.view.month_ls_cmb.get()
        year     = self.view.year_ls_cmb.get()
        savepath = os.path.expanduser('~') + '/Documents'
        savename = 'script_usage_data_{}-{}'.format(month, year)
        csvfile  = FileDialog.asksaveasfilename(
            initialdir=savepath, initialfile = savename, 
            filetypes=([('CSV','*.csv')]), defaultextension='.csv')
        if csvfile:
            try:
                # Python 2
                with open(csvfile, 'wb') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(self.dataCols)
                    csv_writer.writerows(data)
            except TypeError:
                # Python 3
                with open(csvfile, 'w') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(self.dataCols)
                    csv_writer.writerows(data)


    def exportCountCsv(self, *args):
        data     = self.getCountTable()
        month    = self.view.month_ls_cmb.get()
        year     = self.view.year_ls_cmb.get()
        colLs    = [self.order]
        colLs.extend(self.model.getSuborderList(self.suborder))
        colLs.append('total')
        savepath = os.path.expanduser('~') + '/Documents'
        savename = 'script_usage_{}-{}_{}-{}'.format(self.order, self.suborder, month, year)
        csvfile  = FileDialog.asksaveasfilename(
            initialdir=savepath, initialfile = savename, 
            filetypes=([('CSV','*.csv')]), defaultextension='.csv')
        if csvfile:
            try:
                # Python 2
                with open(csvfile, 'wb') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(colLs)
                    csv_writer.writerows(data)
            except TypeError:
                # Python 3
                with open(csvfile, 'w') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(colLs)
                    csv_writer.writerows(data)


class Model:
    def __init__(self):

        self.dbpath   = 'C:/' # <---- database path. same as "LayoutTool/logScriptUsage.py"

        self.dbfile   = 'layouttool_script_usage.db'
        self.connection = sqlite3.connect(self.dbpath + self.dbfile)


    def getDateLs(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT DISTINCT strftime('%Y', timestamp) as month 
                          FROM script_usage ORDER by month """)
        year_ls_raw = cursor.fetchall()
        cursor.execute("""SELECT DISTINCT strftime('%m', timestamp) as month 
                          FROM script_usage ORDER by month """)
        month_ls_raw = cursor.fetchall()
        cursor.close()
        return year_ls_raw, month_ls_raw
    

    def getData(self, year, month, order, suborder):
        cursor = self.connection.cursor()
        if month == 'All' and year == 'All':
            sqlcmd = """SELECT * FROM script_usage ORDER by {}, {}
                     """.format(order, suborder)
        elif month == 'All' and year != 'All':
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%Y', timestamp) = '{}' 
                        ORDER by {}, {}
                     """.format(year, order, suborder)
        elif month != 'All' and year == 'All':
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%m', timestamp) = '{}' 
                        ORDER by {}, {}
                     """.format(month, order, suborder)
        else:
            sqlcmd = """SELECT * FROM script_usage 
                        WHERE strftime('%m-%Y', timestamp) = '{}-{}' 
                        ORDER by {}, {}
                     """.format(month, year, order, suborder)
        cursor.execute(sqlcmd)
        data = cursor.fetchall()
        cursor.close()
        return data
    

    def getSuborderList(self, suborder):
        cursor = self.connection.cursor()
        cursor.execute("""
                       SELECT DISTINCT {}
                       FROM script_usage
                       """.format(suborder))
        data = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: x[0], data))
    

    def getCountData(self, year, month, order, suborder):
        suborderLs = self.getSuborderList(suborder)
        sqlcmd = 'SELECT {}, \n'.format(order)
        for i in suborderLs:
            sqlcmd = sqlcmd + '    sum(case when {} = "{}" then 1 else 0 end) AS "{}", \n'.format(suborder, i, i)
        sqlcmd = sqlcmd + 'count(*) AS total \nFROM script_usage \n'
        if month == 'All' and year == 'All':
            pass
        elif month == 'All' and year != 'All':
            sqlcmd = sqlcmd + "WHERE strftime('%Y', timestamp) = '{}' \n".format(year)
        elif month != 'All' and year == 'All':
            sqlcmd = sqlcmd + "WHERE strftime('%m', timestamp) = '{}' \n".format(month)
        else:
            sqlcmd = sqlcmd + "WHERE strftime('%m-%Y', timestamp) = '{}-{}' \n".format(month, year)
        sqlcmd = sqlcmd + 'GROUP BY {} \nORDER BY total DESC;'.format(order)
        cursor = self.connection.cursor()
        cursor.execute(sqlcmd)
        data = cursor.fetchall()
        cursor.close()
        return data


UsageStatUI().mainloop()