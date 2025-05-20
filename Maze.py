from ttkbootstrap.tooltip import ToolTip
from tkinter import messagebox
import customtkinter as ctk
from Maze_settings import *
import CTkSpinbox


class App(ctk.CTk):                                    
    def __init__(self):
    ## Setup
        super().__init__(fg_color = COLORS['main'])
        ctk.set_appearance_mode(APPEARANCE)
        x_screen=(self.winfo_screenwidth())                                     # Width of your screen
        y_screen=(self.winfo_screenheight())                                    # Height of your screen
        self.geometry(f'550x550+{int(x_screen/2)-285}+{int(y_screen/2)-270}')   # Size and place of the app
        self.resizable(False, False)                                # You can't resize the app
        self.title('')
    ## Variables
        self.theme_bool = ctk.BooleanVar(    value = False)                     # A variable for theme
        self.is_roll_create = ctk.BooleanVar(value = False)                     # Can you see the names of creators?
        self.is_roll_sn = ctk.BooleanVar(    value = False)                     # Can you see the start/end frame?
        self.radio_var = ctk.IntVar(         value = 0)                         # A variable for chosen weight
        self.SRVar = ctk.IntVar()
        self.SCVar = ctk.IntVar()
        self.ERVar = ctk.IntVar()
        self.ECVar = ctk.IntVar()
    ## Data
        self.movements, self.weights = [], []
        self.start = [0,0] 
        self.end = [N-1, N-1]
        self.current = self.start
        self.x, self.y = 1, 1
    ## Widgets
        self.frame = Frame(self, self.start, self.end, self.roll)
        self.bottom_frame = BottomFrame(self, self.submit, self.SRVar, self.SCVar, self.ERVar, self.ECVar)
        maze = ctk.CTkButton(self, 
                    text = 'Maze', font = FONTS['maze'],
                    fg_color = COLORS['buttons'], text_color = COLORS['text'], hover_color = COLORS['hover'],
                    command = self.bruteforce, corner_radius = 30, border_color = 'black', border_width = 2)
        self.theme = Theme(self, self.theme)
        self.create_frame = ctk.CTkFrame(self,
                                fg_color = '#fcff40',
                                corner_radius = 10,
                                border_color = 'purple',
                                border_width = 4)
        self.creators = Creators(self, self.roll, self.create_frame)
        self.start_end_roll = ctk.CTkButton(self,
                                text = 'Start/End Coordinates',
                                text_color = 'black',
                                fg_color = COLORS['buttons'], 
                                command = lambda: self.roll(info = 'sn'),
                                hover_color = COLORS['hover'],
                                font = FONTS['submit'],
                                corner_radius = 20)
        self.put_nums = self.frame.put_numbers
        self.new_num_btn = ctk.CTkButton(self, 
                                text = 'Add Numbers?',
                                text_color = 'black',
                                fg_color = COLORS['buttons'],
                                font = FONTS['submit'],
                                hover_color = COLORS['hover'],
                                command = lambda: NewNumbers(self.put_nums))
        self.bottom_frame.lift(aboveThis = self.start_end_roll)
        self.bottom_frame.lift(aboveThis = self.new_num_btn)
      #layout
        maze.place(anchor = 'center', x = 275, y = 19.25, relwidth = 0.2, relheight = 0.065)
        self.create_frame.place(relx = self.x, rely = 0.12, relheight = 0.7, relwidth = 0.415, anchor = 'nw')
        self.start_end_roll.pack(side = 'bottom', pady = 5)
        self.new_num_btn.pack(side = 'bottom')
    ## Event Bindings
        self.bind('<Escape>', lambda event: self.destroy())
        self.bind('<Return>', lambda event: self.bruteforce())
    ## Run
        self.mainloop()

    def bruteforce(self, visited = {}, weight_of_passing = 0):
        try:
            self.frame.draw(self.path, color = 'transparent')
            self.frame.start_end(self.start, self.end)
            self.frame.put_numbers()
        except : pass

        for i in range(0, (1 << Num)):              #Checking all possible ways that a number will be in passing or not
            self.current = self.start
            temp = self.check_state(i)
            if len(temp) == 0:                      #There was no way
                continue

            for loc in temp:
                if loc in NUMBERS and not visited.get(str(loc), False):
                    weight_of_passing += NUMBER[MAX_INTG*loc[0] + loc[1]]
                    visited[str(loc)] = True
            self.movements.append(temp)
            self.weights.append(weight_of_passing)
            #print(i,' :\n',temp,'\n')
            #print(weight_of_passing , "\n with this\n" , temp)
        self.solution()

    class Pair:
        def __init__(self, x, y, st):
            self.x = x
            self.y = y
            self.weight = pow(x - st[0], 2) + pow(y - st[1], 2) #This field would be used for sorting

    def check_state(self, i, flag = True):
        chosen_numbers = []                         # Numbers that we want to see in passing
        tree_numbers = {}                           # Numbers that we shouldn't see in passing
        for j in range(Num):
            if (i&(1<<j)) != 0:                     # Look at the J'st bit, is it 0 or 1...?
                chosen_numbers.append(App.Pair(NUMBERS[j][0], NUMBERS[j][1], self.start))
            else:
                tree_numbers[str(NUMBERS[j])] = True
                                                    # Sorting in order of being close to starting point

        chosen_numbers.sort(key = lambda pair: pair.weight)
        chosen_numbers.append(App.Pair(self.end[0], self.end[1], self.start))
                                                    # Saving the movements
        movements = [self.current]
        visited = {str(self.current) : True}
        for num in chosen_numbers:
            cor = [num.x , num.y]
            if not visited.get(str(cor), False):
                path = self.bfs(cor, tree_numbers)   #Using bfs to reach the next chosen number with minimum movements
                if len(path) == 0:
                    flag = False
                    break
                for step in path:
                    movements.append(step)
                    visited[str(step)] = True
                self.current = cor
        if not flag:                                #There is no way to move with this chosen numbers
            return []
        else:
            return movements

    def bfs(self, cor, tree_numbers, moved = []):# Returns the min path from 'self.current' to 'cor' if there is any
        queue = [self.current]
        parent = {}
        visited = {}
        while len(queue) > 0:
            temp = queue.pop(0)
            visited[str(temp)] = True
            if temp == cor or temp == self.end:
                break
            x = temp[0]
            y = temp[1]
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if (i == j)or(i == -j):                               # Invalid moves
                        continue
                    if (x+i < 0)or(x+i >= N)or(y+j < 0)or(y+j >= N):      # Out of Maze
                        continue
                    if visited.get(str([x+i, y+j]), False):               # Visited
                        continue
                    if TREES_DICT.get(str([x+i, y+j]), False):            # Trees
                        continue
                    if tree_numbers.get(str([x+i, y+j]), False):          # Numbers we don't want to see
                        continue
                    queue.append([x + i, y + j])
                    parent[MAX_INTG * (x + i) + (y + j)] = [x, y]
        if not visited.get(str(cor), False):
            return []
        while cor != self.current:
            moved.append(cor)
            cor = parent[MAX_INTG*cor[0] + cor[1]]
        moved.reverse()
        return moved

    def solution(self):
        if len(self.weights) == 0:
            ask = messagebox.showerror(title = 'Passing Not Found', message = 'Sorry,There is no place to go.')
            if ask:
                self.destroy()

        self.combine = dict(zip(self.weights, self.movements))
        if self.combine:
            self.window = Window(set(self.weights), self.radio_var, self.ok)
        else: self.destroy()

    def theme(self, event = None):
        self.theme_bool.set(not self.theme_bool.get())
        if self.theme_bool.get():
            ctk.set_appearance_mode('dark')
            self.theme.configure(text = 'Light')
        else:
            ctk.set_appearance_mode('light')
            self.theme.configure(text = 'Dark')

    def submit(self):
        self.start = [self.SRVar.get(),self.SCVar.get()]
        self.end = [self.ERVar.get(),self.ECVar.get()]
        self.current = self.start
        try:
            self.frame.draw(self.path, color = 'transparent')
            self.frame.put_numbers()
        except: pass
        finally:
            self.frame.start_end(self.start, self.end)
            self.dead_ends, self.can_go, self.path, self.results, self.cross_ways, self.weights = [],[],[],[],[],[]
            self.roll(info = 'sn')

    def ok(self):
            try:
                self.frame.draw(self.path, color = 'transparent')
                self.frame.put_numbers()
            except: pass
            sum_ = self.radio_var.get()
            self.path = self.combine[sum_]
            self.frame.draw(self.path, COLORS['path'])

    def roll(self, info = None):
        if info == 'sn':
            if not self.is_roll_sn.get():
                if self.y > 0.87:
                    self.y -= 0.02
                    self.bottom_frame.place(rely = self.y)
                    self.after(50, lambda: self.roll(info = 'sn'))
                else: self.is_roll_sn.set(not self.is_roll_sn.get())
            else:
                if self.y < 1:
                    self.y += 0.02
                    self.bottom_frame.place(rely = self.y)
                    self.after(50, lambda: self.roll(info = 'sn'))
                else: self.is_roll_sn.set(not self.is_roll_sn.get())
        else:
            if not self.is_roll_create.get():
                if self.x > 0.6:
                    self.x -= 0.02
                    self.create_frame.place(relx = self.x)
                    self.after(20, self.roll)
                else: self.is_roll_create.set(not self.is_roll_create.get())
            else:
                if self.x < 1:
                    self.x += 0.02
                    self.create_frame.place(relx = self.x)
                    self.after(20, self.roll)
                else: self.is_roll_create.set(not self.is_roll_create.get())

class Frame(ctk.CTkFrame):
    def __init__(self, parent, start, end, roll):
        self.roll = roll
        self.start = start
        self.end = end
    ## Setup
        super().__init__(parent, fg_color = COLORS['maze'], corner_radius=20)
        self.place(anchor = 'nw', relx = 0.1, rely = 0.07, relwidth = 0.8, relheight = 0.8)
    ## Grid
        self.rowconfigure((list(range(FIELDS[0]))), weight = 1, uniform = 'a')
        self.columnconfigure((list(range(FIELDS[1]))), weight = 1, uniform = 'a')
    ## widgets
        self.start_end(self.start,self.end)
        self.put_numbers()
    ## Put the trees in place:
        for tuple_ in TREES:
            tree = ctk.CTkFrame(self,fg_color = COLORS['trees'] ,corner_radius=15)
            tree.grid(row = tuple_[0],column = tuple_[1],sticky = 'nsew',padx = 1,pady = 1)
        
    def put_numbers(self):
        for tuple_ in NUMBERS:
            if tuple_ not in TREES:
                num = ctk.CTkLabel(self,
                            text = NUMBER[MAX_INTG*tuple_[0] + tuple_[1]],
                            text_color = COLORS['numbers'],
                            corner_radius = 6,
                            fg_color = COLORS['numbers fg'],
                            font = FONTS['numbers'])
                num.grid(row = tuple_[0], column = tuple_[1], sticky = 'nsew', padx = 6, pady = 6)

                ToolTip(widget = num, 
                        text = NUMBER[MAX_INTG*tuple_[0] + tuple_[1]],
                        bootstyle = 'danger-inverse',
                        delay = 0)
                
    def start_end(self, start, end):
        try:
            self.start_new.grid_forget()
            self.end_new.grid_forget()
        except: pass
        self.start_new = ctk.CTkLabel(self,text='S', text_color='red', fg_color='transparent', font=FONTS['SE'])
        self.end_new = ctk.CTkLabel(self,text='E', text_color='red', fg_color='transparent', font=FONTS['SE'])
        self.start_new.grid(row = start[0], column=start[1], sticky='nsew')
        self.end_new.grid(row = end[0], column=end[1], sticky='nsew')
   
    def draw(self, path, color):
        for step in path:
            self.cor = ctk.CTkFrame(self,
                            fg_color = color ,
                            corner_radius = 25, 
                            width = 20, height = 20)
            self.cor.grid(row = step[0], column = step[1])  

class BottomFrame(ctk.CTkFrame):
    def __init__(self, parent, submit_com , s_row,s_col,e_row,e_col ):
        super().__init__(parent, fg_color = 'transparent')
        self.place(anchor = 'nw', relx = 0, rely = 1, relwidth = 1, relheight = 0.2)
    ## Create SpinBox with Labels ##
        self.frame('Start Row:',  x = 0,    y = 0,    var = s_row, value = 0)
        self.frame('Start Col:  ',x = 0,    y = 0.35, var = s_col, value = 0)
        self.frame('End Row:',    x = 0.65, y = 0,    var = e_row, value = 9)
        self.frame('End Col:  ',  x = 0.65, y = 0.35, var = e_col, value = 9)
    ## Submit Button ##
        submit = ctk.CTkButton(self, 
                        text = 'Submit', 
                        font = FONTS['submit'],
                        text_color = COLORS['text'], 
                        fg_color = COLORS['buttons'], 
                        hover_color = COLORS['hover'],
                        corner_radius = 30, 
                        command = submit_com)
        submit.place(anchor = 'center',relx = 0.51,rely = 0.31,relwidth = 0.17)

    def frame(self, text, x,y, var, value):
        frame = ctk.CTkFrame(self, fg_color=COLORS['small frame'])
        frame.place(relx = x,rely = y)
        ctk.CTkLabel(frame,text=text, text_color=COLORS['text'],font=FONTS['new cor']).pack(padx = 3,pady = 3,side = 'left')
        CTkSpinbox.CTkSpinbox(frame, min_value=0, max_value=9, width=100, height=35, variable=var, start_value=value).pack(padx = 3,pady = 1,side = 'left')

class Theme(ctk.CTkLabel):
    def __init__(self, parent, theme_func):
        self.switch = theme_func
        super().__init__(master = parent, text = 'Dark',
        text_color = COLORS['switch'] ,font = FONTS['theme'],)
        self.place(relx = 0.94, rely = 0.03, anchor = 'center')
        self.bind('<Button>', self.switch)

class Creators(ctk.CTkButton):
    def __init__(self,parent, creator, frame):
        super().__init__(parent,
                    text = 'Creators',
                    text_color = COLORS['main'],
                    fg_color = COLORS['main'],
                    height = 40,
                    font = FONTS['creators'],
                    hover_color = COLORS['creators hover'],
                    corner_radius = 30,
                    command = creator)
        self.place(relx = 0.18, rely = 0.03, anchor = 'center')

        for name in NAMES:
            ctk.CTkLabel(frame,
                    text = name,
                    text_color = 'black',
                    font = FONTS['names']).pack(pady = 5,padx = 5,expand = True, fill = 'both',ipadx = 0)

class Window(ctk.CTk):
    def __init__(self, weights, var, ok):
    ## Setup
        super().__init__(fg_color = 'pink')
        height = (len(weights)*50)+50
        x_screen = (self.winfo_screenwidth())
        y_screen = (self.winfo_screenheight())
        self.geometry(f'350x{height}+{int(x_screen/2)-600}+{int(y_screen/2)-height/2}')
        self.maxsize(350, y_screen)
        self.minsize(350, 200)
        self.title('')
    ## Label
        self.label = ctk.CTkLabel(self,
                            text=f'You have {len(weights)} options:',
                            font = FONTS['SE'],
                            corner_radius=30)
        self.label.pack()
    ## Radio buttons
        for weight in weights:
            radio = ctk.CTkRadioButton(self, 
                            text = f'sum {weight}',
                            value = weight, variable = var,
                            border_color = 'red',
                            border_width_checked = 17,
                            border_width_unchecked = 3,
                            text_color = 'black',
                            fg_color = 'green',
                            font = FONTS['numbers'],
                            hover_color = 'light green',
                            height = 20)
            radio.pack(pady = 10)
    ## OK button
        ctk.CTkButton(self,
                    text = 'OK',
                    font = FONTS['SE'],
                    command = ok,
                    fg_color = 'red',
                    text_color = 'black',
                    hover_color = 'gray',
                    height = 40).place(anchor = 'center',relx = 0.5,rely = 0.9)
    ## Event Binding
        self.bind('<Return>', lambda event: ok())
        self.bind('<Escape>',lambda event: self.destroy())
    ## Run
        self.mainloop()

class NewNumbers(ctk.CTk):
    def __init__(self, put_num):
    ## Setup
        super().__init__(fg_color = 'pink')
        self.put_num = put_num
        x_screen=(self.winfo_screenwidth())
        y_screen=(self.winfo_screenheight())
        self.geometry(f'400x250+{int(x_screen/2)+230}+{int(y_screen/2)-200}')
        self.title('')
    ## Data
        self.option_num_var = ctk.IntVar(value = 1)
        self.option_row_var = ctk.IntVar(value = 1)
        self.option_col_var = ctk.IntVar(value = 1)
    ## Widgets
        number_lbl = ctk.CTkLabel(self,
                            text = 'The Number',
                            text_color = 'black',
                            font = FONTS['submit'],
                            fg_color = COLORS['buttons'],
                            corner_radius = 5)
        row_lbl = ctk.CTkLabel(self,
                            text = 'The Row',
                            text_color = 'black',
                            font = FONTS['submit'],
                            fg_color = COLORS['buttons'],
                            corner_radius = 5)
        col_lbl = ctk.CTkLabel(self,
                            text = 'The Col',
                            text_color = 'black',
                            font = FONTS['submit'],
                            fg_color = COLORS['buttons'],
                            corner_radius = 5)
        num = ctk.CTkOptionMenu(self,
                        width = 40,
                        anchor='center',
                        corner_radius = 5,
                        fg_color = 'yellow',
                        text_color = 'black',
                        font = FONTS['SE'],
                        button_color = 'yellow',
                        button_hover_color = 'red',
                        dropdown_fg_color = 'light green',
                        dropdown_font = FONTS['theme'],
                        dropdown_text_color = 'black',
                        dropdown_hover_color = 'green',
                        values = DROP_VALUES,
                        variable = self.option_num_var)
        row = ctk.CTkOptionMenu(self,
                        width = 40,
                        anchor='center',
                        corner_radius = 5,
                        fg_color = 'yellow',
                        text_color = 'black',
                        font = FONTS['SE'],
                        button_color = 'yellow',
                        button_hover_color = 'red',
                        dropdown_fg_color = 'light green',
                        dropdown_font = FONTS['theme'],
                        dropdown_text_color = 'black',
                        dropdown_hover_color = 'green',
                        values = DROP_VALUES,
                        variable = self.option_row_var)
        col = ctk.CTkOptionMenu(self,
                        width = 40,
                        anchor='center',
                        corner_radius = 5,
                        fg_color = 'yellow',
                        text_color = 'black',
                        font = FONTS['SE'],
                        button_color = 'yellow',
                        button_hover_color = 'red',
                        dropdown_fg_color = 'light green',
                        dropdown_font = FONTS['theme'],
                        dropdown_text_color = 'black',
                        dropdown_hover_color = 'green',
                        values = DROP_VALUES,
                        variable = self.option_col_var)
        submit_btn = ctk.CTkButton(self,
                                text='Create',
                                fg_color=COLORS['buttons'],
                                font=FONTS['SE'],
                                text_color='black',
                                corner_radius=15,
                                width=100,
                                command = self.command)
    ## Layout
        number_lbl.place(relx = 0.05, rely = 0.1 )
        row_lbl.place   (relx = 0.45, rely = 0.1 )
        col_lbl.place   (relx = 0.75, rely = 0.1 )
        num.place       (relx = 0.12, rely = 0.25)
        row.place       (relx = 0.48, rely = 0.25)
        col.place       (relx = 0.77, rely = 0.25)
        submit_btn.place(relx = 0.5,  rely = 0.8, anchor = 'center')
    ## Events
        self.bind('<Return>', lambda event: self.command())
        self.bind('<Escape>', lambda event: self.destroy())
    ## Run
        self.mainloop()

    def command(self):
        new_num = self.option_num_var.get()
        NUMBERS.append([self.option_row_var.get(), self.option_col_var.get()])
        NUMBER[MAX_INTG * int(self.option_row_var.get()) + int(self.option_col_var.get())] = new_num
        ctk.CTkLabel(self,
                    text = str(new_num),
                    text_color = COLORS['numbers'],
                    corner_radius = 6,
                    fg_color = COLORS['numbers fg'],
                    font = FONTS['numbers'])
        self.put_num()

if __name__ == '__main__':
    App()
