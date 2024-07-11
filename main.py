import tkinter as tk
from trie import Trie
import webbrowser

# Load words from the file and insert them into the Trie
trie = Trie()
with open('american-english.txt', 'r') as file:
    words = file.read().splitlines()
    for word in words:
        trie.insert(word)

# Function to find similar words
def find_similar_words(word_fragment):
    return trie.search(word_fragment)

# Function to update suggestions in the listbox
def update_suggestions(event):
    word_fragment = entry.get()
    suggestions = find_similar_words(word_fragment)
    listbox.delete(0, tk.END)
    for suggestion in suggestions:
        listbox.insert(tk.END, suggestion)

# Function to replace entry text with selected suggestion
def on_listbox_select(event):
    if listbox.curselection():
        selected_word = listbox.get(listbox.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selected_word)

# Create the main window
root = tk.Tk()
root.title("Word Auto-complete")

# Add title label
title_label = tk.Label(root, text="Word Auto-complete", font=("Helvetica", 16))
title_label.pack(pady=10)

# Add GitHub link
def open_github(event):
    webbrowser.open_new("https://github.com/meta-syfu/Real-Time-Auto-Completion-word")

github_label = tk.Label(root, text="GitHub Repo", font=("Helvetica", 10), fg="blue", cursor="hand2")
github_label.pack(pady=5)
github_label.bind("<Button-1>", open_github)

# Frame for input and suggestion listbox
frame = tk.Frame(root)
frame.pack(pady=20)

# Input entry
entry = tk.Entry(frame, width=50)
entry.pack()
entry.bind('<KeyRelease>', update_suggestions)

# Suggestion listbox
listbox = tk.Listbox(frame, width=50, height=10)
listbox.pack(pady=20)
listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Run the application
root.mainloop()
