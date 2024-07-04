import tkinter as tk
import webbrowser

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
        self.list.bind('<<ListboxSelect>>', self.on_list_select)
        self.post_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.textField.insert(tk.END, 'programming')

        self.info_likes = tk.Frame(self)
        self.likes_label = tk.Label(self.info_likes, text="Likes:")
        self.likes_label.pack(side=tk.LEFT)
        self.likes = tk.Label(self.info_likes, text="0")
        self.likes.pack(side=tk.LEFT)

        self.info_comments = tk.Frame(self)
        self.comments_label = tk.Label(self.info_comments, text="Comments:")
        self.comments = tk.Label(self.info_comments, text="0")

        self.comments_label.pack(side=tk.LEFT)
        self.comments.pack(side=tk.LEFT)

        self.info_link = tk.Frame(self)
        self.link_label = tk.Label(self.info_link, text="Link:")
        self.link = tk.Label(self.info_link, text="")
        self.link_label.pack(side=tk.LEFT)
        self.link.pack(side=tk.LEFT)

        self.info_likes.pack(fill=tk.X, padx=10)
        self.info_comments.pack(fill=tk.X, padx=10)
        self.info_link.pack(fill=tk.X, padx=10, pady=10)




        for p in db.DB().get_all():
            self.list.insert(tk.END, f"{p['title']}")

    def on_button_click(self):
        # self.textField.insert(tk.END, 'Hello, world!\n')
        self.button.config(state=tk.DISABLED, text='Scraping...')
        for p in self.scraper.get(self.textField.get()):
            self.list.insert(tk.END, f"{p['title']}")
        self.update_idletasks()
        self.button.config(state=tk.NORMAL, text='Scrape')

    def on_list_select(self,event):
        index = self.list.curselection()[0]
        post = db.DB().get_all()[index]
        print(post)
        self.likes.config(text=post['score'])
        self.comments.config(text=post['number_comments'])
        self.link.config(text="Link", cursor="hand2", fg="blue")
        self.link.bind("<Button-1>", lambda e:  webbrowser.open_new("https://www.reddit.com/" + post['url']))


