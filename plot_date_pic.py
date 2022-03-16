from config import *

def plot_date_pic(dates):
    
    month = {1: 'Janauary',
         2: 'February',
         3: 'March',
         4: 'April',
         5: 'May',
         6: 'June',
         7: 'July',
         8: 'August',
         9: 'September',
         10: 'October',
         11: 'November',
         12: 'December'}
    
    #dates = [datetime.datetime.strptime(date, '%d.%m.%y') for date in dates]
    min_date, max_date = min(dates), max(dates)
    
    from_monday = min_date - datetime.timedelta(days = min_date.weekday())
    to_sunday = max_date + datetime.timedelta(days = 7 - max_date.weekday() - 1)
    
    N = ceil((to_sunday - from_monday).days / 7)
    M = 7

    days = np.zeros((N, M))

    curr_day = from_monday

    months, days_ = [], []

    for i in range(N*M):
        months.append(curr_day.month)
        days_.append(curr_day.day)
        for date in dates:
            if date == curr_day:
                days[i//7][i%7] += 1
        curr_day += datetime.timedelta(days = 1)
        
    plt.rcParams['figure.dpi'] = 300
    ax = plt.axes()
    sns.heatmap(days, 
                cmap=sns.light_palette("seagreen", as_cmap=True), 
                linewidths=2, linecolor='grey', 
                annot = np.array(days_).reshape(-1, 7),
                cbar=False,
                yticklabels=False,
                xticklabels=['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
                ax = ax,
                square=True
               )
    ax.set_title(', '.join([month[i] for i in sorted(list(set(months)))]))
    plot_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    plot_name += '.jpg'
    plt.savefig(plot_name)
    plt.close()
    return plot_name