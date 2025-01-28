"""
- Imports necessary libraries for clustering and visualization.
- Standardizes the 'Amount' column and applies KMeans clustering.
- Maps clusters to low, medium, high categories.
- Saves results to a CSV with transaction details and cluster labels.
- Generates and returns bar and pie charts for transaction distribution.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Method to perform KMeans clustering and save results to CSV
def perform_clustering_and_visualize(data):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Standardizing the Amount column
    scaler = StandardScaler()
    df['Amount_Scaled'] = scaler.fit_transform(df[['Amount']])
    
    # Apply KMeans with 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster_KMeans'] = kmeans.fit_predict(df[['Amount_Scaled']])
    
    # Sorting the cluster centers to map them correctly
    cluster_centers_sorted = sorted(zip(kmeans.cluster_centers_.flatten(), range(len(kmeans.cluster_centers_))), key=lambda x: x[0])
    
    # Mapping clusters based on sorted centers to ensure lowest amount goes to Cluster 0, then Cluster 1, and highest goes to Cluster 2
    cluster_mapping = {cluster_id: new_id for new_id, (center, cluster_id) in enumerate(cluster_centers_sorted)}
    
    # Applying the new cluster mapping
    df['Cluster_KMeans_Mapped'] = df['Cluster_KMeans'].map(cluster_mapping)
    
    # Saving the DataFrame to a new CSV file
    output_file_path = r'C:\BFSI_OCR\data\clustered_transactions.csv'
    df[['Transaction ID', 'Description', 'Amount', 'Cluster_KMeans_Mapped']].to_csv(output_file_path, index=False)

    # Set the style for the plots
    sns.set(style="whitegrid")

    # Bar Graph of Transactions Count per Cluster
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Cluster_KMeans_Mapped', hue='Cluster_KMeans_Mapped', palette=["orange", "yellow", "green"])
    
    # Add titles and labels for bar graph
    plt.title('Transaction Count per Cluster', fontsize=16)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Count of Transactions', fontsize=12)
    
    # Show bar chart
    bar_fig = plt.gcf()
    plt.close(bar_fig)  

    # Pie Chart of Cluster Distribution with Descriptions in Labels
    cluster_counts = df['Cluster_KMeans_Mapped'].value_counts()

    # Descriptive labels for the clusters
    cluster_labels = {
        0: 'Cluster 0: Low Amount',
        1: 'Cluster 1: Medium Amount',
        2: 'Cluster 2: High Amount'
    }

    # Prepare the labels list with descriptions
    labels = [cluster_labels.get(cluster_id, f'Cluster {cluster_id}') for cluster_id in cluster_counts.index]

    # Plot the pie chart with the original style and tilt
    plt.figure(figsize=(8, 8))
    plt.pie(cluster_counts, labels=labels, autopct='%1.1f%%', colors=["orange", "yellow", "green"], startangle=90)

    # Add title in the center of pie chart
    plt.title('Cluster Distribution in Transactions', fontsize=16, weight='bold', loc='center')

    # Ensure the title is at the center
    plt.tight_layout()
    
    # Show pie chart
    pie_fig = plt.gcf()
    plt.close(pie_fig)  # To prevent it from blocking the execution

    return df, bar_fig, pie_fig
