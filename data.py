import kagglehub

# Download latest version
path = kagglehub.dataset_download(handle="bismasajjad/global-ai-job-market-and-salary-trends-2025")

print("Path to dataset files:", path)