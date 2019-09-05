import pandas as pd

def pandas_fill_in_empty_from_up(df:pd.DataFrame,cond=lambda val:pd.isnull(val)):
	new_df: pd.DataFrame
	new_df = df.copy()

	pref_rpw = None
	for idx, rows in new_df.iterrows():
		for col in new_df.columns:
			val = rows[col]
			if cond(val):
				rows.at[col] = pref_rpw[col]
		pref_rpw = rows.copy()
	return new_df
