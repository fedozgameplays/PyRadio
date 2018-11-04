import vlc
import tkinter
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def resize(file, size):
    image = tkinter.PhotoImage(file=file)
    return image.subsample(size)


settings = ""
lb2 = ""
vol = 80
desc = ""
window_width = "800"
window_height = "400"
Instance = vlc.Instance()
player = Instance.media_player_new()

main = tkinter.Tk()
main.geometry(window_width+"x"+window_height)
main.attributes("-alpha", "1.0")
main.title("PyRadio")
main.resizable(False, False)

setup = open("settings.bin", "r")
colormode = setup.readline()
# language=setup.readline(2)
setup.close()
if colormode == "0":
    play = resource_path("play.png")
    pause = resource_path("Pause.png")
    forward = resource_path("forward.png")
    backward = resource_path("backward.png")
    button_play = resize(play, 5)
    button_pause = resize(pause, 5)
    button_forward = resize(forward, 8)
    button_backward = resize(backward, 8)
    button_color = "#f0f0ed"
    font_color = "black"
elif colormode == "1":
    play = resource_path("play_white.png")
    pause = resource_path("Pause_white.png")
    forward = resource_path("forward_white.png")
    backward = resource_path("backward_white.png")
    button_play = resize(play, 5)
    button_pause = resize(pause, 5)
    button_forward = resize(forward, 8)
    button_backward = resize(backward, 8)
    main.configure(background="#0B0B3B")
    button_color = "#0B0B3B"
    font_color = "white"


def radio_url(url):
    global list_player, playing, player, desc, l2
    Media_list = Instance.media_list_new([url])
    list_player = Instance.media_list_player_new()
    list_player.set_media_list(Media_list)
    list_player.set_media_player(player)
    list_player.play()
    main.update()
    playing = True
    radio_buttons[0]["image"] = button_pause


url = ["http://stream.antenne1.de/stream1/livestream.mp3", "http://mp3channels.webradio.antenne.de/antenne", "http://streams.br.de/bayern3_2.m3u",
       "http://streams.bigfm.de/bigfm-deutschland-128-aac?usid=0-0-H-A-D-30", "http://avw.mdr.de/streams/284320-0_mp3_high.m3u", "http://streams.rsa-sachsen.de/rsa-live/mp3-192/mediaplayerrsa",
       "http://energyradio.de/sachsen", "http://energyradio.de/berlin", "http://www.vtuner.com/vtunerweb/asp/StatLaunchMP3.asp?id=6407&Link=1",
       "http://streams.ffh.de/radioffh/mp3/hqlivestream.m3u", "http://streams.radiopsr.de/psr-live/mp3-192/listenlive/play.m3u"]


def channel_control(channel):
    if channel == "0":
        radio_url(url[0])
    elif channel == "1":
        radio_url(url[1])
    elif channel == "2":
        radio_url(url[2])
    elif channel == "3":
        radio_url(url[3])
    elif channel == "4":
        radio_url(url[4])
    elif channel == "5":
        radio_url(url[5])
    elif channel == "6":
        radio_url(url[6])
    elif channel == "7":
        radio_url(url[7])
    elif channel == "8":
        radio_url(url[8])
    elif channel == "9":
        radio_url(url[9])
    elif channel == "10":
        radio_url(url[10])


def radio_control(option):
    global lb1, player, playing, channel
    if option == 1:
        if playing is True:
            player.stop()
            playing = False
            radio_buttons[0]["image"] = button_play
        elif playing is False:
            channel = lb1.curselection()
            channel = str(channel).replace("(", "")
            channel = str(channel).replace(")", "")
            channel = str(channel).replace(",", "")
            print(channel)
            channel_control(channel)
    else:
        channel = lb1.curselection()
        channel = str(channel).replace("(", "")
        channel = str(channel).replace(")", "")
        channel = str(channel).replace(",", "")
        if option == 2:
            channel = int(channel)-1
        if option == 3:
            channel = int(channel)+1
        print(channel)
        lb1.selection_clear(0, "end")
        lb1.selection_set(channel)
        main.update()
        player.stop()
        channel_control(str(channel))


def volume(vol):
    global player
    player.audio_set_volume(int(vol))


def save():
    global settings, lb2
    colormode = lb2.curselection()
    colormode = str(colormode).replace("(", "")
    colormode = str(colormode).replace(")", "")
    colormode = str(colormode).replace(",", "")
    setup = open("settings.bin", "r")
    data1 = setup.readline()
    # data2=setup.readline(2)
    setup.close()
    data1 = colormode
    # data2=""
    setup = open("settings.bin", "w")
    setup.writelines(str(data1))  # +(str(data2)))
    setup.close()
    settings.destroy()
    return


def settings():
    global settings, lb2
    settings = tkinter.Toplevel(main)
    settings.geometry("500x250")
    settings.title("Einstellungen")
    settings.lift(aboveThis=main)
    settings.configure(background=button_color)
    settingbin = open("settings.bin", "r")
    setting = settingbin.readline()
    # setting = settingbin.readline(2)
    l1 = tkinter.Label(settings, text="Farbmodus", fg=font_color, bg=button_color)
    l1.place(rely="0.05", relx="0.02")
    lb2 = tkinter.Listbox(settings, height="2", selectmode="single", fg=font_color, bg=button_color)
    lb2.insert(1, "Hell")
    lb2.insert(2, "Dunkel")
    lb2.selection_set(setting)
    lb2.place(rely="0.18", relx="0.022")
    b8 = tkinter.Button(settings, text="Speichern", fg=font_color, bg=button_color, command=save)
    b8.place(rely="0.8", relx="0.8")


def about():
    about = tkinter.Toplevel(main)
    about.geometry("250x200")
    about.title("Über")
    about.lift(aboveThis=main)
    about.configure(background=button_color)
    label_text = ["PyRadio", "Version: 1.1", "Autor: Kevin Rossmeier", "Kontakt:", "E-Mail: kevinrossmeier@live.de"]
    about_labels = []
    for i in range(len(label_text)):
        about_labels.append(tkinter.Label(about, text=label_text[i], fg=font_color, bg=button_color))
        about_labels[i].place(x=10, y=2*i*10+10)


playing = False

radio_buttons = []
menu_button = []
button_images = [button_play, button_backward, button_forward]
button_y = ["0.26", "0.32", "0.32"]
button_x = ["0.15", "0.04", "0.31"]
stations = ["Antenne 1", "Antenne Bayern", "Bayern 3", "bigFM", "MDR Jump", "R.SA Sachsen", "Energy (Sachsen)", "Energy (Berlin)", "KISS FM", "Hit Radio FFH", "Radio PSR"]
menu_items = ["Einstellungen", "Hilfe", "Über", "Beenden"]
menu_commands = [settings, "", about, main.destroy]

s1 = tkinter.Scale(main, orient="horizontal", bg=font_color, fg=font_color, showvalue="0", variable=vol, length="280", troughcolor=button_color, bd="1", relief="flat", border="1", command=volume)
s1.place(rely="0.62", relx="0.04")
s1.set(vol)
lb1 = tkinter.Listbox(main, width="60", height="11", selectmode="single", bg=button_color, fg=font_color)

for i in range(len(button_images)):
    radio_buttons.append(tkinter.Button(main, image=button_images[i], relief="flat", border="0", bg=button_color, activebackground=button_color, command=lambda i=i: radio_control(i+1)))
    radio_buttons[i].place(rely=button_y[i], relx=button_x[i])

for i in range(1, len(stations)+1):
    lb1.insert(i, stations[i-1])
lb1.place(rely="0.1", relx="0.5")

for i in range(len(menu_items)):
    menu_button.append(tkinter.Button(main, text=menu_items[i], width="27", height="1", bg=button_color, fg=font_color, command=menu_commands[i]))
    menu_button[i].grid(column=i, row=5)

main.mainloop()
