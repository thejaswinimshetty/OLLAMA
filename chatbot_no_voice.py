"""
Modern Desktop Chatbot with Ollama Integration
A ChatGPT-like interface built with Python Tkinter
Features: Document Upload (Voice features disabled for compatibility)
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, Canvas, filedialog
import requests
import json
import threading
from datetime import datetime
import os
import pickle
from pathlib import Path

# Document processing
import PyPDF2
import docx


class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Chat")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Conversation history for context
        self.conversation_history = []
        self.current_chat_id = None
        
        # Document context
        self.document_context = ""
        self.current_document = None
        
        # Chat storage
        self.chat_storage_dir = Path("chat_history")
        self.chat_storage_dir.mkdir(exist_ok=True)
        
        # Ollama configuration
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "llama3.2:latest"
        
        # Enhanced dark theme colors
        self.bg_color = "#0d1117"
        self.chat_bg = "#0d1117"
        self.sidebar_bg = "#161b22"
        self.user_bubble = "#238636"
        self.bot_bubble = "#21262d"
        self.text_color = "#c9d1d9"
        self.input_bg = "#0d1117"
        self.input_border = "#30363d"
        self.button_hover = "#2ea043"
        self.accent_color = "#58a6ff"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the enhanced user interface"""
        self.root.configure(bg=self.bg_color)
        
        # Main container with sidebar
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar for chat history
        self.sidebar = tk.Frame(main_container, bg=self.sidebar_bg, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        sidebar_header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            sidebar_header,
            text="💬 Chat History",
            font=("Segoe UI", 12, "bold"),
            bg=self.sidebar_bg,
            fg=self.text_color
        ).pack(anchor=tk.W)
        
        # New chat button
        new_chat_btn = tk.Button(
            sidebar_header,
            text="+ New Chat",
            font=("Segoe UI", 9, "bold"),
            bg=self.user_bubble,
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.new_chat
        )
        new_chat_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Chat history list with scrollbar
        history_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        history_scrollbar = tk.Scrollbar(history_frame, bg=self.sidebar_bg)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            bg=self.sidebar_bg,
            fg=self.text_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            selectbackground=self.user_bubble,
            selectforeground="#ffffff",
            yscrollcommand=history_scrollbar.set,
            activestyle='none'
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        self.history_listbox.bind('<<ListboxSelect>>', self.load_selected_chat)
        
        # Load chat history
        self.refresh_chat_history()
        
        # Main chat area
        chat_container_main = tk.Frame(main_container, bg=self.bg_color)
        chat_container_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header with gradient effect
        header_frame = tk.Frame(chat_container_main, bg=self.sidebar_bg, height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.sidebar_bg)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=self.sidebar_bg)
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="💬 Ollama AI Chat",
            font=("Segoe UI", 18, "bold"),
            bg=self.sidebar_bg,
            fg=self.accent_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        status_frame = tk.Frame(header_content, bg=self.sidebar_bg)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Label(
            status_frame,
            text="● Online",
            font=("Segoe UI", 10),
            bg=self.sidebar_bg,
            fg="#3fb950"
        )
        self.status_indicator.pack(side=tk.TOP, anchor=tk.E)
        
        model_label = tk.Label(
            status_frame,
            text=f"Model: {self.model_name.split(':')[0]}",
            font=("Segoe UI", 9),
            bg=self.sidebar_bg,
            fg="#8b949e"
        )
        model_label.pack(side=tk.TOP, anchor=tk.E)
        
        # Chat display area with custom canvas
        chat_container = tk.Frame(chat_container_main, bg=self.chat_bg)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))
        
        # Canvas for custom scrollbar
        self.chat_canvas = Canvas(
            chat_container,
            bg=self.chat_bg,
            highlightthickness=0
        )
        
        # Custom scrollbar
        scrollbar = tk.Scrollbar(
            chat_container,
            orient=tk.VERTICAL,
            command=self.chat_canvas.yview,
            bg=self.sidebar_bg,
            troughcolor=self.chat_bg,
            width=12,
            relief=tk.FLAT
        )
        
        self.chat_frame = tk.Frame(self.chat_canvas, bg=self.chat_bg)
        
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor=tk.NW, width=self.chat_canvas.winfo_reqwidth())
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind canvas resize
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.bind("<Configure>", lambda e: self.chat_canvas.itemconfig(self.chat_canvas.find_withtag("all")[0], width=e.width))
        
        # Input area with border
        input_container = tk.Frame(chat_container_main, bg=self.bg_color)
        input_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Input frame with border effect
        input_border = tk.Frame(input_container, bg=self.input_border, bd=0)
        input_border.pack(fill=tk.X)
        
        input_frame = tk.Frame(input_border, bg=self.input_bg)
        input_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Text input field with placeholder effect
        self.input_field = tk.Text(
            input_frame,
            height=3,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=15,
            pady=12,
            wrap=tk.WORD,
            insertbackground=self.accent_color
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_field.bind("<Return>", self.handle_enter_key)
        self.input_field.focus()
        
        # Button container
        button_frame = tk.Frame(input_frame, bg=self.input_bg)
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        # Upload document button
        self.upload_button = tk.Button(
            button_frame,
            text="📄",
            font=("Segoe UI", 12),
            bg=self.bot_bubble,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.upload_document
        )
        self.upload_button.pack(side=tk.LEFT, padx=(0, 8))
        self.upload_button.bind("<Enter>", lambda e: self.upload_button.config(bg=self.input_border))
        self.upload_button.bind("<Leave>", lambda e: self.upload_button.config(bg=self.bot_bubble))
        
        # Clear button
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️",
            font=("Segoe UI", 12),
            bg=self.bot_bubble,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.clear_chat
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 8))
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg=self.input_border))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg=self.bot_bubble))
        
        # Send button with hover effect
        self.send_button = tk.Button(
            button_frame,
            text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.user_bubble,
            fg="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.button_hover))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.user_bubble))
        
        # Welcome message
        self.display_bot_message("Hello! 👋 I'm your AI assistant powered by Ollama. How can I help you today?")
        
    def handle_enter_key(self, event):
        """Handle Enter key press (Shift+Enter for new line)"""
        if event.state & 0x1:  # Shift key is pressed
            return
        else:
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send user message and get bot response"""
        user_message = self.input_field.get("1.0", tk.END).strip()
        
        if not user_message:
            return
        
        # Clear input field
        self.input_field.delete("1.0", tk.END)
        
        # Display user message
        self.display_user_message(user_message)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Auto-save after user message
        self.save_current_chat()
        
        # Disable send button while processing
        self.send_button.config(state=tk.DISABLED, text="Thinking...")
        self.status_indicator.config(text="● Thinking...", fg="#f85149")
        
        # Get bot response in separate thread to avoid UI freezing
        thread = threading.Thread(target=self.get_bot_response, args=(user_message,))
        thread.daemon = True
        thread.start()
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def new_chat(self):
        """Start a new chat"""
        # Save current chat if it has messages
        if self.conversation_history:
            self.save_current_chat()
        
        # Clear current chat
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.conversation_history = []
        self.document_context = ""
        self.current_document = None
        self.current_chat_id = None
        
        # Refresh history list
        self.refresh_chat_history()
        
        self.display_bot_message("Hello! 👋 I'm your AI assistant powered by Ollama. How can I help you today?")
    
    def clear_chat(self):
        """Clear current chat without saving"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.conversation_history = []
        self.document_context = ""
        self.current_document = None
        self.current_chat_id = None
        self.display_bot_message("Chat cleared! How can I help you?")
    
    def save_current_chat(self):
        """Save current chat to storage"""
        if not self.conversation_history:
            return
        
        # Generate chat ID if new
        if not self.current_chat_id:
            self.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get first user message as title
        title = "New Chat"
        for msg in self.conversation_history:
            if msg["role"] == "user":
                title = msg["content"][:50]
                if len(msg["content"]) > 50:
                    title += "..."
                break
        
        # Save chat data
        chat_data = {
            "id": self.current_chat_id,
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "messages": self.conversation_history,
            "document_context": self.document_context,
            "document_name": self.current_document
        }
        
        file_path = self.chat_storage_dir / f"{self.current_chat_id}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(chat_data, f)
        
        self.refresh_chat_history()
    
    def refresh_chat_history(self):
        """Refresh the chat history list"""
        self.history_listbox.delete(0, tk.END)
        
        # Load all chat files
        chat_files = sorted(self.chat_storage_dir.glob("*.pkl"), reverse=True)
        
        for chat_file in chat_files:
            try:
                with open(chat_file, 'rb') as f:
                    chat_data = pickle.load(f)
                    
                # Format display
                timestamp = datetime.fromisoformat(chat_data["timestamp"])
                display_text = f"{timestamp.strftime('%m/%d %H:%M')} - {chat_data['title']}"
                
                self.history_listbox.insert(tk.END, display_text)
                self.history_listbox.itemconfig(tk.END, {'bg': self.sidebar_bg})
            except Exception as e:
                print(f"Error loading chat: {e}")
    
    def load_selected_chat(self, event):
        """Load selected chat from history"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
        
        # Save current chat first
        if self.conversation_history:
            self.save_current_chat()
        
        # Get selected chat file
        chat_files = sorted(self.chat_storage_dir.glob("*.pkl"), reverse=True)
        selected_index = selection[0]
        
        if selected_index >= len(chat_files):
            return
        
        chat_file = chat_files[selected_index]
        
        try:
            with open(chat_file, 'rb') as f:
                chat_data = pickle.load(f)
            
            # Clear current chat display
            for widget in self.chat_frame.winfo_children():
                widget.destroy()
            
            # Load chat data
            self.current_chat_id = chat_data["id"]
            self.conversation_history = chat_data["messages"]
            self.document_context = chat_data.get("document_context", "")
            self.current_document = chat_data.get("document_name", None)
            
            # Display all messages
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    self.display_user_message(msg["content"])
                else:
                    self.display_bot_message(msg["content"])
            
            # Show document info if loaded
            if self.current_document:
                self.display_bot_message(f"📄 Document loaded: {self.current_document}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load chat: {str(e)}")
    
    def upload_document(self):
        """Upload and process document (PDF, TXT, DOCX)"""
        file_path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[
                ("All Supported", "*.pdf *.txt *.docx"),
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("Word documents", "*.docx")
            ]
        )
        
        if not file_path:
            return
        
        try:
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Show processing message
            self.display_bot_message(f"📄 Processing document: {file_name}...")
            
            # Extract text based on file type
            if file_ext == '.pdf':
                text = self.extract_pdf_text(file_path)
            elif file_ext == '.txt':
                text = self.extract_txt_text(file_path)
            elif file_ext == '.docx':
                text = self.extract_docx_text(file_path)
            else:
                self.display_bot_message("❌ Unsupported file format!")
                return
            
            if text.strip():
                self.document_context = text
                self.current_document = file_name
                word_count = len(text.split())
                self.display_bot_message(
                    f"✅ Document loaded successfully!\n\n"
                    f"📄 File: {file_name}\n"
                    f"📊 Words: {word_count:,}\n\n"
                    f"You can now ask questions about this document!"
                )
            else:
                self.display_bot_message("❌ Could not extract text from the document!")
                
        except Exception as e:
            self.display_bot_message(f"❌ Error processing document: {str(e)}")
    
    def extract_pdf_text(self, file_path):
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def extract_txt_text(self, file_path):
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def extract_docx_text(self, file_path):
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def display_user_message(self, message):
        """Display user message in chat with modern bubble design"""
        # Message container
        msg_container = tk.Frame(self.chat_frame, bg=self.chat_bg)
        msg_container.pack(fill=tk.X, pady=8, padx=10)
        
        # Right align for user messages
        bubble_frame = tk.Frame(msg_container, bg=self.chat_bg)
        bubble_frame.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Timestamp and label
        header_frame = tk.Frame(bubble_frame, bg=self.chat_bg)
        header_frame.pack(anchor=tk.E, pady=(0, 4))
        
        timestamp = datetime.now().strftime("%H:%M")
        tk.Label(
            header_frame,
            text=f"You • {timestamp}",
            font=("Segoe UI", 9),
            bg=self.chat_bg,
            fg="#8b949e"
        ).pack(side=tk.RIGHT)
        
        # Message bubble
        bubble = tk.Frame(bubble_frame, bg=self.user_bubble, bd=0)
        bubble.pack(anchor=tk.E)
        
        msg_label = tk.Label(
            bubble,
            text=message,
            font=("Segoe UI", 11),
            bg=self.user_bubble,
            fg="#ffffff",
            wraplength=500,
            justify=tk.LEFT,
            padx=16,
            pady=12
        )
        msg_label.pack()
        
        self.scroll_to_bottom()
    
    def display_bot_message(self, message):
        """Display bot message in chat with modern bubble design"""
        # Message container
        msg_container = tk.Frame(self.chat_frame, bg=self.chat_bg)
        msg_container.pack(fill=tk.X, pady=8, padx=10)
        
        # Left align for bot messages
        bubble_frame = tk.Frame(msg_container, bg=self.chat_bg)
        bubble_frame.pack(side=tk.LEFT, anchor=tk.W)
        
        # Timestamp and label
        header_frame = tk.Frame(bubble_frame, bg=self.chat_bg)
        header_frame.pack(anchor=tk.W, pady=(0, 4))
        
        timestamp = datetime.now().strftime("%H:%M")
        tk.Label(
            header_frame,
            text=f"🤖 AI Assistant • {timestamp}",
            font=("Segoe UI", 9),
            bg=self.chat_bg,
            fg="#8b949e"
        ).pack(side=tk.LEFT)
        
        # Message bubble
        bubble = tk.Frame(bubble_frame, bg=self.bot_bubble, bd=0)
        bubble.pack(anchor=tk.W)
        
        msg_label = tk.Label(
            bubble,
            text=message,
            font=("Segoe UI", 11),
            bg=self.bot_bubble,
            fg=self.text_color,
            wraplength=500,
            justify=tk.LEFT,
            padx=16,
            pady=12
        )
        msg_label.pack()
        
        self.scroll_to_bottom()
    
    def stream_bot_message(self, message_generator):
        """Display bot message with streaming effect"""
        # Message container
        msg_container = tk.Frame(self.chat_frame, bg=self.chat_bg)
        msg_container.pack(fill=tk.X, pady=8, padx=10)
        
        # Left align for bot messages
        bubble_frame = tk.Frame(msg_container, bg=self.chat_bg)
        bubble_frame.pack(side=tk.LEFT, anchor=tk.W)
        
        # Timestamp and label
        header_frame = tk.Frame(bubble_frame, bg=self.chat_bg)
        header_frame.pack(anchor=tk.W, pady=(0, 4))
        
        timestamp = datetime.now().strftime("%H:%M")
        tk.Label(
            header_frame,
            text=f"🤖 AI Assistant • {timestamp}",
            font=("Segoe UI", 9),
            bg=self.chat_bg,
            fg="#8b949e"
        ).pack(side=tk.LEFT)
        
        # Message bubble
        bubble = tk.Frame(bubble_frame, bg=self.bot_bubble, bd=0)
        bubble.pack(anchor=tk.W)
        
        # Streaming text label
        msg_label = tk.Label(
            bubble,
            text="",
            font=("Segoe UI", 11),
            bg=self.bot_bubble,
            fg=self.text_color,
            wraplength=500,
            justify=tk.LEFT,
            padx=16,
            pady=12
        )
        msg_label.pack()
        
        full_response = ""
        try:
            for chunk in message_generator:
                if chunk:
                    full_response += chunk
                    msg_label.config(text=full_response)
                    self.scroll_to_bottom()
                    self.root.update_idletasks()
        except Exception as e:
            error_msg = f"\n[Error: {str(e)}]"
            msg_label.config(text=full_response + error_msg)
        
        return full_response
    
    def get_bot_response(self, user_message):
        """Get response from Ollama API with streaming"""
        try:
            # Prepare the prompt with document context if available
            if self.document_context:
                prompt = f"""You have access to the following document content:

--- DOCUMENT START ---
{self.document_context[:4000]}
--- DOCUMENT END ---

User question: {user_message}

Please answer based on the document content above."""
            else:
                prompt = user_message
            
            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True
            }
            
            # Make streaming request to Ollama
            response = requests.post(
                self.ollama_url,
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                # Generator for streaming response
                def response_generator():
                    for line in response.iter_lines():
                        if line:
                            try:
                                json_response = json.loads(line)
                                if "response" in json_response:
                                    yield json_response["response"]
                            except json.JSONDecodeError:
                                continue
                
                # Stream the response
                full_response = self.stream_bot_message(response_generator())
                
                # Add to conversation history
                self.conversation_history.append({"role": "assistant", "content": full_response})
                
                # Auto-save after bot response
                self.save_current_chat()
                
            else:
                error_message = f"Error: Ollama API returned status code {response.status_code}"
                self.root.after(0, self.display_bot_message, error_message)
                
        except requests.exceptions.ConnectionError:
            error_message = "❌ Cannot connect to Ollama. Please make sure Ollama is running.\n\nStart Ollama with: ollama serve"
            self.root.after(0, self.display_bot_message, error_message)
        except requests.exceptions.Timeout:
            error_message = "⏱️ Request timed out. The model might be taking too long to respond."
            self.root.after(0, self.display_bot_message, error_message)
        except Exception as e:
            error_message = f"❌ An error occurred: {str(e)}"
            self.root.after(0, self.display_bot_message, error_message)
        finally:
            # Re-enable send button
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="Send ➤"))
            self.root.after(0, lambda: self.status_indicator.config(text="● Online", fg="#3fb950"))


def main():
    """Main function to run the chatbot application"""
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
