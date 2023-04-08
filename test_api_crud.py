import requests

# URL base de la API
BASE_URL = 'http://localhost:8000'

# Ejemplo de un post para crear
new_post = {
    "title": "Mi nuevo post",
    "author": "Tadeo",
    "content": "Este es mi nuevo post"
}

# Creamos un nuevo post
response = requests.post(f'{BASE_URL}/posts', json=new_post)
if response.status_code == 200:
    created_post = response.json()
    print(f'Se creó el post con ID {created_post["id"]}')
else:
    print('Ocurrió un error al crear el post')

# Obtenemos todos los posts
response = requests.get(f'{BASE_URL}/posts')
if response.status_code == 200:
    posts = response.json()
    print(f'Se encontraron {len(posts)} posts:')
    for post in posts:
        print(f'{post["id"]} - {post["title"]}')
else:
    print('Ocurrió un error al obtener los posts')

# Actualizamos un post
post_id = created_post['id']
updated_post = {
    "title": "Mi post actualizado",
    "author": "Juan Perez",
    "content": "Este es mi post actualizado"
}
response = requests.put(f'{BASE_URL}/posts/{post_id}', json=updated_post)
if response.status_code == 200:
    print(f'Se actualizó el post con ID {post_id}')
else:
    print('Ocurrió un error al actualizar el post')

# Obtenemos un post por su ID
response = requests.get(f'{BASE_URL}/posts/{post_id}')
if response.status_code == 200:
    post = response.json()
    print(f'Se encontró el post con ID {post_id}:')
    print(f'{post["id"]} - {post["title"]}')
else:
    print(f'Ocurrió un error al obtener el post con ID {post_id}')

# Eliminamos un post
response = requests.delete(f'{BASE_URL}/posts/{post_id}')
if response.status_code == 200:
    print(f'Se eliminó el post con ID {post_id}')
else:
    print('Ocurrió un error al eliminar el post')
