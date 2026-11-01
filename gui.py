import customtkinter as ctk
from brain import Brain
import threading
import socket
import uuid
from tools.tool_router import ToolRouter
from tools.file import run_upload_file
from tools.file_processor import FileProcessor
from tools.upload_file_tool import UploadFileTool
from tools.upload_image.image_tool import upload_image
from tkinter import messagebox
#Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Elara_GUI:

    def __init__(self, root):

        self.root = root
        self.brain = Brain()
        self.session_id = "default"
        self.mode=None
        self.web_page=0
        self.web_pagination_visible=False
        self.web_message_start=False
        self.tool_router=ToolRouter()
        self.file_processor=FileProcessor()
        self.upload_file_tool=UploadFileTool(self.brain.router.memory)
        self.tool_router.register(
            "upload_files",
            self.upload_file_tool.run
        )
        self.tool_router.register(
            "image_uploaded",
            upload_image)

        self.image_context=None
        

    # Window
        self.root.title("ELARA")
        self.root.minsize(850, 550)

     # Main background
        self.root.configure(fg_color="#0B0B12")
        
    # Main layout
    
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="#0B0B12",
            corner_radius=0
        )
        self.main_frame.pack(
            fill="both",
            expand=True
        )
    # Sidebar
       
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            width=230,
            fg_color="#101019",
            corner_radius=0
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

    # ELARA logo
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="✦  ELARA",
            font=("Arial", 24, "bold"),
            text_color="#A970FF"
        )
        self.logo.pack(
            padx=25,
            pady=(30, 35),
            anchor="w"
        )

    # New chat button
        self.new_chat_button = ctk.CTkButton(
            self.sidebar,
            text="+  New Chat",
            height=42,
            corner_radius=10,
            fg_color="#1B1B29",
            hover_color="#292943",
            text_color="#E8E8F0",
            font=("Arial", 13),
            anchor="w",
            command=self.new_chat
        )
        self.new_chat_button.pack(
            padx=18,
            fill="x"
        )

    # Sidebar section
        self.history_label = ctk.CTkLabel(
            self.sidebar,
            text="CONVERSATIONS",
            font=("Arial", 11, "bold"),
            text_color="#686878"
        )
        self.history_label.pack(
            padx=22,
            pady=(35, 12),
            anchor="w"
        )

    # Placeholder for conversations
        self.history_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#39394D",
            scrollbar_button_hover_color="#7C4DFF"
        )
        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0,10)
        )

    #sider bar manegment

        self.side_bar_tools=ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        self.side_bar_tools.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=(5,15)
        )

        self.knowledge_manegment=ctk.CTkButton(
            self.side_bar_tools,
            text="Knowledge",
            height=40,
            corner_radius=8,
            fg_color="#181824",
            hover_color="#292943",
            text_color="#E8E8F0",
            anchor="w",
            font=("Arial",13),
            command= self.open_knowledge_manager
        )

        self.knowledge_manegment.pack(
            fill="x",
            pady=(0,6)
        )

        self.project_manegment=ctk.CTkButton(
            self.side_bar_tools,
            text=" Projects",
            height=40,
            corner_radius=8,
            fg_color="#181824",
            hover_color="#292943",
            text_color="#E8E8F0",
            anchor="w",
            font=("Arial",13),
            command=self.open_project_manager
        )

        self.project_manegment.pack(
            fill="x"
        )


    # Right side
        
        self.content = ctk.CTkFrame(
            self.main_frame,
            fg_color="#0B0B12",
            corner_radius=0
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )
     # Header
        
        self.header = ctk.CTkFrame(
            self.content,
            height=75,
            fg_color="#0F0F18",
            corner_radius=0
        )
        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(False)

        self.title = ctk.CTkLabel(
            self.header,
            text="ELARA",
            font=("Arial", 18, "bold"),
            text_color="#F2F2F7"
        )
        self.title.pack(
            side="left",
            padx=25
        )
    #status
        
        self.status = ctk.CTkLabel(
            self.header,
            text="●  Checking...",
            font=("Arial", 11),
            text_color="#AAAAAA"
        )
        self.status.pack(
            side="right",
            padx=25
        )
    # Chat area
        
        self.chat = ctk.CTkTextbox(
            self.content,
            fg_color="#0B0B12",
            text_color="#E8E8F0",
            font=("Arial", 14),
            wrap="word",
            corner_radius=0,
            border_width=0
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(15, 10)
        )

        self.chat.configure(
            state="disabled"
        )

        # Web pagination
        self.web_nav_frame = ctk.CTkFrame(
            self.content,
            height=45,
            fg_color="#0B0B12",
            corner_radius=0
        )

        self.web_nav_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 5)
        )

        self.web_nav_frame.pack_propagate(False)

        self.previous_web_button = ctk.CTkButton(
            self.web_nav_frame,
            text="← Previous",
            width=100,
            height=32,
            corner_radius=8,
            fg_color="#181824",
            hover_color="#292943",
            text_color="#E8E8F0",
            command=self.previous_web_page
        )

        self.next_web_button = ctk.CTkButton(
            self.web_nav_frame,
            text="Next →",
            width=100,
            height=32,
            corner_radius=8,
            fg_color="#181824",
            hover_color="#292943",
            text_color="#E8E8F0",
            command=self.next_web_page
        )

        self.web_page_label = ctk.CTkLabel(
            self.web_nav_frame,
            text="",
            font=("Arial", 11),
            text_color="#777788"
        )

        self.hide_web_navigation()

     # Input area
    
        self.input_frame = ctk.CTkFrame(
            self.content,
            height=80,
            fg_color="#101019",
            corner_radius=0
        )
        self.input_frame.pack(
            fill="x"
        )

        self.input_frame.pack_propagate(False)

    #Tool button
        self.tool_btn=ctk.CTkButton(
            self.input_frame,
            text="+",
            width=20,
            height=20,
            corner_radius=12,
            fg_color="#181824",
            hover_color="#D8D8E5",
            font=("Arial",22,"bold"),
            command=self.show_tools
        )
        self.tool_btn.pack(
            side="left",
            padx=(20,8),
            pady=17
        )

     # Message input
        self.input_box = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Message ELARA...",
            height=50,
            corner_radius=12,
            fg_color="#181824",
            border_color="#29293A",
            text_color="#F0F0F5",
            placeholder_text_color="#666677",
            font=("Arial", 13)
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=15
        )
    # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="➤",
            width=55,
            height=45,
            corner_radius=12,
            fg_color="#7C4DFF",
            hover_color="#925FFF",
            font=("Arial", 18, "bold"),
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=(0, 20),
            pady=17
        )
        self.refresh_history()
        self.check_connection()

    # Add message

    def add_message(self, sender, message):

        self.chat.configure(state="normal")

        self.chat.insert(
            "end",
            f"{sender}\n",
            "sender"
        )

        self.chat.insert(
            "end",
            f"{message}\n\n"
        )

        self.chat.configure(state="disabled")

        self.chat.see("end")

    def show_thinking(self):
        self.chat.configure(state="normal")
        self.chat.insert(
            "end",
            "ELARA\n",
            "thinking_sender"
        )
        self.chat.insert(
            "end",
            "✦ ELARA is thinking ...\n\n",
            "thinking"
        )
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def hide_thinking(self):
        self.chat.configure(state="normal")
        star=self.chat.search(
            "✦ ELARA is thinking ...",
            "1.0",
            backwards=True
        )
        if star:
            end=f"{star} lineend + 1c"
            self.chat.delete(star,end)
            send_start=self.chat.search(
            "ELARA",
            "1.0",
            backwards=True)
            if send_start:
                sender_end=f"{send_start} lineend + 1c"

                self.chat.delete(send_start,sender_end)

        self.chat.configure(state="disabled")
        self.chat.see(end)

    #hide navigation

    def hide_web_navigation(self):
        self.previous_web_button.pack_forget()
        self.next_web_button.pack_forget()
        self.web_page_label.pack_forget()

        self.web_nav_frame.pack_forget()

        self.web_pagination_visible = False

    #show navigation

    def show_web_navigation(self):
        self.web_nav_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 5)
        )

        self.previous_web_button.pack(
            side="left",
            padx=(5, 10)
        )

        self.web_page_label.pack(
            side="left",
            expand=True
        )

        self.next_web_button.pack(
            side="right",
            padx=(10, 5)
        )

        self.web_pagination_visible = True

    def next_web_page(self):

        self.show_thinking()

        def process():
            response = self.brain.next_web_page(
                self.session_id
            )

            self.root.after(
                0,
                self.hide_thinking
            )

            self.root.after(
                0,
                lambda: self.replace_web_result(response)
            )

        threading.Thread(
            target=process,
            daemon=True
        ).start()

    def previous_web_page(self):

        self.show_thinking()

        def process():
            response = self.brain.previous_web_page(
                self.session_id
            )

            self.root.after(
                0,
                self.hide_thinking
            )

            self.root.after(
                0,
                lambda: self.replace_web_result(response)
            )

        threading.Thread(
            target=process,
            daemon=True
        ).start()

    def replace_web_result(self, response):

        if self.web_message_start is not None:

            self.chat.configure(state="normal")

            self.chat.delete(
                self.web_message_start,
                "end"
            )

            self.chat.configure(state="disabled")

        self.web_message_start = self.chat.index("end-1c")

        self.add_message(
            "ELARA",
            response
        )

        self.update_web_navigation()
            
    # Send message
    
    def send_message(self):

        message = self.input_box.get().strip()

        if not message:
            return

        self.hide_web_navigation()
        self.web_message_start=None


        self.add_message(
            "You",
            message
        )

        self.show_thinking()
        self.input_box.delete(
            0,
            "end"
        )

        thread = threading.Thread(
            target=self.think,
            args=(message,self.mode,self.image_context),
            daemon=True
        )

        thread.start()

    # Brain processing
    
    def think(self, message,mode,image_context=None):

        if image_context:
            message=(
                "The user uploaded an image. The following text was extracted from the image:\n"
                f"{image_context}""user.s question:\n"
                f"{message}"
            )

        response = self.brain.think(
            self.session_id,
            message,
            mode
        )
        self.root.after(
            0,
            self.hide_thinking
        )

        if mode=="web":
            self.root.after(
            0,
            lambda: self.show_web_result(
                response
            )
        )
            
        else:
            self.root.after(
                0,
                lambda: self.add_message(
                    "ELARA",
                    response
                )
            )
        self.root.after(
            0,
            self.refresh_history
        )

        if mode == "web":
            self.mode=None

    def show_web_result(self,response):
        self.web_message_start=self.chat.index("end-1c")
        self.add_message(
            "Elara",
            response
        )
        self.web_page=0
        self.show_web_navigation()
        self.update_web_navigation()

    def update_web_navigation(self):

        session = self.brain.web_sessions.get(
            self.session_id
        )

        if not session:
            return

        claims = session["claims"]
        page = session["page"]

        total_pages = (len(claims) + 9) // 10

        self.web_page_label.configure(
            text=f"Page {page + 1} / {total_pages}"
        )

        if page <= 0:
            self.previous_web_button.configure(
                state="disabled"
            )
        else:
            self.previous_web_button.configure(
                state="normal"
            )

        if (page + 1) >= total_pages:
            self.next_web_button.configure(
                state="disabled"
            )
        else:
            self.next_web_button.configure(
                state="normal"
            )


    #new chat
    def new_chat(self):
        self.session_id=str(uuid.uuid4())
        self.chat.configure(state="normal")
        self.chat.delete("1.0","end")
        self.chat.configure(state="disabled")
        self.input_box.focus()

    #connection cheker
    def check_connection(self):

        def check():
            try:
                import urllib.request

                urllib.request.urlopen(
                    "https://www.google.com",
                    timeout=3
                )

                online = True

            except Exception:
                online = False

            self.root.after(
                0,
                lambda: self.update_connection_status(online)
            )

        threading.Thread(
            target=check,
            daemon=True
        ).start()

        # Check again in 5 seconds
        self.root.after(
            5000,
            self.check_connection
        )

    # update connection
    def update_connection_status(self,online):
        if online:
            self.status.configure(
                text="🟢 Online",
                text_color="#63F5A4"
            )
        else:
            self.status.configure(
                text="🩸 Offline",
                text_color="#FF6B6B"
            )

    #refresh history
    def refresh_history(self):
        print("history refreash started")
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        memory=self.brain.router.memory
        sessions=memory.get_chat_sessions()
        print(f"history sessions:{len(sessions)}")
        for session in sessions:
            session_id=session["session_id"]
            title=session["title"]
            if not title:
                title="New chat"

            title=" ".join(title.split())

            if len(title)>20:
                title=title[:20]+"..."

            row=ctk.CTkFrame(
                self.history_frame,
                fg_color="transparent"
            )
            row.pack(
                fill="x",
                padx=4,
                pady=2)

            button=ctk.CTkButton(
                row,
                text=title,
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#1B1B29",
                text_color="#D8D8E5",
                anchor="w",
                font=("Arial",12),
                command=lambda sid=session_id: self.load_chat(sid)
            )
            button.pack(
                side="left",
                fill="x",
               expand=True
            )

            delete_btn=ctk.CTkButton(
                row,
                text="🗑️",
                width=35,
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#3A2025",
                text_color="#888899",
                font=("Arial",12),
                command=lambda sid=session_id: self.delete_chat(sid)
            )
            delete_btn.pack(
                side="right",
                padx=(3,0))

    def load_chat(self,session_id):
        self.session_id=session_id
        messages=self.brain.router.memory.get_conversation(session_id)
        self.chat.configure(state="normal")
        self.chat.delete("1.0","end")

        for message in messages:
            role=message["role"]
            text=message["message"]
            if role =="user":
                sender="You"
            else:
                sender="Elara"
            self.chat.insert(
                "end",f"{sender}\n"
            )
            self.chat.insert(
                "end",f"{text}\n\n"
            )
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def delete_chat(self,session_id):
        memory=self.brain.router.memory
        memory.delete_conversation(session_id)
        if self.session_id == session_id:
            self.session_id = str(uuid.uuid4())
        
        self.chat.configure(state="normal")
        self.chat.delete("1.0","end")
        self.chat.configure(state="disabled")
        self.refresh_history()

    def show_tools(self):
        menu=ctk.CTkToplevel(self.root)
        menu.title("Tools bar")
        menu.geometry("250*250")
        menu.resizable(False,False)
        menu.configure(
            fg_color="#101019"
        )
        title=ctk.CTkLabel(
            menu,
            text="Tool bar",
            font=("Arial",16,"bold"),
            text_color="#A970FF"
        )
        title.pack(
            pady=(20,15)
        )
        #upload file

        file_btn=ctk.CTkButton(
            menu,
            text="📎upload file",
            height=40,
            corner_radius=10,
            fg_color="#181824",
            hover_color="#292943",
            anchor="w",
            command=self.upload_files
        )
        file_btn.pack(
            fill="x",
            padx=20,
            pady=5
        )
        #upload images
        image_btn=ctk.CTkButton(
            menu,
            text="🖼️ upload images",
            height=40,
            corner_radius=10,
            fg_color="#181824",
            hover_color="#292943",
            anchor="w",
            command=self.upload_images
        )
        image_btn.pack(
            fill="x",
            padx=20,
            pady=5
        )

        #web searck
        web_btn=ctk.CTkButton(
            menu,
            text="🌐web search",
            height=40,
            corner_radius=10,
            fg_color="#181824",
            hover_color="#292943",
            anchor="w",
            command=self.web_search
        )
        web_btn.pack(
            fill="x",
            padx=20,
            pady=5
        )
        #image generation

        image_gen=ctk.CTkButton(
            menu,
            text="🖼️ image generation",
            height=40,
            corner_radius=10,
            fg_color="#181824",
            hover_color="#292943",
            anchor="w",
            command=self.image_generation
        )
        image_gen.pack(
            fill="x",
            padx=20,
            pady=5
        )

    def upload_files(self):
        result=self.tool_router.run("upload_files")
        if not result["success"]:
            self.add_message(
                "Elara",
                f"Tool error:{result['error']}"
            )
            return

        file_result=result["result"]
        if not file_result.get("selected",False):
            return
        
        file_path=file_result.get("file_path","")
        file_name=file_result.get("file_name","")
        extension=file_result.get("extension","")
        content=file_result.get("content","")
        knowledge_id=file_result.get("knowledge_id")

        self.add_message(
            "You",
            f"📎File :{file_name}"
        )

        chunk_count=file_result.get("chunk_count",0)
        
        self.add_message(
            "Elara",
            f"file selected successfully.\n Type: {extension}.\n content extracted: {len(content)} characters.\n chunk created:{chunk_count}\n knowledge_id: {knowledge_id}"
        )


    def upload_images(self):
        result = self.tool_router.run(
            "image_uploaded"
        )

        print(result)

        if not result["success"]:
            self.add_message(
                "ELARA",
                f"Image processing failed: {result['error']}"
            )
            return

        image_result = result["result"]

        if not image_result.get("selected"):
            return

        if "error" in image_result:
            self.add_message(
                "ELARA",
                f"Image processing failed: {image_result['error']}"
            )
            return

        text = image_result.get("text", "")
        self.image_context = text
        self.mode="image"

        self.add_message(
            "IMAGE",
            text if text else "No text was detected in the image."
        )


    def web_search(self):
        self.mode="web"
        self.add_message(
            "Elara",
            "🌐web mode activated\n"
        )
        self.input_box.focus()

    def image_generation(self):
        self.mode="image_gen"
        self.add_message(
            "Elara",
            "Image generation mode activated\n"
        )
        self.input_box.focus()
  
    def open_knowledge_manager(self):
        print("open knowledge is invoked.")

        memory = self.brain.router.memory

        window = ctk.CTkToplevel(self.root)
        window.title("ELARA - Knowledge Manager")
        window.geometry("850x550")
        window.minsize(650, 400)
        window.configure(fg_color="#0B0B12")

        # Window title
        heading = ctk.CTkLabel(
            window,
            text="Knowledge Manager",
            font=("Arial", 22, "bold"),
            text_color="#A970FF"
        )
        heading.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # Main content
        body = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )
        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # Document list
        left = ctk.CTkFrame(
            body,
            width=280,
            fg_color="#101019"
        )
        left.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )
        left.pack_propagate(False)

        # Document details
        right = ctk.CTkFrame(
            body,
            fg_color="#101019"
        )
        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        search_box = ctk.CTkEntry(
            left,
            placeholder_text="Search knowledge...",
            height=38
        )
        search_box.pack(
            fill="x",
            padx=10,
            pady=10
        )

        document_list = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color="#444466",
            scrollbar_button_hover_color="#A970FF"
        )
        document_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )
        document_list.grid_columnconfigure(0,weight=1)

        title_label = ctk.CTkLabel(
            right,
            text="Select a document",
            font=("Arial", 17, "bold"),
            text_color="#A970FF",
            wraplength=480
        )
        title_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        source_label = ctk.CTkLabel(
            right,
            text="",
            font=("Arial", 11),
            text_color="#888899",
            wraplength=480
        )
        source_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        content_box = ctk.CTkTextbox(
            right,
            wrap="word",
            fg_color="#181824",
            text_color="#E8E8F0",
            activate_scrollbars=True
        )
        content_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )
        content_box.configure(state="disabled")

        selected = {"id": None}
        documents = []

        def show_document(document):
            selected["id"] = document["id"]

            title_label.configure(
                text=document["title"] or "Untitled"
            )

            source_label.configure(
                text=(
                    f"Source: {document['source'] or 'Unknown'}\n"
                    f"Tags: {document['tags'] or 'None'}"
                )
            )

            content_box.configure(state="normal")
            content_box.delete("1.0", "end")
            content_box.insert(
                "1.0",
                document["content"] or ""
            )
            content_box.configure(state="disabled")

        def refresh_documents():
            nonlocal documents

            documents = memory.get_all_knowledge()

            print("[KM] Documents returned:", len(documents), flush=True)

            query = search_box.get().strip().lower()

            # Clear the existing document buttons
            for widget in document_list.winfo_children():
                widget.destroy()

            filtered = []

            # Filter the documents
            for document in documents:
                title = str(document["title"] or "").lower()
                source = str(document["source"] or "").lower()
                tags = str(document["tags"] or "").lower()

                if query and not any(
                    query in field
                    for field in (title, source, tags)
                ):
                    continue

                filtered.append(document)

            print("[KM] Filtered documents:", len(filtered), flush=True)

            # Display the document buttons
            for row, document in enumerate(filtered):
                title = document["title"] or "Untitled"

                button = ctk.CTkButton(
                    document_list,
                    text=title,
                    anchor="w",
                    height=38,
                    fg_color="#181824",
                    hover_color="#292943",
                    text_color="#E8E8F0",
                    command=lambda item=document: show_document(item)
                )

                button.grid(
                    row=row,
                    column=0,
                    sticky="ew",
                    padx=3,
                    pady=2
                )

            if not filtered:
                ctk.CTkLabel(
                    document_list,
                    text="No documents found.",
                    text_color="#888899"
                ).pack(pady=15)
        def delete_selected():

            knowledge_id = selected["id"]

            if knowledge_id is None:
                messagebox.showinfo(
                    "Knowledge Manager",
                    "Select a document first.",
                    parent=window
                )
                return

            confirmed = messagebox.askyesno(
                "Delete Knowledge",
                "Delete this knowledge record permanently?",
                parent=window
            )

            if not confirmed:
                return

            memory.delete_knowledge(knowledge_id)
            memory.delete_knowledge_chunks(knowledge_id)

            selected["id"] = None

            title_label.configure(text="Select a document")
            source_label.configure(text="")

            content_box.configure(state="normal")
            content_box.delete("1.0", "end")
            content_box.configure(state="disabled")

            refresh_documents()

        search_box.bind(
            "<KeyRelease>",
            lambda event: refresh_documents()
        )

        delete_button = ctk.CTkButton(
            right,
            text="Delete Selected Document",
            height=38,
            fg_color="#8B2635",
            hover_color="#A83245",
            command=delete_selected
        )

        delete_button.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        refresh_documents()

    def open_project_manager(self):

        memory = self.brain.router.memory

        window = ctk.CTkToplevel(self.root)
        window.title("ELARA - Project Manager")
        window.geometry("850x550")
        window.minsize(650, 400)
        window.configure(fg_color="#0B0B12")

        heading = ctk.CTkLabel(
            window,
            text="Project Manager",
            font=("Arial", 22, "bold"),
            text_color="#A970FF"
        )
        heading.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        body = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )
        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # Project list
        left = ctk.CTkFrame(
            body,
            width=280,
            fg_color="#101019"
        )
        left.pack(
            side="left",
            fill="both",
            padx=(0, 12)
        )
        left.pack_propagate(False)

        # Project details
        right = ctk.CTkFrame(
            body,
            fg_color="#101019"
        )
        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        search_box = ctk.CTkEntry(
            left,
            placeholder_text="Search projects...",
            height=38
        )
        search_box.pack(
            fill="x",
            padx=10,
            pady=10
        )

        project_list = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent"
        )
        project_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )

        details = ctk.CTkTextbox(
            right,
            wrap="word",
            fg_color="#181824",
            text_color="#E8E8F0"
        )
        details.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
        details.configure(state="disabled")

        def show_project(project):

            project_id = project["id"]
            name = project["name"]

            state = memory.get_project_state(name)
            plan = memory.get_plan(project_id)
            notes = memory.find_notes(project_id)

            lines = [
                f"Project: {name}",
                "",
                f"Description: {project['description'] or 'None'}",
                f"Status: {project['status'] or 'Unknown'}",
                f"Priority: {project['priority'] or 'Unknown'}",
                "",
                "PROJECT STATE",
                "-------------"
            ]

            if state:

                lines.extend([
                    f"Vision: {state['vision'] or 'None'}",
                    f"Current phase: {state['current_phase'] or 'None'}",
                    f"Current module: {state['current_module'] or 'None'}",
                    f"Current goal: {state['current_goal'] or 'None'}",
                    f"Next goal: {state['next_goal'] or 'None'}",
                    f"Completion: {state['completion']}%"
                ])

            else:
                lines.append("No project state recorded.")

            lines.extend([
                "",
                "PROJECT PLAN",
                "------------"
            ])

            if plan:

                for step in plan:

                    lines.append(
                        f"{step['step_number']}. "
                        f"{step['title']} "
                        f"[{step['status']}]"
                    )

            else:
                lines.append("No plan recorded.")

            lines.extend([
                "",
                "PROJECT NOTES",
                "-------------"
            ])

            if notes:

                for index, note in enumerate(notes, start=1):

                    lines.append(
                        f"{index}. {note['note']}"
                    )

            else:
                lines.append("No notes recorded.")

            details.configure(state="normal")
            details.delete("1.0", "end")
            details.insert("1.0", "\n".join(lines))
            details.configure(state="disabled")

        def refresh_projects():

            projects = memory.get_all_projects()

            query = search_box.get().strip().lower()

            for widget in project_list.winfo_children():
                widget.destroy()

            filtered = []

            for project in projects:
                name = str(project["name"] or "").lower()
                description = str(
                    project["description"] or ""
                ).lower()

                if query and query not in name and query not in description:
                    continue

                filtered.append(project)

            for project in filtered:

                button = ctk.CTkButton(
                    project_list,
                    text=project["name"],
                    anchor="w",
                    height=38,
                    fg_color="transparent",
                    hover_color="#292943",
                    command=lambda item=project: show_project(item)
                )

                button.pack(
                    fill="x",
                    padx=3,
                    pady=2
                )

            if not filtered:

                ctk.CTkLabel(
                    project_list,
                    text="No projects found.",
                    text_color="#888899"
                ).pack(pady=15)

        search_box.bind(
            "<KeyRelease>",
            lambda event: refresh_projects()
        )

        refresh_projects()



# Start application

root = ctk.CTk()

app = Elara_GUI(root)

root.mainloop()
