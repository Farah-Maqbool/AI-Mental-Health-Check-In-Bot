import kagglehub

# Download latest version
path = kagglehub.dataset_download("elvis23/mental-health-conversational-data")

print("Path to dataset files:", path)