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

        self.title('Layout Scripts Statistic')
        self.geometry('1000x800+300+100')

        pw = PanedWindow(self, orient='vertical', sashpad=15, sashrelief='raised')
        pw.pack(fill='both', expand=True, padx=10, pady=10)
        

        # --- Data Section ---

        data_frm = ttk.Frame(pw)
        data_frm.pack(fill='both', expand=True)

        # input widgets
        func_frm = ttk.Frame(data_frm)
        func_frm.pack(fill='x', pady=(0,5))

        data_l_frm = ttk.Frame(func_frm)
        data_l_frm.pack(side='left')

        ttk.Label(data_l_frm, text='Table:').grid(row=0, column=0)
        self.table_cmb = ttk.Combobox(data_l_frm, width=15, state="readonly")
        self.table_cmb.grid(row=0, column=1, padx=(0,10), pady=3)
        refresh_btn = ttk.Button(data_l_frm, text='Refresh', width = 15, 
                                     command=self.control.refresh)
        refresh_btn.grid(row=0, column=3, padx=(0,10), pady=3)
        self.sel_count_l = ttk.Label(data_l_frm, text='Selected rows: 0')
        self.sel_count_l.grid(row=0, column=5, padx=(0,10))
        ttk.Label(data_l_frm, text='From:').grid(row=1, column=0)
        self.dateFrom_ls_cmb = ttk.Combobox(data_l_frm, width=15, state="readonly")
        self.dateFrom_ls_cmb.grid(row=1, column=1, padx=(0,10), pady=3)
        ttk.Label(data_l_frm, text='To:').grid(row=1, column=2)
        self.dateTo_ls_cmb = ttk.Combobox(data_l_frm, width=15, state="readonly")
        self.dateTo_ls_cmb.grid(row=1, column=3, padx=(0,10), pady=3)
        ttk.Label(data_l_frm, text='Sort:').grid(row=1, column=4)
        self.sort_cmb = ttk.Combobox(data_l_frm, width=15, state="readonly")
        self.sort_cmb.grid(row=1, column=5, padx=(0,10), pady=3)
        ttk.Label(data_l_frm, text='Subsort:').grid(row=1, column=6)
        self.subsort_cmb = ttk.Combobox(data_l_frm, width=15, state="readonly")
        self.subsort_cmb.grid(row=1, column=7, padx=(0,10), pady=3)

        data_r_frm = ttk.Frame(func_frm)
        data_r_frm.pack(side='right')

        ttk.Label(data_r_frm, text='').grid(row=0, column=0, pady=(0,5))
        exportdata_btn = ttk.Button(data_r_frm, text='Export CSV', width = 15, 
                                     command=lambda: self.control.exportCsv('data'))
        exportdata_btn.grid(row=1, column=0, sticky='s')

        # data table
        table_frm = ttk.Frame(data_frm)
        table_frm.pack(fill='both', expand=True)
        self.tabledata = ttk.Treeview(table_frm, show='headings', selectmode='extended')
        scly_tabledata = ttk.Scrollbar(table_frm, command=self.tabledata.yview)
        scly_tabledata.pack(side='right', fill='y')
        self.tabledata.configure(yscrollcommand=scly_tabledata.set)
        self.tabledata.pack(fill='both', expand=True)
        
        pw.add(data_frm, height=350, minsize=100)


        # --- Count Section ---

        count_frm = ttk.Frame(pw)
        count_frm.pack(fill='both', expand=True, padx=10)
        
        # button widgets
        countBtns_frm = ttk.Frame(count_frm)
        countBtns_frm.pack(anchor='e')
        exportcount_btn = ttk.Button(countBtns_frm, text='Export CSV', width = 15, 
                                     command= lambda: self.control.exportCsv('count'))
        exportcount_btn.pack(side='left')
        
        # count TAB
        count_tab = ttk.Notebook(count_frm)
        count_tab.pack(fill='both', expand=True)
        tablecount_frm = ttk.Frame(count_tab)
        tablecount_frm.pack(fill='both', expand=True)

        graphcount_frm = ttk.Frame(count_tab)
        graphcount_frm.pack(fill='both', expand=True)

        count_tab.add(tablecount_frm, text = '{: ^20}'.format('Table')) 
        count_tab.add(graphcount_frm, text = '{: ^20}'.format('Graph')) 

        # count graph
        try:
            self.figure = Figure()
            self.graph_canvas = FigureCanvasTkAgg(self.figure, master = graphcount_frm)
            self.graph_canvas.get_tk_widget().pack(expand = 1, fill = 'both')
        except:
            self.errorTx = ttk.Label(graphcount_frm,
                    text='Error: Can not import "matplotlib" and "pandas" modules.').pack(
                expand=True)


        # count table
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

        self.dateFrom_ls_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.dateTo_ls_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.sort_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.subsort_cmb.bind('<<ComboboxSelected>>', self.control.refresh)
        self.table_cmb.bind('<<ComboboxSelected>>', self.control.tableRefresh)
        self.tabledata.bind('<<TreeviewSelect>>', self.control.showSelectedCount)


try:  # Python 3
    from tkinter import filedialog as FileDialog
except ImportError:  # Python 2
    import tkFileDialog as FileDialog
try:
    import pandas as pd
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    pass
from datetime import datetime
import os


class Control:
    def __init__(self):

        self.model = Model()
        self.view  = UsageStatUI(self)

        self.tableLs = self.model.getTables()
        self.table   = self.tableLs[0]
        self.date    = datetime.now().strftime('%Y-%m')

        self.view.table_cmb['values'] = self.tableLs
        self.view.table_cmb.current(self.tableLs.index(self.table))
        self.tableRefresh()


    def tableRefresh(self, *args):
        self.table    = self.view.table_cmb.get()
        self.dataCols = self.model.getColumns(self.table)

        self.view.tabledata['column'] = self.dataCols
        for num, col in enumerate(self.dataCols):
            self.view.tabledata.column('{}'.format(num), 
                                        width=60 if num == 0 else 150 
                                        if col != self.dataCols[-1] else 250)
            self.view.tabledata.heading('{}'.format(num), text=col)

        date_ls_raw = self.model.getDateLs(self.table)
        self.date_ls = list(map(lambda x: x[0], date_ls_raw))
        self.view.dateFrom_ls_cmb['values'] = self.date_ls
        self.view.dateFrom_ls_cmb.current(self.date_ls.index(self.date))
        self.view.dateTo_ls_cmb['values'] = self.date_ls
        self.view.dateTo_ls_cmb.current(self.date_ls.index(self.date))
        self.view.sort_cmb['values'] = self.dataCols
        self.view.sort_cmb.current(2)
        self.view.subsort_cmb['values'] = self.dataCols
        self.view.subsort_cmb.current(3)
        self.refresh()


    def refresh(self, *args):
        self.dateFrom = self.view.dateFrom_ls_cmb.get()
        self.dateTo   = self.view.dateTo_ls_cmb.get()
        self.order    = self.view.sort_cmb.get()
        self.suborder = self.view.subsort_cmb.get()
        self.generateDataTable()
        self.generateCountTable()
        self.generateCountGraph()


    def showSelectedCount(self, *args):
        sel = len(self.view.tabledata.selection())
        self.view.sel_count_l.config(text = 'Selected rows: {}'.format(sel))


    def generateDataTable(self, *args):
        self.view.tabledata.delete(*self.view.tabledata.get_children())
        self.data = self.model.getData(self.table,
            self.dateFrom, self.dateTo, self.order, self.suborder)
        for i in self.data:
            self.view.tabledata.insert(parent = '', index='end', iid=i[0]
                ,values=(i[0], i[1], i[2], i[3], i[4], i[5]))


    def generateCountTable(self, *args):
        self.view.tablecount.delete(*self.view.tablecount.get_children())
        colLs = [self.order]
        colLs.extend(self.model.getSuborderList(self.table, self.suborder))
        colLs.append('total')
        self.view.tablecount.configure(column=colLs)
        self.countData = self.model.getCountData(self.table, 
            self.dateFrom, self.dateTo, self.order, self.suborder)
        for i in range(len(colLs)):
            self.view.tablecount.column('{}'.format(i), 
                                        width = 170 if i==0 else 50, 
                                        stretch = 0)
            self.view.tablecount.heading('{}'.format(i), text=colLs[i])
        for i in self.countData:
            self.view.tablecount.insert(parent = '', index='end', iid=i[0]
                ,values=(i))


    def generateCountGraph(self):
        try:
            self.view.figure.clear()
            ax = self.view.figure.add_subplot()
            self.view.figure.subplots_adjust(left = 0.06, bottom = 0.12,
                                             right = 0.94, top = 0.88)
            colLs = [self.order]
            colLs.extend(self.model.getSuborderList(self.table, self.suborder))
            data = list(map(lambda x: list(x)[:-1], self.countData))
            df = pd.DataFrame(data, columns=colLs)
            df.plot(x = colLs[0], kind='bar', stacked=True, fontsize=8, 
                    width=0.8, ax=ax, xticks = [],
                    title='{} - {}'.format(self.order, self.suborder))
            ax.legend(fontsize = 9, draggable = True)
            x = [i[0] for i in data]
            for i in range(len(x)):
                ax.annotate(x[i], xy = (i, 0), xytext = (-3,10), rotation = 90, 
                            textcoords = 'offset points',fontsize = 8)
            self.view.graph_canvas.draw()
        except:
            pass


    def exportCsv(self, table, *args):
        savepath = os.path.expanduser('~') + '/Documents'
        if table == 'data':
            col  = self.dataCols
            data = self.data
            savename = '{}_data_{}-{}'.format(
                self.table, self.dateFrom, self.dateTo)
        elif table == 'count':
            col  = [self.order]
            col.extend(self.model.getSuborderList(self.table, self.suborder))
            col.append('total')
            data = self.countData
            savename = '{}_count_{}-{}_{}-{}'.format(
                self.table, self.order, self.suborder, self.dateFrom, self.dateTo)
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
            self.dbfile = pref["db_file"]

        self.connection = sqlite3.connect(self.dbfile)


    def getTables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table'
            """)
        table_ls_raw = cursor.fetchall()
        cursor.close()
        tables = (
            list(
                filter(
                    lambda x: x != 'sqlite_sequence',
                    list(map(lambda x: x[0], table_ls_raw))
                )
            )
        )
        return tables


    def getColumns(self, table):
        cursor = self.connection.cursor()
        cursor.execute("""
            PRAGMA table_info({})
            """.format(table))
        column_ls_raw = cursor.fetchall()
        cursor.close()
        columns = (list(map(lambda x: x[1], column_ls_raw)))
        return columns


    def getDateLs(self, table):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT strftime('%Y-%m', timestamp) as date 
            FROM {} ORDER by date """.format(table))
        date_ls_raw = cursor.fetchall()
        cursor.close()
        return date_ls_raw
    

    def getData(self, table, dateFrom, dateTo, order, suborder):
        if order == 'timestamp':
            order = 'DATE(timestamp)'
        if suborder == 'timestamp':
            suborder = 'DATE(timestamp)'
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM {} 
            WHERE timestamp BETWEEN '{}-01' and '{}-32' 
            ORDER by {}, {}""".format(
            table, dateFrom, dateTo, order, suborder))
        data = cursor.fetchall()
        cursor.close()
        return data
    

    def getSuborderList(self, table, suborder):
        if suborder == 'timestamp':
            suborder = 'DATE(timestamp)'
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT {}
            FROM {}
            """.format(suborder, table))
        data = cursor.fetchall()
        cursor.close()
        return list(map(lambda x: x[0], data))
    

    def getCountData(self, table, dateFrom, dateTo, order, suborder):
        if order == 'timestamp':
            order = 'DATE(timestamp)'
        if suborder == 'timestamp':
            suborder = 'DATE(timestamp)'
        suborderLs = self.getSuborderList(table, suborder)
        sqlcmd = 'SELECT {}, \n'.format(order)
        for i in suborderLs:
            sqlcmd = sqlcmd + 'sum(case when {} = "{}" then 1 else 0 end) AS "{}", \n'.format(
                suborder, i, i)
        sqlcmd = sqlcmd + """
                    count(*) AS total
                    FROM {}
                    WHERE timestamp BETWEEN '{}-01' and '{}-32'
                    GROUP BY {}""".format(
            table, dateFrom, dateTo, order)
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