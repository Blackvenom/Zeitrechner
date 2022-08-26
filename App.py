import tkinter as tk
import Model, View, Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Zeitrechner')

        # create a model (default break: 50min)
        model = Model.Model(0, 50)

        # create a view and place it on the root window
        view = View.View(self)
        view.grid(row=0, column=0, padx=10, pady=10)
        view.columnconfigure(tuple(range(2)), weight=1)

        # create a controller
        controller = Controller.Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

if __name__ == '__main__':
    app = App()
    app.mainloop()