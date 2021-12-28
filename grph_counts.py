
def graph_counts(count_df, persist):
  fig,ax = plt.subplots(figsize=(10,8))
  fig.autofmt_xdate()
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  ax.xaxis.set_major_locator(years)
  # ax.xaxis.set_minor_locator(months)
  # To get python native datetime: 
  # py_date = count['creation'].dt.to_pydatetime()
  x_num = mdates.date2num(count_df['creation'])
  # Again bar uses a scalar for X axis, so can't use a simple offset
  # to plot multiple series
  # For the record: 
  # ax.bar(h_count['creation'],s_count['counts'],width=25)
  # works
  spacing = 365 / 3
  ax.set_title("Safe vs Questionable sketches")
  ax.set_xlabel('Year')
  ax.set_ylabel('Sketches')
  ax.bar(x_num - spacing/2 ,count_df['safe'],width=spacing,
         align='center',label='Safe',color='#72CDEE')
  ax.bar(x_num + spacing/2,count_df['questionable'],width=spacing,
        align='center',label='Questionable', color='#F7941D' )
  # automfmt _xdate does this too:
  #ax.xaxis_date()
  ax.legend()
  return fig
