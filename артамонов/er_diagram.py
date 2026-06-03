# ============================================================
# er_diagram.py — УНИВЕРСАЛЬНЫЙ генератор ER-диаграмм для SQLite
# Использование: python er_diagram.py [путь_к_БД] [выходной_файл]
# Не требует ввода данных — читает схему из sqlite_master
# Использует Graphviz для идеального позиционирования и связей.
# ============================================================

import sqlite3
import sys
import os

try:
    import graphviz
except ImportError:
    print("Установите graphviz: pip install graphviz")
    sys.exit(1)

def get_schema(db_path):
    """Извлечение полной схемы БД: таблицы, столбцы, PK, FK."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]

    schema = {}
    for table in tables:
        cur.execute(f"PRAGMA table_info([{table}])")
        columns = []
        for row in cur.fetchall():
            columns.append({
                "name": row[1], "type": row[2],
                "notnull": bool(row[3]), "pk": bool(row[5])
            })

        cur.execute(f"PRAGMA foreign_key_list([{table}])")
        fks = []
        for row in cur.fetchall():
            fks.append({"from": row[3], "to_table": row[2], "to_col": row[4]})

        schema[table] = {"columns": columns, "fks": fks}
    conn.close()
    return schema

def generate_er_diagram(db_path, output_path="er_diagram"):
    """Главная функция: генерация ER-диаграммы с помощью Graphviz."""
    schema = get_schema(db_path)
    if not schema:
        print("БД пуста или не содержит таблиц.")
        return

    if output_path.endswith('.pdf') or output_path.endswith('.png'):
        output_path = output_path[:-4]

    dot = graphviz.Digraph(
        "ER-Diagram",
        filename=output_path,
        engine='dot',
        node_attr={'shape': 'none', 'fontname': 'Segoe UI', 'fontsize': '10'},
        edge_attr={'fontname': 'Segoe UI', 'fontsize': '9', 'color': '#555555'}
    )
    
    # Настройки графа для красивого размещения слева направо (LR) или сверху вниз (TB)
    dot.attr(rankdir='LR', nodesep='0.8', ranksep='1.5')

    # Добавляем узлы (таблицы)
    for table_name, info in schema.items():
        pk_cols = {c["name"] for c in info["columns"] if c["pk"]}
        fk_cols = {fk["from"] for fk in info["fks"]}
        
        # Формируем HTML-подобную метку для таблицы
        label = f'<<table border="0" cellborder="1" cellspacing="0" cellpadding="6">'
        label += f'<tr><td bgcolor="#1565C0"><font color="white"><b>{table_name}</b></font></td></tr>'
        
        for col in info["columns"]:
            cname = col["name"]
            ctype = col["type"]
            nn = " NOT NULL" if col["notnull"] and not col["pk"] else ""
            
            icon = ""
            bg = "#ffffff"
            if cname in pk_cols:
                icon = "<b>[PK]</b> "
                bg = "#FFF9C4" # Светло-жёлтый для первичных ключей
            elif cname in fk_cols:
                icon = "<b>[FK]</b> "
                bg = "#E3F2FD" # Светло-синий для внешних ключей
            
            label += f'<tr><td align="left" bgcolor="{bg}" port="{cname}">{icon}{cname} <font color="#666666"><i>({ctype}{nn})</i></font></td></tr>'
            
        label += '</table>>'
        
        dot.node(table_name, label=label)

    # Добавляем связи (внешние ключи)
    for table_name, info in schema.items():
        for fk in info["fks"]:
            from_col = fk["from"]
            to_table = fk["to_table"]
            to_col = fk["to_col"]
            
            if to_table in schema:
                # Связь от дочерней таблицы к родительской (один ко многим)
                dot.edge(f"{table_name}:{from_col}", f"{to_table}:{to_col}", 
                         arrowhead="crow", arrowtail="none", dir="both")

    # Рендер
    dot.render(output_path, format='pdf', cleanup=True)
    dot.render(output_path, format='png', cleanup=True)
    
    print(f"[OK] ER-диаграмма успешно пересоздана: {output_path}.pdf и {output_path}.png")


# ==================== ТОЧКА ВХОДА ====================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
    else:
        db = sys.argv[1]

    out = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "er_diagram")

    if not os.path.exists(db):
        print(f"Файл БД не найден: {db}")
        sys.exit(1)

    generate_er_diagram(db, out)
