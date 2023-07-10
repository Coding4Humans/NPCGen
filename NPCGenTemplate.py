
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

defaults = {
            "Setting:": "[[Enter setting text here]]",
            "Game Type:": "[[Enter game type here]]",
            "Full Name:": "[[Enter character's full name here]]",
            "Nickname:": "[[Enter character's nickname here]]",
            "Age:": "[[Enter character's age here]]",
            "Race:": "[[Enter character's race here]]",
            "Height:": "[[Enter character's height here]]",
            "Weight:": "[[Enter character's weight here]]",
            "Notable Features:": "[[Enter notable features here]]",
            "Religion:": "[[Enter character's religion here]]",
            "Sexual Orientation:": "[[Enter character's sexual orientation here]]",
            "Relationship Status:": "[[Enter character's relationship status here]]",
            "Background:": "[[Give a brief history of the character from childhood to their present age.]]",
            "Abilities and Skills:": "[[What skills and talents does the character have? What are they good at, what are they bad at?]]",
            "Equipment:": "[[What type of equipment do they have on them? What is the quality or craftsmanship of their equipment?]]",
            "Voice and Mannerisms:": "[[How do they talk to strangers? How do they talk to people they know well? What characteristics does their voice or speaking mannerisms have?]]",
            "Connections and Allies:": "[[Who do they know that is noteworthy? Who are they connected to? Do they have any relatives?]]",
            "Personal Motivations:": "[[What are they driven by? What are they passionate about?]]",
            "Character Development:": "[[What kind of character development can we expect to experience when spending time with this character?]]",
            "Plot Hook:": "[[Create at least 3 compelling one or two sentence long plot hooks to give the players a reason to be interested in this character.]]"
        } 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

# configure window
        self.title("Simple RPG NPC Template Generator")
        self.geometry(f"{1200}x{780}")

# configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Generate Button , trying to replace this with dynamic updating entry fields
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command=self.main_button_1_generate_event)
        self.main_button_1.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

# Right column || Scrollable Frame || Where user can enter parameter
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Custom Parameters")
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_entries = list(defaults.values())

# Creates the entry fields with the default text as the key for the dictionary
        for i, (label_text, default_value) in enumerate(defaults.items()):
            entry_field = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text=label_text)
            entry_field.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_entries.append(default_value)


# Defaulting the entry field
        #default_text = self.main_button_1_generate_event()
        self.textbox.insert("0.0", f"{self.main_button_1_generate_event()}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

   
    def sidebar_button_event(self):
        print("sidebar_button click")
    
       

    # Push the Generate Button is pushed
    def main_button_1_generate_event(self):
        print("Generating")

        # Update dictionary values with user input
        for entry_field, (label_text, _) in zip(self.scrollable_frame.children.values(), defaults.items()):
            user_input = entry_field.get()
            if user_input:
                defaults[label_text] = user_input

        # Generate and print template
        template = f'''
        You are now a highly skilled and creative roleplayer. 
        You excel at creating interesting characters for players to interact with.

        First, I’d like for you to generate a character. 
        I will give you a specific set of attributes and I would like you to fill them out. 
        If I want specific features I will include them, otherwise, please generate new attributes based on the instructions below.

        Setting:
        {defaults["Setting:"]}

        Game Type:
        {defaults["Game Type:"]}

        Character Description
        Full name: {defaults["Full Name:"]}
        Nickname: {defaults["Nickname:"]}
        Age: {defaults["Age:"]}
        Race: {defaults["Race:"]}
        Height: {defaults["Height:"]}
        Weight: {defaults["Weight:"]}
        Notable features: {defaults["Notable Features:"]}

        Personality Traits:
        Religion: {defaults["Religion:"]}
        Sexual orientation: {defaults["Sexual Orientation:"]}
        Relationship status: {defaults["Relationship Status:"]}

        Background: 
        {defaults["Background:"]}

        Abilities and skills: 
        {defaults["Abilities and Skills:"]}

        Equipment: 
        {defaults["Equipment:"]}

        Voice and Mannerisms: 
        {defaults["Voice and Mannerisms:"]}

        Connections and Allies: 
        {defaults["Connections and Allies:"]}

        Personal Motivations: 
        {defaults["Personal Motivations:"]}

        Character Development: 
        {defaults["Character Development:"]}

        Plot Hook: 
        {defaults["Plot Hook:"]}
        '''

        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", template)

if __name__ == "__main__":
    app = App()
    app.mainloop()