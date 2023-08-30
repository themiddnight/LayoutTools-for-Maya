try:  # Python 3
    from tkinter import Tk, PanedWindow
    from tkinter import ttk
except ImportError:  # Python 2
    from Tkinter import Tk, PanedWindow
    import ttk


class UsageStatUI(Tk):
    def __init__(self, control):
        Tk.__init__(self)

        self.control = control
        self.colums = self.control.dataCols

        self.title('Layout Scripts Statistic')
        self.geometry('1000x700+300+100')

        pw = PanedWindow(self, orient='vertical', sashpad=5, sashrelief='solid')
        pw.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Data table ---

        # input widgets
        data_frm = ttk.Frame(pw)
        data_frm.pack(fill='both', expand=True)
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
        exportdata_btn = ttk.Button(data_r_frm, text='Export CSV', width = 15, 
                                     command=lambda: self.control.exportCsv('data'))
        exportdata_btn.grid(row=1, column=0, sticky='s')

        # data table
        table_frm = ttk.Frame(data_frm)
        table_frm.pack(fill='both', expand=True)
        self.tabledata = ttk.Treeview(table_frm, column=self.colums,
                                      show='headings', selectmode='extended')
        sclx_tabledata = ttk.Scrollbar(table_frm, orient='horizontal', 
                                       command=self.tabledata.xview)
        sclx_tabledata.pack(side='bottom', fill='x')
        scly_tabledata = ttk.Scrollbar(table_frm, 
                                       command=self.tabledata.yview)
        scly_tabledata.pack(side='right', fill='y')
        self.tabledata.configure(xscrollcommand=sclx_tabledata.set,
                                yscrollcommand=scly_tabledata.set)
        self.tabledata.pack(fill='both', expand=True)
        coldata_w_ls = [60, 150, 100, 200, 70, 300]
        coldata_s_ls = [0, 1, 1, 1, 1, 1]
        for i in range(6):
            self.tabledata.column('{}'.format(i), width=coldata_w_ls[i], 
                                  stretch=coldata_s_ls[i])
            self.tabledata.heading('{}'.format(i), text=self.colums[i])
        
        pw.add(data_frm, height=350, minsize=100)


        # --- Count table ---
        
        # button widgets
        count_frm = ttk.Frame(pw)
        count_frm.pack(fill='both', expand=True, padx=10, pady=10)
        countBtns_frm = ttk.Frame(count_frm)
        countBtns_frm.pack(anchor='e', pady=(0,10))
        viewCountGrph_btn = ttk.Button(countBtns_frm, text='View Graph', 
                                     width = 15, command=self.control.showGraph)
        viewCountGrph_btn.pack(padx=10, side='left')
        exportcount_btn = ttk.Button(countBtns_frm, text='Export CSV', width = 15, 
                                     command= lambda: self.control.exportCsv('count'))
        exportcount_btn.pack(side='left')
        
        # count table
        tablecount_frm = ttk.Frame(count_frm)
        tablecount_frm.pack(fill='both', expand=True)
        self.tablecount = ttk.Treeview(tablecount_frm, show='headings')
        sclx_tablesum = ttk.Scrollbar(tablecount_frm, orient='horizontal', 
                                      command=self.tablecount.xview)
        sclx_tablesum.pack(side='bottom', fill='x')
        scly_tablesum = ttk.Scrollbar(tablecount_frm, 
                                      command=self.tablecount.yview)
        scly_tablesum.pack(side='right', fill='y')
        self.tablecount.configure(xscrollcommand=sclx_tablesum.set,
                                  yscrollcommand=scly_tablesum.set)
        self.tablecount.pack(fill='both', expand=True)

        pw.add(count_frm, minsize=100)


        # --- bindings ---

        self.month_ls_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.year_ls_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.sort_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.subsort_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.tabledata.bind('<<TreeviewSelect>>', self.control.showSelectedCount)


try:  # Python 3
    from tkinter import filedialog as FileDialog, messagebox
except ImportError:  # Python 2
    import tkFileDialog as FileDialog, tkMessageBox as messagebox
from datetime import datetime
import os
class Control:
    def __init__(self):

        self.dataCols = ('id', 'timestamp', 'user', 'script', 'runfrom', 'filename')
        self.order    = 'script'
        self.suborder = 'runfrom'
        self.year_ls  = list(['All'])
        self.month_ls = list(['All'])
        self.year, self.month = datetime.now().strftime('%Y-%m').split('-')

        self.view  = UsageStatUI(self)
        self.model = Model()
        
        year_ls_raw, month_ls_raw = self.model.getDateLs()
        self.year_ls.extend(map(lambda x: x[0], year_ls_raw))
        self.month_ls.extend(map(lambda x: x[0], month_ls_raw))
        self.view.month_ls_cmb['values'] = self.month_ls
        self.view.month_ls_cmb.current(self.month_ls.index(self.month))
        self.view.year_ls_cmb['values'] = self.year_ls
        self.view.year_ls_cmb.current(self.year_ls.index(self.year))
        self.view.sort_cmb['values'] = self.dataCols
        self.view.sort_cmb.current(self.dataCols.index(self.order))
        self.view.subsort_cmb['values'] = self.dataCols
        self.view.subsort_cmb.current(self.dataCols.index(self.suborder))
        self.refresh()


    def refresh(self, *args):
        self.year     = self.view.year_ls_cmb.get()
        self.month    = self.view.month_ls_cmb.get()
        self.order    = self.view.sort_cmb.get()
        self.suborder = self.view.subsort_cmb.get()
        self.generateDataTable()
        self.generateCountTable()


    def generateDataTable(self, *args):
        self.view.tabledata.delete(*self.view.tabledata.get_children())
        self.data = self.model.getData(self.year, self.month, self.order, self.suborder)
        for i in self.data:
            self.view.tabledata.insert(parent = '', index='end', iid=i[0]
                ,values=(i[0], i[1], i[2], i[3], i[4], i[5]))


    def generateCountTable(self, *args):
        self.view.tablecount.delete(*self.view.tablecount.get_children())
        colLs = [self.order]
        colLs.extend(self.model.getSuborderList(self.suborder))
        colLs.append('total')
        self.view.tablecount.configure(column=colLs)
        self.countData = self.model.getCountData(self.year, self.month, self.order, self.suborder)
        for i in range(len(colLs)):
            self.view.tablecount.column('{}'.format(i), 
                                        width = 170 if i==0 else 50, 
                                        stretch = 0)
            self.view.tablecount.heading('{}'.format(i), text=colLs[i])
        for i in self.countData:
            self.view.tablecount.insert(parent = '', index='end', iid=i[0]
                ,values=(i))


    def showSelectedCount(self, *args):
        sel = len(self.view.tabledata.selection())
        self.view.sel_count_l.config(text = 'Selected rows: {}'.format(sel))


    def showGraph(self):
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            colLs = [self.order]
            colLs.extend(self.model.getSuborderList(self.suborder))
            data = list(map(lambda x: list(x)[:-1], self.countData))
            df = pd.DataFrame(data, columns=colLs)
            ax = df.plot(x = colLs[0], kind='bar', stacked=True, fontsize=8, 
                         width=0.8, figsize=[10,5], zorder = 1,
                         title='{} - {}'.format(self.order, self.suborder))
            ax.grid(visible=True, axis='y', linewidth=0.5, zorder = 0)
            plt.xticks(rotation=30, horizontalalignment='right')
            plt.show()
        except ImportError:
            messagebox.showerror(
                title='No Package', 
                message='No "matplotlib" and "pandas" library in the system.')


    def exportCsv(self, table, *args):
        savepath = os.path.expanduser('~') + '/Documents'
        month    = self.view.month_ls_cmb.get()
        year     = self.view.year_ls_cmb.get()
        if table == 'data':
            col  = self.dataCols
            data = self.data
            savename = 'scriptUsage_data_{}-{}'.format(
                month, year)
        elif table == 'count':
            col  = [self.order]
            col.extend(self.model.getSuborderList(self.suborder))
            col.append('total')
            data = self.countData
            savename = 'scriptUsage_count_{}-{}_{}-{}'.format(
                self.order, self.suborder, month, year)
        csvfile = FileDialog.asksaveasfilename(
            initialdir=savepath, initialfile = savename, 
            filetypes=([('CSV','*.csv')]), defaultextension='.csv')
        if csvfile:
            self.model.saveCsv(col, data, csvfile)


import sqlite3
import csv
import json
class Model:
    def __init__(self):

        with open('data/settings.json', 'r') as f:
            pref = json.load(f)
            self.dbfile = pref["db_file"] # <---- database path. same as "LayoutTool/logScriptUsage.py"

        self.connection = sqlite3.connect(self.dbfile)


    def getDateLs(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT DISTINCT strftime('%Y', timestamp) as year 
                          FROM script_usage ORDER by year """)
        year_ls_raw = cursor.fetchall()
        cursor.execute("""SELECT DISTINCT strftime('%m', timestamp) as month 
                          FROM script_usage ORDER by month """)
        month_ls_raw = cursor.fetchall()
        cursor.close()
        return year_ls_raw, month_ls_raw
    

    def getData(self, year, month, order, suborder):
        ''' SELECT * FROM script_usage 
            WHERE timestamp BETWEEN '{}' and '{}' .format(
            "yyyy-mm A", "yyyy-mm B")
        '''
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
            sqlcmd = sqlcmd + 'sum(case when {} = "{}" then 1 else 0 end) AS "{}", \n'.format(suborder, i, i)
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
    

    def saveCsv(self, col, data, path):
        try:                # Python 2
            with open(path, 'wb') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(col)
                csv_writer.writerows(data)
        except TypeError:   # Python 3
            with open(path, 'w') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(col)
                csv_writer.writerows(data)



if __name__ == '__main__':
    app = Control()
    app.view.mainloop()