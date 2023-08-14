import requests
import csv
import os
import os.path
import datetime


headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

def get_workspace_ids():
    
    WORKSPACE_STARTS = 0
    WORKSPACE_LIMIT = 50
    workspace_ids = []
    while True:
        response = requests.get(
            f'https://api.prod.timetoknow.com/PlayAppService/channelQuery/'
            f'section?limit={WORKSPACE_LIMIT}&orderBy=&section=CONTENT_WORKSPACES&sortOrder'
            f'=ASC&start={WORKSPACE_STARTS}', headers=headers
            
        )
    
        data = response.json()
        
        workspace_ids.extend([id['id'] for id in data])
        
        WORKSPACE_STARTS += WORKSPACE_LIMIT
        
        break
        
    return workspace_ids


def get_courses_workspace(workspace_id):
    response = requests.get(
        f'https://api.prod.timetoknow.com/LibraryService/v2/channels/'
        f'{workspace_id}/content?contentOrderBy='
        f'publishExtraData.serverPublishDate&contentSortOrder=DESC', headers=headers
    )
    
    data = response.json()
    workspace_name = data.get('name')
    library_items = data.get('libraryItems', [])
    extracted_data = []
    for item in library_items:
        extracted_data.append(
            {
            'Estante': workspace_name,
            'ID do Curso': item.get('id'),
            'Nome do curso': item.get('name'),
            'Status': item.get('isPublished'),
            'Modificado': datetime.datetime.fromisoformat\
                        (item.get('modified').replace("Z", "+00:00")).date()\
                        if item.get('modified') else None    
            })
        print(f'Estante: {workspace_name}\n Conteudo: {extracted_data}\n')
 
    return extracted_data

def write_to_csv(data, writer):
    for row in data:
        writer.writerow(row)


def main():
    workspace_ids = get_workspace_ids()
    filename = "Charon_workspaces.csv"
    name, extension = os.path.splitext(filename)
    counter = 1
    
    while os.path.isfile(filename):
        filename = f"{name}_{counter}{extension}"
        counter += 1
        
    fieldnames = ['Estante', 'ID do Curso', 'Nome do curso', 'Status', 'Modificado']
    
    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for id in workspace_ids:
            data_courses = get_courses_workspace(id)
            write_to_csv(data_courses, writer)
    
        
        
if __name__ == "__main__":
    main()
    
    
    


    

 