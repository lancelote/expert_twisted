from six.moves import tkinter
from six.moves.tkinter import scrolledtext


class Application(tkinter.Frame):
    def __init__(self, root):
        super(Application, self).__init__(root)
        self.pack()
        self.hello_button = tkinter.Button(
            self, text='say hello', command=self.say_hello)
        self.world_button = tkinter.Button(
            self, text='say world', command=self.say_world)
        self.output = scrolledtext.ScrolledText(master=self)
        self.hello_button.pack(side='top')
        self.world_button.pack(side='top')
        self.output.pack(side='top')

    def say_hello(self):
        self.output_line('hello')

    def say_world(self):
        self.output_line('world')

    def output_line(self, text):
        self.output.insert(tkinter.INSERT, text + '\n')


if __name__ == '__main__':
    Application(tkinter.Tk()).mainloop()
