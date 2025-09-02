import time
import random
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def wait_for_tatkal():
    now = datetime.datetime.now()
    target = now.replace(hour=10, minute=0, second=35, microsecond=0)
    if now > target:
        return
    print("⏳ Waiting for Tatkal booking to open...")
    while datetime.datetime.now() < target:
        time.sleep(0.5)

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

class TatkalWarriorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tatkal Warrior – Pro Autofill")
        self.root.geometry("800x500")
        self.passengers = []
        tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(root, text="Age").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(root, text="Gender").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(root, text="Berth").grid(row=0, column=3, padx=5, pady=5)
        tk.Label(root, text="Mobile").grid(row=0, column=4, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.berth_var = tk.StringVar()
        self.mobile_var = tk.StringVar()
        tk.Entry(root, textvariable=self.name_var).grid(row=1, column=0)
        tk.Entry(root, textvariable=self.age_var, width=5).grid(row=1, column=1)
        ttk.Combobox(root, textvariable=self.gender_var, values=["Male","Female","Other"], width=8).grid(row=1, column=2)
        ttk.Combobox(root, textvariable=self.berth_var, values=["Lower","Middle","Upper","Side Lower","Side Upper"], width=12).grid(row=1, column=3)
        tk.Entry(root, textvariable=self.mobile_var, width=12).grid(row=1, column=4)
        tk.Button(root, text="➕ Add Passenger", command=self.add_passenger).grid(row=2, column=0, pady=10)
        tk.Button(root, text="▶ Start Booking", command=self.start_booking).grid(row=2, column=1, pady=10)
        self.passenger_list = tk.Listbox(root, width=120)
        self.passenger_list.grid(row=3, column=0, columnspan=6, pady=10)

    def add_passenger(self):
        passenger = {
            "name": self.name_var.get(),
            "age": self.age_var.get(),
            "gender": self.gender_var.get(),
            "berth": self.berth_var.get(),
            "mobile": self.mobile_var.get(),
        }
        self.passengers.append(passenger)
        self.passenger_list.insert(tk.END, f"{passenger['name']} | {passenger['age']} | {passenger['gender']} | {passenger['berth']} | {passenger['mobile']}")
        self.clear_form()

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.berth_var.set("")
        self.mobile_var.set("")

    def start_booking(self):
        if not self.passengers:
            messagebox.showerror("Error", "Please add at least one passenger!")
            return
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.maximize_window()
            driver.get("https://www.irctc.co.in/nget/train-search")
            messagebox.showinfo("IRCTC", "Login manually and press OK when ready!")
            wait_for_tatkal()
            for idx, p in enumerate(self.passengers):
                try:
                    name_box = driver.find_element(By.ID, f"addPassengerForm:psdetail:{idx}:psgnName")
                    human_typing(name_box, p["name"])
                    age_box = driver.find_element(By.ID, f"addPassengerForm:psdetail:{idx}:psgnAge")
                    human_typing(age_box, p["age"])
                    gender_dropdown = driver.find_element(By.ID, f"addPassengerForm:psdetail:{idx}:psgnGender")
                    gender_dropdown.send_keys(p["gender"][0])
                    berth_dropdown = driver.find_element(By.ID, f"addPassengerForm:psdetail:{idx}:berthChoice")
                    berth_dropdown.send_keys(p["berth"][0])
                except Exception as e:
                    print("Passenger autofill error:", e)
            try:
                mob_box = driver.find_element(By.ID, "mobileNo")
                mob_box.clear()
                human_typing(mob_box, self.passengers[0]["mobile"])
            except:
                pass
            messagebox.showinfo("Tatkal Warrior", "Passenger autofill done! Please solve captcha manually.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TatkalWarriorApp(root)
    root.mainloop()
