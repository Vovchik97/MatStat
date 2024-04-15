import tkinter as tk
import subprocess


def update_fields():
    emission = emission_var.get()
    if emission == 1:  # Без выбросов
        length_entry.grid_remove()
        number_resample_entry.grid_remove()
        N_entry.grid(row=6, column=1, padx=10)
        N_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        length_label.grid_remove()
        number_resample_label.grid_remove()
    elif emission == 2 or emission == 3:  # С выбросами
        N_entry.grid_remove()
        N_label.grid_remove()
        length_entry.grid(row=7, column=1, padx=10)
        length_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        number_resample_entry.grid(row=8, column=1, padx=10)
        number_resample_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)


def run_emission():
    emission = emission_var.get()
    # location = location_var.get()
    # scale = scale_var.get()

    if emission == 1:
        location = location_var.get()
        scale = scale_var.get()
        N = N_var.get()
        python_file = "without_emissions\\main.py"
        subprocess.run(["python", python_file, str(location), str(scale), str(N)])
    elif emission == 2:
        location = location_var.get()
        scale = scale_var.get()
        length = length_var.get()
        number_resample = number_resample_var.get()
        python_file = "symmetrical_emissions\\main.py"
        subprocess.run(["python", python_file, str(location), str(scale), str(length), str(number_resample)])
    elif emission == 3:
        location = location_var.get()
        scale = scale_var.get()
        length = length_var.get()
        number_resample = number_resample_var.get()
        python_file = "asymmetric_emissions\\main.py"
        subprocess.run(["python", python_file, str(location), str(scale), str(length), str(number_resample)])


root = tk.Tk()
root.title("Выбор типа выбросов")

emission_var = tk.IntVar()
location_var = tk.DoubleVar()
scale_var = tk.DoubleVar()
N_var = tk.IntVar()
length_var = tk.DoubleVar()
number_resample_var = tk.IntVar()

tk.Label(root, text="Выберите тип выбросов:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

tk.Radiobutton(root, text="Без выбросов", variable=emission_var, value=1, command=update_fields).grid(row=1, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=10)
tk.Radiobutton(root, text="С симметричными выбросами", variable=emission_var, value=2, command=update_fields).grid(
    row=2, column=0, sticky="w", padx=10)
tk.Radiobutton(root, text="С ассиметричными выбросами", variable=emission_var, value=3, command=update_fields).grid(
    row=3, column=0, sticky="w", padx=10)

tk.Label(root, text="Location:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=location_var).grid(row=4, column=1, padx=10)

tk.Label(root, text="Scale:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=scale_var).grid(row=5, column=1, padx=10)

N_entry = tk.Entry(root, textvariable=N_var)
N_label = tk.Label(root, text="N:")
length_entry = tk.Entry(root, textvariable=length_var)
length_label = tk.Label(root, text="Length:")
number_resample_entry = tk.Entry(root, textvariable=number_resample_var)
number_resample_label = tk.Label(root, text="Number of Resample:")

tk.Button(root, text="Запустить", command=run_emission).grid(row=9, columnspan=2, pady=10)

root.mainloop()
