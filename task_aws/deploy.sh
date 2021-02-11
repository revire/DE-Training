mkdir -p lambda_layers/python/lib/python3.8/site-packages
sudo pip install -r requirments.txt -t lambda_layers/python/lib/python3.8/site-packages/
cd lambda_layers && zip -r lambda_layer.zip python
cd ../lambda_tf && terraform apply -auto-approve -lock=false