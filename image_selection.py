"""This project select sheets files and works with."""

import customtkinter as ctk
from tkinter import Menu, Listbox
import os
import shutil
from PIL import Image
import cv2
from boxing import trace_box

class ImageSelector():
    def __init__(self, show: bool = False):
        self.app = ctk.CTk()
        self.app.title("Separador de imagens")
        self.local_path = ""
        self.lbl = ""
        try:
            with open("config.cfg", "r") as config:
                self.local_path = config.read().split("\n")[0]
                self.extension = config.read().split("\n")[1]
        except:
            self.extension = ".jpg"
        
        self.extension = ".jpg" if self.extension == "" else self.extension
            
        self.local_path = "C:\\" if self.local_path == "" else self.local_path

        self.cfg = open("config.cfg", "w")
        self.labels = open("labels.txt", "w")

        self.app.geometry("800x560")
        self.file_path = ctk.CTkLabel(master=self.app,text="Localização:")
        self.file_path.place(relx=0.1, rely=0.05, anchor="center")
        self.entry_file = ctk.CTkEntry(self.app,
                                       justify="center",
                                       state="disabled"
                                       )
        self.entry_file.insert(0, os.getcwd())
        self.entry_file.place(relx=0.55, rely=0.05, relwidth=0.75, anchor="center")

        def select_archieve(runnable=True):
            sel_arch = ctk.CTk()
            sel_arch.geometry("300x500")
            sel_arch.title("Selecionar pasta ("+ self.local_path +")")
            list_box = Listbox(sel_arch, 
                            justify="left")
            def actualizate(runnable=True):
                # print("actualizating")
                try:
                    selected = list_box.get(list_box.curselection())
                    list_box.delete(0, list_box.size())
                    # print(selected)
                    if len(selected) > 0:
                        if selected[:3] == "-> ":
                            if selected[3:] != "..":
                                # print(os.getcwd()+"\\"+selected[3:])
                                os.chdir(os.getcwd()+"\\"+selected[3:])
                            else:
                                path = os.getcwd().split("\\")
                                # print(os.getcwd()[:-len(path[-1])])
                                os.chdir(os.getcwd()[:-len(path[-1])])
                        # else:
                        #     self.entry_file.delete(0, ctk.END)
                        #     self.local_path = os.getcwd()
                        #     self.entry_file.insert(0, os.getcwd()+"\\"+selected)
                        #     sel_arch.destroy()
                    sel_arch.title("Selecionar pasta ("+ os.getcwd() +")")
                except:
                    if self.entry_file.get() == "":
                        os.chdir(self.local_path)
                    else:
                        path = self.entry_file.get().split("\\")
                        os.chdir(self.entry_file.get())

                # archieves = [item for item in os.listdir() if "." in item and item[0] != "$"]
                folders   = [item for item in os.listdir() if "." not in item and item[0] != "$"]
                if os.getcwd() != "C:\\":
                    list_box.insert(0, "-> ..")
                    root = 1
                else:
                    root = 0
                for i, item in enumerate(folders):
                    list_box.insert(i+root, "-> "+item)
                # for i, item in enumerate(archieves):
                #     list_box.insert(len(folders)+i+root, item)
            actualizate()
            list_box.bind("<Double-1>",actualizate)
            list_box.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.8, anchor="center")
            def select(runnable = True):
                self.entry_file.configure(state="normal")
                self.entry_file.delete(0, ctk.END)
                self.local_path = os.getcwd()
                self.entry_file.insert(0, os.getcwd())
                self.entry_file.configure(state="disabled")
                refresh()
                sel_arch.destroy()
            sel_folder = ctk.CTkButton(master=sel_arch,text="Selecionar pasta",command=select)
            sel_folder.place(relx=0.5, rely=0.925, anchor="center")
            sel_arch.mainloop()
            

        def config(runnable=True):
            cfg = ctk.CTk()
            cfg.geometry("300x150")
            cfg.title("Configurações")
            lb_extension = ctk.CTkLabel(cfg,text="Extensão das imagens: ")
            lb_extension.place(relx=0.275, rely=0.35, anchor="center")
            def confirm(runnable = True):
                self.extension = cbb_extensions.get()
                refresh()
                cfg.destroy()
            bt_ok = ctk.CTkButton(cfg, text="Confirmar", command=confirm)
            bt_ok.place(relx=0.5, rely=0.65, anchor="center")
            values = [".jpg",'.jpeg',".png",".gif",".bmp",".raw"]
            cbb_extensions = ctk.CTkComboBox(cfg, values=values, width=75)
            if self.extension != "":
                cbb_extensions.set(self.extension)
            cbb_extensions.place(relx=0.75, rely=0.35, anchor="center")
            cfg.mainloop()

        def image_selection(runnable = True):
            try:
                self.image_show.destroy()
            finally:
                wdt = self.fr_image.winfo_width()*0.95
                hgt = self.fr_image.winfo_height()*0.95
                img_path = self.images_list.get(self.images_list.curselection())
                try:
                    img, self.lbl = trace_box(
                        img_path,
                        padding=(0, "percent"),
                        box_inflation=(1, 1),
                        show=False
                    )
                    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                except:
                    no()
                image = ctk.CTkImage(light_image=img, size=(wdt, hgt))
                self.image_show = ctk.CTkLabel(self.fr_image, image=image, text="")
                self.image_show.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")

        self.fr_image = ctk.CTkFrame(self.app, fg_color="white")
        self.fr_image.place(relx=0.6, rely=0.5, relheight=0.675, relwidth=0.6, anchor="center")

        self.remaining_images_label = ctk.CTkLabel(self.app, text="Imagens restantes: ")
        self.remaining_images_label.place(relx=0.15, rely=0.15, anchor="center")

        self.images_list = Listbox(self.app, justify="left")
        self.images_list.bind("<<ListboxSelect>>", image_selection)
        self.images_list.place(relx=0.15, rely=0.55, relheight=0.75, relwidth=0.2, anchor="center")

        def refresh(runnable = True):
            self.images_list.delete(0, self.images_list.size())
            images = [item for item in os.listdir() if item[-1*len(self.extension):] == self.extension]
            for i, item in enumerate(images):
                self.images_list.insert(i, item)
            if len(images) > 0:
                self.remaining_images_label.configure(text="Imagens restantes: "+str(len(images)))
            else:
                self.remaining_images_label.configure(text="Imagens restantes: ")
            if self.images_list.curselection():
                self.images_list.selection_set(self.images_list.curselection())
            else:
                self.images_list.selection_set(0)
            try:
                image_selection()
            except:
                pass

        def yes(runnable = True):
            if "Sim" not in os.listdir():
                os.mkdir("Sim")
            image = self.images_list.get(self.images_list.curselection())
            shutil.move(image, "Sim/"+image)
            print("Label: " + image + " -> " + str(self.lbl))
            self.labels.write(image + " -> " + str(self.lbl) + "\n")
            refresh()
        
        def no(runnable = True):
            if "Nao" not in os.listdir():
                os.mkdir("Nao")
            image = self.images_list.get(self.images_list.curselection())
            shutil.move(image, "Nao/"+image)
            refresh()

        self.bt_yes = ctk.CTkButton(self.app, text="Sim -->", command=yes)
        self.bt_yes.place(relx=0.75, rely=0.925, anchor="center")

        self.bt_no = ctk.CTkButton(self.app, text="<-- Não", command=no)
        self.bt_no.place(relx=0.5, rely=0.925, anchor="center")

        self.app.bind("<Left>", no)
        self.app.bind("<Right>", yes)

        # top menu
        self.menu = Menu(master=self.app)

        # first cascade
        self.file_menu = Menu(master=self.menu, tearoff=0)
        self.file_menu.add_command(label="Selecionar pasta | ctrl+A", command=select_archieve)
        self.menu.add_cascade(label="Arquivo", menu=self.file_menu)

        # seccond cascade
        self.config_menu = Menu(master=self.menu, tearoff=0)
        self.config_menu.add_command(label="Configurações | ctrl+O", command=config)
        self.menu.add_cascade(label="Opções", menu=self.config_menu)

        self.app.config(menu=self.menu)
        self.app.bind("<Control-a>", select_archieve)
        self.app.bind("<Control-o>", config)

        self.app.mainloop()
        self.cfg.write(self.local_path+"\n"+self.extension)
        self.cfg.close()
        self.labels.close()

        # print(read_archieve(r"C:\Users\rma8\Desktop\Materiais\dataset.csv"))

if __name__ == "__main__":
    ImageSelector(True)