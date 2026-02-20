"""
Modern Desktop Chatbot with Ollama Integration
A ChatGPT-like interface built with Python Tkinter
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, Canvas
import requests
import json
import threading
from datetime import datetime


class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Chat")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Conversation history for context
        self.conversation_history = []
        
        # Ollama configuration
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "llama3.2:latest"  # Full model name with tag
        
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
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_container, bg=self.sidebar_bg, height=70)
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
        chat_container = tk.Frame(main_container, bg=self.chat_bg)
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
        input_container = tk.Frame(main_container, bg=self.bg_color)
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
    
    def clear_chat(self):
        """Clear chat history"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.conversation_history = []
        self.display_bot_message("Chat cleared! How can I help you?")
    
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
            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "prompt": user_message,
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
