
# Todo:
# - Create a progress bar of some sort for when the app locks up while generating from OpenAI
# - Create a tab for Generating NPC and selecting from generated NPC to have conversation with
# Extra: keep count of token use and save to file each time it's updated

from tkinter import messagebox
from datetime import datetime
import customtkinter
import os
import openai
from dotenv import load_dotenv, find_dotenv

# Get api key from .env
_=load_dotenv(find_dotenv())
My_API_Key = os.getenv("OPENAI_API_KEY")
openai.api_key = My_API_Key

# Set up GUI system defaults
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# The default keys and values for the template. 
# Am considering moving this to a data structure to control the types of inputs from the person (i.e. game type etc) but not really important
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

# Default file paths and folders
conversation_log_file_path = "conversation_log.txt"
token_count_file_path = "token_cost.txt"
folder_path = "./Characters"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #instance and default variables for template, role and req to pass between button_template_event and button_generate_event
        self.template = ""
        self.role = ""
        self.output_requierments = ""

        # configure window
        self.title("Simple RPG NPC Template Generator")
        self.geometry(f"{1200}x{850}")

        # configure grid layout 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_rowconfigure((1, 2), weight=0)
        self.grid_rowconfigure(4, weight=5)


        # create textbox to preview the template
        self.template_textbox = customtkinter.CTkTextbox(self, width=250, height=20)
        self.template_textbox.grid(row=0, column=0, padx=(5, 0), pady=(20, 0), sticky="nsew")
        # template button
        self.button_tempalte = customtkinter.CTkButton(master=self, text="Generate Template", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command=self.button_template_event)
        self.button_tempalte.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew")

        # create textbox to show generated text
        self.generated_textbox = customtkinter.CTkTextbox(self,width=250, height=400)
        self.generated_textbox.grid(row=3, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        # generate response button
        self.button_generate = customtkinter.CTkButton(master=self, text="Generate AI Response", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command=self.button_generate_event)
        self.button_generate.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew")

        # Generate save button to save the generated response to a file
        self.button_save = customtkinter.CTkButton(master=self, text="Save Generated Character", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                   command=self.button_save_event)
        self.button_save.grid(row=4, column=1, padx=(20, 20), pady=(5, 5), sticky="nsew")
        # create test button
        self.button_test = customtkinter.CTkButton(master=self, text="Test Button", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                   command=lambda: self.extract_text_after_pattern(
                                                        text=self.generated_textbox.get("1.0", "end-1c"), 
                                                        start_pattern="Full name:", 
                                                        end_pattern="Nickname:")
                                                        ) # testing, return origonal button_save_event
        self.button_test.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="e")

        # create token counter frame
        self.token_frame = customtkinter.CTkFrame(self)
        self.token_frame.grid(row=4, column=0, padx=(5, 5), pady=(5, 5), sticky="w")
        self.token_frame.grid_columnconfigure(0, weight=1)
        # create token counter under the AI generated response 
        self.tokens_label = customtkinter.CTkLabel(master=self.token_frame, text="Tokens Used: ")
        self.tokens_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="n")
        self.tokens_text = customtkinter.CTkTextbox(master=self.token_frame)
        self.tokens_text.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="n")
        self.tokens_text.insert("0.0", "")
        self.token_info = customtkinter.CTkLabel(master=self.token_frame, text="Token cost 4k Context Input: $0.0015 Output: $0.002 per 1k tokens")




        # Right column || Scrollable Frame || Where user can enter parameter
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, height=800, label_text="Custom Parameters")
        self.scrollable_frame.grid(row=0, rowspan=4, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_entries = list(defaults.values())

        # Creates the entry fields with the default text as the key for the dictionary
        for i, (label_text, default_value) in enumerate(defaults.items()):
            entry_field = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text=label_text)
            entry_field.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_entries.append(default_value)


        # Defaulting the template and generated textboxes
        self.template_textbox.insert("0.0", f"")
        self.generated_textbox.insert("0.0", f"")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    # Exttract specific text given start and end pattern. 
    # Todo:
    # - Use for finding the file name in button_save_event
    # - use for creating the character select tabs (get their name, game, race, etc)
    def extract_text_after_pattern(self, text, start_pattern, end_pattern):
        print("Extracting")
        start_index = text.find(start_pattern)
        if start_index != -1:
            start_index += len(start_pattern) # move index to end of pattern
            end_index = text.find(end_pattern, start_index)
            if end_index != -1:
                return print(text[start_index:end_index].strip())
            return "" # Return empty if pattern or newline character not found
        
    # Generate a template to print to the template textbox and send to the API
    def button_template_event(self):
        print("Generating Template")
        
        # Update dictionary values with user input
        for entry_field, (label_text, _) in zip(self.scrollable_frame.children.values(), defaults.items()):
            user_input = entry_field.get()
            if user_input:
                defaults[label_text] = user_input
        
        # Genrate and update instructions to the model based on template 
        # commented for brevity
        # You are now a highly skilled and creative roleplayer. You excel at creating interesting characters for players to interact with. After you generate a character, you will then role play as the character within the spexified setting and interact with the player
        
        role = f"""You are now a highly skilled and creative roleplayer. 
        You excel at creating interesting characters for players to interact with. 
        """
        template = f'''
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
        output_requierments = f"All outputs must be in plain text format."


        # print template results to template_textbox
        self.template_textbox.delete("0.0", "end")
        self.template_textbox.insert("0.0", template)

        #store generated template
        self.template = template
        self.role = role
        self.output_requierments = output_requierments

    # AI Generate button event
    def button_generate_event (self):
        print("Sending to GPT")
        # Send the prompt to  OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # set to chat 3.5 turbo @ 4k
            messages=[
                {"role": "system", "content": self.role},
                {"role": "system", "content": self.output_requierments},
                {"role": "system", "content": self.template}
                ]
        )


        # isntance the generated response and token counts
        generated_response = response['choices'][0]['message']['content']
        prompt_tokens = response['usage']['prompt_tokens']              # tokens used during user prompt
        completion_tokens = response['usage']['completion_tokens']      # tokens used to generate response
        
        # figure out cost of tokens
        prompt_cost = (prompt_tokens/1000) * 0.0015
        completion_cost = (completion_tokens/1000) * 0.002
        total_tokens = prompt_tokens + completion_tokens
        total_cost = round(prompt_cost + completion_cost, 3)

        token_printout = f"Input Tokens: {prompt_tokens}[${round(prompt_cost, 3)}] Output Tokens: {completion_tokens}[${round(completion_cost, 3)}] Total: {total_tokens}[${total_cost}]"
        
        # print generated results to generated_textbox
        self.generated_textbox.delete("0.0", "end")
        self.generated_textbox.insert("0.0", generated_response)
        
        # update token count
        self.tokens_text.delete("0.0", "end")
        self.tokens_text.insert("0.0", token_printout)
        print(f"Total Tokens: {total_tokens} || Total Cost: {total_cost}")

        # save generated template and response to file
        print("Saving conversation")
        with open(conversation_log_file_path, "a") as file:
            file.write(self.template + "\n" + generated_response + "\n")
            file.write(token_printout + "\n")
            file.write("\n" + "==========" *50 + "\n") #section break. perhaps add in time or date of convo or something at some point

        return generated_response
        

    # Button event to save the generated character to a file with error catch
    def button_save_event(self):

        #check if character has been generated
        generated_response = self.generated_textbox.get("1.0", "end-1c") 
        if not generated_response:
            messagebox.showerror("Error:", "Please generate a character first.")
            return

        # Extract character Full Name - ====================offload this to the extraction function
        full_name_start = generated_response.find("Full name:") + len("Full name:")
        nickname_start = generated_response.find("Nickname:")
        character_name = generated_response[full_name_start:nickname_start].strip()
        if not character_name:
            messagebox.showerror("Error", "Unable to extract characte's Full name from generated response")
            return
        
        #check if the folder exists. if not, create if user wants to
        if not os.path.exists(folder_path):
            response = messagebox.askyesno("Error", "The 'Characters' folder does not exist. \nWould you like to create one?")
            if response:
                os.makedirs(folder_path)
                messagebox.showinfo("Success", "The 'Characters' folder has been created.")
            else:
                return
        
        file_name = f"{character_name}.txt"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            confirm = messagebox.askyesno("File Exists", "The file already exists. Do you want to overwrite it?")
            if not confirm:
                return

        with open(file_path, "w") as file:
            file.write(generated_response)
        messagebox.showinfo("Save Successful", f"The generated character has been saved as '{file_name}'.")


if __name__ == "__main__":
    app = App()
    app.mainloop()