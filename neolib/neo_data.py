import pandas as pd

def pandas_fill_in_empty_from_up(df:pd.DataFrame,cond=lambda val:pd.isnull(val)):
	new_df: pd.DataFrame
	df.fillna('')
	new_df = df.copy()
	#new_df.fillna('')

	pref_rpw = None
#	print(new_df.columns,list(new_df.dtypes))
	for idx, rows in new_df.iterrows():
		if pref_rpw is None:
			pref_rpw = rows.copy()
			continue
		for col in new_df.columns:
			if col =="목적":
				continue
			val = rows[col]
			new_val = pref_rpw[col]
			if cond(val) and not pd.isnull(new_val):

				#print(col,new_val)

				rows.at[col] = new_val
				val = rows[col]
			new_df.loc[idx] =rows
		rows.fillna('')
		pref_rpw = rows.copy()
		#pref_rpw.fillna('')

	# 	print(rows)
	#
	#
	# for idx, rows in new_df.iterrows():
	# 	print('##########', idx)
	# 	print(rows)
	# 	#pref_rpw.fillna()
	return new_df


if __name__ == '__main__':
	xls_flie = 'D:/PROJECT/china cc/docs/테스트 기능 정리 20190910.xlsx'
	#xls_flie ='D:/PROJECT/china cc/docs/테스트 기능 정리 20190905.xlsx'
	df = pd.read_excel(xls_flie)

	new_df = pandas_fill_in_empty_from_up(df)
	print(new_df)

