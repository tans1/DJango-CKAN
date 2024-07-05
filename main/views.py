from django.shortcuts import render
import requests
from datetime import datetime
import json



def index(request): 
    dcat_json_url = 'https://localhost:8443/api/3/action/current_package_list_with_resources'

    response = requests.get(dcat_json_url, verify=False)
    data = response.json()
    datasets = []
    
    for dataset in data.get('result', []):
        dataset_info = {
            'author': dataset.get('author', ''),
            'organization': {
                'name': dataset['organization']['name'],
                'title': dataset['organization']['title'],
                'description': dataset['organization'].get('description', ''),
                'image_url': dataset['organization'].get('image_url', ''),
            },
            'creation_date': datetime.fromisoformat(dataset['metadata_created']).strftime("%d-%m-%y"),
            'name': dataset['name'],
            'title': dataset['title'],
            'description': dataset['notes'],
            'tags': [tag['name'] for tag in dataset['tags']],
            'license': {
                'id': dataset['license_id'],
                'title': dataset['license_title'],
                'url': dataset['license_url'],
            },
            'resources': [{
                'name': resource['name'],
                'format': resource['format'],
                'url': resource['url'],
                'description': resource['description'],
                'created': datetime.fromisoformat(resource['created']).strftime("%d-%m-%y"),
                'size': resource['size'],
            } for resource in dataset['resources']],
            
        }
        datasets.append(dataset_info)
    return render(request, 'index.html', {'datasets': datasets, 'json' : json.dumps(data, indent=2)})
