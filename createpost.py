import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import subprocess

class BlogPostCreator:
    def __init__(self, root):
        self.root = root
        root.title("Blog Post Creator")
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(main_frame, text="Post Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Categories
        ttk.Label(main_frame, text="Categories:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.categories_entry = ttk.Entry(main_frame, width=50)
        self.categories_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Tags
        ttk.Label(main_frame, text="Tags:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.tags_entry = ttk.Entry(main_frame, width=50)
        self.tags_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Content
        ttk.Label(main_frame, text="Content:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.content_text = tk.Text(main_frame, width=60, height=20)
        self.content_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        # Create button
        create_button = ttk.Button(main_frame, text="Create Post", command=self.create_post)
        create_button.grid(row=4, column=1, pady=20)

    def git_sync(self, title):
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', f'New Post - {title}'], check=True)
            subprocess.run(['git', 'push'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("Git Error", f"Failed to sync with GitHub: {str(e)}")
            return False

    def process_content(self, content):
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if (stripped and 
                not stripped.startswith(('#', '*', '-')) and 
                not stripped[0].isdigit()):
                processed_lines.append(line + " <br>")
            else:
                processed_lines.append(line)
                
        return '\n'.join(processed_lines)

    def create_post(self):
        title = self.title_entry.get().strip()
        if not title:
            tk.messagebox.showwarning("Warning", "Please enter a title")
            return
            
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%Y-%m-%d %H:%M:%S +0800")
        
        filename = f"{date_str}-{title.lower().replace(' ', '-')}.md"
        filepath = os.path.join('_posts', filename)
        
        categories = [cat.strip() for cat in self.categories_entry.get().split(',') if cat.strip()]
        tags = [tag.strip() for tag in self.tags_entry.get().split(',') if tag.strip()]
        
        content = self.content_text.get('1.0', 'end-1c')
        processed_content = self.process_content(content)
        
        post_content = f"""---
layout: post
title: "{title}"
date: {time_str}
categories: [{', '.join(categories)}]
tags: [{', '.join(tags)}]
---

{processed_content}"""
        
        os.makedirs('_posts', exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(post_content)
            
        if self.git_sync(title):
            self.title_entry.delete(0, 'end')
            self.categories_entry.delete(0, 'end')
            self.tags_entry.delete(0, 'end')
            self.content_text.delete('1.0', 'end')
            tk.messagebox.showinfo("Success", f"Post created and synced: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogPostCreator(root)
    root.mainloop()