#!/usr/bin/env python
# coding: utf-8

from tkinter import *
import tkinter.ttk
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import mysql.connector
import PIL
from PIL import ImageTk, Image
import tkinter.font
from tkinter import font
import random
from glob import glob
from tkinter import messagebox
import numpy as np


# Setting food categories dictionary -----------------------------------------------------------------------------------------------
# Global Variables
PW = 'PASSWORD'

foodcategories = {0:'grains', 1:'snacks', 2:'barbecues', 3:'noodles', 4:'rice', 
                  5:'stir_fries', 6:'sidedishes', 7:'drinks', 8:'stews', 9:'steamed', 
                  10:'fries', 11:'sashimi', 12:'instant', 13:'others'}

foodcategories_r = {'grains':0, 'snacks':1, 'barbecues':2, 'noodles':3, 'rice':4,
                    'stir_fries':5, 'sidedishes':6,'drinks':7, 'stews':8,'steamed':9,
                    'fries':10,'sashimi':11, 'instant':12, 'others':13}
                    
# Connection for Mysql ---------------------------------------------------------------------------------------------------
def db_connect():
    # mydb = pymysql.connect( 
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    # passwd="wjdtkfkd12!@",
    passwd = PW,
    database="eatmate")
    return mydb


# Initialize the results when you press the left menu  ---------------------------------------------------------------------------------------------------
def clear_frame(middle_frame):
    for contents in middle_frame.winfo_children():
        contents.destroy()   

def go_back(toplevel):
    toplevel.destroy()

# Search and user menu ----------------------------------------------------------------------------------------------------------------   
     
# Search function 
def entry_search(middle_frame, search_entry, event='<Return>'):

    ## set keyword
    keyword = str(search_entry.get())
    
    ## search keyword
    mydb = db_connect()
    myCursor = mydb.cursor()
    q = f"""    select foodName, kcal, carbo, protein, fat, foodId from eatmate.food
    where foodName like "%{keyword}%"
    group by foodId
    """
    myCursor.execute(q)
    myResult = myCursor.fetchall()
    search_frame = Frame(middle_frame, bg='white')
    search_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    ## Search Result
    Label(search_frame, text="Search Result", font=("Candara",17),fg='darkorange', bg='white', anchor=CENTER).place(relx=0.05, rely=0.05)

        ### Set grid
    for i in range(3):
        Label(search_frame, bg='white').grid(column=0, row=i)
    Label(search_frame, bg='white').grid(column=12, row=18)
    for i in range(13):
        if i%2 == 0:
            search_frame.columnconfigure(i, weight=1)
   
        ### display Search Result
    for i, col in enumerate(['Food Name','Calorie(kcal)','Carbohydrate(g)','Protein(g)','Fat(g)','Eat']):
            Label(search_frame, text=col, bg='navajo white', font=("Arial", 10)).grid(column=1+2*i, row=3)
    
        ### if search results exist
    if myResult:
            #### if number of search results bigger than 14
        if len(myResult) > 14:
            myResult = random.sample(myResult, k=14)
            #### display search results
        for i, result in enumerate(myResult):
            name, kcal, carbo, protein, fat, id = result
            for j, col in enumerate(result[:-1]):
                Label(search_frame, text=col, bg='white').grid(row=4+i, column=1+2*j)
            Button(search_frame, text='Eat',command=lambda id=id, name=name:eat(id, name)).grid(row=4+i, column=11)
    
        ### if search result do not exist
    else: 
        Label(middle_frame, text=f'There is no food about "{keyword}".', bg='white', font=("Candara", 15)).place(anchor=CENTER, relx=0.5, rely=0.55)
            #### search result empty
        for i in range(14):
            for j in range(5):
                Label(search_frame, bg='white').grid(column=1+2*j, row=4+i)


# Initialize the eat table
def clear_records(middle_frame, image_obj, medal_obj):

    ## Really want to Clear?
    response = messagebox.askokcancel("Ok Cancel", "Really want to Clear?")

        ### if ok, eat table initialize
    if response:
        mydb = db_connect()
        myCursor = mydb.cursor()
        q = "truncate table eatmate.eat"
        myCursor.execute(q)
        mydb.commit()
        clear_frame(middle_frame)
        open_user(middle_frame, image_obj, medal_obj)
        mydb.close()

        
        
        
# User button
def open_user(middle_frame, image_obj, medal_obj):

    ## Set frame
    Frame(middle_frame, bg='floral white').place(relx=0.03, rely=0.04, relwidth=0.9, relheight=0.34)
    Frame(middle_frame, bg='floral white').place(relx=0.03, rely=0.4, relwidth=0.9, relheight=0.27)
    Frame(middle_frame, bg='floral white').place(relx=0.03, rely=0.72, relwidth=0.9, relheight=0.20)    

    ## Set grid
    Label(middle_frame, bg='floral white').grid(column=0, row=0)
    for i in range(1, 15) :
        Label(middle_frame, bg='floral white').grid(column=6, row=i)
    Label(middle_frame, bg='floral white').grid(column=6, row=30)
    for i in range(4):
        middle_frame.columnconfigure(i*2, weight=1)

    ## Rank
    Label(middle_frame, text="Rank", font=("Candara",17),
                    fg='darkorange', bg='floral white', anchor=CENTER).place(relx=0.05, rely=0.05)

        ### Clear Button
    clear_button = Button(middle_frame, bg='white', text='Clear', command=lambda: clear_records(middle_frame, image_obj, medal_obj))
    clear_button.place(relx=0.89, rely=0.9, relwidth=0.08)
    
        ### After ordering foodid by the number of times eaten in descending order,
        ### food name, carbohydrate, protein, and fat columns are extracted.
    mydb = db_connect()
    myCursor = mydb.cursor()
    q = """    select f.foodId, c.foodCat, c.foodName, c.carbo, c.protein, c.fat
    from (select foodId, count(*) as cnt from eatmate.eat
    group by foodId
    order by count(*) desc) as f
    left join eatmate.food as c
    using (foodId)
    group by foodId
    order by cnt desc
    """
    myCursor.execute(q)
    myResult = myCursor.fetchall()
    mydb.close()

        ### if eat table is empty
    if len(myResult) < 3:
        Label(middle_frame, text='There is no RECORD.', bg='floral white', font=("Candara", 15)).place(relx=0.4, rely=0.17)
        Label(middle_frame, text='There is no RECORD.', bg='floral white', font=("Candara", 15)).place(relx=0.4, rely=0.8)
    
        ### if eat table is not empty
    else:
        mean_list = list(zip(*myResult))

            #### display Rank Food (1st, 2nd, 3rd)
        for i, (_, cat, name, _, _, _) in enumerate(myResult[:3]):
            Label(middle_frame, image=image_obj[foodcategories_r[cat]], bg='white').grid(column=1+2*i, row=3) 
            Label(middle_frame, text=f'No.{i+1} {name}', bg='floral white', font=("나눔스퀘어_ac", 10)).grid(column=1+2*i, row=4)

            #### compare eat table mean to food table mean
        for i, nutrient in enumerate(['Carbohydrate','Protein','Fat']):
            Label(middle_frame, text=nutrient, bg='navajo white', font=("Arial", 10)).grid(column=1+2*i, row=15)
            Label(middle_frame, text=f'{round(np.mean(mean_list[i+3]), 2)} / {[34.16, 5.69, 7.88][i]}', bg='floral white').grid(column=1+2*i, row=16)

            #### display medal image
        for i in range(len(medal_obj)):
            medal_label = Label(middle_frame, image=medal_obj[i], bd=0, bg='floralwhite')
            medal_label.place(relx=0.07+(0.272*(i+(0.02*i))), rely=0.105)
    
    ## Participation Award
    Label(middle_frame, text="Participation Award", font=("Candara",17),fg='darkorange', bg='floral white', anchor=CENTER).place(relx=0.05, rely=0.4)

        ### if number of search results smaller than 3
    if len(myResult) <= 3:
        Label(middle_frame, text='There is no RECORD.', bg='floral white', font=("Candara", 15)).place(relx=0.4, rely=0.5)

        ### display participation awards
    else:
        for i, (_, _, name, _, _, _) in enumerate(myResult[3:7]):
            Label(middle_frame, text=name, bg='floral white').place(relx=0.13, rely=0.48+(0.05*i))
        for i, (_, _, name, _, _, _) in enumerate(myResult[7:11]):
            Label(middle_frame, text=name, bg='floral white').place(relx=0.53, rely=0.48+(0.05*i))

    ## Your Taste
    Label(middle_frame, text="Your Taste", font=("Candara",17),fg='darkorange', bg='floral white', anchor=CENTER).place(relx=0.05, rely=0.71)
                    
        
# Homepage. -------------------------------------------------------------------------------------------------------------

    ## Home button Functions
def homebutton_show(window, catkey, frame_image_obj, back_img, reset_img):

        ### When random search
    if catkey=='random_meal':
        catkey = random.choice(['grains','barbecues','noodles','rice', 'stir_fries', 'sidedishes', 'stews','steamed','fries','sashimi','instant','others'])
    elif catkey=='random_dessert':
        catkey = random.choice(['snacks', 'drinks'])

        ### Main homebutton function
    h_top = Toplevel(window)
    h_top.geometry("300x300")
    h_top.title('EatMate')
    h_top.resizable(0,0)
    
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT foodName, foodId FROM food WHERE foodCat = '{catkey}' LIMIT 30;""")
    myresult = cursor.fetchall()
                            
    random_food = random.choice(myresult)
    random_foodName = random_food[0]
    random_foodId = random_food[1]
    new_catkey = catkey
    
    result_bg_image = Label(h_top, image=frame_image_obj[foodcategories_r[catkey]])
    result_bg_image.place(x=0, y=0)
    result_textlabel = Label(h_top, text=random_foodName, font=("나눔스퀘어_ac", 10), bg='floralwhite')
    result_textlabel.place(relwidth=0.5, relheight=0.15, relx=0.25, rely=0.55)  
    
    eat_button = Button(h_top, text='EAT', bg="orange",fg='white', anchor=CENTER, bd=0,
                        font=font.Font(family="Candara",size=11, weight='bold'), 
                        command=lambda: eat(random_foodId, random_foodName, h_top))
    eat_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.7)
    
    back_button = Button(h_top, image=back_img, relief='flat', command=lambda: go_back(h_top))
    back_button.place(relx=0.05, rely=0.85)
    
    random_button = Button(h_top, image=reset_img, relief='flat', 
                           command=lambda: [go_back(h_top), homebutton_show(window, new_catkey, frame_image_obj, back_img, reset_img)])
    random_button.place(relx=0.85, rely=0.85)
    
    conn.close()    


    ## Making hombuttons
def homebutton(window, middle_frame, image_obj, frame_image_obj, back_img, reset_img): 
    middle_titlelabel = Label(middle_frame, text="Choose category you want to eat", bg='white', fg='darkorange',
                           font=("Candara", 15, 'bold'), anchor=CENTER)
    middle_titlelabel.place(relx=0.27, rely=0.03)
    
    cat_button0 = Button(middle_frame, image=image_obj[0], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[0], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[0]}", compound='top')
    cat_button0.place(relx=0.13, rely=0.13)
    
    cat_button1 = Button(middle_frame, image=image_obj[1], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[1], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[1]}", compound='top')
    cat_button1.place(relx=0.13+0.2, rely=0.13)
    
    cat_button2 = Button(middle_frame, image=image_obj[2], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[2], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[2]}", compound='top')
    cat_button2.place(relx=0.13+0.4, rely=0.13)
    
    cat_button3 = Button(middle_frame, image=image_obj[3], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[3], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[3]}", compound='top')
    cat_button3.place(relx=0.13+0.6, rely=0.13)
    
    cat_button4 = Button(middle_frame, image=image_obj[4], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[4], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[4]}", compound='top')
    cat_button4.place(relx=0.13, rely=0.43)
    
    cat_button5 = Button(middle_frame, image=image_obj[5], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[5], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[5]}", compound='top')
    cat_button5.place(relx=0.13+0.2, rely=0.43)
    
    cat_button6 = Button(middle_frame, image=image_obj[6], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[6], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[6]}", compound='top')
    cat_button6.place(relx=0.13+0.4, rely=0.43)
    
    cat_button7 = Button(middle_frame, image=image_obj[7], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[7], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[7]}", compound='top')
    cat_button7.place(relx=0.13+0.6, rely=0.43)
    
    cat_button8 = Button(middle_frame, image=image_obj[8], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[8], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[8]}", compound='top')
    cat_button8.place(relx=0.13, rely=0.73)
    
    cat_button9 = Button(middle_frame, image=image_obj[9], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[9], frame_image_obj, back_img, reset_img),
                        text=f"{foodcategories[9]}", compound='top')
    cat_button9.place(relx=0.13+0.2, rely=0.73)
    
    cat_button10 = Button(middle_frame, image=image_obj[10], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[10], frame_image_obj, back_img, reset_img),
                         text=f"{foodcategories[10]}", compound='top')
    cat_button10.place(relx=0.13+0.4, rely=0.73)
    
    cat_button11 = Button(middle_frame, image=image_obj[11], relief='ridge', bd=1, font="Candara",
                        command=lambda: homebutton_show(window, foodcategories[11], frame_image_obj, back_img, reset_img),
                         text=f"{foodcategories[11]}", compound='top')
    cat_button11.place(relx=0.13+0.6, rely=0.73)
        
# Second Page: Category Search ---------------------------------------------------------------------------------------------------------------

    ## Define Category Searching
def category_search(window, cat, frame_image_obj, back_img, reset_img):

    c_top = Toplevel(window)
    c_top.geometry("300x300")
    c_top.resizable(0,0)

    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT f.foodName, f.foodId, f.foodCat FROM eatmate.food as f JOIN eatmate.{cat} as c ON f.foodId = c.foodId""")
    myresult = cursor.fetchall()
    
    random_list = random.choice(myresult)
    random_foodName = random_list[0]
    random_foodId = random_list[1]
    random_foodCat = random_list[2]

    newcat = cat
    
    result_bg_image = Label(c_top, image=frame_image_obj[foodcategories_r[random_foodCat]])
    result_bg_image.place(x=0, y=0)
    result_textlabel = Label(c_top, text=random_foodName, font=("나눔스퀘어_ac", 10), bg='floralwhite')
    result_textlabel.place(relwidth=0.5, relheight=0.15, relx=0.25, rely=0.55)  
    
    eat_button = Button(c_top, text='EAT', bg="orange",fg='white', anchor=CENTER, bd=0,
                        font=font.Font(family="Candara",size=10, weight='bold'), 
                        command=lambda: eat(random_foodId, random_foodName, c_top))
    eat_button.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.7)
    
    random_button = Button(c_top, image=reset_img, relief='flat', 
                           command=lambda: [go_back(c_top), category_search(window, newcat, frame_image_obj, back_img, reset_img)])
    random_button.place(relx=0.85, rely=0.85)
    
    back_button = Button(c_top, image=back_img, relief='flat', command= lambda: go_back(c_top))
    back_button.place(relx=0.05, rely=0.85)
    
    conn.close()

    # Displaying Second page
def page2(window, middle_frame, frame_image_obj, back_img, reset_img):
    
    ## Displaying Headers
    header = ['Nutrient', 'Flavor', 'Special']
    for i in range(len(header)):
        head_label = Label(middle_frame, text=f"{header[i]}", font=("Candara",15),
                           fg='darkorange', bg='white', anchor=CENTER)
        head_label.place(relx=0.05, rely=0.05+(0.3*i))
    
    
    ## First row: Nutrient
    #### Searching for low calories
    lowcal_btn = Button(middle_frame, text="Low-  Calorie", font=("Candara",11), fg='white', bg='gray', 
                        wraplength=45, anchor=CENTER, 
                        command= lambda: category_search(window=window, cat='lowcal', frame_image_obj=frame_image_obj, 
                                                         back_img=back_img, reset_img=reset_img))
    lowcal_btn.place(relwidth=0.11, relheight=0.2, relx=0.06, rely=0.13)

    #### Searching for high proteins
    highprt_btn = Button(middle_frame, text="High-  Protein", font=("Candara",11), fg='white', bg='gray', 
                         wraplength=45, anchor=CENTER, 
                         command= lambda: category_search(window=window, cat='highprt', frame_image_obj=frame_image_obj, 
                                                          back_img=back_img, reset_img=reset_img))
    highprt_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.13, rely=0.13)

    #### Searching for low fat
    lowfat_btn = Button(middle_frame, text="Low- Fat", font=("Candara",11), fg='white', bg='gray', 
                        wraplength=45, anchor=CENTER, 
                        command= lambda: category_search(window=window, cat='lowfat', frame_image_obj=frame_image_obj, 
                                                         back_img=back_img, reset_img=reset_img))
    lowfat_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.26, rely=0.13)

    #### Searching for low carbohydrates
    lowcar_btn = Button(middle_frame, text="Low- Carbo hydrate", font=("Candara",11), fg='white', bg='gray', 
                        wraplength=45, anchor=CENTER, 
                        command= lambda: category_search(window=window, cat='lowcarbo', frame_image_obj=frame_image_obj, 
                                                         back_img=back_img, reset_img=reset_img))
    lowcar_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.39, rely=0.13)


    ## Second row: Flavor
    #### Searching for spicy food
    spicy_btn = Button(middle_frame, text="Spicy", font=("Candara",11), fg='white', bg='gray', 
                       wraplength=45, anchor=CENTER, 
                       command= lambda: category_search(window=window, cat='spicy', frame_image_obj=frame_image_obj, 
                                                        back_img=back_img, reset_img=reset_img))
    spicy_btn.place(relwidth=0.11, relheight=0.2, relx=0.06, rely=0.43)

    #### Searching for sweeties
    sweet_btn = Button(middle_frame, text="Sweet", font=("Candara",11), fg='white', bg='gray', 
                       wraplength=45, anchor=CENTER, 
                       command= lambda: category_search(window=window, cat='dessert', frame_image_obj=frame_image_obj, 
                                                        back_img=back_img, reset_img=reset_img))
    sweet_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.13, rely=0.43)

    #### Searching for greasy food
    greasy_btn = Button(middle_frame, text="Greasy", font=("Candara",11), fg='white', bg='gray', 
                        wraplength=45, anchor=CENTER, 
                        command= lambda: category_search(window=window, cat='oily', frame_image_obj=frame_image_obj, 
                                                         back_img=back_img, reset_img=reset_img))
    greasy_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.26, rely=0.43)

    ## Third row: Special
    #### Searching for munchies
    sweet_btn = Button(middle_frame, text="Mun   chies", font=("Candara",11), fg='white', bg='gray', 
                       wraplength=45, anchor=CENTER, 
                       command= lambda: category_search(window=window, cat='alcoholic', frame_image_obj=frame_image_obj, 
                                                        back_img=back_img, reset_img=reset_img))
    sweet_btn.place(relwidth=0.11, relheight=0.2, relx=0.06, rely=0.73)

    #### Searching for delivery food
    del_btn = Button(middle_frame, text="Delivery", font=("Candara",11), fg='white', bg='gray', 
                     wraplength=45, anchor=CENTER, 
                     command= lambda: category_search(window=window, cat='delivery', frame_image_obj=frame_image_obj, 
                                                      back_img=back_img, reset_img=reset_img))
    del_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.13, rely=0.73)

    #### Searching for healthy food
    heal_btn = Button(middle_frame, text="Healthy", font=("Candara",11), fg='white', bg='gray', 
                      wraplength=45, anchor=CENTER, 
                      command= lambda: category_search(window=window, cat='dietry', frame_image_obj=frame_image_obj, 
                                                       back_img=back_img, reset_img=reset_img))            
    heal_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.26, rely=0.73)

    #### Searching for group dinings
    group_btn = Button(middle_frame, text="Group Meal", font=("Candara",11), fg='white', bg='gray',
                       wraplength=45, anchor=CENTER, 
                       command= lambda: category_search(window=window, cat='eatalong', frame_image_obj=frame_image_obj, 
                                                        back_img=back_img, reset_img=reset_img))
    group_btn.place(relwidth=0.11, relheight=0.2, relx=0.06+0.39, rely=0.73) 

        
        
        
# Third Page: Search by filters-------------------------------------------------------------------------------------------

# EAT Button
def eat(pickId, pickName, window=None):

    ## show information about eatten
    messagebox.showinfo("Message", f"You eat {pickName}")

    ## add food to the eat table
    mydb = db_connect()
    myCursor = mydb.cursor()
    q = f"""    insert into eatmate.eat(foodId, eatTime)
    values({pickId}, now())
    """
    myCursor.execute(q)
    mydb.commit()
    mydb.close()

    ## if there is window, destroy it
    if window:
        go_back(window)
        
# Filter Button > Meal Button
def start_meal(top, small_image_obj, frame_image_obj, back_img, reset_img):

    ## Meal window
    ttop = Toplevel(top)
    ttop.geometry('300x400')
    ttop.title('EatMate')
    ttop.resizable(0,0)
    tt_top_frame = Frame(ttop, bg='darkorange')
    tt_top_frame.place(relheight=1, relwidth=1, relx=0, rely=0)

    ## What kind of Food?
    Label(tt_top_frame, text='What kind of Food?', bg='darkorange', fg='white', font=font.Font(family="Candara",size=15)).pack()
    
    meal_list = ['grains','barbecues','noodles','rice', 'stir_fries', 'sidedishes', 'stews','steamed','fries','sashimi','instant','others']
    meal_idx = [0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]

        ### Category Buttons
    for i, (name, idx) in enumerate(zip(meal_list, meal_idx)):
        Button(tt_top_frame, text=name, image=small_image_obj[idx], command=lambda ttop=ttop, name=name, frame_image_obj=frame_image_obj: 
                homebutton_show(ttop, name, frame_image_obj, back_img, reset_img), compound='center', font=font.Font(family='Candara', size=13, weight='bold'), 
                fg='black', relief='flat').place(relx=0.05+(i%3)*0.3, rely=0.1+int(i/3)*0.20, relwidth=0.27, relheight=0.19)
    
        ### Random Button 
    random_button = Button(tt_top_frame, text='Random', bg='white', fg='darkorange',
    font=font.Font(family='Candara', size=13, weight='bold'), relief='flat', command=lambda: homebutton_show(ttop, 'random_meal', frame_image_obj, back_img, reset_img))
    random_button.place(relx=0.35, relwidth=0.27, rely=0.9, relheight=0.08)

# Filter Button > Dessert Button
def start_dessert(top, big_image_obj, frame_image_obj, back_img, reset_img):

    ## Dessert window
    ttop = Toplevel(top)
    ttop.geometry('300x400')
    ttop.title('EatMate')
    ttop.resizable(0,0)
    tt_top_frame = Frame(ttop, bg='darkorange')
    tt_top_frame.place(relheight=1, relwidth=1, relx=0, rely=0)

    ## What kind of Food?
    Label(tt_top_frame, text='What kind of Food?', bg='darkorange', fg='white', font=font.Font(family="Candara",size=15)).pack()

        ### Snacks Button
    snacks = Button(tt_top_frame, text='snacks', image=big_image_obj[1], font=font.Font(family="Candara",size=30, weight='bold'), command=lambda: homebutton_show(ttop, 'snacks', frame_image_obj, back_img, reset_img),compound='center', fg='black', relief='flat')
    snacks.place(relx=0.1, rely=0.07, relheight=0.4, relwidth=0.8)

        ### Drinks Button
    drinks = Button(tt_top_frame, text='drinks', image=big_image_obj[7], font=font.Font(family="Candara",size=30, weight='bold'), command=lambda: homebutton_show(ttop, 'drinks', frame_image_obj, back_img, reset_img),compound='center', fg='black', relief='flat')
    drinks.place(relx=0.1, rely=0.48, relheight=0.4, relwidth=0.8)
    
        ### Ramdom Button
    random_button = Button(tt_top_frame, text='Random', bg='white', fg='darkorange',
    font=font.Font(family='Candara', size=13, weight='bold'), relief='flat', command=lambda: homebutton_show(ttop, 'random_dessert', frame_image_obj, back_img, reset_img))
    random_button.place(relx=0.35, relwidth=0.27, rely=0.9, relheight=0.08)

# Filter Button
def start_filter(window, middle_frame, small_image_obj, big_image_obj, frame_image_obj, back_img, reset_img, imgs):

    ## display loading image
    Label(middle_frame, image = imgs[0], bg='white').place(relx=0.45, rely=0.5)
    Label(middle_frame, text="Filtering", font=("Candara",17), bg='white').place(relx=0.45, rely=0.45)

    ## Filter window
    top = Toplevel(window)
    top.geometry('300x400')
    top.title('EatMate')
    top.resizable(0,0)

    ## set frame
    t_top_frame = Frame(top, bg='darkorange')
    t_top_frame.place(relheight=1, relwidth=1, relx=0, rely=0)

    ## What kind of Food?
    Label(t_top_frame, text='What kind of Food?', bg='darkorange', fg='white', font=font.Font(family="Candara",size=15)).pack() 

        ### Meal Button
    meal_button = Button(t_top_frame, font=font.Font(family="Candara",size=30, weight='bold'), 
    fg='white', image=imgs[1], text="Meal", command=lambda: start_meal(top, small_image_obj, frame_image_obj, back_img, reset_img), 
    compound="center", relief='flat')
    meal_button.place(relx=0.1, rely=0.07, relheight=0.45, relwidth=0.8)
    
        ### Dessert Button
    dessert_button = Button(t_top_frame, font=font.Font(family="Candara", size=30, weight='bold'), 
    fg='white', image=imgs[2], text="Dessert", command=lambda: start_dessert(top, big_image_obj, frame_image_obj, back_img, reset_img),
    compound="center", relief='flat')
    dessert_button.place(relx=0.1, rely=0.53, relheight=0.45, relwidth=0.8)

    
# Main ---------------------------------------------------------------------------------------------------------------    
def main():
    # Main Window
    window = Tk()
    window.title("EatMate") # set title
    window.geometry("800x600")
    window.resizable(0,0)
    
    # Image storage
    # image_list = glob("C:/Users/user/Desktop/SQL/프로젝트/images/*png")
    image_list = glob("images/*png")
    image_obj = []

    for x in image_list:
        image = Image.open(x)
        image_resized = image.resize((80,90))
        image_obj.append(ImageTk.PhotoImage(image_resized))
    
    small_image_obj = []
    for x in (image_list):
        image = Image.open(x)
        image_resized = image.resize((85,80))
        small_image_obj.append(ImageTk.PhotoImage(image_resized))
        
    big_image_obj = []
    for x in (image_list):
        image = Image.open(x)
        image_resized = image.resize((300,400))
        big_image_obj.append(ImageTk.PhotoImage(image_resized))
        
    frame_image_obj=[]
    for x in (image_list):
        image = Image.open(x)
        image_resized = image.resize((300,300))
        frame_image_obj.append(ImageTk.PhotoImage(image_resized))

    # Screen Layout

        ## Left Frame: Menu
    left_frame = Frame(window, bg='oldlace')
    left_frame.place(relwidth=0.2, relheight=1)

    left_title = Label(left_frame, text="EatMate", font=("Candara", 20, 'bold'), fg='darkorange', bg='oldlace')
    left_title.pack(anchor=NE, padx=12, pady=10)

            ### Menu Button
                #### Home Menu
    left_button1 = Button(left_frame, text="Home", font="Candara",
                          fg='orange', bg='white', command= lambda: [clear_frame(middle_frame), homebutton(window, middle_frame, image_obj, frame_image_obj, back_img, reset_img)],
                          relief='groove', anchor=CENTER)
    left_button1.place(relwidth=0.8, relheight=0.07, relx=0.1, rely=0.1)

                #### Group Menu
    left_button2 = Button(left_frame, text="Group", font="Candara",
                          fg='orange', bg='white', command= lambda:[clear_frame(middle_frame), page2(window, middle_frame, frame_image_obj, back_img, reset_img)],
                          relief='groove', anchor=CENTER)
    left_button2.place(relwidth=0.8, relheight=0.07, relx=0.1, rely=0.18)

                #### Filter Menu
    left_button3 = Button(left_frame, text="Filter", font="Candara",
                          fg='orange', bg='white', 
                          relief='groove', anchor=CENTER,
                          command=lambda: [clear_frame(middle_frame), 
                                           start_filter(window, middle_frame, small_image_obj, big_image_obj, frame_image_obj, back_img, reset_img, imgs)])
    left_button3.place(relwidth=0.8, relheight=0.07, relx=0.1, rely=0.26)

    # left_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/spoon.png')
    left_img = Image.open('images/etc/spoon.png')
    left_img = left_img.resize((40,40))
    left_img = ImageTk.PhotoImage(left_img)
    left_spoon = Label(left_frame, image=left_img, bd=0, bg='oldlace')
    left_spoon.place(relx=0.06, rely=0.016)
    
        ## Upper Frame: Search box and user button
    top_frame = Frame(window, bg='darkorange')
    top_frame.place(relwidth=0.8, relheight=0.2, relx=0.2, rely=0.0)
    
            ### Search Box
    search_entry = Entry(top_frame, font=20, bd=0)
    search_entry.place(relwidth=0.65, relheight=0.35, relx=0.16, rely=0.15)
    search_entry.bind('<Return>', lambda x: [clear_frame(middle_frame), entry_search(middle_frame=middle_frame, search_entry=search_entry, event=x)])
    
            ### Magifying glass button
    # sbg_image = Image.open('C:/Users/user/Desktop/SQL/프로젝트/search.png')
    sbg_image = Image.open('images/etc/search.png')
    sbg_image = sbg_image.resize((40,40))
    simg = ImageTk.PhotoImage(sbg_image, master=top_frame)
    search_image = Button(top_frame,image=simg, bg='white',bd=0, command=lambda:[clear_frame(middle_frame), entry_search(middle_frame, search_entry)])
    search_image.place(relx=0.093, rely=0.15)        
        
            ### Medal images
    # medal_list = glob("C:/Users/user/Desktop/SQL/프로젝트/medal/*PNG")
    medal_list = glob("images/etc/medal/*png")
    medal_obj = []

    for x in medal_list:
        medal = Image.open(x)
        medal = medal.resize((50,70))
        medal_obj.append(ImageTk.PhotoImage(medal))

            ### User Button
    # bg_image = Image.open('C:/Users/user/Desktop/SQL/프로젝트/user_button.png')
    bg_image = Image.open('images/etc/profile2.png')
    bg_image = bg_image.resize((50, 50))
    img = ImageTk.PhotoImage(bg_image, master=top_frame)
    user_button = Button(top_frame, image=img, bg='darkorange', bd=0,
                        command=lambda: [clear_frame(middle_frame), open_user(middle_frame, image_obj, medal_obj)])
    user_button.place(relx=0.88, rely=0.1)
            
        
        ## Middle Frame: show result
    middle_frame = Frame(window, bg='white')
    middle_frame.place(relwidth=0.8, relheight=0.8, relx=0.2, rely=0.2)

            ### Back image
    # back_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/back.png')
    back_img = Image.open('images/etc/back.png')
    back_img = back_img.resize((30,30))
    back_img = ImageTk.PhotoImage(back_img)
    
            ### Reset image
    # reset_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/reload.png')
    reset_img = Image.open('images/etc/reload.png')
    reset_img = reset_img.resize((30,30))
    reset_img = ImageTk.PhotoImage(reset_img)

    # Home menu as the default
    homebutton(window, middle_frame, image_obj, frame_image_obj, back_img, reset_img)

    
    # load_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/loading.png')
    load_img = Image.open('images/etc/loading.png')
    load_img = load_img.resize((70, 50))
    load_img = ImageTk.PhotoImage(load_img, master = middle_frame) 

    # meal_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/meal.png')
    meal_img = Image.open('images/etc/meal.png')
    meal_img = meal_img.resize((240, 200))
    meal_img = ImageTk.PhotoImage(meal_img)

    # dessert_img = Image.open('C:/Users/user/Desktop/SQL/프로젝트/dessert.png')
    dessert_img = Image.open('images/etc/dessert.png')
    dessert_img = dessert_img.resize((240, 200))
    dessert_img = ImageTk.PhotoImage(dessert_img)
    imgs = [load_img, meal_img, dessert_img]
    
    # Run application   
    window.mainloop()

if __name__ == '__main__':
    main()






