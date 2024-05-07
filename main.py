import tkinter as tk

from plotting import without_emissions, with_symmetrical_emissions, with_asymmetrical_emissions


def run_emission():
    emission = emission_var.get()
    location = location_var.get()
    scale = scale_var.get()
    n = n_var.get()
    number_resample = number_resample_var.get()

    if emission == 1:
        without_emissions(location, scale, n, number_resample)
    elif emission == 2:
        with_symmetrical_emissions(location, scale, n, number_resample)
    elif emission == 3:
        with_asymmetrical_emissions(location, scale, n, number_resample)


root = tk.Tk()
root.title("Выбор типа выбросов")

location_var = tk.DoubleVar()
scale_var = tk.DoubleVar()
n_var = tk.IntVar()
emission_var = tk.IntVar()
number_resample_var = tk.IntVar()

tk.Label(root, text="Выберите тип выбросов:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Radiobutton(root, text="Без выбросов", variable=emission_var, value=1).grid(row=1, column=0, sticky="w", padx=10)
tk.Radiobutton(root, text="С симметричными выбросами", variable=emission_var, value=2).grid(row=2, column=0, sticky="w",
                                                                                            padx=10)
tk.Radiobutton(root, text="С ассиметричными выбросами", variable=emission_var, value=3).grid(row=3, column=0,
                                                                                             sticky="w", padx=10)

# location
tk.Label(root, text="Location:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=location_var).grid(row=4, column=1, padx=10)

# scale
tk.Label(root, text="Scale:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=scale_var).grid(row=5, column=1, padx=10)

# n
tk.Label(root, text="N:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=n_var).grid(row=6, column=1, padx=10)

# number of resample
tk.Label(root, text="Number of Resample:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=number_resample_var).grid(row=7, column=1, padx=10)

tk.Button(root, text="Запустить", command=run_emission).grid(row=8, columnspan=2, pady=10)

root.mainloop()
