import requests
from tkinter import Tk, Label, Button, PhotoImage
from io import BytesIO
from PIL import Image, ImageTk

class PokedexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.configure(bg="white")
        self.height = 200
        self.width = 200
        self.x = (root.winfo_screenwidth()//2)-(self.width//2)
        self.y = (root.winfo_screenheight()//2)-(self.height//2)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))

        self.current_pokemon_id = 1

        self.name_label = Label(root, text="", font=("./assets/font/font.ttf", 16), fg="#a76ff0", bg="white")
        self.name_label.pack()

        self.image_label = Label(root, bg="white")
        self.image_label.pack()

        self.load_pokemon_data()
        self.update_ui()

        next_button = Button(root, text="Next Pokemon", command=self.next_pokemon, font=("./assets/font/font.ttf"), fg="#b68f40", bg="white", borderwidth=0)
        next_button.pack()

    def load_pokemon_data(self):
        api_url = f"https://pokeapi.co/api/v2/pokemon/{self.current_pokemon_id}/"
        response = requests.get(api_url)
        data = response.json()

        self.pokemon_name = data['name'].capitalize()

        sprite_url = data['sprites']['front_default']
        sprite_response = requests.get(sprite_url)
        image_data = Image.open(BytesIO(sprite_response.content))
        self.pokemon_image = ImageTk.PhotoImage(image_data)

    def update_ui(self):
        self.name_label.config(text=self.pokemon_name)
        self.image_label.config(image=self.pokemon_image)

    def next_pokemon(self):
        self.current_pokemon_id += 1
        self.load_pokemon_data()
        self.update_ui()

if __name__ == "__main__":
    root = Tk()
    app = PokedexApp(root)
    root.mainloop()
