import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from basic_functions import *
from time import sleep


class Layout(tk.Tk):
    def __init__(self):
        super().__init__()
        pygame.init()
        initialize_songs()

        # tamanho da janela, cor de fundo e nome.
        self.title("Olha a Pedra")
        self.geometry("300x420+290+85")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.control = True
        self.offset = 0

        # Imagens
        image_icon = tk.PhotoImage(file="Images/ispotifai.png")
        self.iconphoto(False, image_icon)

        top = tk.PhotoImage(file="Images/banner.png")
        self.background = tk.Label(self, image=top, bg="#000000")
        self.background.image = top
        self.background.pack()

        img = get_album_cover()

        tam = img.resize((150, 150), Image.Resampling.LANCZOS)
        nova_img = ImageTk.PhotoImage(tam)

        self.capa = tk.Label(self, image=nova_img, bg="#000000", bd=0)
        self.capa.image = nova_img
        self.capa.place(x=78, y=62)

        img_de_play = tk.PhotoImage(file="Images/play_button.png")
        self.botao_de_play = tk.Button(self, image=img_de_play, bg="#000000", command=unpause_song, bd=0)
        self.botao_de_play.image = img_de_play
        self.botao_de_play.place(x=148, y=320)

        img_de_pause = tk.PhotoImage(file="Images/pause.png")
        self.botao_de_pause = tk.Button(self, image=img_de_pause, bg="#000000", bd=0, command=pause_song)
        self.botao_de_pause.image = img_de_pause
        self.botao_de_pause.place(x=105, y=329)

        img_de_anterior = tk.PhotoImage(file="Images/anterior.png")
        self.botao_de_anterior = tk.Button(self, image=img_de_anterior, bg="#000000", bd=0, command=self.previous_button)
        self.botao_de_anterior.image = img_de_anterior
        self.botao_de_anterior.place(x=55, y=329)

        img_de_proxima = tk.PhotoImage(file="Images/proxima.png")
        self.botao_de_proximo = tk.Button(self, image=img_de_proxima, bg="#000000", bd=0, command=self.next_button)
        self.botao_de_proximo.image = img_de_proxima
        self.botao_de_proximo.place(x=220, y=329)

        # self.progress_music = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=250, mode='determinate', maximum=400)
        # self.progress_music.place(x=25, y=270)

        # barra de progressão nova

        self.frame_progress = tk.Frame(self)
        self.frame_progress.place(x=38, y=260)

        self.music_bar = ttk.Scale(self.frame_progress, from_=0, to=1, orient=tk.HORIZONTAL, value=0, length=220, command=self.control_control)
        self.music_bar.bind("<ButtonRelease-1>", self.set_timestamp)
        self.music_bar.grid(row=1, column=600)



        # botões aleatorio e de repetição

        aleatorio_image = tk.PhotoImage(file="Images/aleatorio_off.png")
        self.aleatorio_button = tk.Button(self, image=aleatorio_image, bg="#000000", bd=0, command=self.random_config)
        self.aleatorio_button.image = aleatorio_image
        self.aleatorio_button.place(x=28, y=335)

        repetir_tudo = tk.PhotoImage(file="Images/repetir_off.png")
        self.repetir_button = tk.Button(self, image=repetir_tudo, bg="#000000", bd=0, command=self.repeat_config)
        self.repetir_button.image = repetir_tudo
        self.repetir_button.place(x=260, y=330)

        # barra de volume
        self.master_frame = tk.Frame(self)
        self.master_frame.place(x=20, y=80)

        # volume
        self.volume = ttk.Scale(self.master_frame, from_=1, to=0, orient=tk.VERTICAL, value=0.5, length=125, command=set_volume)
        self.volume.grid(row=1, column=600)

        # menu de opções
        menu_de_opcoes = tk.Menu(self)

        # menu file
        fileMenu = tk.Menu(menu_de_opcoes, tearoff=0)
        fileMenu.add_command(label="Adicionar Diretório", command=search_directory)
        fileMenu.add_command(label="Open file")
        fileMenu.add_command(label="Save")
        menu_de_opcoes.add_cascade(label="File", menu=fileMenu)

        # outras opções, mas sem o cascade
        menu_de_opcoes.add_command(label="Edit")
        menu_de_opcoes.add_command(label="View")
        menu_de_opcoes.add_command(label="Navigate")

        self.config(menu=menu_de_opcoes)

        if self.control:
            self.progress_bar()
        self.check_end_song()

    @staticmethod
    def update_cover(capa: tk.Label):
        image = get_album_cover()

        size = image.resize((150, 150), Image.Resampling.LANCZOS)
        new_img = ImageTk.PhotoImage(size)
        capa.config(image=new_img)
        capa.photo_ref = new_img

    def next_button(self):
        if get_repeat_mode() == 2:
            self.repeat_config()
        next_song()
        self.update_cover(self.capa)
        self.offset = 0

    def previous_button(self):
        previous_song()
        sleep(0.1)
        self.update_cover(self.capa)
        self.offset = 0

    def progress_bar(self):
        """
        A função vai atualizar a barra de progresso a cada 50 milissegundos.
        :return: None.
        """
        if self.control:
            if get_current_play_time() != 0:
                self.music_bar.configure(value=(mixer.music.get_pos()/1000)/get_current_play_time() + get_start_time()/get_current_play_time())
            self.music_bar.update()
            self.music_bar.after(50, self.progress_bar)

    def check_end_song(self):
        """
        A função irá verificar a cada 50 milissegundos se a música acabou. Se acabou, tocará a próxima da fila.
        :return: None.
        """
        if end_song_to_next():
            self.offset = 0
        end_song_to_next()
        self.update_cover(self.capa)
        self.update()
        self.after(50, self.check_end_song)

    def repeat_config(self):
        repeat_songs()

        if get_repeat_mode() == 0:
            repeat_image = tk.PhotoImage(file="Images/repetir_off.png")
        elif get_repeat_mode() == 1:
            repeat_image = tk.PhotoImage(file="Images/repetir_tudo.png")
        else:
            repeat_image = tk.PhotoImage(file="Images/repetir_1.png")

        self.repetir_button.configure(image=repeat_image)
        self.repetir_button.image = repeat_image

    def random_config(self):
        randomize_songs()

        if get_random_mode():
            aleatorio_image = tk.PhotoImage(file="Images/aleatorio_on.png")
        else:
            aleatorio_image = tk.PhotoImage(file="Images/aleatorio_off.png")

        self.aleatorio_button.configure(image=aleatorio_image)
        self.aleatorio_button.image = aleatorio_image

    def set_timestamp(self, event):
        self.offset = self.music_bar.get()
        set_time(self.offset * get_current_play_time())
        self.control = True
        self.progress_bar()

    def control_control(self, value):
        self.control = False


layout = Layout()
tk.mainloop()
