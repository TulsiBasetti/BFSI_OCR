"""
Financial Transaction Analysis Streamlit App

Features:
- Upload & analyze Payslips, Profit & Loss, Invoices, and Bank Statements.
- Visualize data using bar charts, pie charts, and scatter plots.
- Cluster transactions (Unsupervised), extract insights (Supervised), and use API data (Semi-Supervised).
- Supports images, PDFs, and CSV files with downloadable reports.
"""

import sys
import os
import streamlit as st
import pandas as pd
from unsupervised.clustering import perform_clustering_and_visualize  
from supervised.profit_loss import process_image as process_profit_loss  
from supervised.payslip import process_payslip  
from supervised.invoice import process_invoice  
from supervised.bank_statements import process_bank_statement, plot_category_spending
from semi_supervised.api_visualization import plot_payment_mode_distribution  

st.title("Financial Transaction Analysis")

# Dropdown to select the document type
doc_type = st.selectbox("Select the document type:", ["Payslip", "Profit & Loss", "Invoice", "Bank Statement", "Semi-supervised API", "Unsupervised Data"])

# Upload image or PDF or CSV based on the selected document type
if doc_type == "Unsupervised Data":
    # Handle CSV file upload for clustering
    uploaded_file = st.file_uploader("Choose a CSV file for clustering", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Show the original DataFrame
        st.subheader("Original Data")
        st.write(df)
        
        # Check if the necessary columns exist
        if 'Amount' in df.columns and 'Description' in df.columns:
            # Perform clustering and get results
            clustered_df, bar_fig, pie_fig = perform_clustering_and_visualize(df)

            # Display the clustered DataFrame
            st.subheader("Clustered Data")
            st.write(clustered_df[['Transaction ID', 'Description', 'Amount', 'Cluster_KMeans_Mapped']])

            # Display the bar chart
            st.subheader("Transaction Count per Cluster (Bar Chart)")
            st.pyplot(bar_fig)

            # Display the pie chart
            st.subheader("Cluster Distribution in Transactions (Pie Chart)")
            st.pyplot(pie_fig)
            
            # Provide download link for the clustered CSV
            st.subheader("Download the Clustered Data")
            st.download_button(
                label="Download Clustered CSV",
                data=clustered_df.to_csv(index=False).encode('utf-8'),
                file_name="clustered_transactions.csv",
                mime="text/csv"
            )
        else:
            st.error("The uploaded file must contain 'Amount' and 'Description' columns.")

else:
    # For other document types (Payslip, Profit & Loss, Invoice, Bank Statement, API)
    uploaded_file = st.file_uploader("Choose an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])

    if doc_type == "Semi-supervised API":
        st.subheader("Visualizing API Data (Pie Chart)")
        # Call function to generate the API visualization
        img_base64 = plot_payment_mode_distribution()
        # Display image in Streamlit frontend
        st.image(f"data:image/png;base64,{img_base64}", use_container_width=True)

    elif uploaded_file is not None:
        if doc_type in ["Payslip", "Profit & Loss", "Invoice"]:
            # Handle image files
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process the image based on the selected document type
            if doc_type == "Payslip":
                # Process the payslip image
                earnings, bar_chart, pie_chart = process_payslip(image_path)

                # Display extracted earnings data as a table
                st.subheader("Extracted Data From Payslip:")
                st.dataframe(earnings)

                # Display the Bar Chart
                st.subheader("Earnings Distribution (Bar Chart):")
                st.image(bar_chart, caption="Bar Chart", use_container_width=True)

                # Display the Pie Chart
                st.subheader("Earnings Distribution (Pie Chart):")
                st.image(pie_chart, caption="Pie Chart", use_container_width=True)

            elif doc_type == "Profit & Loss":
                # Process the Profit & Loss image
                data, pie_chart, bar_chart = process_profit_loss(uploaded_file)

                # Display extracted data (as a table)
                st.subheader("Extracted Data From Profit & Loss:")
                st.dataframe(data)

                # Display the Pie Chart
                st.subheader("Business Expenses (Pie Chart):")
                st.image(pie_chart, caption="Pie Chart", use_container_width=True)

                # Display the Bar Chart
                st.subheader("Business Expenses (Bar Chart):")
                st.image(bar_chart, caption="Bar Chart", use_container_width=True)

            elif doc_type == "Invoice":
                # Process the uploaded invoice image
                df, bar_chart, line_chart, pie_chart = process_invoice(image_path)

                # Display extracted data (as a table)
                st.subheader("Extracted Data From Invoice:")
                st.dataframe(df)

                # Display the Bar Chart
                if bar_chart:
                    st.subheader("Invoice Totals (Bar Chart):")
                    st.pyplot(bar_chart)
                else:
                    st.write("No valid bar chart data.")

                # Display the Line Chart
                if line_chart:
                    st.subheader("Invoice Totals (Line Chart):")
                    st.pyplot(line_chart)
                else:
                    st.write("No valid line chart data.")

                # Display the Pie Chart
                if pie_chart:
                    st.subheader("Invoice Totals (Pie Chart):")
                    st.pyplot(pie_chart)
                else:
                    st.write("No valid pie chart data.")

        elif doc_type == "Bank Statement":
            # Handle bank statement PDF files
            temp_pdf_path = "temp_uploaded_pdf.pdf"
            # Write the uploaded PDF to a temporary file
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Process the uploaded PDF
            st.subheader("Processing the uploaded Bank Statement PDF...")
            df = process_bank_statement(temp_pdf_path)

            # Display basic data
            st.subheader("Extracted the Transaction data of First 5 Records:")
            st.dataframe(df.head())  

            # Visualize the spending distribution by category
            st.subheader("Spending Distribution In The Form of Pie Chart, Bar Graph,Scatter Plot")
            plot_category_spending(df)

            #Clean up the temporary file
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

            st.success("Bank statement processed successfully!")

    else:
        st.warning("Please upload a document to start.")
