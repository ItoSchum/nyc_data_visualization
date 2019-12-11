#!/usr/local/var/pyenv/shims/python3
#!python3
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
import pandas as pd
import psycopg2

try:
	os.chdir(os.getcwd())
	print(os.getcwd())
except:
	pass

# %%
# open selected osver
csv_dirname = './csv_import'
def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(r"%s" % path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]
csv_name_list = find_csv_filenames(csv_dirname)

# csv_path_list = []
# for csv_name in csv_name_list:
	# csv_path = os.path.join(os.path.expanduser(csv_dirname), csv_name)
	# csv_path_list.append(csv_path)


# %%
# DBNAME = 'project'
# USER = 'project'
# PASSWORD = 'project'
# PORT = 5432

def import_csv():

	# try:
	# # Connect to Database
	# 	conn = psycopg2.connect(database = DBNAME,user = USER,password = PASSWORD, port = PORT)
	# 	conn.autocommit = True
	# except:
	# 	print("Cannot connect to db.")
	# 	os.sys.exit(0)

	# cur = conn.cursor()
	# commands = []

	for csv_name in csv_name_list:
		csv_path = os.path.join(os.getcwd(), os.path.expanduser(csv_dirname), csv_name)

		df = pd.read_csv(csv_path)
		column_names = list(df.columns)

		str_column_names = ", ".join(column_names)
		table_name = csv_name.split(".")[0]

		try:
			os.system("psql -d project -c \"COPY %s(%s) FROM \'%s\' WITH csv header;\"" % (table_name, str_column_names, csv_path) )
			
			# cur_command = "COPY %s(%s) FROM \'%s\' WITH csv header;" % (table_name, str_column_names, csv_path)
			# cur.execute(cur_command)
			# commands.append(cur_command)
			
			# f = open(r"%s" % csv_path)
			# cur.copy_from(f, temp_unicommerce_status, sep=',')
			# f.close()

			# sql = "COPY %s(%s) FROM \'%s\' WITH csv header;" % (table_name, str_column_names, csv_path)
			# cur.copy_expert(sql, open(csv_path, "r"))
		except:
			print("Cannot COPY csv: %s" % csv_name)

import_csv()
