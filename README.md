# Real-Time-Auto-Completion-word


این پروژه یک برنامه پایتون برای پیشنهاد کلمات نزدیک به کلمه ناقص با استفاده از فایل کلمات `american-english.txt` است. این برنامه به صورت زمان واقعی (real-time) و با استفاده از ساختار داده‌ی `Trie`، کلمات مشابه را پیدا کرده و پیشنهاد می‌دهد. علاوه بر این، کاربر می‌تواند کلمات پیشنهادی را انتخاب کرده و با زدن دکمه Enter آن‌ها را در فیلد ورودی جایگزین کند.


### 1. تعریف ساختار داده‌ی Trie

ساختار داده‌ی `Trie` برای ذخیره و جستجوی کلمات بهینه است. ابتدا کلاس‌های `TrieNode` و `Trie` را تعریف می‌کنیم.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
```
این کلاس هر گره از Trie را نمایندگی می‌کند. `children` یک دیکشنری از گره‌های فرزند و `is_end_of_word` نشان می‌دهد که آیا این گره پایان یک کلمه است یا خیر.

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()
```
این کلاس شامل ریشه Trie و متدهایی برای درج و جستجوی کلمات است.

```python
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
```
این متد کلمات را در ساختار Trie درج می‌کند.

```python
    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._words_with_prefix(node, prefix)
```
این متد به دنبال کلماتی با پیشوند مشخص می‌گردد.

```python
    def _words_with_prefix(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._words_with_prefix(child_node, prefix + char))
        return words
```
این متد به طور بازگشتی کلماتی را که با پیشوند مشخص شده شروع می‌شوند، پیدا می‌کند.

### 2. بارگذاری کلمات در Trie

در فایل `main.py`، کلمات از فایل `american-english.txt` خوانده شده و در ساختار داده‌ی `Trie` درج می‌شوند.

```python
import tkinter as tk
from trie import Trie

# Load words from the file and insert them into the Trie
trie = Trie()
with open('american-english.txt', 'r') as file:
    words = file.read().splitlines()
    for word in words:
        trie.insert(word)
```
ابتدا کلمات از فایل `american-english.txt` خوانده می‌شوند. سپس با استفاده از حلقه، هر کلمه به ساختار داده‌ی `Trie` اضافه می‌شود.

### 3. جستجوی کلمات مشابه

تابع `find_similar_words` از ساختار داده‌ی `Trie` برای پیدا کردن کلمات مشابه استفاده می‌کند.

```python
# Function to find similar words
def find_similar_words(word_fragment):
    return trie.search(word_fragment)
```
این تابع یک پیشوند کلمه را به عنوان ورودی می‌گیرد و با استفاده از متد `search` از کلاس `Trie`، لیستی از کلمات مشابه را باز می‌گرداند.

### 4. بروزرسانی پیشنهادات

این تابع لیست باکس را با پیشنهادات جدید بروزرسانی می‌کند.

```python
# Function to update suggestions in the listbox
def update_suggestions(event):
    word_fragment = entry.get()
    suggestions = find_similar_words(word_fragment)
    listbox.delete(0, tk.END)
    for suggestion in suggestions:
        listbox.insert(tk.END, suggestion)
```
هر بار که کاربر کلیدی را در ورودی فشار می‌دهد، این تابع فراخوانی می‌شود. ابتدا متن ورودی گرفته شده و سپس با استفاده از `find_similar_words`، لیست کلمات مشابه پیدا می‌شود. سپس لیست باکس با پیشنهادات جدید بروزرسانی می‌شود.

### 5. انتخاب و جایگزینی کلمه

کاربر می‌تواند کلمه‌ی پیشنهادی را انتخاب کرده و با زدن دکمه Enter آن را در فیلد ورودی جایگزین کند.

```python
# Function to replace entry text with selected suggestion
def on_listbox_select(event):
    if listbox.curselection():
        selected_word = listbox.get(listbox.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selected_word)
```
این تابع زمانی فراخوانی می‌شود که کاربر کلمه‌ای را از لیست باکس انتخاب می‌کند. کلمه‌ی انتخاب شده در فیلد ورودی جایگزین می‌شود.

### 6. رابط کاربری

رابط کاربری با استفاده از `tkinter` ایجاد شده است.

```python
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
```
- **ایجاد پنجره اصلی**: یک پنجره‌ی اصلی با استفاده از `tkinter` ایجاد شده است.
- **اضافه کردن عنوان**: یک لیبل برای عنوان برنامه اضافه شده است.
- **اضافه کردن لینک گیت‌هاب**: یک لیبل برای لینک گیت‌هاب اضافه شده که با کلیک روی آن، لینک در کلیپ‌بورد کپی می‌شود.
- **ایجاد فریم برای ورودی و لیست باکس**: یک فریم برای جایگذاری ورودی و لیست باکس ایجاد شده است.
- **ورودی متن**: یک ورودی متن برای تایپ کلمه ناقص توسط کاربر ایجاد شده و با هر بار فشردن کلید، تابع `update_suggestions` فراخوانی می‌شود.
- **لیست باکس**: یک لیست باکس برای نمایش پیشنهادات ایجاد شده و با انتخاب کلمه، تابع `on_listbox_select` فراخوانی می‌شود.

## نتیجه‌گیری

این برنامه با استفاده از ساختار داده‌ی `Trie` و رابط کاربری `tkinter`، کلمات مشابه را به صورت زمان واقعی پیشنهاد می‌دهد و با انتخاب کلمه‌ی پیشنهادی توسط کاربر، آن را در فیلد ورودی جایگزین می‌کند. این راه‌حل بهینه و کارآمد است و رابط کاربری ساده و کاربر پسندی دارد.

برای اجرای برنامه، کافی است دستور زیر را در ترمینال اجرا کنید:

```bash
python main.py
```

