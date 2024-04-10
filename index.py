import streamlit as st
import omfvista
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(layout="wide")

# Hide the Streamlit footer by injecting custom CSS
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.set_page_config(layout="wide")
col1, col2 = st.columns([3, 1])  # Creates two columns with the first being three times wider than the second

# Load the project and extract the block model
proj = omfvista.load_project("assets/test_file.omf")
vol = proj.get("Block Model")
topo = proj.get("Topography")

# Convert cell data to point data
vol_point_data = vol.cell_data_to_point_data()
# Create a slider in Streamlit for the CU_pct threshold
with col1:
    cu_pct_threshold = st.slider('CU_pct Threshold', 
                                min_value=0.0  , 
                                max_value=float(vol['CU_pct'].max()), 
                                value=float(vol['CU_pct'].mean()))

# Threshold the block model by the CU_pct value
cu_thresholded = vol_point_data.threshold(value=cu_pct_threshold, scalars='CU_pct')
# Initialize a new plotter each time to ensure it's fresh
plotter = pv.Plotter(window_size=[600, 400])
plotter.add_mesh(topo, opacity=0.5)

with col1:
    # display the size of the thresholded dataset
    st.write(f"Number of cells in thresholded dataset: {cu_thresholded.n_cells}")

    plotter.add_mesh(cu_thresholded, cmap="coolwarm", clim=[vol['CU_pct'].min(), vol['CU_pct'].max()])
    plotter.add_mesh(vol.outline(), color="k")
    plotter.view_isometric()
    plotter.add_scalar_bar("CU_pct (%)", title_font_size=22)
    plotter.background_color = 'white'
    stpyvista(plotter) # Use the stpyvista integration to render the plot in Streamlit.

with col2:
    # Plotting the histogram and threshold line
    fig, ax = plt.subplots()
    ax.hist(vol['CU_pct'], bins=50, color='skyblue', alpha=0.7)  # Adjust bin count as needed
    ax.axvline(cu_pct_threshold, color='r', linestyle='dashed', linewidth=2)
    ax.set_title('Distribution of CU_pct Values')
    ax.set_xlabel('CU_pct')
    ax.set_ylabel('Frequency')
    # Display the plot in Streamlit
    st.pyplot(fig)


