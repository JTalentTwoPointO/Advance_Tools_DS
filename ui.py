import tkinter as tk
import scrape
import db
# ui for a main window with a text box and button for a link
class MainWindow(tk.Tk):
    def __init__(self):
        self.scraper = scrape.Scraper()

        tk.Tk.__init__(self)
        self.title('Reddit Web Scraper')
        self.geometry('800x500')
        self.frame = tk.Frame(self)
        self.icon = tk.PhotoImage(file='public/icon.png')
        self.iconphoto(False, self.icon)
        self.textField = tk.Entry(self.frame)
        self.label = tk.Label(self.frame, text="Reddit Search:")
        self.button = tk.Button(self.frame, text='Search', command=self.on_button_click)

        self.label.pack(side=tk.LEFT)
        self.textField.pack(expand=True, fill=tk.X, side=tk.LEFT)
        self.button.pack(padx=10)
        self.frame.pack(padx=10, pady=10, fill='x')

        self.post_frame = tk.Frame(self)
        self.list = tk.Listbox(self.post_frame)
        self.list.pack(fill=tk.BOTH, expand=True)
        self.post_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.textField.insert(tk.END, 'programming')

        for p in db.DB().get_all():
            self.list.insert(tk.END, f"{p['title']}")

    def on_button_click(self):
        # self.textField.insert(tk.END, 'Hello, world!\n')
        self.button.config(state=tk.DISABLED, text='Scraping...')
        for p in self.scraper.get(self.textField.get()):
            self.list.insert(tk.END, f"{p['title']}")
        self.update_idletasks()
        self.button.config(state=tk.NORMAL, text='Scrape')