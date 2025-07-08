import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import numpy as np
import json
import csv
import requests
from typing import Dict, List, Optional
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import seaborn as sns
import re

class GradeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Wangci_学生成绩综合管理系统 v2.0")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e1e2e')  # 深色主题背景
        
        # 设置文件保存路径为程序所在目录
        self.app_directory = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
        
        # 设置现代化的样式主题
        self.setup_styles()
        
        # 数据存储
        self.current_data = pd.DataFrame()
        self.classes = {}  # 存储多个班级数据
        self.current_class = None
        self.ratios = [2, 4, 4]  # 默认比例 [实验:课堂表现:期末]
        self.gemini_api_key = ""
        self.selected_model = "gemini-2.5-flash"  # 默认模型
        self.sort_reverse = {}  # 存储每列的排序状态
        self.data_source_var = None  # 数据源指示器变量
        
        # 可视化分析相关
        self.analysis_class = None
        self.analysis_data = pd.DataFrame()
        self.charts_to_save = []
        
        # 可用模型列表 - 更新到最新版本
        self.available_models = {
            "gemini-2.5-flash": "Gemini 2.5 Flash",
            "gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite (预览版)",
            "gemini-1.5-pro": "Gemini 1.5 Pro",
            "gemini-1.5-flash": "Gemini 1.5 Flash",
            "gemini-1.0-pro": "Gemini 1.0 Pro"
        }
        
        # 创建界面
        self.create_widgets()
        self.load_persistent_data()  # 改为加载持久化数据
        
        # 设置程序关闭时保存数据
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """设置现代化UI样式 - 简化版本"""
        # 定义颜色方案
        self.colors = {
            'bg': '#1e1e2e',           # 深色背景
            'fg': '#cdd6f4',           # 浅色文字
            'select_bg': '#89b4fa',    # 选中背景（蓝色）
            'select_fg': '#1e1e2e',    # 选中文字
            'button_bg': '#6c7086',    # 按钮背景
            'button_hover': '#89b4fa', # 按钮悬停
            'entry_bg': '#313244',     # 输入框背景
            'frame_bg': '#181825',     # 框架背景
            'accent': '#f38ba8',       # 强调色（粉色）
            'success': '#a6e3a1',      # 成功色（绿色）
            'warning': '#fab387',      # 警告色（橙色）
            'error': '#f38ba8'         # 错误色（红色）
        }
        
    def create_widgets(self):
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 创建渐变效果的标题框架
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'], height=80)
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.columnconfigure(0, weight=1)
        
        # 主标题
        title_label = tk.Label(title_frame, 
                              text="🎓  Wangci_学生成绩综合管理系统",
                              font=('Arial', 24, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg'])
        title_label.grid(row=0, column=0, pady=10)
        
        # 副标题
        subtitle_label = tk.Label(title_frame,
                                 text="Wangci_期末数据管理",
                                 font=('Arial', 12),
                                 fg=self.colors['select_bg'],
                                 bg=self.colors['bg'])
        subtitle_label.grid(row=1, column=0)
        
        # 左侧控制面板
        control_frame = tk.LabelFrame(main_frame, text="🎛️ 控制面板", 
                                     bg=self.colors['frame_bg'],
                                     fg=self.colors['fg'],
                                     font=('Arial', 11, 'bold'),
                                     bd=2, relief='solid')
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          padx=(0, 15), pady=10, ipadx=20, ipady=20)
        
        # 班级选择区域
        class_section = tk.Frame(control_frame, bg=self.colors['frame_bg'])
        class_section.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        tk.Label(class_section, text="📚 当前班级:", 
                font=('Arial', 12, 'bold'),
                fg=self.colors['fg'], bg=self.colors['frame_bg']).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 班级选择和删除按钮组合
        class_control_frame = tk.Frame(class_section, bg=self.colors['frame_bg'])
        class_control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        class_control_frame.columnconfigure(0, weight=1)
        
        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(class_control_frame, textvariable=self.class_var, 
                                       width=20, state="readonly", font=('Arial', 10))
        self.class_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.class_combo.bind('<<ComboboxSelected>>', self.on_class_change)
        
        # 删除班级按钮
        def create_button(parent, text, command, bg_color, fg_color=None):
            if fg_color is None:
                fg_color = self.colors['bg'] if bg_color != self.colors['button_bg'] else self.colors['fg']
            
            btn = tk.Button(parent, text=text, command=command,
                           bg=bg_color, fg=fg_color,
                           font=('Arial', 8, 'bold'),
                           relief='flat', bd=0, padx=8, pady=4,
                           cursor='hand2')
            
            # 添加悬停效果
            def on_enter(e):
                btn['bg'] = self.colors['button_hover']
                btn['fg'] = self.colors['select_fg']
            
            def on_leave(e):
                btn['bg'] = bg_color
                btn['fg'] = fg_color
                
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            
            return btn
        
        delete_class_btn = create_button(class_control_frame, "🗑️", self.delete_class, self.colors['error'])
        delete_class_btn.grid(row=0, column=1)
        
        class_section.columnconfigure(0, weight=1)
        
        # 分隔线
        separator1 = tk.Frame(control_frame, height=2, bg=self.colors['button_bg'])
        separator1.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # 比例设置区域
        ratio_section = tk.Frame(control_frame, bg=self.colors['frame_bg'])
        ratio_section.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        tk.Label(ratio_section, text="⚖️ 成绩比例:", 
                font=('Arial', 12, 'bold'),
                fg=self.colors['fg'], bg=self.colors['frame_bg']).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # 比例输入框架
        ratio_input_frame = tk.Frame(ratio_section, bg=self.colors['frame_bg'])
        ratio_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 实验比例
        exp_frame = tk.Frame(ratio_input_frame, bg=self.colors['frame_bg'])
        exp_frame.grid(row=0, column=0, padx=(0, 10))
        tk.Label(exp_frame, text="🧪 实验", font=('Arial', 9),
                fg=self.colors['fg'], bg=self.colors['frame_bg']).grid(row=0, column=0)
        self.ratio1_var = tk.StringVar(value="2")
        ratio1_entry = tk.Entry(exp_frame, textvariable=self.ratio1_var, width=8, 
                               justify='center', font=('Arial', 10, 'bold'),
                               bg=self.colors['entry_bg'], fg=self.colors['fg'],
                               relief='flat', bd=5)
        ratio1_entry.grid(row=1, column=0, pady=(2, 0))
        
        # 课堂比例
        class_frame = tk.Frame(ratio_input_frame, bg=self.colors['frame_bg'])
        class_frame.grid(row=0, column=1, padx=(0, 10))
        tk.Label(class_frame, text="👥 课堂", font=('Arial', 9),
                fg=self.colors['fg'], bg=self.colors['frame_bg']).grid(row=0, column=0)
        self.ratio2_var = tk.StringVar(value="4")
        ratio2_entry = tk.Entry(class_frame, textvariable=self.ratio2_var, width=8,
                               justify='center', font=('Arial', 10, 'bold'),
                               bg=self.colors['entry_bg'], fg=self.colors['fg'],
                               relief='flat', bd=5)
        ratio2_entry.grid(row=1, column=0, pady=(2, 0))
        
        # 期末比例
        final_frame = tk.Frame(ratio_input_frame, bg=self.colors['frame_bg'])
        final_frame.grid(row=0, column=2)
        tk.Label(final_frame, text="📝 期末", font=('Arial', 9),
                fg=self.colors['fg'], bg=self.colors['frame_bg']).grid(row=0, column=0)
        self.ratio3_var = tk.StringVar(value="4")
        ratio3_entry = tk.Entry(final_frame, textvariable=self.ratio3_var, width=8,
                               justify='center', font=('Arial', 10, 'bold'),
                               bg=self.colors['entry_bg'], fg=self.colors['fg'],
                               relief='flat', bd=5)
        ratio3_entry.grid(row=1, column=0, pady=(2, 0))
        
        # 分隔线
        separator2 = tk.Frame(control_frame, height=2, bg=self.colors['button_bg'])
        separator2.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # 按钮区域
        button_section = tk.Frame(control_frame, bg=self.colors['frame_bg'])
        button_section.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 创建自定义按钮样式
        def create_main_button(parent, text, command, bg_color, fg_color=None):
            if fg_color is None:
                fg_color = self.colors['bg'] if bg_color != self.colors['button_bg'] else self.colors['fg']
            
            btn = tk.Button(parent, text=text, command=command,
                           bg=bg_color, fg=fg_color,
                           font=('Arial', 10, 'bold'),
                           relief='flat', bd=0, padx=15, pady=8,
                           cursor='hand2')
            
            # 添加悬停效果
            def on_enter(e):
                btn['bg'] = self.colors['button_hover']
                btn['fg'] = self.colors['select_fg']
            
            def on_leave(e):
                btn['bg'] = bg_color
                btn['fg'] = fg_color
                
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            
            return btn
        
        # 主要操作按钮
        apply_btn = create_main_button(button_section, "🔄 应用比例", self.apply_ratios, self.colors['accent'])
        apply_btn.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8))
        
        # 数据操作按钮
        import_btn = create_main_button(button_section, "📁 导入文件", self.import_file, self.colors['button_bg'])
        import_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 4), pady=2)
        
        new_class_btn = create_main_button(button_section, "➕ 新建班级", self.create_new_class, self.colors['button_bg'])
        new_class_btn.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(4, 0), pady=2)
        
        save_btn = create_main_button(button_section, "💾 保存数据", self.save_data, self.colors['button_bg'])
        save_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=(0, 4), pady=2)
        
        export_btn = create_main_button(button_section, "📊 导出Excel", self.export_excel, self.colors['button_bg'])
        export_btn.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(4, 0), pady=2)
        
        ai_btn = create_main_button(button_section, "🤖 AI助手", self.show_ai_dialog, self.colors['accent'])
        ai_btn.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(8, 0))
        
        # 添加可视化统计按钮
        stats_btn = create_main_button(button_section, "📈 可视化统计", self.show_statistics, self.colors['success'])
        stats_btn.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(8, 0))
        
        button_section.columnconfigure(0, weight=1)
        button_section.columnconfigure(1, weight=1)
        
        # 右侧数据表格区域
        table_frame = tk.LabelFrame(main_frame, text="📋 成绩数据表", 
                                   bg=self.colors['frame_bg'],
                                   fg=self.colors['fg'],
                                   font=('Arial', 11, 'bold'),
                                   bd=2, relief='solid')
        table_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                        pady=10, ipadx=15, ipady=15)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # 创建现代化Treeview
        tree_frame = tk.Frame(table_frame, bg=self.colors['frame_bg'])
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, show='headings', height=15)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加现代化滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 绑定双击编辑事件
        self.tree.bind('<Double-1>', self.on_cell_edit)
        
        # 现代化状态栏
        status_frame = tk.Frame(main_frame, bg=self.colors['frame_bg'], height=35)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=0)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 系统就绪")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.colors['frame_bg'], fg=self.colors['success'], 
                               font=('Arial', 10), anchor=tk.W, padx=15)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=8)
        
        # 数据源指示器
        self.data_source_var = tk.StringVar()
        self.data_source_var.set("💾 自动保存")
        data_source_label = tk.Label(status_frame, textvariable=self.data_source_var,
                                    bg=self.colors['frame_bg'], fg=self.colors['select_bg'], 
                                    font=('Arial', 9), anchor=tk.E, padx=15)
        data_source_label.grid(row=0, column=1, sticky=(tk.E), pady=8)
    
    def delete_class(self):
        """删除当前班级"""
        if not self.current_class or not self.classes:
            messagebox.showwarning("⚠️ 警告", "没有班级可删除")
            return
            
        result = messagebox.askyesno("🗑️ 删除确认", 
                                   f"确定要删除班级 '{self.current_class}' 吗？\n此操作不可撤销！")
        if result:
            # 删除班级
            del self.classes[self.current_class]
            
            # 更新界面
            if self.classes:
                # 选择第一个剩余班级
                self.current_class = list(self.classes.keys())[0]
                self.current_data = self.classes[self.current_class].copy()
                self.class_combo['values'] = list(self.classes.keys())
                self.class_combo.set(self.current_class)
                self.calculate_scores()
                self.update_display()
                self.status_var.set(f"🗑️ 班级已删除，当前班级: {self.current_class}")
            else:
                # 没有班级了，加载示例数据
                self.load_sample_data()
                self.status_var.set("🗑️ 班级已删除，已重新加载示例数据")
            
            self.auto_save_data()  # 自动保存
    
    def setup_matplotlib_chinese(self):
        """配置matplotlib中文字体"""
        try:
            # 设置matplotlib后端
            matplotlib.use('TkAgg')
            
            # 尝试不同的中文字体
            chinese_fonts = [
                'SimHei',           # 黑体 (Windows)
                'Microsoft YaHei',  # 微软雅黑 (Windows)
                'PingFang SC',      # 苹方 (macOS)
                'Hiragino Sans GB', # 冬青黑体 (macOS)
                'WenQuanYi Micro Hei', # 文泉驿微米黑 (Linux)
                'DejaVu Sans'       # 默认字体
            ]
            
            for font in chinese_fonts:
                try:
                    plt.rcParams['font.sans-serif'] = [font]
                    # 测试字体是否可用
                    fig, ax = plt.subplots(figsize=(1, 1))
                    ax.text(0.5, 0.5, '测试', fontsize=10)
                    plt.close(fig)
                    break
                except:
                    continue
            
            # 其他matplotlib设置
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            plt.rcParams['figure.facecolor'] = '#1e1e2e'
            plt.rcParams['axes.facecolor'] = '#181825'
            plt.rcParams['text.color'] = 'white'
            plt.rcParams['axes.labelcolor'] = 'white'
            plt.rcParams['xtick.color'] = 'white'
            plt.rcParams['ytick.color'] = 'white'
            plt.rcParams['axes.edgecolor'] = 'white'
            
        except Exception as e:
            print(f"设置中文字体失败: {e}")

    def show_statistics(self):
        """显示可视化统计窗口"""
        if not self.classes:
            messagebox.showwarning("⚠️ 警告", "没有班级数据可统计")
            return
        
        # 配置matplotlib中文显示
        self.setup_matplotlib_chinese()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📈 班级可视化统计分析")
        stats_window.geometry("1200x800")
        stats_window.configure(bg='#1e1e2e')
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        # 存储当前分析的班级数据
        self.analysis_class = None
        self.analysis_data = pd.DataFrame()
        
        # 创建顶部控制栏
        control_frame = tk.Frame(stats_window, bg='#181825', height=80)
        control_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        control_frame.pack_propagate(False)
        
        # 班级选择区域
        class_select_frame = tk.Frame(control_frame, bg='#181825')
        class_select_frame.pack(side=tk.LEFT, padx=(20, 0), pady=15)
        
        tk.Label(class_select_frame, text="📚 选择要分析的班级:", 
                font=('Arial', 12, 'bold'),
                fg='#cdd6f4', bg='#181825').pack(anchor=tk.W)
        
        select_frame = tk.Frame(class_select_frame, bg='#181825')
        select_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.stats_class_var = tk.StringVar()
        class_combo = ttk.Combobox(select_frame, textvariable=self.stats_class_var,
                                  values=list(self.classes.keys()),
                                  state="readonly", width=25, font=('Arial', 10))
        class_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 设置默认选择当前班级
        if self.current_class:
            self.stats_class_var.set(self.current_class)
        
        # 生成分析按钮
        generate_btn = tk.Button(select_frame, text="🔍 生成分析", 
                                command=lambda: self.generate_statistics_analysis(notebook, info_label),
                                bg='#89b4fa', fg='#1e1e2e', 
                                font=('Arial', 10, 'bold'),
                                relief='flat', bd=0, padx=20, pady=8)
        generate_btn.pack(side=tk.LEFT)
        
        # 右侧按钮区域
        button_frame = tk.Frame(control_frame, bg='#181825')
        button_frame.pack(side=tk.RIGHT, padx=(0, 20), pady=15)
        
        # 保存按钮
        self.save_charts_btn = tk.Button(button_frame, text="💾 保存所有图表", 
                                        command=lambda: self.save_all_charts(),
                                        bg='#a6e3a1', fg='#1e1e2e', 
                                        font=('Arial', 10, 'bold'),
                                        relief='flat', bd=0, padx=20, pady=8,
                                        state='disabled')
        self.save_charts_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # AI分析按钮
        self.ai_analysis_btn = tk.Button(button_frame, text="🤖 AI分析", 
                                        command=lambda: self.generate_ai_analysis(),
                                        bg='#f38ba8', fg='#1e1e2e', 
                                        font=('Arial', 10, 'bold'),
                                        relief='flat', bd=0, padx=20, pady=8,
                                        state='disabled')
        self.ai_analysis_btn.pack(side=tk.LEFT)
        
        # 信息标签
        info_label = tk.Label(control_frame, 
                             text="请先选择班级并生成分析",
                             bg='#181825', fg='#fab387', font=('Arial', 9))
        info_label.pack(side=tk.BOTTOM, pady=(0, 10))
        
        # 创建notebook用于多个统计页面
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # 初始化存储图表用于保存
        self.charts_to_save = []
        
        # 显示提示页面
        self.show_welcome_tab(notebook)

    def show_welcome_tab(self, notebook):
        """显示欢迎页面"""
        frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(frame, text="📋 开始分析")
        
        welcome_frame = tk.Frame(frame, bg='#181825')
        welcome_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # 标题
        title_label = tk.Label(welcome_frame, text="📈 班级可视化统计分析系统",
                              font=('Arial', 20, 'bold'),
                              fg='#f38ba8', bg='#181825')
        title_label.pack(pady=(50, 30))
        
        # 说明文字
        instructions = """🔍 使用步骤：

1. 在上方选择要分析的班级
2. 点击"🔍 生成分析"按钮
3. 查看各种统计图表和排名
4. 可选择"🤖 AI分析"获取智能分析报告
5. 点击"💾 保存所有图表"导出结果

📊 分析内容包括：
• 成绩分布统计（直方图、饼图、箱线图、趋势图）
• 成绩对比分析（平均分对比、相关性分析）  
• 学生排名榜（详细排名和等级）
• 统计摘要报告（数据总结和分析）
• AI智能分析（3000字深度报告）

请选择班级开始分析！"""
        
        instruction_label = tk.Label(welcome_frame, text=instructions,
                                    font=('Arial', 12),
                                    fg='#cdd6f4', bg='#181825',
                                    justify=tk.LEFT)
        instruction_label.pack(pady=20)

    def generate_statistics_analysis(self, notebook, info_label):
        """生成统计分析"""
        selected_class = self.stats_class_var.get()
        if not selected_class or selected_class not in self.classes:
            messagebox.showwarning("⚠️ 警告", "请先选择要分析的班级")
            return
        
        # 设置分析数据
        self.analysis_class = selected_class
        self.analysis_data = self.classes[selected_class].copy()
        
        if self.analysis_data.empty:
            messagebox.showwarning("⚠️ 警告", "选择的班级没有数据")
            return
        
        # 更新信息标签
        info_label.config(text=f"班级: {selected_class} | 学生数: {len(self.analysis_data)} | 统计时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 清除现有标签页
        for tab in notebook.tabs():
            notebook.forget(tab)
        
        # 重新初始化图表存储
        self.charts_to_save = []
        
        # 计算成绩（使用临时数据）
        temp_current_data = self.current_data
        temp_current_class = self.current_class
        
        self.current_data = self.analysis_data.copy()
        self.current_class = self.analysis_class
        self.calculate_scores()
        self.analysis_data = self.current_data.copy()  # 更新分析数据
        
        # 恢复原始数据
        self.current_data = temp_current_data
        self.current_class = temp_current_class
        
        # 生成各个分析页面
        self.create_score_distribution_tab(notebook)
        self.create_score_comparison_tab(notebook)
        self.create_ranking_tab(notebook)
        self.create_summary_tab(notebook)
        
        # 启用按钮
        self.save_charts_btn.config(state='normal')
        self.ai_analysis_btn.config(state='normal')
        
        # 选择第一个标签页
        notebook.select(0)

    def create_score_distribution_tab(self, notebook):
        """创建成绩分布统计页面"""
        frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(frame, text="📊 成绩分布")
        
        try:
            # 创建图形
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('#1e1e2e')
            
            # 使用分析数据
            data = self.analysis_data
            
            # 1. 总成绩直方图
            if '总成绩' in data.columns:
                scores = data['总成绩'].dropna()
                n, bins, patches = ax1.hist(scores, bins=15, alpha=0.8, color='#89b4fa', edgecolor='white', linewidth=0.5)
                ax1.set_title('总成绩分布', fontsize=14, color='white', pad=20)
                ax1.set_xlabel('分数', color='white', fontsize=12)
                ax1.set_ylabel('人数', color='white', fontsize=12)
                ax1.tick_params(colors='white')
                ax1.grid(True, alpha=0.3, color='white')
                
                # 添加统计信息
                mean_score = scores.mean()
                ax1.axvline(mean_score, color='#f38ba8', linestyle='--', linewidth=2, 
                           label=f'平均分: {mean_score:.1f}')
                ax1.legend(loc='upper right')
                
                # 在柱状图上显示数值
                for i, v in enumerate(n):
                    if v > 0:
                        ax1.text(bins[i] + (bins[1] - bins[0])/2, v + 0.1, int(v), 
                                ha='center', va='bottom', color='white', fontsize=9)
            
            # 2. 成绩等级饼图
            if '总成绩' in data.columns:
                scores = data['总成绩'].dropna()
                excellent = len(scores[scores >= 90])
                good = len(scores[(scores >= 80) & (scores < 90)])
                medium = len(scores[(scores >= 70) & (scores < 80)])
                pass_count = len(scores[(scores >= 60) & (scores < 70)])
                fail = len(scores[scores < 60])
                
                labels = ['优秀(90+)', '良好(80-89)', '中等(70-79)', '及格(60-69)', '不及格(<60)']
                sizes = [excellent, good, medium, pass_count, fail]
                colors = ['#a6e3a1', '#89b4fa', '#fab387', '#f9e2af', '#f38ba8']
                
                # 只显示有数据的部分
                non_zero_data = [(label, size, color) for label, size, color in zip(labels, sizes, colors) if size > 0]
                if non_zero_data:
                    labels_nz, sizes_nz, colors_nz = zip(*non_zero_data)
                    wedges, texts, autotexts = ax2.pie(sizes_nz, labels=labels_nz, colors=colors_nz, 
                                                       autopct='%1.1f%%', startangle=90,
                                                       textprops={'color': 'white', 'fontsize': 10})
                    ax2.set_title('成绩等级分布', fontsize=14, color='white', pad=20)
            
            # 3. 各科成绩箱线图
            score_cols = ['实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩']
            available_cols = [col for col in score_cols if col in data.columns]
            if available_cols:
                data_for_box = [data[col].dropna().values for col in available_cols]
                box_plot = ax3.boxplot(data_for_box, labels=[col.replace('成绩', '') for col in available_cols],
                                      patch_artist=True)
                ax3.set_title('各科成绩分布', fontsize=14, color='white', pad=20)
                ax3.set_ylabel('分数', color='white', fontsize=12)
                ax3.tick_params(colors='white')
                ax3.grid(True, alpha=0.3, color='white')
                
                # 设置箱线图颜色
                colors_box = ['#89b4fa', '#a6e3a1', '#fab387', '#f9e2af', '#f38ba8', '#cba6f7']
                for patch, color in zip(box_plot['boxes'], colors_box[:len(box_plot['boxes'])]):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                # 设置其他元素颜色
                for element in ['whiskers', 'fliers', 'medians', 'caps']:
                    plt.setp(box_plot[element], color='white')
            
            # 4. 成绩趋势（如果有多次实验）
            exp_cols = ['实验一', '实验二', '实验三', '实验四']
            available_exp_cols = [col for col in exp_cols if col in data.columns]
            if len(available_exp_cols) >= 2:
                mean_scores = [data[col].mean() for col in available_exp_cols]
                std_scores = [data[col].std() for col in available_exp_cols]
                x_pos = range(len(available_exp_cols))
                
                # 绘制均值线
                line = ax4.plot(x_pos, mean_scores, marker='o', linewidth=3, 
                               markersize=8, color='#a6e3a1', markerfacecolor='#a6e3a1',
                               markeredgecolor='white', markeredgewidth=1)
                
                # 添加误差线
                ax4.errorbar(x_pos, mean_scores, yerr=std_scores, fmt='none', 
                            ecolor='#fab387', elinewidth=2, capsize=5, alpha=0.7)
                
                ax4.set_title('实验成绩趋势', fontsize=14, color='white', pad=20)
                ax4.set_xlabel('实验次数', color='white', fontsize=12)
                ax4.set_ylabel('平均分', color='white', fontsize=12)
                ax4.set_xticks(x_pos)
                ax4.set_xticklabels([f'实验{i+1}' for i in range(len(available_exp_cols))])
                ax4.tick_params(colors='white')
                ax4.grid(True, alpha=0.3, color='white')
                
                # 在点上标注数值
                for i, (x, y) in enumerate(zip(x_pos, mean_scores)):
                    ax4.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                               xytext=(0,10), ha='center', color='white', fontweight='bold')
            
            # 设置所有子图的背景
            for ax in [ax1, ax2, ax3, ax4]:
                ax.set_facecolor('#181825')
            
            plt.tight_layout(pad=3.0)
            
            # 将图形嵌入tkinter
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 保存图表引用
            self.charts_to_save.append(('成绩分布统计', fig))
            
        except Exception as e:
            error_label = tk.Label(frame, text=f"❌ 图表生成失败: {str(e)}", 
                                  fg='red', bg='#1e1e2e', font=('Arial', 12))
            error_label.pack(expand=True)
            print(f"创建成绩分布图表失败: {e}")

    def create_score_comparison_tab(self, notebook):
        """创建成绩对比页面"""
        frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(frame, text="📈 成绩对比")
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            fig.patch.set_facecolor('#1e1e2e')
            
            # 使用分析数据
            data = self.analysis_data
            
            # 1. 各科平均分对比
            score_cols = ['实验平均分', '课堂表现', '期末成绩', '总成绩']
            available_cols = [col for col in score_cols if col in data.columns]
            if available_cols:
                means = [data[col].mean() for col in available_cols]
                colors = ['#89b4fa', '#a6e3a1', '#fab387', '#f38ba8'][:len(available_cols)]
                
                bars = ax1.bar(range(len(available_cols)), means, color=colors, alpha=0.8, 
                              edgecolor='white', linewidth=1)
                ax1.set_title('各科平均分对比', fontsize=14, color='white', pad=20)
                ax1.set_ylabel('平均分', color='white', fontsize=12)
                ax1.set_xticks(range(len(available_cols)))
                ax1.set_xticklabels([col.replace('成绩', '').replace('平均分', '') for col in available_cols])
                ax1.tick_params(colors='white')
                ax1.grid(True, alpha=0.3, color='white', axis='y')
                
                # 在柱状图上显示数值
                for i, (bar, v) in enumerate(zip(bars, means)):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5, 
                            f'{v:.1f}', ha='center', va='bottom', color='white', 
                            fontweight='bold', fontsize=11)
            
            # 2. 成绩相关性热力图
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            score_numeric_cols = [col for col in numeric_cols if any(keyword in col for keyword in 
                                ['实验', '课堂', '期末', '总成绩']) and col != '序号']
            
            if len(score_numeric_cols) >= 2:
                corr_matrix = data[score_numeric_cols].corr()
                
                # 创建热力图
                im = ax2.imshow(corr_matrix.values, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
                
                ax2.set_title('成绩相关性热力图', fontsize=14, color='white', pad=20)
                ax2.set_xticks(range(len(score_numeric_cols)))
                ax2.set_yticks(range(len(score_numeric_cols)))
                
                # 设置标签
                labels = [col.replace('成绩', '').replace('平均分', '') for col in score_numeric_cols]
                ax2.set_xticklabels(labels, rotation=45, ha='right')
                ax2.set_yticklabels(labels)
                ax2.tick_params(colors='white')
                
                # 添加相关系数文本
                for i in range(len(score_numeric_cols)):
                    for j in range(len(score_numeric_cols)):
                        text_color = 'white' if abs(corr_matrix.iloc[i, j]) < 0.5 else 'black'
                        text = ax2.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                      ha="center", va="center", color=text_color, 
                                      fontweight='bold', fontsize=10)
                
                # 添加颜色条
                cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
                cbar.ax.tick_params(colors='white')
                cbar.set_label('相关系数', color='white', fontsize=10)
            
            # 设置背景
            for ax in [ax1, ax2]:
                ax.set_facecolor('#181825')
            
            plt.tight_layout(pad=3.0)
            
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 保存图表引用
            self.charts_to_save.append(('成绩对比分析', fig))
            
        except Exception as e:
            error_label = tk.Label(frame, text=f"❌ 图表生成失败: {str(e)}", 
                                  fg='red', bg='#1e1e2e', font=('Arial', 12))
            error_label.pack(expand=True)
            print(f"创建成绩对比图表失败: {e}")

    def create_ranking_tab(self, notebook):
        """创建学生排名页面"""
        frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(frame, text="🏆 学生排名")
        
        # 使用分析数据
        data = self.analysis_data
        
        # 创建排名表格
        rank_frame = tk.Frame(frame, bg='#181825')
        rank_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(rank_frame, text="🏆 学生总成绩排行榜", 
                              font=('Arial', 16, 'bold'),
                              fg='#f38ba8', bg='#181825')
        title_label.pack(pady=(10, 20))
        
        # 创建排名表格
        columns = ('排名', '姓名', '学号', '总成绩', '等级')
        rank_tree = ttk.Treeview(rank_frame, columns=columns, show='headings', height=20)
        
        # 设置列标题
        rank_tree.heading('排名', text='🏆 排名')
        rank_tree.heading('姓名', text='👤 姓名')
        rank_tree.heading('学号', text='🆔 学号')
        rank_tree.heading('总成绩', text='📊 总成绩')
        rank_tree.heading('等级', text='🎯 等级')
        
        # 设置列宽
        rank_tree.column('排名', width=80, anchor='center')
        rank_tree.column('姓名', width=100, anchor='center')
        rank_tree.column('学号', width=120, anchor='center')
        rank_tree.column('总成绩', width=100, anchor='center')
        rank_tree.column('等级', width=100, anchor='center')
        
        # 插入排名数据
        if '总成绩' in data.columns:
            # 按总成绩排序
            sorted_data = data.sort_values('总成绩', ascending=False).reset_index(drop=True)
            
            for i, (_, row) in enumerate(sorted_data.iterrows()):
                rank = i + 1
                name = row.get('姓名', 'N/A')
                student_id = row.get('学号', 'N/A')
                score = row.get('总成绩', 0)
                
                # 确定等级和标签
                if score >= 90:
                    level = "优秀 🏆"
                    tag = 'excellent'
                elif score >= 80:
                    level = "良好 🥈"
                    tag = 'good'
                elif score >= 70:
                    level = "中等 🥉"
                    tag = 'medium'
                elif score >= 60:
                    level = "及格 ✅"
                    tag = 'pass'
                else:
                    level = "不及格 ❌"
                    tag = 'fail'
                
                # 添加特殊排名标识
                if rank == 1:
                    rank_display = "🥇 1"
                elif rank == 2:
                    rank_display = "🥈 2"
                elif rank == 3:
                    rank_display = "🥉 3"
                else:
                    rank_display = str(rank)
                
                rank_tree.insert('', 'end', values=(rank_display, name, student_id, f"{score:.1f}", level), tags=(tag,))
        
        # 配置标签样式
        rank_tree.tag_configure('excellent', background='#a6e3a1', foreground='#1e1e2e')
        rank_tree.tag_configure('good', background='#89b4fa', foreground='#1e1e2e')
        rank_tree.tag_configure('medium', background='#fab387', foreground='#1e1e2e')
        rank_tree.tag_configure('pass', background='#f9e2af', foreground='#1e1e2e')
        rank_tree.tag_configure('fail', background='#f38ba8', foreground='#1e1e2e')
        
        # 添加滚动条
        rank_scrollbar = ttk.Scrollbar(rank_frame, orient='vertical', command=rank_tree.yview)
        rank_tree.configure(yscrollcommand=rank_scrollbar.set)
        
        rank_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rank_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_summary_tab(self, notebook):
        """创建统计摘要页面"""
        frame = tk.Frame(notebook, bg='#1e1e2e')
        notebook.add(frame, text="📋 统计摘要")
        
        # 创建滚动文本区域
        summary_frame = tk.Frame(frame, bg='#181825')
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        summary_text = tk.Text(summary_frame, wrap=tk.WORD, 
                              bg='#313244', fg='#cdd6f4', 
                              font=('Arial', 12),
                              relief='flat', bd=10)
        summary_text.pack(fill=tk.BOTH, expand=True)
        
        # 生成统计摘要
        summary_content = self.generate_detailed_analysis()
        summary_text.insert(tk.END, summary_content)
        summary_text.configure(state='disabled')
        
        # 添加滚动条
        summary_scrollbar = tk.Scrollbar(summary_frame, command=summary_text.yview)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        summary_text.config(yscrollcommand=summary_scrollbar.set)

    def generate_ai_analysis(self):
        """生成AI分析报告"""
        if self.analysis_data.empty:
            messagebox.showwarning("⚠️ 警告", "请先生成统计分析")
            return
        
        # 加载API设置
        self.load_api_settings()
        
        if not self.gemini_api_key:
            result = messagebox.askyesno("🔑 需要API密钥", 
                                       "AI分析需要设置Gemini API密钥。\n是否现在前往设置？")
            if result:
                self.show_ai_dialog()
            return
        
        # 创建AI分析窗口
        ai_window = tk.Toplevel(self.root)
        ai_window.title(f"🤖 {self.analysis_class} - AI智能分析")
        ai_window.geometry("900x700")
        ai_window.configure(bg='#1e1e2e')
        ai_window.transient(self.root)
        ai_window.grab_set()
        
        # 标题
        title_frame = tk.Frame(ai_window, bg='#1e1e2e', height=60)
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"🤖 {self.analysis_class} - AI智能分析报告",
                              font=('Arial', 16, 'bold'),
                              fg='#f38ba8', bg='#1e1e2e')
        title_label.pack(pady=15)
        
        # 分析结果显示区域
        result_frame = tk.Frame(ai_window, bg='#181825')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))
        
        # 文本显示区域
        text_frame = tk.Frame(result_frame, bg='#181825')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        result_text = tk.Text(text_frame, wrap=tk.WORD,
                             bg='#313244', fg='#cdd6f4', 
                             font=('Arial', 11),
                             relief='flat', bd=8)
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=result_text.yview,
                                bg='#181825', troughcolor='#313244')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        
        # 按钮区域
        button_frame = tk.Frame(ai_window, bg='#1e1e2e')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_analysis():
            """保存AI分析报告"""
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                clean_class_name = re.sub(r'[<>:"/\\|?*]', '_', self.analysis_class)
                filename = f"{clean_class_name}_{timestamp}_AI分析报告.txt"
                
                file_path = os.path.join(self.app_directory, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result_text.get("1.0", "end-1c"))
                
                messagebox.showinfo("✅ 保存成功", f"AI分析报告已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ 保存失败", f"保存分析报告时出错: {str(e)}")
        
        save_btn = tk.Button(button_frame, text="💾 保存报告", command=save_analysis,
                            bg='#a6e3a1', fg='#1e1e2e', font=('Arial', 10, 'bold'),
                            relief='flat', bd=0, padx=20, pady=8)
        save_btn.pack(side=tk.LEFT)
        
        tk.Button(button_frame, text="❌ 关闭", command=ai_window.destroy,
                 bg='#f38ba8', fg='#1e1e2e', font=('Arial', 10, 'bold'),
                 relief='flat', bd=0, padx=20, pady=8).pack(side=tk.RIGHT)
        
        # 显示加载状态
        result_text.insert(tk.END, "🤖 AI正在分析班级数据，请稍候...\n\n")
        result_text.insert(tk.END, "📊 正在处理成绩分布、统计数据和学生表现...\n")
        result_text.insert(tk.END, "⏳ 预计生成3000字详细分析报告，请耐心等待...\n")
        ai_window.update()
        
        try:
            # 准备发送给AI的数据
            data_summary = self.prepare_data_for_ai()
            
            # 构建AI分析请求
            prompt = f"""请对以下班级成绩数据进行深度分析，生成一份3000字左右的详细分析报告。

班级信息：
{data_summary}

请从以下角度进行分析：
1. 整体成绩概况与分布特征
2. 各科目成绩详细分析
3. 学生个体表现差异分析
4. 成绩相关性和规律发现
5. 班级教学效果评估
6. 数据驱动的教学洞察

要求：
- 分析要深入、专业、有见地
- 基于具体数据进行分析，不要空泛概括
- 提供具体的数字支撑和统计结论
- 语言专业但易懂，适合教育工作者阅读
- 字数控制在3000字左右
- 结构清晰，分点论述

请直接开始分析报告："""
            
            # 调用AI
            response = self.call_gemini_api(prompt)
            
            # 清除加载状态，显示结果
            result_text.delete("1.0", tk.END)
            
            if response.startswith("❌"):
                result_text.insert(tk.END, f"AI分析失败：\n\n{response}")
            else:
                # 添加报告头部信息
                header = f"""🤖 {self.analysis_class} AI智能分析报告
生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
分析模型：{self.available_models.get(self.selected_model, self.selected_model)}
班级规模：{len(self.analysis_data)}人
分析深度：深度智能分析

{'='*50}

"""
                result_text.insert(tk.END, header + response)
            
            result_text.config(state='disabled')
            
        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"❌ AI分析出错：{str(e)}")

    def prepare_data_for_ai(self):
        """准备发送给AI的数据摘要"""
        data = self.analysis_data
        
        # 基本统计信息
        summary = f"""班级名称：{self.analysis_class}
学生总数：{len(data)}人
统计时间：{datetime.now().strftime('%Y年%m月%d日')}

"""
        
        # 成绩统计
        if '总成绩' in data.columns:
            total_scores = data['总成绩'].dropna()
            summary += f"""总成绩统计：
- 平均分：{total_scores.mean():.2f}分
- 最高分：{total_scores.max():.2f}分  
- 最低分：{total_scores.min():.2f}分
- 标准差：{total_scores.std():.2f}分
- 中位数：{total_scores.median():.2f}分

"""
            
            # 等级分布
            excellent = len(total_scores[total_scores >= 90])
            good = len(total_scores[(total_scores >= 80) & (total_scores < 90)])
            medium = len(total_scores[(total_scores >= 70) & (total_scores < 80)])
            pass_count = len(total_scores[(total_scores >= 60) & (total_scores < 70)])
            fail = len(total_scores[total_scores < 60])
            
            summary += f"""成绩等级分布：
- 优秀(90+)：{excellent}人 ({excellent/len(total_scores)*100:.1f}%)
- 良好(80-89)：{good}人 ({good/len(total_scores)*100:.1f}%)
- 中等(70-79)：{medium}人 ({medium/len(total_scores)*100:.1f}%)
- 及格(60-69)：{pass_count}人 ({pass_count/len(total_scores)*100:.1f}%)
- 不及格(<60)：{fail}人 ({fail/len(total_scores)*100:.1f}%)

"""
        
        # 各科成绩分析
        score_cols = ['实验平均分', '课堂表现', '期末成绩']
        available_cols = [col for col in score_cols if col in data.columns]
        
        if available_cols:
            summary += "各科成绩统计：\n"
            for col in available_cols:
                col_data = data[col].dropna()
                if len(col_data) > 0:
                    summary += f"- {col}：平均{col_data.mean():.2f}分，最高{col_data.max():.2f}分，最低{col_data.min():.2f}分\n"
            summary += "\n"
        
        # 前后排名学生（不包含具体姓名，只统计）
        if '总成绩' in data.columns:
            sorted_data = data.sort_values('总成绩', ascending=False)
            top_3_scores = sorted_data['总成绩'].head(3).tolist()
            bottom_3_scores = sorted_data['总成绩'].tail(3).tolist()
            
            summary += f"""排名信息：
- 前三名成绩：{', '.join([f'{score:.1f}分' for score in top_3_scores])}
- 后三名成绩：{', '.join([f'{score:.1f}分' for score in bottom_3_scores])}

"""
        
        # 成绩比例设置
        summary += f"成绩计算比例：实验{self.ratios[0]} : 课堂{self.ratios[1]} : 期末{self.ratios[2]}\n\n"
        
        # 添加部分详细数据样本（不含姓名）
        summary += "数据样本（前10名学生成绩分布，已匿名化）：\n"
        if '总成绩' in data.columns:
            sample_data = data.nlargest(10, '总成绩')[['实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩', '总成绩']]
            summary += sample_data.to_string(index=False)
        
        return summary

    def save_all_charts(self):
        """保存所有图表到文件夹"""
        if not hasattr(self, 'analysis_class') or not self.analysis_class:
            messagebox.showwarning("⚠️ 警告", "请先生成统计分析")
            return
            
        try:
            # 创建文件夹名称（班级名称+时间）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 清理班级名称中的特殊字符
            clean_class_name = re.sub(r'[<>:"/\\|?*]', '_', self.analysis_class)
            folder_name = f"{clean_class_name}_{timestamp}_统计图表"
            
            # 在程序目录下创建文件夹
            save_dir = os.path.join(self.app_directory, folder_name)
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存所有图表
            saved_files = []
            for chart_name, fig in self.charts_to_save:
                # 清理文件名
                clean_chart_name = re.sub(r'[<>:"/\\|?*]', '_', chart_name)
                file_path = os.path.join(save_dir, f"{clean_chart_name}.png")
                
                # 保存图表
                fig.savefig(file_path, dpi=300, bbox_inches='tight', 
                           facecolor='#1e1e2e', edgecolor='none')
                saved_files.append(clean_chart_name + ".png")
            
            # 保存统计摘要文本
            summary_path = os.path.join(save_dir, "统计摘要.txt")
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(self.generate_detailed_analysis())
            saved_files.append("统计摘要.txt")
            
            # 保存原始数据
            data_path = os.path.join(save_dir, f"{clean_class_name}_数据.xlsx")
            self.analysis_data.to_excel(data_path, index=False, engine='openpyxl')
            saved_files.append(f"{clean_class_name}_数据.xlsx")
            
            # 显示成功消息
            success_msg = f"✅ 图表保存成功！\n\n"
            success_msg += f"📁 保存位置: {save_dir}\n\n"
            success_msg += f"📊 保存文件:\n"
            for file_name in saved_files:
                success_msg += f"  • {file_name}\n"
            
            messagebox.showinfo("🎉 保存成功", success_msg)
            
            # 更新状态
            self.status_var.set(f"📊 图表已保存到: {folder_name}")
            
            # 询问是否打开文件夹
            if messagebox.askyesno("📂 打开文件夹", "是否要打开保存的文件夹？"):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(save_dir)
                    elif os.name == 'posix':  # macOS and Linux
                        import sys
                        os.system(f'open "{save_dir}"' if sys.platform == 'darwin' else f'xdg-open "{save_dir}"')
                except:
                    pass
            
        except Exception as e:
            messagebox.showerror("❌ 保存失败", f"保存图表时出错: {str(e)}")
            print(f"保存图表失败: {e}")

    def generate_detailed_analysis(self):
        """生成详细的班级分析报告"""
        if not hasattr(self, 'analysis_data') or self.analysis_data.empty:
            return "当前没有数据可分析"
            
        data = self.analysis_data
        class_name = self.analysis_class
            
        analysis = f"📊 {class_name} 详细统计报告\n"
        analysis += "=" * 50 + "\n\n"
        
        # 基本信息
        analysis += "📋 基本信息:\n"
        analysis += f"• 班级名称: {class_name}\n"
        analysis += f"• 学生总数: {len(data)}人\n"
        analysis += f"• 统计时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        analysis += f"• 成绩比例: 实验:{self.ratios[0]} : 课堂:{self.ratios[1]} : 期末:{self.ratios[2]}\n\n"
        
        if '总成绩' in data.columns:
            total_scores = data['总成绩'].dropna()
            
            # 总体统计
            analysis += "📈 总成绩统计:\n"
            analysis += f"• 平均分: {total_scores.mean():.2f}分\n"
            analysis += f"• 中位数: {total_scores.median():.2f}分\n"
            analysis += f"• 最高分: {total_scores.max():.2f}分\n"
            analysis += f"• 最低分: {total_scores.min():.2f}分\n"
            analysis += f"• 标准差: {total_scores.std():.2f}分\n"
            analysis += f"• 分数范围: {total_scores.max() - total_scores.min():.2f}分\n\n"
            
            # 等级分布
            excellent = len(total_scores[total_scores >= 90])
            good = len(total_scores[(total_scores >= 80) & (total_scores < 90)])
            medium = len(total_scores[(total_scores >= 70) & (total_scores < 80)])
            pass_count = len(total_scores[(total_scores >= 60) & (total_scores < 70)])
            fail = len(total_scores[total_scores < 60])
            total_students = len(total_scores)
            
            analysis += "🎯 成绩等级分布:\n"
            analysis += f"• 优秀(90+): {excellent}人 ({excellent/total_students*100:.1f}%)\n"
            analysis += f"• 良好(80-89): {good}人 ({good/total_students*100:.1f}%)\n"
            analysis += f"• 中等(70-79): {medium}人 ({medium/total_students*100:.1f}%)\n"
            analysis += f"• 及格(60-69): {pass_count}人 ({pass_count/total_students*100:.1f}%)\n"
            analysis += f"• 不及格(<60): {fail}人 ({fail/total_students*100:.1f}%)\n"
            analysis += f"• 及格率: {(total_students-fail)/total_students*100:.1f}%\n\n"
            
            # 各科成绩分析
            score_cols = ['实验平均分', '课堂表现', '期末成绩']
            available_score_cols = [col for col in score_cols if col in data.columns]
            
            if available_score_cols:
                analysis += "📊 各科成绩分析:\n"
                for col in available_score_cols:
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        analysis += f"• {col}:\n"
                        analysis += f"  - 平均分: {col_data.mean():.2f}分\n"
                        analysis += f"  - 最高分: {col_data.max():.2f}分\n"
                        analysis += f"  - 最低分: {col_data.min():.2f}分\n"
                        analysis += f"  - 标准差: {col_data.std():.2f}分\n"
                analysis += "\n"
            
            # 前三名和后三名
            sorted_data = data.sort_values('总成绩', ascending=False).reset_index(drop=True)
            
            analysis += "🏆 成绩排名:\n"
            analysis += "前三名:\n"
            for i in range(min(3, len(sorted_data))):
                row = sorted_data.iloc[i]
                name = row.get('姓名', 'N/A')
                score = row.get('总成绩', 0)
                analysis += f"  {i+1}. {name}: {score:.2f}分\n"
            
            if len(sorted_data) > 3:
                analysis += "\n后三名:\n"
                for i in range(max(0, len(sorted_data)-3), len(sorted_data)):
                    row = sorted_data.iloc[i]
                    name = row.get('姓名', 'N/A')
                    score = row.get('总成绩', 0)
                    rank = i + 1
                    analysis += f"  {rank}. {name}: {score:.2f}分\n"
            
            analysis += "\n"
        
        return analysis
    
    # === 以下是原有的其他方法 ===
    
    def load_sample_data(self):
        """加载示例数据"""
        sample_data = {
            '序号': list(range(1, 40)),
            '学号': ['220951038', '240951001', '240951002', '240951003', '240951004', 
                    '240951005', '240951006', '240951007', '240951008', '240951009',
                    '240951010', '240951011', '240951012', '240951013', '240951014',
                    '240951015', '240951016', '240951017', '240951018', '240951019',
                    '240951020', '240951021', '240951022', '240951023', '240951024',
                    '240951025', '240951026', '240951027', '240951028', '240951029',
                    '240951030', '240951031', '240951032', '240951033', '240951034',
                    '240951035', '240951036', '240951037', '240951039'],
            '姓名': ['张洋', '赵诗怡', '乔佳莹', '吴雅诗', '镇欣', '袁紫威', '谭薇', '刘迅',
                    '曹伶俐', '常姿', '孔艺阳', '陈乐儿', '蒋梦佳', '吕宇杰', '陈若然',
                    '夏雨欣', '李师', '程思语', '王鹏', '易子洁', '林芷芯', '袁梦',
                    '朱雅丽', '梅唐甜', '姚昌琦', '郑铭潇', '訾雪莲', '羊引舅',
                    '邓佳佳', '马畅', '张宁', '周阳', '喻超越', '南德利', '黄璜',
                    '叶佳', '李幸兰', '朱玲', '刘佳明'],
            '实验一': [75, 90, 70, 65, 90, 80, 70, 70, 83, 90, 90, 88, 70, 60, 90,
                     60, 55, 60, 55, 60, 55, 55, 60, 80, 90, 93, 92, 93, 75, 70,
                     55, 78, 65, 79, 93, 90, 87, 95, 75],
            '实验二': [80, 97, 75, 61, 95, 63, 61, 60, 94, 85, 88, 89, 84, 76, 92,
                     64, 82, 75, 65, 75, 65, 65, 70, 74, 90, 90, 95, 95, 83, 69,
                     65, 95, 63, 78, 94, 89, 90, 88, 88],
            '实验三': [75, 89, 80, 66, 92, 75, 80, 80, 80, 88, 90, 87, 82, 66, 88,
                     68, 85, 66, 70, 70, 70, 66, 70, 75, 90, 88, 93, 94, 80, 80,
                     66, 85, 66, 75, 90, 93, 88, 92, 75],
            '实验四': [70, 92, 86, 72, 90, 78, 76, 78, 80, 84, 92, 90, 92, 70, 92,
                     78, 84, 76, 70, 82, 80, 68, 74, 88, 90, 88, 90, 94, 90, 84,
                     72, 92, 68, 82, 92, 96, 90, 90, 68],
            '课堂表现': [66, 85, 76, 66, 72, 70, 67, 65, 82, 92, 95, 78, 80, 92, 83,
                      65, 78, 70, 65, 84, 63, 62, 84, 83, 98, 98, 98, 95, 85, 63,
                      85, 66, 64, 63, 99, 95, 88, 86, 72],
            '期末成绩': [64, 70, 79, 63.5, 72.5, 87, 75.5, 78.5, 80.5, 73, 75, 66,
                      74, 87, 68.5, 57.5, 65.5, 73, 70, 70.5, 68.5, 71, 67, 56,
                      96, 85, 84, 55.5, 80, 67, 93, 69, 63, 61.5, 55, 58, 72, 80, 60]
        }
        
        self.current_data = pd.DataFrame(sample_data)
        self.classes['24酒管1班(专升本)'] = self.current_data.copy()
        self.current_class = '24酒管1班(专升本)'
        self.class_combo['values'] = list(self.classes.keys())
        self.class_combo.set(self.current_class)
        
        self.calculate_scores()
        self.update_display()
        self.status_var.set("🎓 示例数据加载完成，欢迎使用 Wangci_学生成绩综合管理系统！")
        self.data_source_var.set("📋 示例数据")
    
    def load_persistent_data(self):
        """加载持久化数据，如果没有则使用示例数据"""
        auto_save_file = os.path.join(self.app_directory, "grade_system_auto_save.json")
        
        if os.path.exists(auto_save_file):
            try:
                with open(auto_save_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                
                # 恢复班级数据
                self.classes = {}
                for class_name, class_data in saved_data.get('classes', {}).items():
                    self.classes[class_name] = pd.DataFrame(class_data)
                
                # 恢复当前班级和比例设置
                self.current_class = saved_data.get('current_class')
                self.ratios = saved_data.get('ratios', [2, 4, 4])
                
                # 设置比例显示
                self.ratio1_var.set(str(self.ratios[0]))
                self.ratio2_var.set(str(self.ratios[1]))
                self.ratio3_var.set(str(self.ratios[2]))
                
                if self.classes and self.current_class in self.classes:
                    self.current_data = self.classes[self.current_class].copy()
                    self.class_combo['values'] = list(self.classes.keys())
                    self.class_combo.set(self.current_class)
                    self.calculate_scores()
                    self.update_display()
                    self.status_var.set(f"📂 已加载保存的数据 - 当前班级: {self.current_class}")
                    self.data_source_var.set("💾 已保存数据")
                else:
                    self.load_sample_data()
                
            except Exception as e:
                print(f"加载保存数据失败: {e}")
                self.load_sample_data()
        else:
            self.load_sample_data()
    
    def auto_save_data(self):
        """自动保存数据"""
        if not self.classes:
            return
            
        try:
            auto_save_file = os.path.join(self.app_directory, "grade_system_auto_save.json")
            save_data = {
                'classes': {},
                'current_class': self.current_class,
                'ratios': self.ratios,
                'save_time': datetime.now().isoformat()
            }
            
            # 转换DataFrame为字典
            for class_name, data in self.classes.items():
                save_data['classes'][class_name] = data.to_dict()
            
            with open(auto_save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # 更新数据源指示器
            if hasattr(self, 'data_source_var'):
                self.data_source_var.set("💾 已自动保存")
                
        except Exception as e:
            print(f"自动保存失败: {e}")
        
    def calculate_scores(self):
        """根据比例计算成绩"""
        if self.current_data.empty:
            return
            
        # 计算实验平均分
        exp_cols = ['实验一', '实验二', '实验三', '实验四']
        if all(col in self.current_data.columns for col in exp_cols):
            self.current_data['实验平均分'] = self.current_data[exp_cols].mean(axis=1).round(1)
        
        # 根据比例计算加权分数
        total_ratio = sum(self.ratios)
        if '实验平均分' in self.current_data.columns and '课堂表现' in self.current_data.columns and '期末成绩' in self.current_data.columns:
            self.current_data['实验加权分'] = (self.current_data['实验平均分'] * self.ratios[0] / total_ratio).round(1)
            self.current_data['课堂加权分'] = (self.current_data['课堂表现'] * self.ratios[1] / total_ratio).round(1)
            self.current_data['期末加权分'] = (self.current_data['期末成绩'] * self.ratios[2] / total_ratio).round(1)
            
            # 计算总成绩
            self.current_data['总成绩'] = (
                self.current_data['实验加权分'] + 
                self.current_data['课堂加权分'] + 
                self.current_data['期末加权分']
            ).round(1)
            
        # 更新班级数据
        if self.current_class:
            self.classes[self.current_class] = self.current_data.copy()
    
    def apply_ratios(self):
        """应用新的比例设置"""
        try:
            self.ratios = [
                float(self.ratio1_var.get()),
                float(self.ratio2_var.get()),
                float(self.ratio3_var.get())
            ]
            self.calculate_scores()
            self.update_display()
            self.status_var.set(f"✅ 比例已更新: {':'.join(map(str, self.ratios))}")
            self.auto_save_data()  # 自动保存
        except ValueError:
            messagebox.showerror("❌ 错误", "请输入有效的数字比例")
            self.status_var.set("❌ 比例更新失败")
    
    def update_display(self):
        """更新表格显示"""
        if self.current_data.empty:
            return
            
        # 清空当前数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 设置列
        columns = list(self.current_data.columns)
        self.tree['columns'] = columns
        
        # 定义表格标签样式 - 使用基本配置
        self.tree.tag_configure('excellent', background='#a6e3a1', foreground='#1e1e2e')  # 绿色 - 优秀
        self.tree.tag_configure('good', background='#89b4fa', foreground='#1e1e2e')       # 蓝色 - 良好
        self.tree.tag_configure('medium', background='#fab387', foreground='#1e1e2e')     # 橙色 - 中等
        self.tree.tag_configure('pass', background='#f9e2af', foreground='#1e1e2e')       # 黄色 - 及格
        self.tree.tag_configure('fail', background='#f38ba8', foreground='#1e1e2e')       # 红色 - 不及格
        self.tree.tag_configure('normal', background='#313244', foreground='#cdd6f4')     # 默认行
        
        # 配置树形视图的基本样式
        try:
            # 尝试设置基本样式
            self.tree.configure(style='Treeview')
        except:
            # 如果样式失败，使用默认配置
            pass
        
        # 可排序的列
        sortable_columns = ['实验平均分', '课堂表现', '期末成绩', '总成绩']
        
        # 配置列
        for col in columns:
            # 为可排序列添加排序符号
            if col in sortable_columns:
                sort_symbol = " ▲▼" if col not in self.sort_reverse else (" ▼" if self.sort_reverse[col] else " ▲")
                display_text = f"{col}{sort_symbol}"
            else:
                display_text = col
                
            self.tree.heading(col, text=display_text, command=lambda c=col: self.sort_by_column(c))
            
            if col in ['学号']:
                self.tree.column(col, width=100, anchor='center')
            elif col in ['姓名']:
                self.tree.column(col, width=80, anchor='center')
            elif col in ['总成绩']:
                self.tree.column(col, width=120, anchor='center')
            elif col in sortable_columns:
                self.tree.column(col, width=90, anchor='center')
            else:
                self.tree.column(col, width=70, anchor='center')
        
        # 插入数据
        for index, row in self.current_data.iterrows():
            values = []
            tag = 'normal'
            
            for col in columns:
                val = row[col]
                if pd.notna(val):
                    if col == '总成绩':
                        score = float(val)
                        if score >= 90:
                            values.append(f"{score:.1f} 🏆")
                            tag = 'excellent'
                        elif score >= 80:
                            values.append(f"{score:.1f} 🥈")
                            tag = 'good'
                        elif score >= 70:
                            values.append(f"{score:.1f} 🥉")
                            tag = 'medium'
                        elif score >= 60:
                            values.append(f"{score:.1f} ✅")
                            tag = 'pass'
                        else:
                            values.append(f"{score:.1f} ❌")
                            tag = 'fail'
                    else:
                        values.append(str(val))
                else:
                    values.append('')
            
            # 插入行并设置标签
            self.tree.insert('', 'end', values=values, tags=(tag,))
    
    def sort_by_column(self, col):
        """按列排序"""
        if col not in ['实验平均分', '课堂表现', '期末成绩', '总成绩']:
            return
            
        # 切换排序方向
        self.sort_reverse[col] = not self.sort_reverse.get(col, False)
        
        # 提取数值进行排序
        def sort_key(row):
            val = row[col]
            if pd.isna(val):
                return -999 if self.sort_reverse[col] else 999
            return float(val)
        
        # 执行排序
        self.current_data = self.current_data.sort_values(
            by=col, 
            ascending=not self.sort_reverse[col],
            na_position='last' if not self.sort_reverse[col] else 'first'
        ).reset_index(drop=True)
        
        # 更新序号
        self.current_data['序号'] = range(1, len(self.current_data) + 1)
        
        # 更新班级数据
        if self.current_class:
            self.classes[self.current_class] = self.current_data.copy()
        
        # 刷新显示
        self.update_display()
        
        # 更新状态
        direction = "降序" if self.sort_reverse[col] else "升序"
        self.status_var.set(f"📊 已按 {col} {direction} 排序")
        self.auto_save_data()  # 自动保存
    
    def on_cell_edit(self, event):
        """处理单元格编辑"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
            
        column = self.tree.identify_column(event.x)
        if not column:
            return
            
        # 获取列名
        col_index = int(column.replace('#', '')) - 1
        if col_index < 0 or col_index >= len(self.tree['columns']):
            return
            
        col_name = self.tree['columns'][col_index]
        
        # 只允许编辑原始成绩列
        editable_cols = ['实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩', '姓名']
        if col_name not in editable_cols:
            messagebox.showinfo("提示", f"列 '{col_name}' 不可编辑")
            return
            
        # 获取当前值
        current_value = self.tree.item(item, 'values')[col_index]
        
        # 创建编辑对话框
        new_value = simpledialog.askstring("编辑", f"编辑 {col_name}:", initialvalue=current_value)
        if new_value is None:
            return
            
        # 更新数据
        row_index = self.tree.index(item)
        try:
            if col_name in ['实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩']:
                new_value = float(new_value)
            self.current_data.iloc[row_index, self.current_data.columns.get_loc(col_name)] = new_value
            
            # 重新计算和显示
            self.calculate_scores()
            self.update_display()
            self.status_var.set(f"📚 已更新 {col_name}: {new_value}")
            self.auto_save_data()  # 自动保存
            
        except ValueError:
            messagebox.showerror("❌ 错误", "请输入有效的数值")
            self.status_var.set("❌ 数据更新失败")
    
    def import_file(self):
        """导入文件 - 增加AI处理选项"""
        file_path = filedialog.askopenfilename(
            title="📁 选择要导入的文件",
            filetypes=[
                ("Excel文件", "*.xlsx *.xls"),
                ("CSV文件", "*.csv"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            self.status_var.set("📤 正在导入文件...")
            self.root.update()
            
            if file_path.endswith(('.xlsx', '.xls')):
                data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                data = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.endswith('.json'):
                data = pd.read_json(file_path)
            else:
                messagebox.showerror("❌ 错误", "不支持的文件格式")
                return
            
            # 检查数据格式是否符合要求
            required_columns = ['序号', '学号', '姓名', '实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩']
            if not all(col in data.columns for col in required_columns):
                # 数据格式不标准，询问是否使用AI转换
                use_ai = messagebox.askyesno("🤖 格式转换", 
                                           "导入的数据格式不标准，是否使用AI自动转换格式？\n\n"
                                           "选择'是'：使用AI转换（需要API密钥）\n"
                                           "选择'否'：直接导入原始数据")
                
                if use_ai:
                    # 使用AI处理数据
                    processed_data = self.process_import_with_ai(data)
                    if processed_data is not None:
                        data = processed_data
                    else:
                        return  # AI处理失败
                        
            # 创建新班级
            class_name = simpledialog.askstring("📚 班级名称", "请输入班级名称:")
            if class_name:
                self.classes[class_name] = data
                self.current_class = class_name
                self.current_data = data.copy()
                
                # 更新班级选择器
                self.class_combo['values'] = list(self.classes.keys())
                self.class_combo.set(class_name)
                
                self.calculate_scores()
                self.update_display()
                self.status_var.set(f"✅ 文件导入成功: {os.path.basename(file_path)}")
                self.auto_save_data()  # 自动保存
                
        except Exception as e:
            messagebox.showerror("❌ 导入错误", f"导入文件时出错: {str(e)}")
            self.status_var.set("❌ 文件导入失败")
    
    def process_import_with_ai(self, data):
        """使用AI处理导入的数据"""
        # 加载API设置
        self.load_api_settings()
        
        if not self.gemini_api_key:
            messagebox.showerror("❌ 错误", "未设置AI API密钥，请先在AI助手中配置")
            return None
        
        try:
            # 将数据转换为CSV格式供AI处理
            csv_content = data.to_csv(index=False)
            
            # 构建AI请求
            prompt = f"""请将下面的学生数据转换为标准格式。

导入的数据：
{csv_content}

转换要求：
1. 保持所有学生姓名和原始成绩完全不变
2. 转换成CSV格式，列顺序必须是：序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩
3. 如果某列数据缺失，填入0
4. 如果列名不完全匹配，请根据含义对应
5. 序号从1开始连续编号
6. 保持所有数据的真实性，不要修改任何学生信息

请直接返回标准CSV格式，第一行为列标题：
序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩

重要：绝对不要修改学生姓名和成绩，只做格式转换！"""
            
            # 显示处理状态
            processing_window = tk.Toplevel(self.root)
            processing_window.title("🤖 AI处理中")
            processing_window.geometry("400x200")
            processing_window.configure(bg='#1e1e2e')
            processing_window.transient(self.root)
            processing_window.grab_set()
            
            status_label = tk.Label(processing_window, text="🤖 AI正在转换数据格式...\n请稍候",
                                  font=('Arial', 12),
                                  fg='#cdd6f4', bg='#1e1e2e')
            status_label.pack(expand=True)
            
            processing_window.update()
            
            # 调用AI
            response = self.call_gemini_api(prompt)
            processing_window.destroy()
            
            if response.startswith("❌"):
                messagebox.showerror("❌ AI处理失败", response)
                return None
            
            # 处理AI返回的CSV数据
            from io import StringIO
            
            # 清理响应，提取CSV部分
            lines = response.strip().split('\n')
            csv_lines = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('```') and ',' in line:
                    csv_lines.append(line)
            
            if not csv_lines:
                messagebox.showerror("❌ 处理失败", "AI返回的数据格式不正确")
                return None
            
            # 确保第一行是标题
            if not csv_lines[0].startswith('序号'):
                csv_lines.insert(0, "序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩")
            
            # 创建DataFrame
            csv_content = '\n'.join(csv_lines)
            processed_data = pd.read_csv(StringIO(csv_content))
            
            # 验证必要列
            required_columns = ['序号', '学号', '姓名', '实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩']
            if not all(col in processed_data.columns for col in required_columns):
                messagebox.showerror("❌ 处理失败", f"处理后的数据仍缺少必要列")
                return None
            
            # 数据清理
            processed_data = processed_data.dropna(subset=['姓名'])
            processed_data = processed_data.reset_index(drop=True)
            processed_data['序号'] = range(1, len(processed_data) + 1)
            
            messagebox.showinfo("✅ 成功", "AI数据格式转换完成！")
            return processed_data
            
        except Exception as e:
            messagebox.showerror("❌ AI处理错误", f"AI处理数据时出错: {str(e)}")
            return None
    
    def create_new_class(self):
        """创建新班级"""
        class_name = simpledialog.askstring("➕ 新建班级", "请输入班级名称:")
        if not class_name:
            return
            
        # 创建空的数据框架
        columns = ['序号', '学号', '姓名', '实验一', '实验二', '实验三', '实验四', 
                  '课堂表现', '期末成绩']
        new_data = pd.DataFrame(columns=columns)
        
        self.classes[class_name] = new_data
        self.current_class = class_name
        self.current_data = new_data.copy()
        
        # 更新界面
        self.class_combo['values'] = list(self.classes.keys())
        self.class_combo.set(class_name)
        self.update_display()
        self.status_var.set(f"✅ 新班级创建成功: {class_name}")
        self.auto_save_data()  # 自动保存
    
    def on_class_change(self, event):
        """切换班级"""
        selected_class = self.class_var.get()
        if selected_class in self.classes:
            self.current_class = selected_class
            self.current_data = self.classes[selected_class].copy()
            self.calculate_scores()
            self.update_display()
            self.status_var.set(f"📚 当前班级: {selected_class}")
            self.auto_save_data()  # 自动保存
    
    def save_data(self):
        """保存数据"""
        if not self.classes:
            messagebox.showwarning("⚠️ 警告", "没有数据可保存")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="💾 保存数据",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set("💾 正在保存数据...")
                self.root.update()
                
                # 将所有班级数据转换为可序列化格式
                save_data = {}
                for class_name, data in self.classes.items():
                    save_data[class_name] = data.to_dict()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                    
                self.status_var.set(f"✅ 数据保存成功: {os.path.basename(file_path)}")
                messagebox.showinfo("🎉 成功", "数据保存成功!")
                
            except Exception as e:
                messagebox.showerror("❌ 保存错误", f"保存数据时出错: {str(e)}")
                self.status_var.set("❌ 数据保存失败")
    
    def export_excel(self):
        """导出到Excel"""
        if self.current_data.empty:
            messagebox.showwarning("⚠️ 警告", "没有数据可导出")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="📊 导出Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set("📊 正在导出Excel...")
                self.root.update()
                
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for class_name, data in self.classes.items():
                        data.to_excel(writer, sheet_name=class_name, index=False)
                        
                self.status_var.set(f"✅ Excel导出成功: {os.path.basename(file_path)}")
                messagebox.showinfo("🎉 成功", "Excel文件导出成功!")
                
            except Exception as e:
                messagebox.showerror("❌ 导出错误", f"导出Excel时出错: {str(e)}")
                self.status_var.set("❌ Excel导出失败")

    def load_api_settings(self):
        """加载API设置"""
        try:
            settings_file = os.path.join(self.app_directory, "ai_settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.gemini_api_key = settings.get('api_key', '')
                    self.selected_model = settings.get('selected_model', 'gemini-2.5-flash')
        except Exception as e:
            print(f"加载API设置失败: {e}")

    def save_api_settings(self):
        """保存API设置"""
        try:
            settings_file = os.path.join(self.app_directory, "ai_settings.json")
            settings = {
                'api_key': self.gemini_api_key,
                'selected_model': self.selected_model
            }
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存API设置失败: {e}")

    def show_ai_dialog(self):
        """显示AI助手对话框"""
        # 加载API设置
        self.load_api_settings()
        
        ai_window = tk.Toplevel(self.root)
        ai_window.title("🤖 AI数据格式转换助手")
        ai_window.geometry("1000x700")
        ai_window.configure(bg='#1e1e2e')
        ai_window.resizable(True, True)
        
        ai_window.transient(self.root)
        ai_window.grab_set()
        
        # 主标题区域
        title_frame = tk.Frame(ai_window, bg='#1e1e2e', height=60)
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🤖 AI数据格式转换助手",
                            font=('Arial', 18, 'bold'),
                            fg='#f38ba8', bg='#1e1e2e')
        title_label.pack(side=tk.TOP, pady=(8, 3))
        
        subtitle_label = tk.Label(title_frame, text="粘贴您的真实学生数据，AI自动转换为标准格式",
                                font=('Arial', 11),
                                fg='#89b4fa', bg='#1e1e2e')
        subtitle_label.pack(side=tk.TOP)
        
        # 创建主要内容区域
        main_content = tk.Frame(ai_window, bg='#1e1e2e')
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 左侧：配置和数据输入区域
        left_frame = tk.Frame(main_content, bg='#181825', width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # 右侧：对话显示区域
        right_frame = tk.Frame(main_content, bg='#181825')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # === 左侧内容 ===
        
        # API配置区域
        api_frame = tk.LabelFrame(left_frame, text="🔑 AI配置", 
                                bg='#181825', fg='#cdd6f4',
                                font=('Arial', 10, 'bold'), bd=2, relief='solid')
        api_frame.pack(fill=tk.X, padx=12, pady=(12, 8))
        
        # API密钥输入
        key_input_frame = tk.Frame(api_frame, bg='#181825')
        key_input_frame.pack(fill=tk.X, padx=8, pady=8)
        
        tk.Label(key_input_frame, text="API密钥:", 
                font=('Arial', 9), fg='#cdd6f4', bg='#181825').pack(anchor=tk.W, pady=(0, 3))
        
        key_var = tk.StringVar(value=self.gemini_api_key)
        key_entry = tk.Entry(key_input_frame, textvariable=key_var, width=35,
                        show="*", bg='#313244', fg='#cdd6f4', 
                        font=('Arial', 9), relief='flat', bd=4)
        key_entry.pack(fill=tk.X, pady=(0, 8))
        
        # 模型选择
        model_frame = tk.Frame(api_frame, bg='#181825')
        model_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        tk.Label(model_frame, text="模型:", 
                font=('Arial', 9), fg='#cdd6f4', bg='#181825').pack(side=tk.LEFT)
        
        self.model_var = tk.StringVar(value=self.selected_model)
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var,
                                values=list(self.available_models.keys()),
                                state="readonly", width=25, font=('Arial', 8))
        model_combo.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)
        
        # 按钮区域
        btn_frame = tk.Frame(api_frame, bg='#181825')
        btn_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        def save_and_test():
            self.gemini_api_key = key_var.get()
            self.selected_model = self.model_var.get()
            self.save_api_settings()  # 保存设置
            
            if not self.gemini_api_key:
                chat_display.insert(tk.END, "❌ 请输入API密钥\n\n")
                chat_display.see(tk.END)
                return
            
            save_test_btn['text'] = '🔄 连接中...'
            save_test_btn['state'] = 'disabled'
            ai_window.update()
            
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel(self.selected_model)
                response = model.generate_content("请回复：连接成功")
                
                if response and response.text:
                    chat_display.insert(tk.END, f"✅ 连接成功！模型：{self.available_models.get(self.selected_model)}\n\n")
                    process_btn['state'] = 'normal'
                else:
                    chat_display.insert(tk.END, "❌ 连接异常\n\n")
                    
            except ImportError:
                chat_display.insert(tk.END, "❌ 请安装：pip install google-generativeai\n\n")
            except Exception as e:
                error_msg = str(e)
                if "invalid api key" in error_msg.lower():
                    chat_display.insert(tk.END, "❌ API密钥无效\n\n")
                elif "quota" in error_msg.lower():
                    chat_display.insert(tk.END, "❌ API配额已用完\n\n")
                else:
                    chat_display.insert(tk.END, f"❌ 连接失败：{error_msg}\n\n")
            finally:
                save_test_btn['text'] = '💾 保存并测试'
                save_test_btn['state'] = 'normal'
                chat_display.see(tk.END)
        
        save_test_btn = tk.Button(btn_frame, text="💾 保存并测试", command=save_and_test,
                                bg='#89b4fa', fg='#1e1e2e', font=('Arial', 9, 'bold'),
                                relief='flat', bd=0, padx=12, pady=4)
        save_test_btn.pack(side=tk.LEFT)
        
        def show_help():
            help_text = """🔑 获取API密钥：
1. 访问：https://makersuite.google.com/app/apikey
2. 登录Google账户
3. 创建API密钥
4. 复制粘贴到上方输入框

密钥会自动保存，下次无需重新输入。"""
            chat_display.insert(tk.END, help_text + "\n\n")
            chat_display.see(tk.END)
        
        tk.Button(btn_frame, text="❓ 帮助", command=show_help,
                bg='#fab387', fg='#1e1e2e', font=('Arial', 9, 'bold'),
                relief='flat', bd=0, padx=12, pady=4).pack(side=tk.RIGHT)
        
        # 数据输入区域
        data_frame = tk.LabelFrame(left_frame, text="📋 粘贴您的真实学生数据", 
                                bg='#181825', fg='#cdd6f4',
                                font=('Arial', 10, 'bold'), bd=2, relief='solid')
        data_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        tk.Label(data_frame, text="支持Excel复制、CSV格式等各种学生数据：", 
                font=('Arial', 9), fg='#cdd6f4', bg='#181825').pack(anchor=tk.W, padx=8, pady=(8, 3))
        
        # 数据输入框
        data_input_frame = tk.Frame(data_frame, bg='#181825')
        data_input_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        
        data_text = tk.Text(data_input_frame, wrap=tk.WORD,
                        bg='#313244', fg='#cdd6f4', font=('Arial', 9),
                        relief='flat', bd=4, height=12)
        data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        data_scroll = tk.Scrollbar(data_input_frame, command=data_text.yview,
                                bg='#181825', troughcolor='#313244')
        data_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        data_text.config(yscrollcommand=data_scroll.set)
        
        # 占位符文本
        placeholder_text = """请在此粘贴您的真实学生数据...

示例格式：
学号    姓名    实验1  实验2  实验3  实验4  课堂   期末
220001  张三    85     90     88     92     85     87
220002  李四    78     82     85     80     90     85

支持各种格式：Excel表格复制、CSV、制表符分隔等"""
        
        data_text.insert(tk.END, placeholder_text)
        data_text.bind('<FocusIn>', lambda e: data_text.delete('1.0', tk.END) if data_text.get('1.0', tk.END).strip() == placeholder_text.strip() else None)
        
        # 班级名称输入
        class_input_frame = tk.Frame(data_frame, bg='#181825')
        class_input_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        tk.Label(class_input_frame, text="班级名称:", font=('Arial', 9),
                fg='#cdd6f4', bg='#181825').pack(side=tk.LEFT)
        class_name_var = tk.StringVar(value="导入班级")
        tk.Entry(class_input_frame, textvariable=class_name_var, width=20,
                bg='#313244', fg='#cdd6f4', font=('Arial', 9),
                relief='flat', bd=3).pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)
        
        # === 右侧内容 ===
        
        # 对话显示区域
        chat_frame = tk.LabelFrame(right_frame, text="💬 处理结果", 
                                bg='#181825', fg='#cdd6f4',
                                font=('Arial', 10, 'bold'), bd=2, relief='solid')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 8))
        
        # 对话显示框
        chat_display_frame = tk.Frame(chat_frame, bg='#181825')
        chat_display_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        chat_display = tk.Text(chat_display_frame, wrap=tk.WORD,
                            bg='#313244', fg='#cdd6f4', font=('Arial', 10),
                            relief='flat', bd=4, state='normal')
        chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        chat_scroll = tk.Scrollbar(chat_display_frame, command=chat_display.yview,
                                bg='#181825', troughcolor='#313244')
        chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        chat_display.config(yscrollcommand=chat_scroll.set)
        
        # 欢迎消息
        welcome_msg = f"""🤖 AI数据格式转换助手

功能：将您的真实学生数据转换为系统标准格式

使用步骤：
1. 设置API密钥并测试连接
2. 在左侧粘贴您的真实学生数据
3. 输入班级名称
4. 点击"处理数据"按钮

AI会自动识别您的数据格式，转换为标准格式并导入系统。

请先设置API密钥！
"""
        chat_display.insert(tk.END, welcome_msg)
        
        # 处理按钮
        def process_real_data():
            """处理用户的真实数据"""
            if not self.gemini_api_key:
                chat_display.insert(tk.END, "\n❌ 请先设置并测试API密钥\n\n")
                chat_display.see(tk.END)
                return
            
            user_data = data_text.get("1.0", "end-1c").strip()
            if not user_data or len(user_data) < 20 or "请在此粘贴" in user_data:
                chat_display.insert(tk.END, "\n❌ 请先粘贴您的真实学生数据\n\n")
                chat_display.see(tk.END)
                return
            
            class_name = class_name_var.get().strip()
            if not class_name:
                chat_display.insert(tk.END, "\n❌ 请输入班级名称\n\n")
                chat_display.see(tk.END)
                return
            
            # 显示处理过程
            chat_display.insert(tk.END, f"\n🔄 开始处理您的数据...\n")
            chat_display.insert(tk.END, f"班级名称：{class_name}\n")
            chat_display.insert(tk.END, "🤖 AI正在转换数据格式...\n")
            chat_display.see(tk.END)
            ai_window.update()
            
            process_btn['text'] = '🔄 处理中...'
            process_btn['state'] = 'disabled'
            
            try:
                # 构建AI请求 - 专门处理真实数据
                prompt = f"""请将下面的真实学生数据转换为CSV格式。

用户的原始数据：
{user_data}

转换要求：
1. 这是真实的学生数据，请保持所有学生姓名和原始成绩完全不变
2. 转换成CSV格式，列顺序必须是：序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩
3. 如果某列数据缺失，填入0
4. 如果列名不完全匹配，请根据含义对应（如"实验1"对应"实验一"）
5. 序号从1开始连续编号
6. 保持所有数据的真实性，不要修改任何学生信息

请直接返回标准CSV格式，第一行为列标题：
序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩

重要：绝对不要修改学生姓名和成绩，只做格式转换！"""
                
                # 调用AI
                response = self.call_gemini_api(prompt)
                
                if response.startswith("❌"):
                    chat_display.insert(tk.END, f"AI处理失败：{response}\n\n")
                    chat_display.see(tk.END)
                    return
                
                # 显示处理结果
                chat_display.insert(tk.END, f"✅ AI转换完成，正在导入系统...\n")
                chat_display.see(tk.END)
                ai_window.update()
                
                # 处理CSV数据
                success = self.process_ai_csv_response(response, class_name)
                
                if success:
                    chat_display.insert(tk.END, f"🎉 数据导入成功！\n")
                    chat_display.insert(tk.END, f"✅ 班级：{class_name}\n")
                    chat_display.insert(tk.END, f"✅ 保持了所有原始学生信息不变\n")
                    chat_display.insert(tk.END, f"✅ 数据已加载到系统，可以关闭此窗口查看\n\n")
                    
                    # 清空输入框为下次使用做准备
                    data_text.delete("1.0", tk.END)
                    data_text.insert(tk.END, placeholder_text)
                    class_name_var.set("导入班级")
                    
                else:
                    chat_display.insert(tk.END, f"❌ 数据格式处理失败\n")
                    chat_display.insert(tk.END, f"AI返回的前500字符：\n{response[:500]}...\n\n")
                    
            except Exception as e:
                chat_display.insert(tk.END, f"❌ 处理出错：{str(e)}\n\n")
            finally:
                process_btn['text'] = '🚀 处理数据'
                process_btn['state'] = 'normal'
                chat_display.see(tk.END)
        
        # 按钮区域
        button_frame = tk.Frame(right_frame, bg='#181825')
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        
        process_btn = tk.Button(button_frame, text="🚀 处理数据", command=process_real_data,
                            bg='#a6e3a1', fg='#1e1e2e', font=('Arial', 11, 'bold'),
                            relief='flat', bd=0, padx=25, pady=8, state='disabled')
        process_btn.pack(side=tk.LEFT)
        
        tk.Button(button_frame, text="❌ 关闭", command=ai_window.destroy,
                bg='#f38ba8', fg='#1e1e2e', font=('Arial', 11, 'bold'),
                relief='flat', bd=0, padx=25, pady=8).pack(side=tk.RIGHT)
        
        # 聚焦到API密钥输入框（如果为空）
        if not self.gemini_api_key:
            key_entry.focus_set()
        else:
            data_text.focus_set()

    def process_ai_csv_response(self, response, class_name):
        """处理AI返回的CSV数据并创建班级"""
        try:
            from io import StringIO
            
            # 清理响应，提取CSV部分
            lines = response.strip().split('\n')
            csv_lines = []
            
            for line in lines:
                line = line.strip()
                # 跳过注释、代码块标记等，保留CSV数据
                if line and not line.startswith('#') and not line.startswith('```') and ',' in line:
                    csv_lines.append(line)
            
            if not csv_lines:
                return False
            
            # 确保第一行是标题
            if not csv_lines[0].startswith('序号'):
                csv_lines.insert(0, "序号,学号,姓名,实验一,实验二,实验三,实验四,课堂表现,期末成绩")
            
            # 创建DataFrame
            csv_content = '\n'.join(csv_lines)
            df = pd.read_csv(StringIO(csv_content))
            
            # 验证必要列
            required_columns = ['序号', '学号', '姓名', '实验一', '实验二', '实验三', '实验四', '课堂表现', '期末成绩']
            if not all(col in df.columns for col in required_columns):
                print(f"缺少必要列，当前列：{list(df.columns)}")
                return False
            
            # 数据清理和验证
            df = df.dropna(subset=['姓名'])  # 移除没有姓名的行
            df = df.reset_index(drop=True)
            df['序号'] = range(1, len(df) + 1)  # 重新编号
            
            # 添加到系统
            self.classes[class_name] = df
            self.current_class = class_name
            self.current_data = df.copy()
            
            # 更新界面
            self.class_combo['values'] = list(self.classes.keys())
            self.class_combo.set(class_name)
            
            # 计算成绩
            self.calculate_scores()
            self.update_display()
            
            # 自动保存
            self.auto_save_data()
            
            # 更新状态
            self.status_var.set(f"🎉 成功导入真实数据: {class_name}")
            self.data_source_var.set("📋 真实数据导入")
            
            return True
            
        except Exception as e:
            print(f"处理数据时出错: {e}")
            return False

    def call_gemini_api(self, message):
        """调用真实的Gemini API"""
        if not self.gemini_api_key:
            return "❌ 请先设置有效的 Gemini API 密钥才能使用AI功能。\n\n💡 获取密钥：访问 https://makersuite.google.com/app/apikey"
            
        try:
            # Gemini API 调用
            import google.generativeai as genai
            
            # 配置API
            genai.configure(api_key=self.gemini_api_key)
            
            # 创建模型实例
            model = genai.GenerativeModel(self.selected_model)
            
            # 发送请求
            response = model.generate_content(message)
            
            return response.text
            
        except ImportError:
            return """❌ 缺少必要的库文件！
            
请安装 Google AI SDK：
pip install google-generativeai

安装完成后重启程序即可使用AI功能。"""
            
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "invalid api key" in error_msg.lower():
                return "❌ API密钥无效，请检查您的 Gemini API 密钥是否正确。"
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "⚠️ API调用次数已达上限，请稍后再试或检查您的配额。"
            elif "permission" in error_msg.lower():
                return "❌ 权限不足，请确保您的API密钥有访问所选模型的权限。"
            else:
                return f"❌ API调用出错：{error_msg}\n\n请检查网络连接和API密钥设置。"

    def on_closing(self):
        """程序关闭时保存数据"""
        self.auto_save_data()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = GradeManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()