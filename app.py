import streamlit as st
import pandas as pd
from unsupervised.clustering import perform_clustering_and_visualize  
from supervised.profit_loss import process_image as process_profit_loss  
from supervised.payslip import process_payslip  
from supervised.invoice import process_invoice  
from supervised.bank_statements import process_bank_statement, plot_category_spending
from semi_supervised.api_visualization import plot_payment_mode_distribution  
import os

st.title("Financial Transaction Analysis")

# Step 1: Dropdown to select the document type
doc_type = st.selectbox("Select the document type:", ["Payslip", "Profit & Loss", "Invoice", "Bank Statement", "Semi-supervised API", "Unsupervised Data"])

# Step 2: File upload conditionally based on document type
if doc_type == "Unsupervised Data":
    uploaded_file = st.file_uploader("Choose a CSV file for clustering", type="csv", key="file_uploader")
elif doc_type == "Payslip":
    uploaded_file = st.file_uploader("Choose an image or PDF for Payslip", type=["jpg", "jpeg", "png", "pdf"], key="file_uploader")
elif doc_type == "Profit & Loss":
    uploaded_file = st.file_uploader("Choose an image or PDF for Profit & Loss", type=["jpg", "jpeg", "png", "pdf"], key="file_uploader")
elif doc_type == "Invoice":
    uploaded_file = st.file_uploader("Choose an image or PDF for Invoice", type=["jpg", "jpeg", "png", "pdf"], key="file_uploader")
elif doc_type == "Bank Statement":
    uploaded_file = st.file_uploader("Choose an image or PDF for Bank Statement", type=["pdf"], key="file_uploader")
elif doc_type == "Semi-supervised API":
    uploaded_file = None  # No file upload for this type, as we use an API

# Step 3: Checking if a file is uploaded based on the selected doc_type
if uploaded_file is None and doc_type != "Semi-supervised API":
    st.warning(f"Please upload a {doc_type} document to proceed.")
else:
    # Proceeding with processing after file upload
    if doc_type == "Unsupervised Data":
        if uploaded_file is not None:
            # Handle CSV file upload for clustering
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error("The uploaded CSV is empty. Please upload a valid file.")
            elif 'Amount' in df.columns and 'Description' in df.columns:
                # Show the original DataFrame
                st.subheader("Original Data")
                st.write(df)

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
                    mime="text/csv")
            
            else:
                st.error("The uploaded file must contain 'Amount' and 'Description' columns.")
    elif doc_type == "Payslip":
        # Process the payslip image
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        earnings, bar_chart, pie_chart = process_payslip(image_path)

        # Display extracted earnings data as a table
        st.subheader("Extracted Data From Payslip:")
        st.dataframe(earnings)

        # Display the Bar Chart
        st.subheader("Earnings Distribution (Bar Chart):")
        st.image(bar_chart, caption="Bar Chart")

        # Display the Pie Chart
        st.subheader("Earnings Distribution (Pie Chart):")
        st.image(pie_chart, caption="Pie Chart")
    
    elif doc_type == "Profit & Loss":
        # Process the Profit & Loss image
        data, pie_chart, bar_chart = process_profit_loss(uploaded_file)

        # Display extracted data (as a table)
        st.subheader("Extracted Data From Profit & Loss:")
        st.dataframe(data)

        # Display the Pie Chart
        st.subheader("Business Expenses (Pie Chart):")
        st.image(pie_chart, caption="Pie Chart")

        # Display the Bar Chart
        st.subheader("Business Expenses (Bar Chart):")
        st.image(bar_chart, caption="Bar Chart")

    elif doc_type == "Invoice":
        if uploaded_file is not None:
            # Process the uploaded invoice image
            image_path = "temp_invoice_image.jpg"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process the invoice and get results
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
            
            # Clean up the temporary file
            if os.path.exists(image_path):
                os.remove(image_path)
        else:
            st.warning("Please upload an invoice document to proceed.")

    elif doc_type == "Bank Statement":
        # Handle bank statement PDF files
        temp_pdf_path = "temp_uploaded_pdf.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Process the uploaded PDF
        df = process_bank_statement(temp_pdf_path)

        # Display basic data
        st.subheader("Extracted the Transaction data of First 5 Records:")
        st.dataframe(df.head())  

        # Visualize the spending distribution by category
        st.subheader("Spending Distribution In The Form of Pie Chart, Bar Graph, Scatter Plot")
        plot_category_spending(df)

        # Clean up the temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

    elif doc_type == "Semi-supervised API":
        st.subheader("Visualizing API Data (Pie Chart)")
        # Call function to generate the API visualization
        img_base64 = plot_payment_mode_distribution()
        st.image(f"data:image/png;base64,{img_base64}")
