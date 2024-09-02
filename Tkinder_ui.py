import tkinter as tk
from tkinter import ttk
import pandas as pd
import joblib

# Function to update bike names based on the selected brand
def update_bike_names(event):
    selected_brand = brand_var.get()
    
    # Read the dictionary from the text file
    with open("bike_company.txt", "r") as file:
        bikes_dict = eval(file.read())
    
    # Get the bikes for the selected brand
    bike_names = bikes_dict.get(selected_brand, [])
    
    # Update the bike name Combobox
    bike_combobox['values'] = bike_names
    bike_combobox.set('')  # Clear current selection

# Function to update city names
def update_cities():
    # Read the list of cities from the text file
    with open("cities.txt", "r") as file:
        cities = eval(file.read())
    
    # Sort the cities
    cities.sort()
    
    # Update the city Combobox
    city_combobox['values'] = cities
    city_combobox.set('')  # Clear current selection

# Function to display and predict the selected details
def show_selected_info():
    selected_brand = brand_var.get()
    selected_bike = bike_var.get()
    selected_city = city_var.get()
    bike_age = float(age_var.get())
    kms_driven = int(kms_var.get())
    ownership_status = ownership_var.get()
    ownership_dict = {"First Owner": 1, "Second Owner": 2, "Third Owner": 3, "Fourth Owner": 4}
    ownership_int = ownership_dict.get(ownership_status, 1)  # Convert to integer
    cc_value = float(cc_var.get())
    
    # Create DataFrame
    test_data = pd.DataFrame({
        'bike_name': [selected_bike],
        'city': [selected_city],
        'kms_driven': [kms_driven],
        'owner': [ownership_int],
        'age': [bike_age],
        'power': [cc_value],
        'brand': [selected_brand]
    })
    binary_encoder = joblib.load('data_encoder.pkl')
    model = joblib.load('bike_price_pred_model.pkl')
    
    # Transform the data using the encoder
    test_data_encoded = binary_encoder.transform(test_data)
    
    # Predict the price
    predicted_price = model.predict(test_data_encoded)
    
    # Display the result
    result_label.config(text=f"Predicted Price: RS.{predicted_price[0]:,.2f}", bg='lightgreen')

# Function to find and display the 5 cities with the lowest prices
def find_lowest_price_in_other_cities():
    selected_brand = brand_var.get()
    selected_bike = bike_var.get()
    bike_age = float(age_var.get())
    kms_driven = int(kms_var.get())
    ownership_status = ownership_var.get()
    ownership_dict = {"First Owner": 1, "Second Owner": 2, "Third Owner": 3, "Fourth Owner": 4}
    ownership_int = ownership_dict.get(ownership_status, 1)  # Convert to integer
    cc_value = float(cc_var.get())
    
    # Read the list of cities from the text file
    with open("cities.txt", "r") as file:
        cities = eval(file.read())
    
    # Dictionary to store city and corresponding price
    city_price_dict = {}
    
    # Iterate over each city and predict the price
    for city in cities:
        # Create DataFrame for each city
        test_data = pd.DataFrame({
            'bike_name': [selected_bike],
            'city': [city],
            'kms_driven': [kms_driven],
            'owner': [ownership_int],
            'age': [bike_age],
            'power': [cc_value],
            'brand': [selected_brand]
        })
        
        # Transform the data using the encoder
        test_data_encoded = binary_encoder.transform(test_data)
        
        # Predict the price
        predicted_price = model.predict(test_data_encoded)[0]
        
        # Store city and predicted price in the dictionary
        city_price_dict[city] = predicted_price
    
    # Sort the dictionary by price and get the 5 cities with the lowest prices
    sorted_cities = sorted(city_price_dict.items(), key=lambda x: x[1])[:5]
    
    # Display the result
    lowest_price_label.config(text="Lowest Price Cities:\n" + "\n".join([f"{city}: RS.{price:,.2f}" for city, price in sorted_cities]), bg='lightblue')

# Create the main window
window = tk.Tk()
window.title("Bike and Price Predictor")
window.configure(bg='lightblue')

# Create a frame for the form with a border
frame = tk.Frame(window, bg='#f0f0f0', bd=5, relief='solid', padx=20, pady=20)
frame.pack(padx=20, pady=20)

# Label for the brand selection
label_brand = tk.Label(frame, text="Select Bike Brand:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_brand.pack(pady=5)

# List of bike brands (read from file)
with open("brand.txt", "r") as file:
    brands = eval(file.read())

# Sort the brands
brands.sort()

# Variable to store the selected brand
brand_var = tk.StringVar()

# Create a Combobox for brand selection
brand_combobox = ttk.Combobox(frame, textvariable=brand_var, font=('Arial', 12))
brand_combobox['values'] = brands
brand_combobox['state'] = 'readonly'  # Make the Combobox read-only
brand_combobox.pack(pady=5)

# Bind the brand selection to update the bike names
brand_combobox.bind("<<ComboboxSelected>>", update_bike_names)

# Label for the bike name selection
label_bike = tk.Label(frame, text="Select Bike Name:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_bike.pack(pady=5)

# Variable to store the selected bike name
bike_var = tk.StringVar()

# Create a Combobox for bike name selection
bike_combobox = ttk.Combobox(frame, textvariable=bike_var, font=('Arial', 12))
bike_combobox['state'] = 'readonly'  # Make the Combobox read-only
bike_combobox.pack(pady=5)

# Label for the city selection
label_city = tk.Label(frame, text="Select City:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_city.pack(pady=5)

# Variable to store the selected city
city_var = tk.StringVar()

# Create a Combobox for city selection
city_combobox = ttk.Combobox(frame, textvariable=city_var, font=('Arial', 12))
city_combobox['state'] = 'readonly'  # Make the Combobox read-only
city_combobox.pack(pady=5)

# Load and sort the cities
update_cities()

# Label and Entry for age of bike
label_age = tk.Label(frame, text="Enter Age of Bike (years):", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_age.pack(pady=5)
age_var = tk.StringVar()
entry_age = tk.Entry(frame, textvariable=age_var, font=('Arial', 12), bg='lightyellow', bd=2)
entry_age.pack(pady=5)

# Label and Entry for kms driven
label_kms = tk.Label(frame, text="Enter KMs Driven:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_kms.pack(pady=5)
kms_var = tk.StringVar()
entry_kms = tk.Entry(frame, textvariable=kms_var, font=('Arial', 12), bg='lightyellow', bd=2)
entry_kms.pack(pady=5)

# Label and Combobox for ownership status
label_ownership = tk.Label(frame, text="Select Ownership Status:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_ownership.pack(pady=5)
ownership_var = tk.StringVar()
ownership_combobox = ttk.Combobox(frame, textvariable=ownership_var, font=('Arial', 12))
ownership_combobox['values'] = ["First Owner", "Second Owner", "Third Owner", "Fourth Owner"]
ownership_combobox['state'] = 'readonly'
ownership_combobox.pack(pady=5)

# Label and Entry for CC of bike
label_cc = tk.Label(frame, text="Enter CC of Bike:", bg='#f0f0f0', font=('Arial', 12, 'bold'))
label_cc.pack(pady=5)
cc_var = tk.StringVar()
entry_cc = tk.Entry(frame, textvariable=cc_var, font=('Arial', 12), bg='lightyellow', bd=2)
entry_cc.pack(pady=5)

# Button to confirm the selection and predict
select_button = tk.Button(frame, text="Predict Price", command=show_selected_info, bg='lightgreen', font=('Arial', 12, 'bold'))
select_button.pack(pady=15)

# Button to find the lowest price in other cities
lowest_price_button = tk.Button(frame, text="Lowest Price in Other Cities", command=find_lowest_price_in_other_cities, bg='orange', font=('Arial', 12, 'bold'))
lowest_price_button.pack(pady=5)

# Label to display the result
result_label = tk.Label(frame, text="", bg='white', font=('Arial', 12, 'bold'))
result_label.pack(pady=15)

# Label to display the lowest prices in other cities
lowest_price_label = tk.Label(frame, text="", bg='white', font=('Arial', 12, 'bold'))
lowest_price_label.pack(pady=15)

# Run the Tkinter event loop
window.mainloop()
