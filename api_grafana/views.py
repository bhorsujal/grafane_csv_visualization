from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import os

from qualification_task.settings import BASE_DIR

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'api_grafana/error.html', {'error': 'Please upload a CSV file.'})
        
        # Read CSV file
        csv_data = csv_file.read().decode('utf-8')
        # Parse CSV data into DataFrame
        df = pd.read_csv(StringIO(csv_data))
        
        # Visualize data
        plt.figure(figsize=(10, 6))
        # Assuming first column as x-axis and second column as y-axis, adjust as needed
        plt.plot(df.iloc[:, 0], df.iloc[:, 1])
        plt.xlabel('X-axis label')
        plt.ylabel('Y-axis label')
        plt.title('CSV Data Visualization')
        # Save plot as a temporary file
        plot_path = os.path.join(BASE_DIR, 'api_grafana', 'static', 'plot.png')
        plt.savefig(plot_path)
        plt.close() 
        
        # Pass plot path to template
        return render(request, 'api_grafana/visualization.html', {'plot_path': plot_path})
    
    return render(request, 'api_grafana/home_page.html')
