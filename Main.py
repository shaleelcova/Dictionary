import tkinter
from tkinter import Tk, Frame, Button, Label, Entry, END, StringVar, Radiobutton, IntVar, DISABLED, font
from tkinter.font import nametofont

import tkinter.scrolledtext as scrolledtext
from PyDictionary import PyDictionary
#import test


pd = PyDictionary()


class View(Frame):

    @staticmethod
    def display_search_button(button):
        button.grid(row=1, column=3, sticky="w")

    @staticmethod
    def create_immutable_labels(master):
        primary_bg_color = "#557A95"
        secondary_bg_color = "#59B8BC"

        enter_word_lbl = Label(master, text="Enter Word: ", bg=primary_bg_color)
        definition_lbl = Label(master, text="Definition: ", bg=primary_bg_color)

    @staticmethod
    def create_meaning_label(master):
        primary_bg_color = "#557A95"
        secondary_bg_color = "#59B8BC"

        return Label(master, text="Meaning", wraplength=250, bg=primary_bg_color)

    @staticmethod
    def display_labels(label1, label2, label3, label4):
        label1.grid(row=2, column=0)
        label2.grid(row=2, column=2)
        label3.grid(row=2, column=4)
        label4.grid(row=4, column=0, columnspan=5)#, sticky="w")

    def config_window(self, master):
        Frame.__init__(self, master)
        master.title("Dictionary")
        master.config(bg="#557A95")

        master.grid_columnconfigure(0, weight=2)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=3)
        master.grid_columnconfigure(3, weight=1)
        master.grid_columnconfigure(4, weight=2)

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_rowconfigure(4, weight=1)
        master.grid_rowconfigure(5, weight=5)

        master.geometry("2560x1080")

    @staticmethod
    def config_button(button):
        button.config(width=5, height=2)
        return button

    @staticmethod
    def add_radio_buttons(rb1, rb2, rb3):
        rb1.grid(row=3, column=0, sticky="n")
        rb2.grid(row=3, column=2, sticky="n")
        rb3.grid(row=3, column=4, sticky="n")

    @staticmethod
    def display_text_field(textfield):
        textfield.grid(row=1, column=2, sticky="ew")
        textfield.config(font="Helvetica 20 bold")

    @staticmethod
    def fit_label(event):
        label = event.widget
        label.update
        if not hasattr(label, "original_text"):
            # preserve the original text so we can restore
            # it if the widget grows.
            label.original_text = label.cget("text")

        font_ = nametofont(label.cget("font"))
        text = label.original_text
        max_width = event.width
        actual_width = font_.measure(text)
        if actual_width <= max_width:
            # the original text fits; no need to add ellipsis
            label.configure(text=text)
            print("good")
        else:
            # the original text won't fit. Keep shrinking
            # until it does
            while actual_width > max_width and len(text) > 1:
                text = text[:-1]
                actual_width = font_.measure(text + "...")
            label.configure(text=text + "...")


class Controller:
    def __init__(self, model, view, master):
        self._model = model
        self._view = view
        self._master = master
        self._state = 0 # radiobutton

    def get_model(self):
        return self._model

    def get_view(self):
        return self._view

    def search_button_pressed(self):
        print("pressed")
        return

    def create_labels(self):
        primary_bg_color = "#557A95"
        secondary_bg_color = "#59B8BC"

        def_word_lbl = Label(self._master, text="Definition", bg=primary_bg_color)
        syn_lbl = Label(self._master, text="Synonym", bg=primary_bg_color)
        phrase_lbl = Label(self._master, text="In a phrase", bg=primary_bg_color)
        # def_box = Label(self._master,
        #                 #text="""The name "Sekiro" derives from two different words: "Seki", which comes from "Sekiwan", an old japanese term for person missing an arm. "Ro", which comes from the kanji for "Wolf". Together, they can be read as "One Armed Wolf", which fits with the motif of the main character, known as Wolf, losing his arm."""
        #                 bg=primary_bg_color,
        #                 wraplength=2560,
        #                 anchor="w",
        #                 justify=tkinter.LEFT)
        def_box = scrolledtext.ScrolledText(self._master, undo=True, state=DISABLED, font=("Courier", 16, "italic"))
        #def_box.bind("<Configure>", self._view.fit_label)

        self.create_text_field(def_box)
        self._view.display_labels(def_word_lbl, syn_lbl, phrase_lbl, def_box)

    def create_search_button(self, textfield, box):
        primary_bg_color = "#B1A296"
        secondary_bg_color = "#59B8BC"
        font_color = "#015F63"
        selected_option = IntVar()
        options = (("Definition", "D"), ("Synonym", "S"), ("Example", "E"))
        definition_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=0,
            command=lambda: self.option_selected(selected_option, box)
        )

        syn_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=1,
            command=lambda: self.option_selected(selected_option, box)
        )

        ex_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=2,
            command=lambda: self.option_selected(selected_option, box)
        )

        search_button = self._view.config_button(Button(self._master,
                                                        highlightbackground=primary_bg_color,
                                                        fg=font_color,
                                                        text="Search",
                                                        command=lambda: self.print_word(textfield, box)))
        search_button.bind()
        self._view.display_search_button(search_button)
        self._view.add_radio_buttons(definition_button, syn_button, ex_button)

    def create_text_field(self, box):
        secondary_bg_color = "#B1A296"
        textfield = Entry(self._master, width=20, fg="grey", bg=secondary_bg_color)
        self.create_search_button(textfield, box)

        textfield.insert(END, 'Enter word')
        textfield.bind("<FocusIn>", lambda args: textfield.delete('0', 'end'))
        self._view.display_text_field(textfield)

    def print_word(self, textfield, box):
        text_font = tkinter.font.nametofont("TkDefaultFont")
        bullet_width = text_font.measure("- ")
        em = text_font.measure("m")
        box.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        if textfield is not None: self._model.parse_def(textfield.get())
        box.configure(state='normal')
        box.delete(1.0, END)
        if self._state == 0:
            for grammar in self._model.get_grammars():
                box.insert("insert", f"{grammar}")
                if self._model.get_raw_data() is not None:
                    for meaning in self._model.get_raw_data()[grammar]:
                        print(meaning)
                        box.insert("insert", "\n- " + meaning, "bulleted\n")
                    box.insert("insert", "\n\n")
        elif self._state == 1:
            print("Syn")
        else:
            print("Example")


        #box.insert(1.0, self._model.get_def())
        #box.insert("end", "- " + self._model.get_def(), "bulleted")

        box.configure(state=DISABLED)

        # box['text'] = self._model.get_def()
        # print(box['text'])

    def create_radio_button(self):
        selected_option = IntVar()
        options = (("Definition", "D"), ("Synonym", "S"), ("Example", "E"))
        definition_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=0,
            command=lambda: self.option_selected(selected_option)
        )

        syn_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=1,
            command=lambda: self.option_selected(selected_option)
        )

        ex_button = Radiobutton(
            self._master,
            bg="#557A95",
            variable=selected_option,
            value=2,
            command=lambda: self.option_selected(selected_option)
        )

        self._view.add_radio_buttons(definition_button, syn_button, ex_button)

    def option_selected(self, var, box):
        print(str(var.get()))
        self._state = int(var.get())
        self.print_word(None, box)



    def start(self):
        self._view.config_window(self._master)


class Model:
    def __init__(self):
        self._word = ""
        self._grammars = []
        self._raw_data = []
        self._def = ""
        self._noun = []
        self._verb = ""
        self._adjective = ""
        self._synonym = []
        self._examples = []

    def clear_model(self):
        self._grammars = []
        self._raw_data = []

    def parse_def(self, word):
        print(pd.meaning(word))
        self._raw_data = pd.meaning(word)
        print(self._raw_data)
        if self._raw_data is not None:
            #print(raw_data.keys())
            #print(len(list(raw_data.values())))
            self._def = ''
            self._grammars = list(self._raw_data.keys())
            self._def = list(self._raw_data.values())
            self.set_synonym(word)
            self._examples = pd.getAntonyms(word)
            print(self._examples)
            print(self._synonym)
        else:  # Word doesn't exist
            self._grammars = []
            for x in range(100):
                self._grammars.append("O you cannot spell\n")

        # for grammar in self._grammars:
        #     for meaning in raw_data[grammar]:
        #         self._def += f"\t-\t{meaning}\n"
        #     self._def += "\n"

    def get_raw_data(self):
        return self._raw_data

    def set_synonym(self, syn):
        self._synonym = pd.synonym(syn)

    def get_synonym(self):
        return self._synonym

    @staticmethod
    def word_exist(word):
        try:
            pd.getMeanings(word)
            return True
        except:
            return False

    def get_word(self):
        return self._word

    def set_word(self, word):
        self._word = word

    def get_noun(self):
        result = ''
        for noun in self._noun:
            result += f"{noun}\n"
        return result

    def set_noun(self, noun):
        self._noun = noun

    def get_verb(self):
        return self._verb

    def set_verb(self, verb):
        self._def = verb

    def get_adjective(self):
        return self._adjective

    def set_adjective(self, adj):
        self._def = adj

    def get_def(self):
        return self._def

    def get_grammars(self):
        return self._grammars


class Main:
    def __init__(self):
        self.root = Tk()
        self._controller = Controller(Model(), View(), self.root)
        self._controller.start()
        self._controller.create_labels()
        #self._controller.create_search_button()
        #self._controller.create_text_field()
        #self._controller.create_radio_button()

        self.root.mainloop()


m = Main()
