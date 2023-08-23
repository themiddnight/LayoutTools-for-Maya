from Tkinter import Tk
import tkFileDialog
import ttk
import sqlite3
import os
import csv

dbpath = 'C:/' # <------ path to save database file, same as in "LayoutTool/scriptUsage.py"
dbfile = 'layouttool_script_usage.db'

def refresh(orderby):
	con = sqlite3.connect(dbpath + dbfile)
	cursor = con.cursor()
	cursor.execute("""SELECT DISTINCT strftime('%m', timestamp) as month FROM script_usage ORDER by month """)
	month_ls_raw = cursor.fetchall()
	month_ls = [i[0] for i in month_ls_raw]
	month_ls.insert(0, 'All')
	cursor.execute("""SELECT DISTINCT strftime('%Y', timestamp) as month FROM script_usage ORDER by month """)
	year_ls_raw = cursor.fetchall()
	year_ls = [i[0] for i in year_ls_raw]
	year_ls.insert(0, 'All')
	cursor.close()
	con.close()
	month_ls_cmb['values'] = month_ls
	month_ls_cmb.current(month_ls.index('All'))
	year_ls_cmb['values'] = year_ls
	year_ls_cmb.current(year_ls.index('All'))
	subsort_cmb['values'] = ('id', 'timestamp', 'user', 'script', 'runfrom', 'filename')
	subsort_cmb.current(4)
	generateTable(orderby)

def getTableData(orderby):
	month = month_ls_cmb.get()
	year = year_ls_cmb.get()
	subsort = subsort_cmb.get()
	con = sqlite3.connect(dbpath + dbfile)
	cursor = con.cursor()
	if month == 'All' and year == 'All':
		sqlcmd = """SELECT * FROM script_usage ORDER by {}, {}""".format(orderby, subsort)
	elif month == 'All' and year != 'All':
		sqlcmd = """SELECT * FROM script_usage WHERE strftime('%Y', timestamp) = '{}' ORDER by {}, {}""".format(year, orderby, subsort)
	elif month != 'All' and year == 'All':
		sqlcmd = """SELECT * FROM script_usage WHERE strftime('%m', timestamp) = '{}' ORDER by {}, {}""".format(month, orderby, subsort)
	else:
		sqlcmd = """SELECT * FROM script_usage WHERE strftime('%m-%Y', timestamp) = '{}-{}' ORDER by {}, {}""".format(month, year, orderby, subsort)
	cursor.execute(sqlcmd)
	data = cursor.fetchall()
	cursor.close()
	con.close()
	return data

def generateTable(orderby, *args):
	table.delete(*table.get_children())
	for i in getTableData(orderby):
		table.insert(parent = '', index='end', iid=i[0]
			,values=(i[0], i[1], i[2], i[3], i[4], i[5]))

def exportCsv(orderby):
	data = getTableData(orderby)
	month = month_ls_cmb.get()
	year = year_ls_cmb.get()
	homedir = os.path.expanduser('~')
	savepath = homedir + '/Documents'
	savename = 'layouttool_usage_{}-{}'.format(month, year)
	csvfile = tkFileDialog.asksaveasfilename(initialdir=savepath, initialfile = savename, filetypes=([('CSV','*.csv')]), defaultextension='.csv')
	if csvfile:
		with open(csvfile, 'wb') as f:
			csv_writer = csv.writer(f)
			column_names = ('ID', 'Date/Time', 'User', 'Script', 'Run From', 'File')
			csv_writer.writerow(column_names)
			csv_writer.writerows(data)

def showSelectedCount(*args):
	sel = len(table.selection())
	sel_count_l.config(text = 'Selected rows: {}'.format(sel))
	print sel

app = Tk()

app.title('Layout Statistic')
app.geometry('800x600+500+300')

app_frm = ttk.Frame(app)
app_frm.pack(fill='both', expand=True, padx=10, pady=10)

# create functions widget
func_frm = ttk.Frame(app_frm)
func_frm.pack(fill='x')
ttk.Label(func_frm, text='Month:').pack(side='left')
month_ls_cmb = ttk.Combobox(func_frm, width=10)
month_ls_cmb.pack(side='left', pady = 10, padx=5)
ttk.Label(func_frm, text='Year:').pack(side='left')
year_ls_cmb = ttk.Combobox(func_frm, width=10)
year_ls_cmb.pack(side='left', pady = 10, padx=5)

export_btn = ttk.Button(func_frm, text='Export CSV', width = 15, command=lambda: exportCsv('id'))
export_btn.pack(side='right', pady = 10)
sel_count_l = ttk.Label(func_frm, text='Selected rows: 0')
sel_count_l.pack(side='right', padx=(5,15))
subsort_cmb = ttk.Combobox(func_frm, width=10)
subsort_cmb.pack(side='right', pady = 10, padx=5)
ttk.Label(func_frm, text='Subsort:').pack(side='right')

# create table widget
table_frm = ttk.Frame(app_frm)
table_frm.pack(fill='both', expand=True)
col_w = 70
col_ls = ('ID', 'Date/Time', 'User', 'Script', 'Run From', 'File')
col_cmd = ('id', 'timestamp', 'user', 'script', 'runfrom', 'filename')
col_w_ls = [0, 70, 30, 100, 10, 200]
scl_table = ttk.Scrollbar(table_frm)
scl_table.pack(side='right', fill='y')
table = ttk.Treeview(table_frm, column=col_ls, show='headings', selectmode='extended', yscrollcommand=scl_table.set)
table.pack(fill='both', expand=True)

for i in range(6):
	table.column('{}'.format(i), width=col_w_ls[i])
	table.heading('{}'.format(i), text=col_ls[i], command=lambda x = col_cmd[i]: generateTable(x))


refresh('id')


month_ls_cmb.bind('<<ComboboxSelected>>', lambda x: generateTable('id'))
year_ls_cmb.bind('<<ComboboxSelected>>', lambda x: generateTable('id'))
#subsort_cmb.bind('<<ComboboxSelected>>', lambda x: generateTable('id'))
table.bind('<<TreeviewSelect>>', showSelectedCount)


app.mainloop()
