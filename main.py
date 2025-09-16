#!/usr/bin/env python3
"""
Induction Motor Fault Diagnosis - Main Script
This script serves as the entry point for the motor fault diagnosis system.
"""


# واجهة رسومية بسيطة باستخدام Tkinter
import tkinter as tk
from tkinter import filedialog, messagebox


class MotorFaultGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Induction Motor Fault Diagnosis")
        self.geometry("600x700")
        self.configure(bg="#f5f6fa")

        # إطار للأزرار العلوية
        top_btn_frame = tk.Frame(self, bg="#f5f6fa")
        top_btn_frame.pack(pady=(18, 8))
        tk.Label(top_btn_frame, text="🛠️ Motor Fault Diagnosis", font=("Arial", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(0, 8))
        tk.Button(top_btn_frame, text="رفع ملف بيانات جديد وتحديث النموذج", command=self.upload_data_file, bg="#fdcb6e", fg="black", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        tk.Button(top_btn_frame, text="تصدير نتيجة التشخيص إلى PDF", command=self.export_pdf, bg="#636e72", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        tk.Button(top_btn_frame, text="عرض تقييم النموذج", command=self.show_model_evaluation, bg="#00b894", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        tk.Button(top_btn_frame, text="عرض رسم بياني للبيانات", command=self.show_data_plot, bg="#0984e3", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        tk.Button(top_btn_frame, text="اختبار النموذج على بيانات حية أو محاكاة", command=self.test_live_or_simulated, bg="#fd79a8", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)

        # إطار لإدخال البيانات اليدوية والنتيجة
        main_frame = tk.Frame(self, bg="#f5f6fa")
        main_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(main_frame, text="Step 1: Enter fault data manually", font=("Arial", 12), bg="#f5f6fa", fg="#353b48").pack(pady=(18, 2))
        tk.Label(main_frame, text="Hint: Fill all fields. Numeric fields accept numbers only. For dropdowns, select the closest value to your case.", font=("Arial", 10), bg="#f5f6fa", fg="#e17055", wraplength=500, justify="center").pack(pady=(2, 8))
        manual_frame = tk.Frame(main_frame, bg="#f5f6fa")
        manual_frame.pack(pady=5)

    def test_live_or_simulated(self):
        import pandas as pd
        import random
        from tkinter import Toplevel
        win = Toplevel(self)
        win.title("اختبار النموذج على بيانات حية أو محاكاة")
        win.geometry("480x420")
        win.configure(bg="#f5f6fa")

        tk.Label(win, text="اختبر النموذج على بيانات حية أو محاكاة", font=("Arial", 14, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=12)

        # حقول الإدخال
        fields = [
            ("current", "Current (A)", (0.5, 20)),
            ("voltage", "Voltage (V)", (110, 440)),
            ("power", "Power (W)", (50, 5000)),
            ("rpm", "RPM", (500, 3500)),
            ("vibration_level", "Vibration Level", (0, 10)),
            ("visual_damage", "Visual Damage (0/1)", (0, 1)),
            ("noise_level", "Noise Level", ["Low", "Medium", "High"]),
            ("operating_condition", "Operating Condition", ["Normal", "High Temp", "Overloaded"]),
            ("maintenance_status", "Maintenance Status", ["none", "due soon", "recent"])
        ]
        entry_vars = {}
        entry_frame = tk.Frame(win, bg="#f5f6fa")
        entry_frame.pack(pady=8)
        for i, (key, label, rng) in enumerate(fields):
            tk.Label(entry_frame, text=label, font=("Arial", 10), bg="#f5f6fa").grid(row=i, column=0, sticky="e", padx=2, pady=2)
            var = tk.StringVar()
            entry_vars[key] = var
            if isinstance(rng, tuple):
                tk.Entry(entry_frame, textvariable=var, width=10, font=("Arial", 10)).grid(row=i, column=1, padx=2, pady=2)
            else:
                tk.OptionMenu(entry_frame, var, *rng).grid(row=i, column=1, padx=2, pady=2)

        def fill_simulated():
            for key, label, rng in fields:
                if isinstance(rng, tuple):
                    val = round(random.uniform(rng[0], rng[1]), 2)
                    entry_vars[key].set(str(val))
                else:
                    entry_vars[key].set(random.choice(rng))

        tk.Button(win, text="توليد بيانات محاكاة", command=fill_simulated, bg="#00b894", fg="white", font=("Arial", 11, "bold"), width=18, cursor="hand2").pack(pady=6)

        result_label = tk.Label(win, text="", font=("Arial", 12), bg="#f5f6fa", fg="#192a56", wraplength=400, justify="center")
        result_label.pack(pady=10)

        def run_test():
            try:
                import sys
                from pathlib import Path
                sys.path.append(str(Path(__file__).parent / "src" / "models"))
                from model import train_model
                import pandas as pd
                df_train = pd.read_csv("data/motor_fault_sample_ordered.csv")
                from sklearn.preprocessing import LabelEncoder
                label_encoders = {}
                for col in ["noise_level", "operating_condition", "maintenance_status"]:
                    le = LabelEncoder()
                    df_train[col] = le.fit_transform(df_train[col])
                    label_encoders[col] = le
                feature_cols = [f[0] for f in fields]
                numeric_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]
                values = []
                for key in feature_cols:
                    val = entry_vars[key].get()
                    if val == "":
                        result_label.config(text="يرجى تعبئة جميع الحقول أو توليد بيانات محاكاة.")
                        return
                    if key in numeric_cols:
                        try:
                            values.append(float(val))
                        except ValueError:
                            result_label.config(text=f"قيمة غير صحيحة للحقل {key}: {val}")
                            return
                    elif key in ["noise_level", "operating_condition", "maintenance_status"]:
                        le = label_encoders[key]
                        try:
                            values.append(le.transform([val])[0])
                        except Exception:
                            result_label.config(text=f"قيمة غير صحيحة للحقل {key}: {val}")
                            return
                X_test = [values]
                X_train = df_train[feature_cols].values
                y_train = df_train["fault_label"].values
                model = train_model(X_train, y_train)
                prediction = model.predict(X_test)
                result_label.config(text=f"نتيجة التشخيص للبيانات المدخلة: {prediction[0]}")
            except Exception as e:
                result_label.config(text=f"حدث خطأ أثناء اختبار النموذج:\n{e}")

        tk.Button(win, text="تشخيص البيانات", command=run_test, bg="#fdcb6e", fg="black", font=("Arial", 11, "bold"), width=18, cursor="hand2").pack(pady=6)

        # إدخال البيانات يدوياً
        tk.Label(self, text="Step 1: Enter fault data manually", font=("Arial", 12), bg="#f5f6fa", fg="#353b48").pack(pady=(18, 2))
        tk.Label(self, text="Hint: Fill all fields. Numeric fields accept numbers only. For dropdowns, select the closest value to your case.", font=("Arial", 10), bg="#f5f6fa", fg="#e17055", wraplength=500, justify="center").pack(pady=(2, 8))
        manual_frame = tk.Frame(self, bg="#f5f6fa")
        manual_frame.pack(pady=5)
        self.manual_vars = {}
        fields = [
            ("current", "Current (A)"),
            ("voltage", "Voltage (V)"),
            ("power", "Power (W)"),
            ("rpm", "RPM"),
            ("vibration_level", "Vibration Level"),
            ("visual_damage", "Visual Damage (0/1)"),
            ("noise_level", "Noise Level (Low/Medium/High)"),
            ("operating_condition", "Operating Condition"),
            ("maintenance_status", "Maintenance Status")
        ]
        for i, (key, label) in enumerate(fields):
            tk.Label(manual_frame, text=label, font=("Arial", 10), bg="#f5f6fa").grid(row=i, column=0, sticky="e", padx=2, pady=2)
            var = tk.StringVar()
            if key == "power":
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10), state="readonly")
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                self.power_entry = entry
            elif key in ["noise_level"]:
                options = ["Low", "Medium", "High"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["operating_condition"]:
                options = ["Normal", "High Temp", "Overloaded"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["maintenance_status"]:
                options = ["none", "due soon", "recent"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            else:
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                if key in ["current", "voltage"]:
                    entry.bind("<KeyRelease>", self.update_power)

        # زر التشخيص اليدوي
        tk.Button(manual_frame, text="Diagnose Faults", command=self.diagnose_manual, bg="#44bd32", fg="white", font=("Arial", 13, "bold"), width=22, height=2, cursor="hand2").grid(row=len(fields), column=0, columnspan=2, pady=8)

        # نتيجة التشخيص
        self.result_label = tk.Label(self, text="", font=("Arial", 13), bg="#f5f6fa", fg="#192a56", wraplength=480, justify="center")
        self.result_label.pack(pady=18)

        # ملاحظة للمستخدم (داخل __init__)
        tk.Label(self, text="Tip: You can use the provided sample files in the data folder.\nExample: Try entering values from the CSV for accurate results.", font=("Arial", 10), bg="#f5f6fa", fg="#718093", wraplength=500, justify="center").pack(side=tk.BOTTOM, pady=8)

    def upload_data_file(self):
        from tkinter import filedialog
        import pandas as pd
        try:
            file_path = filedialog.askopenfilename(title="اختر ملف بيانات جديد", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                # دمج البيانات الجديدة مع البيانات القديمة
                df_old = pd.read_csv("data/motor_fault_sample_ordered.csv")
                df_new = pd.read_csv(file_path)
                df_merged = pd.concat([df_old, df_new], ignore_index=True)
                df_merged.to_csv("data/motor_fault_sample_ordered.csv", index=False)
                # إعادة تدريب النموذج
                from sklearn.preprocessing import LabelEncoder
                feature_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage", "noise_level", "operating_condition", "maintenance_status"]
                numeric_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]
                for col in numeric_cols:
                    df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce")
                for col in ["noise_level", "operating_condition", "maintenance_status"]:
                    le = LabelEncoder()
                    df_merged[col] = le.fit_transform(df_merged[col])
                df_merged = df_merged.dropna(subset=numeric_cols)
                X_train = df_merged[feature_cols].values
                y_train = df_merged["fault_label"].values
                import sys
                from pathlib import Path
                sys.path.append(str(Path(__file__).parent / "src" / "models"))
                from model import train_model
                model = train_model(X_train, y_train)
                messagebox.showinfo("Upload Data & Online Learning", "تم رفع الملف ودمج البيانات وتحديث النموذج بنجاح!")
        except Exception as e:
            messagebox.showerror("Error", f"حدث خطأ أثناء رفع أو دمج الملف وتحديث النموذج:\n{e}")

    def export_pdf(self):
        from fpdf import FPDF
        import datetime
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Induction Motor Fault Diagnosis Report", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="L")
            pdf.ln(8)
            pdf.cell(200, 10, txt="Diagnosis Inputs:", ln=True, align="L")
            for key, var in self.manual_vars.items():
                pdf.cell(200, 8, txt=f"{key}: {var.get()}", ln=True, align="L")
            pdf.ln(8)
            pdf.cell(200, 10, txt=f"Diagnosis Result: {self.result_label.cget('text')}", ln=True, align="L")
            pdf.output("diagnosis_report.pdf")
            messagebox.showinfo("Export PDF", "Diagnosis report exported successfully as diagnosis_report.pdf")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting PDF:\n{e}")

    def show_model_evaluation(self):
        import pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix
        import seaborn as sns
        try:
            df = pd.read_csv("data/motor_fault_sample_ordered.csv")
            feature_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage", "noise_level", "operating_condition", "maintenance_status"]
            # تحويل الأعمدة الرقمية فقط إلى float
            numeric_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            from sklearn.preprocessing import LabelEncoder
            for col in ["noise_level", "operating_condition", "maintenance_status"]:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
            # حذف الصفوف التي تحتوي على قيم غير رقمية في الأعمدة الرقمية
            df = df.dropna(subset=numeric_cols)
            X = df[feature_cols].values
            y = df["fault_label"].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            from model import train_model
            model = train_model(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(7,5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
            plt.title(f"مصفوفة الالتباس - دقة النموذج: {round(acc*100,2)}%")
            plt.xlabel("توقع النموذج")
            plt.ylabel("الحقيقة الفعلية")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while evaluating model:\n{e}")

    def show_data_plot(self):
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        try:
            df = pd.read_csv("data/motor_fault_sample_ordered.csv")
            plt.figure(figsize=(8,5))
            sns.countplot(x="fault_label", data=df)
            plt.title("توزيع أنواع الأعطال")
            plt.xlabel("نوع العطل")
            plt.ylabel("عدد الحالات")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting:\n{e}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            from model import train_model
            model = train_model(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(7,5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
            plt.title(f"مصفوفة الالتباس - دقة النموذج: {round(acc*100,2)}%")
            plt.xlabel("توقع النموذج")
            plt.ylabel("الحقيقة الفعلية")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while evaluating model:\n{e}")
    def show_data_plot(self):
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        try:
            df = pd.read_csv("data/motor_fault_sample_ordered.csv")
            plt.figure(figsize=(8,5))
            sns.countplot(x="fault_label", data=df)
            plt.title("توزيع أنواع الأعطال")
            plt.xlabel("نوع العطل")
            plt.ylabel("عدد الحالات")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting:\n{e}")
    def __init__(self):
        super().__init__()
        self.title("Induction Motor Fault Diagnosis")
        self.geometry("600x700")
        self.configure(bg="#f5f6fa")

        # عنوان رئيسي
        tk.Label(self, text="🛠️ Motor Fault Diagnosis", font=("Arial", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(18, 8))

        # زر رفع ملف بيانات جديد وتحديث النموذج
        tk.Button(self, text="رفع ملف بيانات جديد وتحديث النموذج", command=self.upload_data_file, bg="#fdcb6e", fg="black", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        # زر تصدير النتائج إلى PDF
        tk.Button(self, text="تصدير نتيجة التشخيص إلى PDF", command=self.export_pdf, bg="#636e72", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        # زر عرض تقييم النموذج
        tk.Button(self, text="عرض تقييم النموذج", command=self.show_model_evaluation, bg="#00b894", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        # زر عرض رسم بياني للبيانات
        tk.Button(self, text="عرض رسم بياني للبيانات", command=self.show_data_plot, bg="#0984e3", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)

        # إدخال البيانات يدوياً
        tk.Label(self, text="Step 1: Enter fault data manually", font=("Arial", 12), bg="#f5f6fa", fg="#353b48").pack(pady=(18, 2))
        tk.Label(self, text="Hint: Fill all fields. Numeric fields accept numbers only. For dropdowns, select the closest value to your case.", font=("Arial", 10), bg="#f5f6fa", fg="#e17055", wraplength=500, justify="center").pack(pady=(2, 8))
        manual_frame = tk.Frame(self, bg="#f5f6fa")
        manual_frame.pack(pady=5)
        self.manual_vars = {}
        fields = [
            ("current", "Current (A)"),
            ("voltage", "Voltage (V)"),
            ("power", "Power (W)"),
            ("rpm", "RPM"),
            ("vibration_level", "Vibration Level"),
            ("visual_damage", "Visual Damage (0/1)"),
            ("noise_level", "Noise Level (Low/Medium/High)"),
            ("operating_condition", "Operating Condition"),
            ("maintenance_status", "Maintenance Status")
        ]
        for i, (key, label) in enumerate(fields):
            tk.Label(manual_frame, text=label, font=("Arial", 10), bg="#f5f6fa").grid(row=i, column=0, sticky="e", padx=2, pady=2)
            var = tk.StringVar()
            if key == "power":
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10), state="readonly")
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                self.power_entry = entry
            elif key in ["noise_level"]:
                options = ["Low", "Medium", "High"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["operating_condition"]:
                options = ["Normal", "High Temp", "Overloaded"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["maintenance_status"]:
                options = ["none", "due soon", "recent"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            else:
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                if key in ["current", "voltage"]:
                    entry.bind("<KeyRelease>", self.update_power)

        # زر التشخيص اليدوي
        tk.Button(manual_frame, text="Diagnose Faults", command=self.diagnose_manual, bg="#44bd32", fg="white", font=("Arial", 13, "bold"), width=22, height=2, cursor="hand2").grid(row=len(fields), column=0, columnspan=2, pady=8)

        # نتيجة التشخيص
        self.result_label = tk.Label(self, text="", font=("Arial", 13), bg="#f5f6fa", fg="#192a56", wraplength=480, justify="center")
        self.result_label.pack(pady=18)

        # ملاحظة للمستخدم (داخل __init__)
        tk.Label(self, text="Tip: You can use the provided sample files in the data folder.\nExample: Try entering values from the CSV for accurate results.", font=("Arial", 10), bg="#f5f6fa", fg="#718093", wraplength=500, justify="center").pack(side=tk.BOTTOM, pady=8)
    def __init__(self):
        super().__init__()
        self.title("Induction Motor Fault Diagnosis")
        self.geometry("600x700")
        self.configure(bg="#f5f6fa")

        # عنوان رئيسي
        tk.Label(self, text="🛠️ Motor Fault Diagnosis", font=("Arial", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(18, 8))

        # إدخال البيانات يدوياً
        tk.Label(self, text="Step 1: Enter fault data manually", font=("Arial", 12), bg="#f5f6fa", fg="#353b48").pack(pady=(18, 2))
        tk.Label(self, text="Hint: Fill all fields. Numeric fields accept numbers only. For dropdowns, select the closest value to your case.", font=("Arial", 10), bg="#f5f6fa", fg="#e17055", wraplength=500, justify="center").pack(pady=(2, 8))
        manual_frame = tk.Frame(self, bg="#f5f6fa")
        manual_frame.pack(pady=5)
        self.manual_vars = {}
        fields = [
            ("current", "Current (A)"),
            ("voltage", "Voltage (V)"),
            ("power", "Power (W)"),
            ("rpm", "RPM"),
            ("vibration_level", "Vibration Level"),
            ("visual_damage", "Visual Damage (0/1)"),
            ("noise_level", "Noise Level (Low/Medium/High)"),
            ("operating_condition", "Operating Condition"),
            ("maintenance_status", "Maintenance Status")
        ]
        # زر عرض تقييم النموذج
        tk.Button(self, text="عرض تقييم النموذج", command=self.show_model_evaluation, bg="#00b894", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)
        # زر عرض رسم بياني للبيانات
        tk.Button(self, text="عرض رسم بياني للبيانات", command=self.show_data_plot, bg="#0984e3", fg="white", font=("Arial", 12, "bold"), width=28, height=1, cursor="hand2").pack(pady=6)

        for i, (key, label) in enumerate(fields):
            tk.Label(manual_frame, text=label, font=("Arial", 10), bg="#f5f6fa").grid(row=i, column=0, sticky="e", padx=2, pady=2)
            var = tk.StringVar()
            if key == "power":
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10), state="readonly")
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                self.power_entry = entry
            elif key in ["noise_level"]:
                options = ["Low", "Medium", "High"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["operating_condition"]:
                options = ["Normal", "High Temp", "Overloaded"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            elif key in ["maintenance_status"]:
                options = ["none", "due soon", "recent"]
                tk.OptionMenu(manual_frame, var, *options).grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
            else:
                entry = tk.Entry(manual_frame, textvariable=var, width=10, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=2, pady=2)
                self.manual_vars[key] = var
                if key in ["current", "voltage"]:
                    entry.bind("<KeyRelease>", self.update_power)

        # زر التشخيص اليدوي
        tk.Button(manual_frame, text="Diagnose Faults", command=self.diagnose_manual, bg="#44bd32", fg="white", font=("Arial", 13, "bold"), width=22, height=2, cursor="hand2").grid(row=len(fields), column=0, columnspan=2, pady=8)


        # نتيجة التشخيص
        self.result_label = tk.Label(self, text="", font=("Arial", 13), bg="#f5f6fa", fg="#192a56", wraplength=480, justify="center")
        self.result_label.pack(pady=18)

        # ملاحظة للمستخدم (داخل __init__)
        tk.Label(self, text="Tip: You can use the provided sample files in the data folder.\nExample: Try entering values from the CSV for accurate results.", font=("Arial", 10), bg="#f5f6fa", fg="#718093", wraplength=500, justify="center").pack(side=tk.BOTTOM, pady=8)

    # دالة لحساب وتحديث القدرة تلقائياً
    def update_power(self, event=None):
        try:
            current = float(self.manual_vars["current"].get())
            voltage = float(self.manual_vars["voltage"].get())
            power = current * voltage
            self.manual_vars["power"].set(str(round(power, 3)))
        except ValueError:
            self.manual_vars["power"].set("")


    def diagnose_manual(self):
        self.result_label.config(text="")
        try:
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent / "src" / "models"))
            from model import train_model
            import pandas as pd
            # قراءة بيانات التدريب من ملف CSV
            df_train = pd.read_csv("data/motor_fault_sample_ordered.csv")
            # ترميز الأعمدة النصية
            from sklearn.preprocessing import LabelEncoder
            label_encoders = {}
            for col in ["noise_level", "operating_condition", "maintenance_status"]:
                le = LabelEncoder()
                df_train[col] = le.fit_transform(df_train[col])
                label_encoders[col] = le
            feature_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage", "noise_level", "operating_condition", "maintenance_status"]
            numeric_cols = ["current", "voltage", "power", "rpm", "vibration_level", "visual_damage"]
            def is_valid_row(row):
                try:
                    for col in numeric_cols:
                        float(row[col])
                    return True
                except:
                    return False
            df_train = df_train[df_train.apply(is_valid_row, axis=1)]
            # جمع البيانات المدخلة
            values = []
            manual_row = {}
            for key in feature_cols:
                if key == "power":
                    try:
                        current = float(self.manual_vars["current"].get())
                        voltage = float(self.manual_vars["voltage"].get())
                        power = current * voltage
                        self.manual_vars["power"].set(str(power))
                        values.append(power)
                        manual_row[key] = power
                    except ValueError:
                        self.result_label.config(text="Please enter valid numbers for current and voltage to calculate power.")
                        return
                else:
                    val = self.manual_vars[key].get()
                    if val == "":
                        self.result_label.config(text="Please fill all manual fields.")
                        return
                    if key in ["current", "voltage", "rpm", "vibration_level"]:
                        try:
                            values.append(float(val))
                            manual_row[key] = float(val)
                        except ValueError:
                            self.result_label.config(text=f"Invalid value for {key}: {val}. Please enter a number.")
                            return
                    elif key == "visual_damage":
                        try:
                            values.append(int(val))
                            manual_row[key] = int(val)
                        except ValueError:
                            self.result_label.config(text=f"Invalid value for {key}: {val}. Please enter 0 or 1.")
                            return
                    elif key in ["noise_level", "operating_condition", "maintenance_status"]:
                        le = label_encoders[key]
                        try:
                            encoded_val = le.transform([val])[0]
                            values.append(encoded_val)
                            manual_row[key] = val
                        except Exception:
                            self.result_label.config(text=f"Invalid value for {key}: {val}.")
                            return
            # إضافة نتيجة التشخيص (fault_label) كقيمة فارغة مؤقتاً
            manual_row["fault_label"] = "manual_entry"
            # إضافة الصف الجديد إلى ملف التدريب
            df_train_orig = pd.read_csv("data/motor_fault_sample_ordered.csv")
            df_train_orig = pd.concat([df_train_orig, pd.DataFrame([manual_row])], ignore_index=True)
            df_train_orig.to_csv("data/motor_fault_sample_ordered.csv", index=False)
            # إعادة تدريب النموذج
            X_train = df_train[feature_cols].values
            y_train = df_train["fault_label"].values
            import numpy as np
            X_test = np.array([values], dtype=object)
            model = train_model(X_train, y_train)
            prediction = model.predict(X_test)
            # تحديث نتيجة التشخيص في ملف التدريب
            df_train_orig.iloc[-1, df_train_orig.columns.get_loc("fault_label")] = prediction[0]
            df_train_orig.to_csv("data/motor_fault_sample_ordered.csv", index=False)
            self.result_label.config(text=f"Manual Diagnosis result: {prediction[0]}")
            messagebox.showinfo("Online Learning", "تم تحديث النموذج وإضافة البيانات الجديدة بنجاح!")
        except Exception as e:
            self.result_label.config(text="")
            messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    app = MotorFaultGUI()
    app.mainloop()
