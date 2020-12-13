from tkinter import Frame, Label, CENTER, Button, Radiobutton, IntVar, StringVar, BooleanVar, Entry, LEFT
import tkinter as tk
from PIL import Image, ImageTk
import game_functions
import numpy as np
import time
import pygame
import json
from datetime import datetime
import os

N = 4
EDGE_LENGTH = 200
CELL_COUNT = N
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"

LABEL_FONT = ("Verdana", 20)
SMALL_FONT = ("Verdana", 10)

GAME_COLOR = {0: "#e9f5f8", 1: "#285290"}

EMPTY_COLOR = {0: "#f8fcfd", 1: "#3163af"}

TILE_COLORS = {0:{2: "#399cbd", 4: "#44a6c6", 8: "#53adcb", 16: "#83c3d8",
                   32: "#8fcadd", 64: "#9ed1e1", 128: "#add8e6",
                   256: "#bcdfeb", 512: "#cbe6ef", 1024: "#0b4a1c",
                   2048: "#031f0a", 4096: "#000000", 8192: "#000000",}, 
              1:{2: "#3163af", 4: "#7ba1da", 8: "#9ab7e3", 16: "#b8cdeb",
                   32: "#c8d8f0", 64: "#d7e3f4", 128: "#e6eef8",
                   256: "#f6f8fc", 512: "#f2f2f0", 1024: "#0b4a1c",
                   2048: "#031f0a", 4096: "#000000", 8192: "#000000",

              }}

LABEL_COLORS = {0:{2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                   32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                   256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
                   2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0",},
                1:{2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                   32: "#011c08", 64: "#011c08", 128: "#011c08",
                   256: "#011c08", 512: "#011c08", 1024: "#011c08",
                   2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0",
                }}



class Display(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.color = IntVar()
        self.color.set(0)
        self.bg = GAME_COLOR[self.color.get()]
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up, 
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left, 
                         RIGHT_KEY: game_functions.move_right,
                         }
        self.gravitational = False
        self.cont = False
        self.new_game = False
        self.score = 0
        self.timer = 0
        self.ingame = False
        self.grid_cells = []
        self.status_cells = []
        self.game_type_code = IntVar()
        self.game_size = IntVar()
        self.sound = BooleanVar()
        self.player = StringVar()
        self.result_showed = BooleanVar()
        self.game_size.set(4)
        self.sound.set(False)
        self.back_from_partial = BooleanVar()
        self.back_from_partial.set(False)
        self.game_types = [("classic", 0), ("grav", 1)]
        self.nav_bar = Frame(self, bg='pink',
                           width=EDGE_LENGTH*4, height=EDGE_LENGTH)
        self.game_frame = Frame(self)
        self.game_para_cell = Frame()
        self.nav_bar.grid(row=0)
        self.menu_frame = Frame(self, bg='green',
                           width=EDGE_LENGTH*4, height=EDGE_LENGTH)
        self.menu_frame.grid(row=1)
        self.partial_result_frame = Frame()
        self.menu()


        self.mainloop()
    def bring_back_result(self, event):
        self.result_frame.grid_forget()
        self.partial_result_frame.grid_forget()
        self.show_result()

    def show_sum_score(self, event):
        self.result_showed.set(False)
        self.full_result_frame.grid_forget()
        self.partial_result_frame = Frame(self.result_frame, bg=GAME_COLOR[self.color.get()],
                               width=EDGE_LENGTH*2, height=EDGE_LENGTH)
        self.partial_result_frame.grid(padx=CELL_PAD, pady=CELL_PAD)
        quit_button = Button(master=self.partial_result_frame, text="Return", bg=EMPTY_COLOR[self.color.get()],
                              justify=CENTER, font=SMALL_FONT, width=5, height=2)
        quit_button.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=5)
        self.back_from_partial.set(True)
        quit_button.bind('<Button-1>', self.bring_back_result)
        result_dict = {}
        with open('result.json') as outfile:
            results = json.load(outfile)
            temp = results['result']
            for i in temp:
                if i['name'] not in result_dict.keys():
                    result_dict[i['name']] = i
                else:
                    result_dict[i['name']]['score']+=i['score']
        temp_sorted = sorted(list(result_dict.values()), key=lambda k: k['score'], reverse=True)
        name_table_label = Label(master=self.partial_result_frame, text='SUM SCORE', bg=GAME_COLOR[self.color.get()], width=20, height=2)
        name_table_label.grid(row=1, column=0, columnspan=3)
        name_label = Label(master=self.partial_result_frame, text='NAME', bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
        name_label.grid(row=2, column=0, columnspan=2)
        score_label = Label(master=self.partial_result_frame, text='SCORE', bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
        score_label.grid(row=2, column=2)
        for i in range(3,len(temp_sorted)+3): #Rows
            print(i)
            name_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['name']), bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
            name_label_val.grid(row=i, column=0, columnspan=2)
            score_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['score']), bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
            score_label_val.grid(row=i, column=2)

    def show_all_games(self, event):
        self.result_showed.set(False)
        self.full_result_frame.grid_forget()
        self.partial_result_frame = Frame(self.result_frame, bg=GAME_COLOR[self.color.get()],
                               width=EDGE_LENGTH*2, height=EDGE_LENGTH)
        self.partial_result_frame.grid(padx=CELL_PAD, pady=CELL_PAD)
        quit_button = Button(master=self.partial_result_frame, text="Return", bg=EMPTY_COLOR[self.color.get()],
                              justify=CENTER, font=SMALL_FONT, width=5, height=2)
        quit_button.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=5)
        self.back_from_partial.set(True)
        quit_button.bind('<Button-1>', self.bring_back_result)
        result_dict = {}
        with open('result.json') as outfile:
            results = json.load(outfile)
            temp = results['result']
            for i in temp:
                if i['name'] not in result_dict.keys():
                    result_dict[i['name']] = i
                else:
                    if result_dict[i['name']]['score'] < i['score']:
                        result_dict[i['name']] = i
        temp_sorted = list(result_dict.values())
        name_table_label = Label(master=self.partial_result_frame, text='INDIVIDUAL BEST', bg=GAME_COLOR[self.color.get()], width=20, height=2)
        name_table_label.grid(row=1, column=0, columnspan=5)
        name_label = Label(master=self.partial_result_frame, text='NAME', bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
        name_label.grid(row=2, column=0, columnspan=2)
        size_label = Label(master=self.partial_result_frame, text='SIZE', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
        size_label.grid(row=2, column=2)
        time_label = Label(master=self.partial_result_frame, text='TIME', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
        time_label.grid(row=2, column=3)
        score_label = Label(master=self.partial_result_frame, text='SCORE', bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
        score_label.grid(row=2, column=4)
        for i in range(3,len(temp_sorted)+3): #Rows
            print(i)
            name_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['name']), bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
            name_label_val.grid(row=i, column=0, columnspan=2)
            size_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['size']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            size_label_val.grid(row=i, column=2)
            time_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['time']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            time_label_val.grid(row=i, column=3)
            score_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-3]['score']), bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
            score_label_val.grid(row=i, column=4)

    def show_score_by_name(self, event):
        current_name = event.widget['text']
        self.result_showed.set(False)
        self.full_result_frame.grid_forget()
        self.partial_result_frame = Frame(self.result_frame, bg=GAME_COLOR[self.color.get()],
                               width=EDGE_LENGTH*2, height=EDGE_LENGTH)
        self.partial_result_frame.grid(padx=CELL_PAD, pady=CELL_PAD)
        quit_button = Button(master=self.partial_result_frame, text="Return", bg=EMPTY_COLOR[self.color.get()],
                              justify=CENTER, font=SMALL_FONT, width=5, height=2)
        quit_button.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=5)
        self.back_from_partial.set(True)
        quit_button.bind('<Button-1>', self.bring_back_result)
        with open('result.json') as outfile:
            results = json.load(outfile)
            
            temp = results['result']
            temp_with_name = []
            for i in temp:
                if i["name"] == current_name:
                    temp_with_name.append(i)
            #labels
        temp_sorted = sorted(temp_with_name, key=lambda k: k['score'], reverse=True)
        name_label = Label(master=self.partial_result_frame, text='NAME', bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
        name_label.grid(row=1, column=0, columnspan=2)
        size_label = Label(master=self.partial_result_frame, text='SIZE', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
        size_label.grid(row=1, column=2)
        time_label = Label(master=self.partial_result_frame, text='TIME', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
        time_label.grid(row=1, column=3)
        score_label = Label(master=self.partial_result_frame, text='SCORE', bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
        score_label.grid(row=1, column=4)
        for i in range(2,len(temp_sorted)+2): #Rows
            print(i)
            name_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-2]['name']), bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
            name_label_val.grid(row=i, column=0, columnspan=2)
            size_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-2]['size']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            size_label_val.grid(row=i, column=2)
            time_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-2]['time']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            time_label_val.grid(row=i, column=3)
            score_label_val = Label(master=self.partial_result_frame, text=str(temp_sorted[i-2]['score']), bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
            score_label_val.grid(row=i, column=4)

    def show_result(self, event=None):
        if self.result_showed.get() == False:
            self.partial_result_frame.grid_forget()
            self.result_showed.set(True)
            if not self.back_from_partial.get():
                self.menu_frame.grid_forget()
            self.back_from_partial.set(False)
            self.result_frame = Frame(self, bg=GAME_COLOR[self.color.get()],
                               width=EDGE_LENGTH*2, height=EDGE_LENGTH)
            self.result_frame.grid(padx=CELL_PAD, pady=CELL_PAD)
            
            height = 12
            width = 5
            self.full_result_frame = Frame(self.result_frame, bg=GAME_COLOR[self.color.get()],
                               width=EDGE_LENGTH*2, height=EDGE_LENGTH)
            self.full_result_frame.grid(padx=CELL_PAD, pady=CELL_PAD)
            quit_button = Button(master=self.full_result_frame, text="Return", bg=EMPTY_COLOR[self.color.get()],
                              justify=CENTER, font=SMALL_FONT, width=5, height=2)
            quit_button.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=5)
            quit_button.bind('<Button-1>', self.close_result)
            with open('result.json') as outfile:
                results = json.load(outfile)
                
                temp = results['result']
            #labels
            temp_sorted = sorted(temp, key=lambda k: k['score'], reverse=True)
            name_label = Button(master=self.full_result_frame, text='NAME', bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
            name_label.grid(row=1, column=0, columnspan=2)
            name_label.bind('<Button-1>', self.show_all_games)
            size_label = Label(master=self.full_result_frame, text='SIZE', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            size_label.grid(row=1, column=2)
            time_label = Label(master=self.full_result_frame, text='TIME', bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
            time_label.grid(row=1, column=3)
            score_label = Button(master=self.full_result_frame, text='SCORE', bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
            score_label.grid(row=1, column=4)
            score_label.bind('<Button-1>', self.show_sum_score)
            for i in range(2,height): #Rows
                print(i)
                name_label_val = Button(master=self.full_result_frame, text=str(temp_sorted[i-2]['name']), bg=EMPTY_COLOR[self.color.get()], width=10, height=2)
                name_label_val.grid(row=i, column=0, columnspan=2)
                name_label_val.bind('<Button-1>', self.show_score_by_name)
                size_label_val = Label(master=self.full_result_frame, text=str(temp_sorted[i-2]['size']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
                size_label_val.grid(row=i, column=2)
                time_label_val = Label(master=self.full_result_frame, text=str(temp_sorted[i-2]['time']), bg=EMPTY_COLOR[self.color.get()], width=5, height=2)
                time_label_val.grid(row=i, column=3)
                score_label_val = Label(master=self.full_result_frame, text=str(temp_sorted[i-2]['score']), bg=EMPTY_COLOR[self.color.get()], width=7, height=2)
                score_label_val.grid(row=i, column=4)
    
    def close_result(self, event=None):
        self.result_showed.set(False)
        self.result_frame.grid_forget()
        self.menu_frame.grid()

    def start_game(self, event):
        
        self.gravitational = False
        self.score = 0
        self.timer = 0
        self.grid_cells = []
        self.status_cells = []
        self.new_game = False
        self.ingame = True
        current_game_type = self.game_type_code.get()
        if current_game_type == 1:
            self.gravitational = True
        else:
            self.gravitational = False
        game_functions.N = self.game_size.get()
        self.menu_frame.grid_forget()
        self.game_frame.grid()
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()

    
    def continue_game(self, event):
        file_data = open('time.txt', 'r')
        self.game_size.set(int(file_data.readline().strip()))
        game_functions.N = self.game_size.get()
        game_functions.init_var()
        self.gravitational = (file_data.readline().strip()=='True')
        self.matrix = np.genfromtxt('matrix.csv', delimiter=',', dtype=np.int16)
        self.score = int(np.sum(self.matrix))
        self.timer = int(file_data.readline().strip())
        self.grid_cells = []
        self.status_cells = []
        self.new_game = False
        self.ingame = True
        self.menu_frame.grid_forget()
        self.game_frame.grid()
        self.build_grid()
        self.draw_grid_cells()

    def sound_play(self):
        if self.sound.get() == True:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()

    def change_color(self):
        self.configure(bg = GAME_COLOR[self.color.get()])
        for child in self.winfo_children():
            if type(child).__name__ in ['Button', 'Label', 'Radiobutton']:
                child.configure(bg = EMPTY_COLOR[self.color.get()])
            else: 
                child.configure(bg = GAME_COLOR[self.color.get()])
            for child2 in child.winfo_children():
                if type(child2).__name__ in ['Button', 'Label', 'Radiobutton']:
                    child2.configure(bg = EMPTY_COLOR[self.color.get()])
                else:
                    child2.configure(bg = GAME_COLOR[self.color.get()])
                for child3 in child2.winfo_children():
                    if type(child3).__name__ in ['Button', 'Label', 'Radiobutton']:
                        child3.configure(bg = EMPTY_COLOR[self.color.get()])
                    else: 
                        child3.configure(bg = GAME_COLOR[self.color.get()])
                    for child4 in child3.winfo_children():
                        if type(child4).__name__ in ['Button', 'Label', 'Radiobutton']:
                            child4.configure(bg = EMPTY_COLOR[self.color.get()])
                        else:
                            child4.configure(bg = GAME_COLOR[self.color.get()])
                            for child5 in child4.winfo_children():
                                if type(child5).__name__ in ['Button', 'Label', 'Radiobutton']:
                                    child5.configure(bg = EMPTY_COLOR[self.color.get()])
                                else:
                                    child5.configure(bg = GAME_COLOR[self.color.get()])
        self.game_para_cell.configure(bg=EMPTY_COLOR[self.color.get()])
        for child in self.game_para_cell.winfo_children():
            child.configure(bg = EMPTY_COLOR[self.color.get()])


    def menu(self):
        self.configure(bg = GAME_COLOR[self.color.get()])
        mute_icon = ImageTk.PhotoImage(Image.open("mute.png"))
        pygame.mixer.init()
        pygame.mixer.music.load("game_sound.mp3")
        self.sound_play()
        nav_bar = Frame(self.nav_bar,bg=GAME_COLOR[self.color.get()],
                           width=self.nav_bar.winfo_width(), height=EDGE_LENGTH)
        nav_bar.grid(columnspan=2)
        soundframe = Frame(nav_bar, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        soundframe.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        sound_on_checkbutton = Radiobutton(soundframe, text="Sound on", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, value=True, variable=self.sound, padx=15, pady=10, command=self.sound_play)
        sound_on_checkbutton.grid(row=0, column=0, sticky= tk.W)
         
        sound_off_checkbutton = Radiobutton(soundframe, text="Sound off",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, value=False, variable=self.sound , padx=15, pady=10, command=self.sound_play)
        sound_off_checkbutton.grid(row=0, column=1, sticky= tk.W)

        colorframe = Frame(nav_bar, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        colorframe.grid(row=1, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        light_mode_checkbutton = Radiobutton(colorframe, text="Light", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, value=0, variable=self.color, padx=15, pady=10, command=self.change_color)
        light_mode_checkbutton.grid(row=0, column=0, sticky= tk.W)
         
        dark_mode_checkbutton = Radiobutton(colorframe, text="Dark",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, value=1, variable=self.color , padx=15, pady=10, command=self.change_color)
        dark_mode_checkbutton.grid(row=0, column=1, sticky= tk.W)
        
        background = Frame(self.menu_frame, bg=GAME_COLOR[self.color.get()],
                           width=self.menu_frame.winfo_width(), height=EDGE_LENGTH)
        background.grid()

        start_cell = Frame(background, bg=GAME_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        start_cell.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        start_button = Button(master=start_cell, text="Start", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, width=10, height=2)
        start_button.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD)
        continue_button = Button(master=start_cell, text="Continue", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, width=10, height=2)
        continue_button.grid(row=0, column=1, padx=CELL_PAD, pady=CELL_PAD)
        self.game_para_cell = Frame(background, bg=EMPTY_COLOR[self.color.get()])
        self.game_para_cell.grid(row=1, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        game_type_cell = Frame(self.game_para_cell, bg=EMPTY_COLOR[self.color.get()])
        game_type_cell.grid(padx=CELL_PAD, pady=CELL_PAD,row=1, column=0)
        start_button.bind('<Button-1>', self.start_game)
        continue_button.bind('<Button-1>', self.continue_game)
        classic_checkbutton = Radiobutton(game_type_cell, text="Classic",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, value=0, variable=self.game_type_code, padx=15, pady=10)
        classic_checkbutton.grid(row=1, column=0, sticky= tk.W)
         
        grav_checkbutton = Radiobutton(game_type_cell, text="Gravita",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, value=1, variable=self.game_type_code, padx=15, pady=10)
        grav_checkbutton.grid(row=2, column=0, sticky= tk.W)
        game_size_cell = Frame(self.game_para_cell, bg=EMPTY_COLOR[self.color.get()])
        game_size_cell.grid(padx=CELL_PAD, pady=CELL_PAD,row=1, column=1)
        size_4_checkbutton = Radiobutton(game_size_cell, text="4",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, value=4, variable=self.game_size, padx=15, pady=10)
        size_4_checkbutton.grid(row=1, column=1, sticky= tk.W)
         
        size_5_checkbutton = Radiobutton(game_size_cell, text="5",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, value=5, variable=self.game_size, padx=15, pady=10)
        size_5_checkbutton.grid(row=2, column=1, sticky= tk.W)
        result_button = Button(master=background, text="Top score", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, width=10, height=2)
        result_button.grid(row=3, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        result_button.bind('<Button-1>', self.show_result)



    def save_game(self, event):
        np.savetxt('matrix.csv', self.matrix, delimiter=',')
        with open('time.txt', 'w') as outfile:
            outfile.write('{}\n{}\n{}\n'.format(str(self.game_size.get()),str(self.gravitational),str(self.timer)))
        outfile.close()


    def build_grid(self):

        background = Frame(self.game_frame, bg=GAME_COLOR[self.color.get()],
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()
        info_cell = Frame(background, bg=GAME_COLOR[self.color.get()],
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        score_cell = Frame(info_cell, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        score_cell.grid(row=0, column=0, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        score = Label(master=score_cell, text="score: " + str(self.score), bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, width=10, height=2)
        score.grid()
        self.status_cells.append(score)
        timer_cell = Frame(info_cell, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        timer_cell.grid(row=0, column=2, padx=CELL_PAD, pady=CELL_PAD, columnspan=2)
        timer = Label(master=timer_cell, text="timer: "+str(self.timer), bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, width=10, height=2)
        timer.grid()
        save_cell = Frame(info_cell, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get())*2,
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
        save_cell.grid(row=1, padx=CELL_PAD, pady=CELL_PAD, columnspan=4)
        save_button = Button(master=save_cell, text="Save", bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, width=10, height=2)
        save_button.grid()
        
        info_cell.grid(columnspan=self.game_size.get())
        save_button.bind('<Button-1>', self.save_game)
        self.status_cells.append(timer)
        self.timer_count()
        for row in range(1, self.game_size.get()+1):
            grid_row = []
            for col in range(self.game_size.get()):
                cell = Frame(background, bg=EMPTY_COLOR[self.color.get()],
                             width= np.floor(EDGE_LENGTH / self.game_size.get()),
                             height= np.floor(EDGE_LENGTH / self.game_size.get()))
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()


    def draw_grid_cells(self):

        for row in range(self.game_size.get()):
            for col in range(self.game_size.get()):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR[self.color.get()])
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[self.color.get()][tile_value],
                        fg=LABEL_COLORS[self.color.get()][tile_value])
        self.status_cells[0].configure(text="score: "+str(
                        self.score))
        self.update_idletasks()

    def input_name(self, message="You Lose"):
        self.game_frame.grid_forget()
        background = Frame(self, bg=GAME_COLOR[self.color.get()],
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()
        message = Label(background, bg=GAME_COLOR[self.color.get()],font=LABEL_FONT, text=message+ " " +str(self.score)).grid(row=0, column=0, columnspan=2)
        input_name_label = Label(background, text="Your name:",bg=GAME_COLOR[self.color.get()],
                          justify=CENTER, font=LABEL_FONT, width=10, height=2).grid(row=1, column=0)
        input_name_entry = Entry(background, textvariable=self.player).grid(row=1, column=1, padx=CELL_PAD, pady=CELL_PAD)
        input_button = Button(background, text="Summit",bg=EMPTY_COLOR[self.color.get()],
                          justify=CENTER, font=SMALL_FONT, width=10, height=2)
        input_button.grid(columnspan=2, padx=CELL_PAD, pady=CELL_PAD)
        def summit(event):
            if os.stat('result.json').st_size == 0:
                results = {}
                results['result'] = [{
                    'name': 'admin',
                    'size': 4,
                    'time': 0,
                    'score': 0},
                    {'name': str(self.player.get()),
                    'size': int(self.game_size.get()),
                    'time': int(self.timer),
                    'score': int(self.score)}]
                with open('result.json', 'w') as outfile: 
                    json.dump(results, outfile, indent=4)
            else:
                with open('result.json') as outfile:
                    results = json.load(outfile)
                    temp = results['result']
                    y = {
                        'name': str(self.player.get()),
                        'size': int(self.game_size.get()),
                        'time': int(self.timer),
                        'score': int(self.score)
                        }
                    temp.append(y)
                with open('result.json', 'w') as outfile:
                    json.dump(results, outfile, indent=4)
            background.grid_forget()
            self.new_game = True
            self.menu_frame.grid()
            self.game_frame.destroy()
            self.game_frame = Frame(self)

        input_button.bind('<Button-1>', summit)
        

    def key_press(self, event):
        if self.ingame:
            valid_game = True
            key = repr(event.char)
            if key in self.commands:
                self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
                if move_made:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.score = np.sum(self.matrix)
                    self.draw_grid_cells()
                    move_made = False
                    if game_functions.check_for_win(self.matrix) == True:
                        self.input_name("You Win")
                    _, movable = game_functions.fixed_move(self.matrix)
                    if movable == False:
                        self.input_name("You Lost")

    def grav_mov(self):
        self.matrix, move_made, _ = self.commands[DOWN_KEY](self.matrix)
        if move_made:
            self.matrix = game_functions.add_new_tile(self.matrix)
            self.draw_grid_cells()
            move_made = False

    def timer_count(self):
        if not self.new_game:
            self.status_cells[1].configure(text="time: " + str(self.timer))
            self.timer += 1
            if (self.gravitational) & (self.timer%5==3):
                self.grav_mov()
            
            self.after(1000, self.timer_count)

gamegrid = Display()