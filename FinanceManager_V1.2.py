import PySimpleGUI as sg # import libary
import datetime
import calendar
import date_picker as dp
import pandas as pd

def update_gui(gui_data, gui_income_month, gui_expense_month, gui_balance_month):
    window['-tablelist-'].update(gui_data)
    window['-INCOME-'].update('Income\nRM'+str(gui_income_month))
    window['-EXPENSE-'].update('Expense\nRM'+str(gui_expense_month))
    window['-BALANCE-'].update('Balance\nRM'+str(gui_balance_month))
    
def update_df(DF, CUR_MONTH, CUR_YEAR):
    df_sort = DF[DF['Date'].str.contains('{}/{}'.format(CUR_MONTH,CUR_YEAR))]
    data = df_sort.values.tolist()
    income_month = int(df_sort.loc[df['Type']=='Income','Amount'].sum())
    expense_month = int(df_sort.loc[df['Type']=='Expense','Amount'].sum())
    balance_month = income_month - expense_month
    return data, income_month, expense_month, balance_month
    

sg.theme('Default1')  # select theme
sg.theme_text_color('#000000')
sg.theme_background_color('#F0F0F0')

fname = './img/button.png'

#read csv in Pandas
df = pd.read_csv('expenses_dummy(R1).csv', sep=',', engine='python', header=0)
#assign header and data to list
header_list = df.columns.tolist()
#data = df.values.tolist()


#Month, Year Font Style
arrow_font = 'TkFixedFont 7'
mon_year_font = 'TkFixedFont 10'

#Current Month, Year parameter
now = datetime.datetime.now()
cur_month, cur_year = now.month, now.year
mon_names = [calendar.month_name[i] for i in range(1,13)]

data, income_month, expense_month, balance_month = update_df(df,cur_month,cur_year)
#df_sort = df[df['Date'].str.contains('{}/{}'.format(cur_month,cur_year))]
#data = df_sort.values.tolist()
#income_month = int(df_sort.loc[df['Type']=='Income','Amount'].sum())
#expense_month = int(df_sort.loc[df['Type']=='Expense','Amount'].sum())
#balance_month = income_month - expense_month
 
layout = [#First Row
            [sg.B('◄◄', font=arrow_font, border_width=0, key='-YEAR-DOWN-', pad=(3,2)),
            sg.B('◄', font=arrow_font, border_width=0, key='-MON-DOWN-', pad=(0,2)),
            sg.Text('{} {}'.format(mon_names[cur_month - 1], cur_year), size=(38, 1), justification='c', font=mon_year_font, key='-MON-YEAR-', pad=(0,2)),
            sg.B('►', font=arrow_font,border_width=0, key='-MON-UP-', pad=(0,2)),
            sg.B('►►', font=arrow_font,border_width=0, key='-YEAR-UP-', pad=(3,2))],
            
 
            #Second Row
            [sg.Text('Income\nRM{}'.format(income_month), key='-INCOME-', font='Bold', text_color='DarkBlue', justification='c', size=(11,2), relief=sg.RELIEF_RIDGE),
            sg.Text('Expenses\nRM{}'.format(expense_month), key='-EXPENSE-', font='Bold', text_color='Red', justification='c', size=(11,2), relief=sg.RELIEF_RIDGE),
            sg.Text('Balance\nRM{}'.format(balance_month), key='-BALANCE-', font='Bold', justification='c', size=(11,2), relief=sg.RELIEF_RIDGE)],

            #Third Row
            [sg.Table(values=data,
                  headings=header_list,
                  key='-tablelist-',
                  display_row_numbers=False,
                  auto_size_columns=False,
                  num_rows=12)],
            
            #Fourth Row
            [sg.B('',image_filename=fname, key='-ADD-', image_size=(50,50), border_width=0)],
            
            ] 

# construct the window
window = sg.Window('Finance Manager V1.0', layout, element_justification='center')
window_2_active = False

category_list = ('Salary','Allowance', 'Bonus', 'Food', 'Entertainment', 'Utility', 'Others')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'exit': 
        break
    if event == '1':
        popup_get_date()
        
    # Month, Year Selection
    if event in ('-MON-UP-', '-MON-DOWN-', '-YEAR-UP-','-YEAR-DOWN-'):
        cur_month += (event == '-MON-UP-')
        cur_month -= (event == '-MON-DOWN-')
        cur_year += (event == '-YEAR-UP-')
        cur_year -= (event == '-YEAR-DOWN-')
        if cur_month > 12:
            cur_month = 1
            cur_year += 1
        elif cur_month < 1:
            cur_month = 12
            cur_year -= 1
        #Update table data
        data, income_month, expense_month, balance_month = update_df(df,cur_month,cur_year)
        #df_sort = df[df['Date'].str.contains('{}/{}'.format(cur_month,cur_year))]
        #data = df_sort.values.tolist()
        #income_month = int(df_sort.loc[df['Type']=='Income','Amount'].sum())
        #expense_month = int(df_sort.loc[df['Type']=='Expense','Amount'].sum())
        #balance_month = income_month - expense_month
        #Update Dashboard View
        window['-MON-YEAR-'].update('{} {}'.format(mon_names[cur_month - 1], cur_year))
        update_gui(data,income_month,expense_month,balance_month)
        #window['-tablelist-'].update(data)
        #window['-INCOME-'].update('Income\nRM'+str(income_month))
        #window['-EXPENSE-'].update('Expense\nRM'+str(expense_month))
        #window['-BALANCE-'].update('Balance\nRM'+str(balance_month))
        
    #Add transaction record
    if not window_2_active and event == '-ADD-':
        window_2_active = True
        layout2 = [#Form
                    [sg.T('Transaction Type:', size=(13,1)), sg.Combo(('Income', 'Expense'),default_value='Income',key='-TRANS_TYPE-', size=(20, 1))],
                    [sg.T('Date:', size=(13,1)),sg.B('Select Date', key='-TRANS_DATE-', size=(18,1))],
                    [sg.T('Account:', size=(13,1)),sg.Combo(('Bank', 'Cash'), default_value='Bank',key='-TRANS_ACCOUNT-', size=(20, 1))],
                    [sg.T('Category:', size=(13,1)),sg.Combo(category_list, default_value='Salary',key='-TRANS_CATEGORY-', size=(20, 1))],
                    [sg.T('Amount:', size=(13,1)),sg.InputText(size=(20,1),key ='-TRANS_AMOUNT-',tooltip='Currency: MYR')],
                    [sg.B('Save', button_color=('white', 'firebrick3'), size=(10,1), key='-TRANS_SAVE-'),sg.B('Cancel',key='-TRANS_EXIT-')],
                   ]

        window_2 = sg.Window('New Record', layout2)
    
    while window_2_active:
        event2, values2 = window_2.read()
        
        if event2 == sg.WIN_CLOSED or event2 == '-TRANS_EXIT-':
            window_2_active = False
            window_2.close()
        
        #Date selector
        if event2 == '-TRANS_DATE-':
            month,day,year = dp.popup_get_date(location=(window_2.current_location()[0]+130, window_2.current_location()[1]+30))
            trans_date = "{}/{}/{}".format(day,month,year)
            window_2['-TRANS_DATE-'].update(trans_date)
        
        if event2 == '-TRANS_SAVE-':
            df_add = pd.DataFrame ({
                'Date':[trans_date],
                'Type':[values2['-TRANS_TYPE-']],
                'Account':[values2['-TRANS_ACCOUNT-']],
                'Category':[values2['-TRANS_CATEGORY-']],
                'Amount':[int(values2['-TRANS_AMOUNT-'])], 
                })
            df = df.append(df_add, ignore_index=True)
            data, income_month, expense_month, balance_month = update_df(df,cur_month,cur_year)
            update_gui(data,income_month,expense_month,balance_month)
            window_2.close()
        
        
window.close()





