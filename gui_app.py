# gui_app.py

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import logging

from config.settings import VERSION, APP_NAME
from core import generate_case, export_to_excel


# ======================
# 基础设置
# ======================
root = tk.Tk()
root.title(f"{APP_NAME} v{VERSION}")
root.geometry("700x600")

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ======================
# UI更新函数（主线程）
# ======================
def update_ui(result):
    progress.stop()
    btn_generate.config(state="normal")

    if result["success"]:
        status_label.config(text="状态：生成完成 ✅")

        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", result["data"])

        messagebox.showinfo("成功", result["message"])
    else:
        status_label.config(text="状态：失败 ❌")
        messagebox.showwarning("失败", result["message"])


def update_status(text):
    status_label.config(text=f"状态：{text}")


def show_error(msg):
    progress.stop()
    btn_generate.config(state="normal")
    status_label.config(text="状态：失败 ❌")
    messagebox.showerror("错误", msg)


# ======================
# 线程任务（核心）
# ======================
def task(user_input):
    try:
        type_map = {
            "功能测试": "1",
            "异常测试": "2",
            "全部测试": "3"
        }

        type_choice = type_map.get(type_var.get(), "3")

        result = generate_case(
            user_input,
            type_choice,
            callback=lambda x: root.after(0, lambda: update_status(x))
        )

        root.after(0, lambda: update_ui(result))

    except Exception as e:
        logging.error(f"GUI错误: {e}", exc_info=True)

        err_msg = str(e)

        if "Connection" in err_msg or "Timeout" in err_msg:
            user_msg = "网络连接失败，请检查网络"
        elif "401" in err_msg:
            user_msg = "API Key 无效或过期"
        elif "429" in err_msg:
            user_msg = "请求过于频繁，请稍后再试"
        else:
            user_msg = "系统异常，请稍后重试"

        root.after(0, lambda: show_error(user_msg))


# ======================
# 按钮：生成
# ======================
def on_generate():
    user_input = input_text.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showwarning("提示", "请输入需求")
        return

    btn_generate.config(state="disabled")
    status_label.config(text="状态：生成中... ⏳")
    progress.start()

    thread = threading.Thread(
        target=task,
        args=(user_input,),
        daemon=True
    )
    thread.start()


# ======================
# 导出Excel
# ======================
def on_export():
    content = output_text.get("1.0", tk.END).strip()

    if not content:
        messagebox.showwarning("提示", "没有可导出的内容")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel文件", "*.xlsx")],
        title="选择保存位置"
    )

    if not file_path:
        return

    msg = export_to_excel(content, file_path)
    messagebox.showinfo("提示", msg)


# ======================
# UI界面
# ======================

tk.Label(root, text=f"{APP_NAME} v{VERSION}", font=("Arial", 16)).pack(pady=10)

type_var = tk.StringVar()
type_combo = ttk.Combobox(root, textvariable=type_var, state="readonly")
type_combo["values"] = ("全部测试", "功能测试", "异常测试")
type_combo.current(0)
type_combo.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="产品需求：").pack(anchor="w", padx=10)

input_text = tk.Text(root, height=8)
input_text.pack(fill="x", padx=10)

# 按钮区
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_generate = tk.Button(btn_frame, text="生成用例", width=12, command=on_generate)
btn_generate.grid(row=0, column=0, padx=5)

btn_export = tk.Button(btn_frame, text="导出Excel", width=12, command=on_export)
btn_export.grid(row=0, column=1, padx=5)

# 进度条
progress = ttk.Progressbar(root, mode="indeterminate")
progress.pack(fill="x", padx=10, pady=5)

# 状态栏
status_label = tk.Label(root, text="状态：就绪", anchor="w")
status_label.pack(fill="x", padx=10)

# 输出区
tk.Label(root, text="结果：").pack(anchor="w", padx=10)

output_text = tk.Text(root, height=20)
output_text.pack(fill="both", expand=True, padx=10)


# 启动
root.mainloop()