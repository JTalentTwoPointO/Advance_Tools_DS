import tkinter as tk
import webbrowser
import scrape
import db
import pandas as pd
import os
import graph_analysis
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    def __init__(self, database):
        print("Initializing UI")
        self.scraper = scrape.Scraper(database)
        self.database = database

        tk.Tk.__init__(self)
        self.title('Reddit Web Scraper & Graph Analyzer')
        self.geometry('800x600')
        self.frame = tk.Frame(self)

        icon_path = 'public/icon.png'
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.icon)
        else:
            print(f"Icon file not found: {icon_path}")

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

        self.graph_buttons_frame = tk.Frame(self)
        self.analyze_button = tk.Button(self.graph_buttons_frame, text='Analyze Graph', command=self.analyze_graph)
        self.visualize_button = tk.Button(self.graph_buttons_frame, text='Visualize Graph',
                                          command=self.visualize_graph)

        self.analyze_button.pack(side=tk.LEFT, padx=5)
        self.visualize_button.pack(side=tk.LEFT, padx=5)
        self.graph_buttons_frame.pack(padx=10, pady=10)

        self.load_posts()  # Load initial posts

        # Bind the Enter key to the on_button_click method
        self.textField.bind('<Return>', self.on_enter_key)
        # Ensure the text field has focus
        self.textField.focus_set()

    def load_posts(self):
        self.list.delete(0, tk.END)  # Clear the listbox
        for p in self.database.get_all():
            print(f"Loading post: {p['title']}")
            self.list.insert(tk.END, p['title'])

    def on_button_click(self):
        print("Scraping started")
        self.button.config(state=tk.DISABLED, text='Scraping...')
        self.list.delete(0, tk.END)  # Clear the listbox before inserting new items
        for p in self.scraper.get(self.textField.get()):
            print(f"Scraped post: {p['title']}")
            self.list.insert(tk.END, f"{p['title']}")
        self.update_idletasks()
        self.button.config(state=tk.NORMAL, text='Scrape')
        print("Scraping finished")

    def on_enter_key(self, event):
        print("Enter key pressed")
        self.on_button_click()

    def on_list_select(self, event):
        index = self.list.curselection()[0]
        post = self.database.get_all()[index]
        print(f"Selected post: {post['title']}")
        self.likes.config(text=post['score'])
        self.comments.config(text=post['number_comments'])
        self.link.config(text="Link", cursor="hand2", fg="blue")
        self.link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.reddit.com/" + post['url']))

    def analyze_graph(self):
        print("Analyzing graph")
        graph_analysis.analyze_graph()

    def visualize_graph(self):
        print("Visualizing graphs")
        graph_folder = 'graphs'
        if not os.path.exists(graph_folder):
            print(f"Graph folder not found: {graph_folder}")
            return

        new_window = tk.Toplevel(self)
        new_window.title("Graph Visualizations")
        new_window.geometry('800x600')

        canvas = tk.Canvas(new_window)
        scroll_y = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
        scroll_x = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)

        frame = tk.Frame(canvas)

        for image_file in os.listdir(graph_folder):
            if image_file.endswith('.png'):
                img_path = os.path.join(graph_folder, image_file)
                img = Image.open(img_path)
                img = img.resize((400, 300), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=img_tk)
                label.image = img_tk
                label.pack(padx=5, pady=5)

        frame.update_idletasks()
        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
        scroll_x.pack(fill='x', side='bottom')

    def display_data(data):
        df = pd.DataFrame(data)
        print(df)