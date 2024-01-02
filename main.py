import os
import requests
import tkinter

poke_name = None
user_input = None
my_image = None
previous_input = ""
file_name = ""
initial_width = 305
initial_height = 475

form = tkinter.Tk()
form.title("pokOeeMOnOnNonNn")
form.geometry(f"{initial_width}x{initial_height}")

def get_user_input():
    global poke_name, user_input, my_image, previous_input, file_name

    current_input = entry.get()

    if current_input == previous_input:
        return

    previous_input = current_input

    poke_name = current_input
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        api = response.json()

        front = "front_default"
        back = "back_default"

        if api["sprites"].get(front):
            file_name = f"{poke_name}_{front}.png"
            foto = requests.get(api["sprites"][front], allow_redirects=True)
            open(file_name, 'wb').write(foto.content)
            my_image = tkinter.PhotoImage(file=file_name)

        elif api["sprites"].get(back):
            file_name = f"{poke_name}_{back}.png"
            foto = requests.get(api["sprites"][back], allow_redirects=True)
            open(file_name, 'wb').write(foto.content)
            my_image = tkinter.PhotoImage(file=file_name)

        else:
            my_image = None

        display_name.config(text=f"{poke_name.upper()}\n", font=("Courier", 14))
        weight_height.config(text=f"weight: {api['weight']}\nheight: {api['height']}")
        image.config(image=my_image, width=300, height=300)

    except:
        set_initial_size()
        display_name.config(text="HATA! Pokemon bulunamadı.")
        weight_height.config(text="")
        image.config(image="", width=300, height=300)

def on_closing():
    global file_name

    if os.path.exists(file_name):
        os.remove(file_name)

    form.destroy()

def set_initial_size():
    form.geometry(f"{initial_width}x{initial_height}")

entry = tkinter.Entry(form, width=30)
entry.pack(pady=10)

button = tkinter.Button(form, text="Pokemonu Göster", command=get_user_input)
button.pack(pady=10)

display_name = tkinter.Label(form, text="")
display_name.pack()

weight_height = tkinter.Label(form, text="")
weight_height.pack()

image = tkinter.Label(form, width=300, height=300)
image.pack()

form.protocol("WM_DELETE_WINDOW", on_closing)

form.mainloop()
