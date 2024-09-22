import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Function to calculate reactor volumes
def calculate_volumes(F0, k, X):
    V_CSTR = F0 / (k * (1 - X))  # Volume for CSTR
    V_PFR = F0 / k * np.log(1 / (1 - X))  # Volume for PFR
    return V_CSTR, V_PFR

# Function to calculate conversion profile for PFR
def pfr_conversion_profile(F0, k, L):
    x = np.linspace(0, L, 100)
    conversion = 1 - np.exp(-k * x / F0)
    return x, conversion

# Function to calculate conversion as a function of volume for CSTR
def cstr_conversion_vs_volume(F0, k):
    V = np.linspace(0, 5, 100)  # reactor volume from 0 to 5 m^3
    X = 1 - np.exp(-k * F0 * V)
    return V, X

# Streamlit interface
st.title('CSTR and PFR Reactor Design Calculator')

# User inputs
F0 = st.number_input('Enter the feed rate (F0) in mol/s:', value=1.0)
k = st.number_input('Enter the reaction rate constant (k) in s^-1:', value=0.1)
X = st.number_input('Enter the target conversion (X) between 0 and 1:', value=0.5, min_value=0.0, max_value=1.0)

# Calculate volumes
V_CSTR, V_PFR = calculate_volumes(F0, k, X)
st.write(f'Volume required for CSTR: {V_CSTR:.4f} m³')
st.write(f'Volume required for PFR: {V_PFR:.4f} m³')

# Plotting the conversion profile for PFR
L = V_PFR  # Assume length is proportional to volume for simplicity
x_pfr, conversion_pfr = pfr_conversion_profile(F0, k, L)
plt.figure(figsize=(10, 5))
plt.plot(x_pfr, conversion_pfr, label='PFR Conversion Profile', color='blue')
plt.title('Conversion Profile along PFR Length')
plt.xlabel('Reactor Length (m)')
plt.ylabel('Conversion (X)')
plt.axhline(y=X, color='r', linestyle='--', label='Target Conversion')
plt.legend()
st.pyplot(plt)

# Plotting conversion vs volume for CSTR
V_cstr, X_cstr = cstr_conversion_vs_volume(F0, k)
plt.figure(figsize=(10, 5))
plt.plot(V_cstr, X_cstr, label='CSTR Conversion vs Volume', color='green')
plt.title('CSTR Conversion as a Function of Reactor Volume')
plt.xlabel('Reactor Volume (m³)')
plt.ylabel('Conversion (X)')
plt.axvline(x=V_CSTR, color='r', linestyle='--', label='CSTR Volume')
plt.axhline(y=X, color='orange', linestyle='--', label='Target Conversion')
plt.legend()
st.pyplot(plt)

st.write("### Comparison Summary")
st.write(f"The CSTR requires a volume of {V_CSTR:.4f} m³ to achieve a conversion of {X*100:.2f}%.")
st.write(f"The PFR requires a volume of {V_PFR:.4f} m³ to achieve the same conversion.")
