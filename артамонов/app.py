# ============================================================
# app.py — Современное GUI-приложение с динамическим CRUD
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import database as db
from config import *
import random

# ==================== СТИЛИ ====================
def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")
    
    # Основные цвета
    bg_color = "#0F172A"
    surface_color = "#1E293B"
    primary_color = "#3B82F6"
    primary_hover = "#2563EB"
    accent_color = "#8B5CF6"
    text_color = "#F1F5F9"
    text_secondary = "#94A3B8"
    success_color = "#10B981"
    error_color = "#EF4444"
    border_color = "#334155"
    
    style.configure("TFrame", background=bg_color)
    style.configure("Card.TFrame", background=surface_color, relief="flat", borderwidth=0)
    style.configure("TLabel", background=bg_color, foreground=text_color, font=FONTS["body"])
    style.configure("Card.TLabel", background=surface_color, foreground=text_color)
    style.configure("Title.TLabel", font=FONTS["title"], foreground=primary_color)
    style.configure("Heading.TLabel", font=FONTS["heading"], foreground=text_color)
    style.configure("Error.TLabel", foreground=error_color)
    style.configure("Success.TLabel", foreground=success_color)
    
    style.configure("Primary.TButton", font=FONTS["button"], foreground="white", 
                   background=primary_color, borderwidth=0, focuscolor="none")
    style.map("Primary.TButton", background=[("active", primary_hover)])
    
    style.configure("Danger.TButton", font=FONTS["button"], foreground="white",
                   background=error_color, borderwidth=0)
    style.map("Danger.TButton", background=[("active", "#DC2626")])
    
    style.configure("Success.TButton", font=FONTS["button"], foreground="white",
                   background=success_color, borderwidth=0)
    style.map("Success.TButton", background=[("active", "#059669")])
    
    style.configure("Accent.TButton", font=FONTS["button"], foreground="white",
                   background=accent_color, borderwidth=0)
    style.map("Accent.TButton", background=[("active", "#7C3AED")])
    
    style.configure("TEntry", font=FONTS["body"], fieldbackground=surface_color,
                   foreground=text_color, bordercolor=border_color, lightcolor=border_color,
                   darkcolor=border_color, focuscolor=primary_color)
    
    style.configure("Treeview", font=FONTS["body"], rowheight=32,
                   background=surface_color, foreground=text_color,
                   fieldbackground=surface_color, bordercolor=border_color)
    style.map("Treeview", background=[("selected", primary_color)])
    
    style.configure("Treeview.Heading", font=FONTS["button"], background=primary_color,
                   foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[("active", primary_hover)])
    
    style.configure("TNotebook", background=bg_color, borderwidth=0)
    style.configure("TNotebook.Tab", font=FONTS["body"], padding=[15, 8],
                   background=surface_color, foreground=text_secondary)
    style.map("TNotebook.Tab", background=[("selected", primary_color)],
              foreground=[("selected", "white")])
    
    style.configure("Vertical.TScrollbar", background=surface_color, troughcolor=bg_color,
                   bordercolor=border_color, arrowcolor=text_secondary)

# ==================== ЭКРАН АВТОРИЗАЦИИ ====================
class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.fail_count = 0
        self._build()

    def _build(self):
        # Создаем фрейм-контейнер с центрированием
        container = tk.Frame(self, bg=COLORS["bg"])
        container.pack(expand=True, fill="both")
        
        # Центральная карточка
        card = tk.Frame(container, bg="#FFFFFF", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=520)
        
        # Контент карточки
        content = tk.Frame(card, bg="#FFFFFF")
        content.pack(fill="both", expand=True, padx=35, pady=30)
        
        # Логотип
        icon_label = tk.Label(content, text="🏭", font=("Segoe UI", 40),
                             bg="#FFFFFF", fg=COLORS["primary"])
        icon_label.pack(pady=(0, 5))
        
        tk.Label(content, text=APP_TITLE, font=("Segoe UI", 16, "bold"),
                bg="#FFFFFF", fg=COLORS["primary"]).pack()
        tk.Label(content, text=COMPANY_NAME, font=("Segoe UI", 9),
                bg="#FFFFFF", fg="#666666").pack(pady=(3, 20))
        
        # Поле логина
        login_frame = tk.Frame(content, bg="#FFFFFF")
        login_frame.pack(fill="x", pady=5)
        
        tk.Label(login_frame, text="Логин", font=("Segoe UI", 9),
                bg="#FFFFFF", fg="#333333").pack(anchor="w")
        
        self.login_entry = tk.Entry(login_frame, font=("Segoe UI", 10),
                                   bg="#F5F5F5", fg="#333333",
                                   insertbackground=COLORS["primary"],
                                   bd=1, relief="solid", highlightthickness=0)
        self.login_entry.pack(fill="x", pady=(3, 0), ipady=8)
        
        # Поле пароля
        pass_frame = tk.Frame(content, bg="#FFFFFF")
        pass_frame.pack(fill="x", pady=5)
        
        tk.Label(pass_frame, text="Пароль", font=("Segoe UI", 9),
                bg="#FFFFFF", fg="#333333").pack(anchor="w")
        
        self.pass_entry = tk.Entry(pass_frame, font=("Segoe UI", 10),
                                   bg="#F5F5F5", fg="#333333",
                                   insertbackground=COLORS["primary"],
                                   bd=1, relief="solid", show="●")
        self.pass_entry.pack(fill="x", pady=(3, 0), ipady=8)
        
        self.msg_label = tk.Label(content, text="", font=("Segoe UI", 9),
                                  bg="#FFFFFF", wraplength=310, fg=COLORS["error"])
        self.msg_label.pack(pady=10)
        
        # Кнопка входа (внизу по центру)
        button_container = tk.Frame(content, bg="#FFFFFF")
        button_container.pack(fill="x", pady=(10, 0))
        
        login_btn = tk.Button(button_container, text="Войти в систему", 
                              font=("Segoe UI", 11, "bold"),
                              bg=COLORS["primary"], fg="white", 
                              bd=0, cursor="hand2", 
                              activebackground=COLORS["primary_light"],
                              activeforeground="white",
                              relief="flat", highlightthickness=0,
                              command=self._login)
        login_btn.pack(expand=True, ipadx=30, ipady=10)
        
        # Эффект наведения
        def on_enter(e):
            login_btn.config(bg=COLORS["primary_light"])
        def on_leave(e):
            login_btn.config(bg=COLORS["primary"])
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        # Обработка изменения размера окна
        def on_resize(event):
            card.place(relx=0.5, rely=0.5, anchor="center")
        
        self.bind("<Configure>", on_resize)
        
        self.login_entry.focus_set()
        self.login_entry.bind("<Return>", lambda e: self.pass_entry.focus_set())
        self.pass_entry.bind("<Return>", lambda e: self._login())

    def _login(self):
        login = self.login_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not login or not password:
            self._show_msg(MSG_FIELDS_EMPTY, "error")
            return
        
        user, err = db.check_login(login, password)
        
        if err == "blocked":
            self._show_msg(MSG_AUTH_BLOCKED, "error")
        elif err:
            self.fail_count += 1
            if self.fail_count >= MAX_FAILED_ATTEMPTS:
                self._show_msg(MSG_AUTH_BLOCKED, "error")
            else:
                remaining = MAX_FAILED_ATTEMPTS - self.fail_count
                self._show_msg(f"{MSG_AUTH_ERROR}\nОсталось попыток: {remaining}", "error")
        else:
            self._show_msg(MSG_AUTH_SUCCESS, "success")
            self.after(500, lambda: self.app.show_main(user))

    def _show_msg(self, text, kind="error"):
        color = COLORS["error"] if kind == "error" else COLORS["success"]
        self.msg_label.config(text=text, fg=color)

# ==================== АДМИН-ПАНЕЛЬ ====================
class AdminPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._build()
        self.refresh()

    def _build(self):
        # Заголовок
        header = tk.Frame(self, bg=COLORS["surface"], height=60)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        tk.Label(header, text="👥 Управление доступом", font=FONTS["heading"],
                bg=COLORS["surface"], fg=COLORS["text"]).pack(side="left", padx=20)
        tk.Label(header, text="Управление пользователями и группами", font=FONTS["small"],
                bg=COLORS["surface"], fg=COLORS["text_sec"]).pack(side="left", padx=10)
        
        # Основной контейнер
        main_container = tk.Frame(self, bg=COLORS["bg"])
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Двухпанельный макет
        left_panel = tk.Frame(main_container, bg=COLORS["surface"])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_panel = tk.Frame(main_container, bg=COLORS["surface"])
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # ========== ЛЕВАЯ ПАНЕЛЬ - ПОЛЬЗОВАТЕЛИ ==========
        left_inner = tk.Frame(left_panel, bg=COLORS["surface"])
        left_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(left_inner, text="👤 Пользователи системы", font=FONTS["heading"],
                bg=COLORS["surface"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 15))
        
        # Таблица пользователей
        cols = ("ID", "Логин", "Роль", "Заблокирован")
        self.tree = ttk.Treeview(left_inner, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100 if c != "Логин" else 150)
        self.tree.pack(fill="both", expand=True, pady=(0, 15))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        # Форма редактирования
        form_frame = tk.LabelFrame(left_inner, text="Редактирование пользователя",
                                   font=FONTS["body"], bg=COLORS["bg"],
                                   fg=COLORS["text_sec"], padx=15, pady=10)
        form_frame.pack(fill="x")
        
        # Поля ввода в сетке
        row1 = tk.Frame(form_frame, bg=COLORS["bg"])
        row1.pack(fill="x", pady=5)
        tk.Label(row1, text="Логин:", width=12, anchor="w", 
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        self.e_login = tk.Entry(row1, font=FONTS["body"], bg=COLORS["surface"],
                                fg=COLORS["text"], insertbackground=COLORS["primary"])
        self.e_login.pack(side="left", fill="x", expand=True, padx=5)
        
        row2 = tk.Frame(form_frame, bg=COLORS["bg"])
        row2.pack(fill="x", pady=5)
        tk.Label(row2, text="Пароль:", width=12, anchor="w",
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        self.e_pass = tk.Entry(row2, font=FONTS["body"], bg=COLORS["surface"],
                               fg=COLORS["text"], insertbackground=COLORS["primary"], show="●")
        self.e_pass.pack(side="left", fill="x", expand=True, padx=5)
        
        row3 = tk.Frame(form_frame, bg=COLORS["bg"])
        row3.pack(fill="x", pady=5)
        tk.Label(row3, text="Группа:", width=12, anchor="w",
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        self.e_role = ttk.Combobox(row3, state="readonly", width=18, font=FONTS["body"])
        self.e_role.pack(side="left", fill="x", expand=True, padx=5)
        
        # Кнопки действий
        btn_frame = tk.Frame(form_frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="➕ Добавить", font=FONTS["small"],
                 bg=COLORS["success"], fg="white", bd=0, cursor="hand2",
                 command=self._add_user).pack(side="left", padx=4, ipadx=8, ipady=4)
        tk.Button(btn_frame, text="💾 Сохранить", font=FONTS["small"],
                 bg=COLORS["primary"], fg="white", bd=0, cursor="hand2",
                 command=self._save_user).pack(side="left", padx=4, ipadx=8, ipady=4)
        tk.Button(btn_frame, text="🔓 Разблокировать", font=FONTS["small"],
                 bg=COLORS["accent"], fg="white", bd=0, cursor="hand2",
                 command=self._unblock_user).pack(side="left", padx=4, ipadx=8, ipady=4)
        
        self.msg = tk.Label(form_frame, text="", font=FONTS["small"], bg=COLORS["bg"])
        self.msg.pack(pady=5)
        
        # ========== ПРАВАЯ ПАНЕЛЬ - ГРУППЫ ==========
        right_inner = tk.Frame(right_panel, bg=COLORS["surface"])
        right_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(right_inner, text="👥 Группы пользователей", font=FONTS["heading"],
                bg=COLORS["surface"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 15))
        
        # Список групп
        self.group_list = tk.Listbox(right_inner, font=FONTS["body"],
                                     bg=COLORS["bg"], fg=COLORS["text"],
                                     selectbackground=COLORS["primary"],
                                     bd=0, highlightthickness=1,
                                     highlightcolor=COLORS["primary"],
                                     relief="solid")
        self.group_list.pack(fill="both", expand=True, pady=(0, 15))
        
        # Форма управления группами
        group_frame = tk.LabelFrame(right_inner, text="Управление группами",
                                    font=FONTS["body"], bg=COLORS["bg"],
                                    fg=COLORS["text_sec"], padx=15, pady=10)
        group_frame.pack(fill="x")
        
        self.e_group = tk.Entry(group_frame, font=FONTS["body"], bg=COLORS["surface"],
                                fg=COLORS["text"], insertbackground=COLORS["primary"])
        self.e_group.pack(fill="x", pady=5)
        
        group_btns = tk.Frame(group_frame, bg=COLORS["bg"])
        group_btns.pack(fill="x", pady=5)
        
        tk.Button(group_btns, text="➕ Создать группу", font=FONTS["small"],
                 bg=COLORS["success"], fg="white", bd=0, cursor="hand2",
                 command=self._add_group).pack(side="left", padx=4, ipadx=8, ipady=4)
        tk.Button(group_btns, text="❌ Удалить группу", font=FONTS["small"],
                 bg=COLORS["error"], fg="white", bd=0, cursor="hand2",
                 command=self._delete_group).pack(side="left", padx=4, ipadx=8, ipady=4)
        
        self.sel_id = None

    def refresh(self):
        # Обновление таблицы пользователей
        for row in self.tree.get_children():
            self.tree.delete(row)
        for u in db.get_all_users():
            bl = "Да" if u["is_blocked"] else "Нет"
            tag = "blocked" if u["is_blocked"] else ""
            self.tree.insert("", "end", values=(u["id"], u["login"], u["role"], bl), tags=(tag,))
        self.tree.tag_configure("blocked", background=COLORS["blocked"])
        
        # Обновление списка групп
        self.group_list.delete(0, "end")
        groups = db.get_user_groups()
        for g in groups:
            self.group_list.insert("end", g)
        self.e_role.config(values=groups)
        if groups:
            self.e_role.set(groups[0])

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.sel_id = vals[0]
        self.e_login.delete(0, "end")
        self.e_login.insert(0, vals[1])
        self.e_role.set(vals[2])
        self.e_pass.delete(0, "end")

    def _add_user(self):
        login = self.e_login.get().strip()
        pwd = self.e_pass.get().strip()
        role = self.e_role.get()
        if not login or not pwd:
            self.msg.config(text=MSG_FIELDS_EMPTY, fg=COLORS["error"])
            return
        ok, err = db.add_user(login, pwd, role)
        if not ok:
            self.msg.config(text="Логин уже занят!", fg=COLORS["error"])
        else:
            self.msg.config(text="Пользователь успешно создан!", fg=COLORS["success"])
            self.refresh()

    def _save_user(self):
        if not self.sel_id:
            self.msg.config(text="Выберите пользователя для редактирования", fg=COLORS["error"])
            return
        login = self.e_login.get().strip()
        pwd = self.e_pass.get().strip() or None
        role = self.e_role.get()
        db.update_user(int(self.sel_id), login=login, password=pwd, role=role)
        self.msg.config(text="Данные пользователя сохранены", fg=COLORS["success"])
        self.refresh()

    def _unblock_user(self):
        if not self.sel_id:
            self.msg.config(text="Выберите пользователя для разблокировки", fg=COLORS["error"])
            return
        db.update_user(int(self.sel_id), is_blocked=0)
        self.msg.config(text="Аккаунт успешно разблокирован", fg=COLORS["success"])
        self.refresh()

    def _add_group(self):
        name = self.e_group.get().strip()
        if not name:
            return
        ok, err = db.add_user_group(name)
        if ok:
            self.e_group.delete(0, "end")
            self.refresh()
        else:
            messagebox.showerror("Ошибка", f"Не удалось создать группу:\n{err}")

    def _delete_group(self):
        sel = self.group_list.curselection()
        if not sel:
            return
        name = self.group_list.get(sel[0])
        if name in ["Администратор", "Пользователь"]:
            messagebox.showwarning("Внимание", "Нельзя удалить стандартные системные группы!")
            return
        if messagebox.askyesno("Подтверждение", f"Удалить группу '{name}'?"):
            ok, err = db.delete_user_group(name)
            if ok:
                self.refresh()
            else:
                messagebox.showerror("Ошибка", f"Не удалось удалить группу:\n{err}")

# ==================== ДИНАМИЧЕСКИЙ РЕДАКТОР СТРОК ====================
class DynamicRowEditor(tk.Toplevel):
    def __init__(self, parent, table_name, row_data=None, on_save=None):
        super().__init__(parent)
        self.table_name = table_name
        self.row_data = row_data
        self.on_save = on_save
        self.title("Редактирование записи" if row_data else "Новая запись")
        self.geometry("600x700")  # Немного шире
        self.configure(bg=COLORS["bg"])
        self.transient(parent)
        self.grab_set()
        
        self.pk_col = db.get_primary_key(table_name)
        self.cols_info = db.get_table_columns_info(table_name)
        self.entries = {}
        self._build()
        
        # Центрирование окна
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # Заголовок
        header = tk.Frame(self, bg=COLORS["primary"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        icon = "✏️" if self.row_data else "➕"
        title_text = f"{icon} {('Изменить' if self.row_data else 'Создать')} запись"
        tk.Label(header, text=title_text, font=FONTS["heading"],
                bg=COLORS["primary"], fg="white").pack(side="left", padx=20, pady=20)
        tk.Label(header, text=self.table_name, font=FONTS["small"],
                bg=COLORS["primary"], fg=COLORS["selected"]).pack(side="left", pady=22)
        
        # ===== КНОПКИ ВВЕРХУ (гарантированно видны) =====
        btn_top_frame = tk.Frame(self, bg=COLORS["bg"], height=60)
        btn_top_frame.pack(fill="x", side="top", pady=(10, 0))
        btn_top_frame.pack_propagate(False)
        
        btn_inner = tk.Frame(btn_top_frame, bg=COLORS["bg"])
        btn_inner.pack(fill="x", padx=20, pady=12)
        
        # Кнопка Отмена
        cancel_btn = tk.Button(btn_inner, text="❌ Отмена", font=FONTS["button"],
                               bg=COLORS["error"], fg="white", bd=0, cursor="hand2",
                               command=self.destroy)
        cancel_btn.pack(side="left", padx=5, ipadx=20, ipady=8)
        
        # Динамическая кнопка сохранения
        save_text = "➕ Добавить" if not self.row_data else "💾 Сохранить"
        save_btn = tk.Button(btn_inner, text=save_text, font=FONTS["button"],
                             bg=COLORS["success"], fg="white", bd=0, cursor="hand2",
                             command=self._save)
        save_btn.pack(side="right", padx=5, ipadx=20, ipady=8)
        
        # Эффекты наведения
        def on_enter(btn, color):
            btn.config(bg=color)
        
        cancel_btn.bind("<Enter>", lambda e: on_enter(cancel_btn, "#DC2626"))
        cancel_btn.bind("<Leave>", lambda e: on_enter(cancel_btn, COLORS["error"]))
        save_btn.bind("<Enter>", lambda e: on_enter(save_btn, "#059669"))
        save_btn.bind("<Leave>", lambda e: on_enter(save_btn, COLORS["success"]))
        
        # ===== ОСНОВНОЙ КОНТЕЙНЕР С ПОЛЯМИ (со скроллом) =====
        main_container = tk.Frame(self, bg=COLORS["bg"])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_container, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Поля ввода
        for i, col in enumerate(self.cols_info):
            cname = col["name"]
            ctype = col["type"]
            is_pk = col["pk"] > 0
            
            # Пропускаем автоинкрементный PRIMARY KEY при создании
            if is_pk and not self.row_data:
                continue
            
            # Карточка поля
            field_frame = tk.Frame(scrollable_frame, bg=COLORS["surface"],
                                   bd=1, relief="solid", highlightthickness=0)
            field_frame.pack(fill="x", pady=6, padx=10)
            
            inner = tk.Frame(field_frame, bg=COLORS["surface"])
            inner.pack(fill="x", padx=15, pady=10)
            
            # Подпись поля
            lbl_text = cname
            if col["notnull"] and not is_pk:
                lbl_text += " *"
            
            tk.Label(inner, text=lbl_text, font=FONTS["small"],
                    bg=COLORS["surface"], fg=COLORS["text_sec"]).pack(anchor="w")
            
            # Поле ввода
            entry = tk.Entry(inner, font=FONTS["body"], bg=COLORS["bg"],
                            fg=COLORS["text"], insertbackground=COLORS["primary"],
                            bd=1, relief="solid", highlightthickness=0)
            entry.pack(fill="x", pady=(4, 0), ipady=8)  # Увеличен ipady для удобства
            
            # Заполнение данными
            if is_pk and self.row_data:
                entry.insert(0, str(self.row_data.get(cname, "")))
                entry.config(state="readonly", readonlybackground=COLORS["bg"])
            elif self.row_data:
                val = self.row_data.get(cname)
                entry.insert(0, str(val) if val is not None else "")
            
            self.entries[cname] = entry
        
        # Если нет полей для ввода
        if not self.entries:
            tk.Label(scrollable_frame, text="Нет доступных полей для редактирования",
                    font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["error"]).pack(pady=40)

    def _save(self):
        data = {}
        for cname, entry in self.entries.items():
            if str(entry.cget("state")) != "readonly":
                val = entry.get().strip()
                
                # Проверка обязательных полей
                col_info = [c for c in self.cols_info if c["name"] == cname][0]
                if val == "" and col_info["notnull"] and col_info["pk"] == 0:
                    messagebox.showerror("Ошибка", f"Поле '{cname}' обязательно для заполнения!")
                    return
                
                # Преобразование типов
                col_type = col_info["type"].upper()
                if val != "":
                    if "INT" in col_type:
                        try:
                            val = int(val)
                        except ValueError:
                            messagebox.showerror("Ошибка", f"Поле '{cname}' должно быть целым числом!")
                            return
                    elif any(t in col_type for t in ["REAL", "FLOAT", "DOUBLE"]):
                        try:
                            val = float(val)
                        except ValueError:
                            messagebox.showerror("Ошибка", f"Поле '{cname}' должно быть числом!")
                            return
                else:
                    val = None
                
                data[cname] = val
        
        # Сохранение
        if self.row_data:
            pk_val = self.row_data[self.pk_col]
            ok, err = db.update_row(self.table_name, self.pk_col, pk_val, data)
        else:
            ok, err = db.insert_row(self.table_name, data)
        
        if ok:
            if self.on_save:
                self.on_save()
            self.destroy()
        else:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить запись:\n{err}")

# ==================== ПРОСМОТРЩИК ТАБЛИЦ ====================
class DataViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        # Верхняя панель
        top_bar = tk.Frame(self, bg=COLORS["surface"], height=60)
        top_bar.pack(fill="x", padx=20, pady=(20, 15))
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="📊 Просмотр данных", font=FONTS["heading"],
                bg=COLORS["surface"], fg=COLORS["text"]).pack(side="left", padx=20)
        
        # Панель выбора таблицы
        select_frame = tk.Frame(self, bg=COLORS["surface"], height=50)
        select_frame.pack(fill="x", pady=(0, 15))
        select_frame.pack_propagate(False)
        
        inner = tk.Frame(select_frame, bg=COLORS["surface"])
        inner.pack(expand=True, padx=20)
        
        tk.Label(inner, text="Выберите таблицу:", font=FONTS["body"],
                bg=COLORS["surface"], fg=COLORS["text"]).pack(side="left")
        
        self.tables = [t for t in db.get_table_names() 
                      if t not in (TABLE_USERS, "sqlite_sequence", "ГруппыПользователей")]
        self.combo = ttk.Combobox(inner, values=self.tables, state="readonly",
                                  font=FONTS["body"], width=25)
        self.combo.pack(side="left", padx=10)
        self.combo.bind("<<ComboboxSelected>>", self._load_table)
        
        tk.Button(inner, text="🔄 Обновить", font=FONTS["small"],
                 bg=COLORS["bg"], fg=COLORS["text"], bd=0, cursor="hand2",
                 command=self._refresh_list).pack(side="left", padx=5, ipadx=10, ipady=4)

        # Кнопки CRUD
        crud_frame = tk.Frame(select_frame, bg=COLORS["surface"])
        crud_frame.pack(side="right", padx=20)
        
        tk.Button(crud_frame, text="➕ Добавить", font=FONTS["small"],
                 bg=COLORS["success"], fg="white", bd=0, cursor="hand2",
                 command=self._add_row).pack(side="left", padx=4, ipadx=12, ipady=5)
        tk.Button(crud_frame, text="✏️ Изменить", font=FONTS["small"],
                 bg=COLORS["primary"], fg="white", bd=0, cursor="hand2",
                 command=self._edit_row).pack(side="left", padx=4, ipadx=12, ipady=5)
        tk.Button(crud_frame, text="🗑 Удалить", font=FONTS["small"],
                 bg=COLORS["error"], fg="white", bd=0, cursor="hand2",
                 command=self._delete_row).pack(side="left", padx=4, ipadx=12, ipady=5)
        
        # Таблица
        self.table_frame = tk.Frame(self, bg=COLORS["bg"])
        self.table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        if self.tables:
            self.combo.set(self.tables[0])
            self._load_table()

    def _refresh_list(self):
        self.tables = [t for t in db.get_table_names() 
                      if t not in (TABLE_USERS, "sqlite_sequence", "ГруппыПользователей")]
        self.combo.config(values=self.tables)
        if self.tables and self.combo.get() not in self.tables:
            self.combo.set(self.tables[0])
            self._load_table()
        elif not self.tables:
            for w in self.table_frame.winfo_children():
                w.destroy()
            tk.Label(self.table_frame, text="📭 База данных не содержит пользовательских таблиц",
                    font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text_sec"]).pack(pady=40)
            
    def _load_table(self, event=None):
        tname = self.combo.get()
        if not tname:
            return
        
        for w in self.table_frame.winfo_children():
            w.destroy()
        
        self.cols_info, self.rows = db.get_table_data(tname)
        if not self.cols_info:
            tk.Label(self.table_frame, text="Таблица пуста", font=FONTS["body"],
                    bg=COLORS["bg"], fg=COLORS["text_sec"]).pack(pady=40)
            return
        
        # Контейнер с таблицей и скроллом
        tree_container = tk.Frame(self.table_frame, bg=COLORS["bg"])
        tree_container.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_container, columns=self.cols_info, show="headings")
        for c in self.cols_info:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, minwidth=80)
        
        for row in self.rows:
            vals = [row.get(c, "") for c in self.cols_info]
            self.tree.insert("", "end", values=vals)
        
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

    def _get_selected_row(self):
        if not hasattr(self, 'tree') or not self.tree.selection():
            messagebox.showwarning("Внимание", "Выберите строку в таблице!")
            return None
        item_id = self.tree.selection()[0]
        vals = self.tree.item(item_id, "values")
        return dict(zip(self.cols_info, vals))

    def _add_row(self):
        tname = self.combo.get()
        if not tname:
            return
        DynamicRowEditor(self, tname, on_save=self._load_table)

    def _edit_row(self):
        tname = self.combo.get()
        if not tname:
            return
        row_data = self._get_selected_row()
        if row_data:
            DynamicRowEditor(self, tname, row_data=row_data, on_save=self._load_table)

    def _delete_row(self):
        tname = self.combo.get()
        if not tname:
            return
        row_data = self._get_selected_row()
        if not row_data:
            return
        
        pk_col = db.get_primary_key(tname)
        pk_val = row_data.get(pk_col)
        
        if pk_val is None:
            messagebox.showerror("Ошибка", "Не найден первичный ключ!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            ok, err = db.delete_row(tname, pk_col, pk_val)
            if ok:
                self._load_table()
            else:
                messagebox.showerror("Ошибка БД", f"Не удалось удалить:\n{err}")

# ==================== SQL-ПРОЦЕССОР ====================
class QueryRunner(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        # Заголовок
        header = tk.Frame(self, bg=COLORS["surface"], height=60)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        tk.Label(header, text="📝 SQL Запросы", font=FONTS["heading"],
                bg=COLORS["surface"], fg=COLORS["text"]).pack(side="left", padx=20)
        tk.Label(header, text="Выполнение произвольных SQL-запросов", font=FONTS["small"],
                bg=COLORS["surface"], fg=COLORS["text_sec"]).pack(side="left", padx=10)
        
        # Редактор SQL
        editor_frame = tk.Frame(self, bg=COLORS["surface"])
        editor_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(editor_frame, text="SQL Запрос:", font=FONTS["small"],
                bg=COLORS["surface"], fg=COLORS["text_sec"]).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.text_sql = tk.Text(editor_frame, font=FONTS["mono"], height=8,
                                bg=COLORS["bg"], fg=COLORS["text"],
                                insertbackground=COLORS["primary"],
                                bd=1, relief="solid", wrap="word")
        self.text_sql.pack(fill="x", padx=15, pady=(0, 10))
        self.text_sql.insert("1.0", MODULE_3_QUERY.strip())
        
        # Кнопки
        btn_frame = tk.Frame(editor_frame, bg=COLORS["surface"])
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        tk.Button(btn_frame, text="▶ Выполнить запрос", font=FONTS["button"],
                 bg=COLORS["accent"], fg="white", bd=0, cursor="hand2",
                 command=self._run_query).pack(side="left", ipadx=30, ipady=8)
        
        self.status = tk.Label(btn_frame, text="", font=FONTS["small"],
                               bg=COLORS["surface"], fg=COLORS["text_sec"])
        self.status.pack(side="left", padx=15)
        
        # Результаты
        results_frame = tk.Frame(self, bg=COLORS["bg"])
        results_frame.pack(fill="both", expand=True)
        
        tk.Label(results_frame, text="Результат:", font=FONTS["small"],
                bg=COLORS["bg"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(0, 5))
        
        self.res_frame = tk.Frame(results_frame, bg=COLORS["surface"])
        self.res_frame.pack(fill="both", expand=True)

    def _run_query(self):
        query = self.text_sql.get("1.0", "end").strip()
        if not query:
            return
        
        for w in self.res_frame.winfo_children():
            w.destroy()
        
        cols, rows, err = db.execute_query(query)
        
        if err:
            tk.Label(self.res_frame, text=f"❌ Ошибка:\n{err}",
                    font=FONTS["body"], bg=COLORS["surface"],
                    fg=COLORS["error"], justify="left").pack(pady=20, padx=20)
            self.status.config(text="Ошибка выполнения", fg=COLORS["error"])
            return
        
        if not cols:
            tk.Label(self.res_frame, text="✅ Запрос выполнен успешно",
                    font=FONTS["body"], bg=COLORS["surface"],
                    fg=COLORS["success"]).pack(pady=40)
            self.status.config(text="Успешно", fg=COLORS["success"])
            return
        
        # Таблица результатов
        tree_container = tk.Frame(self.res_frame, bg=COLORS["surface"])
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, minwidth=80)
        
        for row in rows:
            tree.insert("", "end", values=row)
        
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        self.status.config(text=f"Строк: {len(rows)}", fg=COLORS["success"])

# ==================== ГЛАВНОЕ ОКНО ====================
class MainWindow(tk.Frame):
    def __init__(self, parent, app, user):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.user = user
        self._build()

    def _build(self):
        # Верхняя панель с информацией о пользователе
        header = tk.Frame(self, bg=COLORS["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Логотип и название слева
        logo_frame = tk.Frame(header, bg=COLORS["primary"])
        logo_frame.pack(side="left", padx=20)
        
        tk.Label(logo_frame, text="🏭", font=("Segoe UI", 20),
                bg=COLORS["primary"], fg="white").pack(side="left")
        tk.Label(logo_frame, text=APP_TITLE, font=("Segoe UI", 14, "bold"),
                bg=COLORS["primary"], fg="white").pack(side="left", padx=8)
        
        # Информация о пользователе справа
        user_frame = tk.Frame(header, bg=COLORS["primary"])
        user_frame.pack(side="right", padx=20)
        
        tk.Label(user_frame, text="👤", font=("Segoe UI", 14),
                bg=COLORS["primary"], fg="white").pack(side="left")
        tk.Label(user_frame, text=f"{self.user['login']} ({self.user['role']})",
                font=("Segoe UI", 10), bg=COLORS["primary"], fg="white").pack(side="left", padx=5)
        
        # Основной контент (область для отображения данных)
        self.content_area = tk.Frame(self, bg=COLORS["bg"])
        self.content_area.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Изначально показываем приветствие
        self._show_welcome()
        
        # Нижняя панель с кнопками навигации
        nav_bar = tk.Frame(self, bg=COLORS["surface"], height=70)
        nav_bar.pack(fill="x", side="bottom")
        nav_bar.pack_propagate(False)
        
        # Контейнер для кнопок (по центру)
        buttons_container = tk.Frame(nav_bar, bg=COLORS["surface"])
        buttons_container.pack(expand=True, pady=10)
        
        # Кнопка "Таблицы"
        tables_btn = tk.Button(buttons_container, text="📊 Таблицы", 
                              font=("Segoe UI", 11, "bold"),
                              bg=COLORS["primary"], fg="white",
                              bd=0, cursor="hand2",
                              activebackground=COLORS["primary_light"],
                              command=lambda: self._show_tables())
        tables_btn.pack(side="left", padx=10, ipadx=20, ipady=8)
        
        # Кнопка "SQL Запросы"
        sql_btn = tk.Button(buttons_container, text="📝 SQL Запросы",
                           font=("Segoe UI", 11, "bold"),
                           bg=COLORS["accent"], fg="white",
                           bd=0, cursor="hand2",
                           activebackground="#7C3AED",
                           command=lambda: self._show_sql())
        sql_btn.pack(side="left", padx=10, ipadx=20, ipady=8)
        
        # Кнопка "Управление" (только для админа)
        if self.user["role"] == "Администратор":
            admin_btn = tk.Button(buttons_container, text="⚙️ Управление",
                                 font=("Segoe UI", 11, "bold"),
                                 bg=COLORS["success"], fg="white",
                                 bd=0, cursor="hand2",
                                 activebackground="#059669",
                                 command=lambda: self._show_admin())
            admin_btn.pack(side="left", padx=10, ipadx=20, ipady=8)
        
        # Кнопка "Выход"
        logout_btn = tk.Button(buttons_container, text="🚪 Выход",
                              font=("Segoe UI", 11, "bold"),
                              bg=COLORS["error"], fg="white",
                              bd=0, cursor="hand2",
                              activebackground="#DC2626",
                              command=self.app.show_login)
        logout_btn.pack(side="left", padx=10, ipadx=20, ipady=8)
        
        # Эффекты наведения для всех кнопок
        for btn in [tables_btn, sql_btn, logout_btn]:
            if self.user["role"] == "Администратор":
                btns = [tables_btn, sql_btn, admin_btn, logout_btn]
            else:
                btns = [tables_btn, sql_btn, logout_btn]
            
            for b in btns:
                original_bg = b.cget("bg")
                def on_enter(e, btn=b, bg=original_bg):
                    btn.config(bg=COLORS["primary_light"] if "#3B82F6" in bg else 
                              ("#7C3AED" if "#8B5CF6" in bg else
                               ("#059669" if "#10B981" in bg else
                                ("#DC2626" if "#EF4444" in bg else bg))))
                def on_leave(e, btn=b, bg=original_bg):
                    btn.config(bg=bg)
                b.bind("<Enter>", on_enter)
                b.bind("<Leave>", on_leave)
    
    def _show_welcome(self):
        # Очищаем область контента
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Показываем приветствие
        welcome_frame = tk.Frame(self.content_area, bg=COLORS["bg"])
        welcome_frame.pack(expand=True)
        
        tk.Label(welcome_frame, text="👋 Добро пожаловать!", 
                font=("Segoe UI", 24, "bold"),
                bg=COLORS["bg"], fg=COLORS["primary"]).pack(pady=20)
        
        tk.Label(welcome_frame, text=f"{self.user['login']}, вы успешно авторизовались в системе",
                font=("Segoe UI", 12), bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)
        
        tk.Label(welcome_frame, text="Выберите нужный раздел в нижней панели навигации",
                font=("Segoe UI", 10), bg=COLORS["bg"], fg=COLORS["text_sec"]).pack(pady=5)
    
    def _show_tables(self):
        # Очищаем область контента
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Показываем просмотрщик таблиц
        dv = DataViewer(self.content_area)
        dv.pack(fill="both", expand=True)
    
    def _show_sql(self):
        # Очищаем область контента
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Показываем SQL процессор
        qr = QueryRunner(self.content_area)
        qr.pack(fill="both", expand=True)
    
    def _show_admin(self):
        # Очищаем область контента
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Показываем админ-панель
        ap = AdminPanel(self.content_area, self.app)
        ap.pack(fill="both", expand=True)

# ==================== ПРИЛОЖЕНИЕ ====================
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_TITLE} — {COMPANY_NAME}")
        self.root.geometry("1300x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=COLORS["bg"])
        
        try:
            self.root.state("zoomed")
        except:
            pass
        
        setup_styles()
        db.init_system_tables()
        self.current_frame = None
        self.show_login()

    def _switch(self, frame_cls, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_cls(self.root, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self._switch(LoginFrame, self)

    def show_main(self, user):
        self._switch(MainWindow, self, user)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()