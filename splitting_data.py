import os
import pandas as pd


output_folder = "C:/Store_Migration/Splits_output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print('Creating folder:', output_folder)
    print('===============================================')
else:
    os.makedirs(output_folder, exist_ok=True)
    print('Output folder already exists:', output_folder)
    print('===============================================')

master_data = pd.read_csv("Store1.CSV", encoding="UTF-8-SIG") 

size = master_data.shape[0] // 4

datasets = []
for i in range(4):
    start_index = i * size
    end_index = start_index + size
    dataset = master_data.iloc[start_index:end_index]
    datasets.append(dataset)

# Save each dataset to a separate CSV file
for i, dataset in enumerate(datasets):
    output_file = os.path.join(output_folder,f'kwt_{i+1}.csv')
    dataset.to_csv(output_file, index=False, encoding="UTF-8-SIG")
    print('Output file saved:', output_file)