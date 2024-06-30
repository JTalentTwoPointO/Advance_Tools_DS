import ui, db
if __name__ == '__main__':
    database = db.DB()
    ui.MainWindow().mainloop()
    database.close()