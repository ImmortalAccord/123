# ============================================================
# config.py — Конфигурация приложения
# ============================================================
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
TABLE_USERS = "Пользователи"

# Пример SQL-запроса для вкладки SQL
MODULE_3_QUERY = '''SELECT 
    o.id AS [Номер заказа],
    c.Название AS [Заказчик],
    o.ДатаЗаказа AS [Дата],
    s.Название AS [Товар],
    p.Цена AS [Цена, руб.],
    pr.Статус AS [Статус производства]
FROM Заказы_покупателя o
JOIN Заказчики c ON o.ЗаказчикId = c.id
JOIN Производство pr ON pr.ЗаказId = o.id
JOIN Спецификация s ON pr.СпецификацияId = s.id
JOIN Цены p ON p.СпецификацияId = s.id
ORDER BY o.ДатаЗаказа DESC;'''

COMPANY_NAME = "ООО «Производство»"
APP_TITLE = "Информационная система"

# Цветовая схема (темная тема)
COLORS = {
    "primary":        "#3B82F6",
    "primary_light":  "#2563EB",
    "accent":         "#8B5CF6",
    "bg":             "#0F172A",
    "surface":        "#1E293B",
    "error":          "#EF4444",
    "success":        "#10B981",
    "text":           "#F1F5F9",
    "text_sec":       "#94A3B8",
    "border":         "#334155",
    "selected":       "#3B82F6",
    "blocked":        "#7F1D1D",
}

FONTS = {
    "title":   ("Segoe UI", 22, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "button":  ("Segoe UI", 10, "bold"),
    "mono":    ("Consolas", 10),
}

MAX_FAILED_ATTEMPTS = 3
MSG_AUTH_SUCCESS   = "Успешный вход в систему"
MSG_AUTH_ERROR     = "Неверный логин или пароль"
MSG_AUTH_BLOCKED   = "Аккаунт заблокирован"
MSG_FIELDS_EMPTY   = "Заполните все поля"

