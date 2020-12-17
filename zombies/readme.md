## Configuração

A aplicação proposta foi escrita em Python utilizando o Django framework. Para subir a infraestrura: 

```shell script
docker-compose up -d --build
```

A aplicação estará disponível em: http://localhost:8080/

## Rotas

As rotas disponíveis são

- Auth
  - Register: `[POST] user/`
  - Login: `[POST] login/`
  - Remove: `[DELETE] user/me`
- POST
  - Create: `[POST] post/`
  - Retrieve one: `[GET] post/{pk}`
  - Retrieve many (paginate): `[GET] /post`
  - Update: `[PUT] /post/{pk}`
  - Search: `[GET] /post/search?q=`

## Demonstração

Para demonstrar a aplicação será utilizado o [HTTPie](https://httpie.io/).

Para a criação do usuário vamos utilizar os dados propostos no desafio. Para criar o usuário, utilizamos `[POST] user/`, assim:

```bash
echo '{
  "displayName": "Brett Wiltshire",
  "email": "brett@email.com",
  "password": "123456",
  "image": "http://4.bp.blogspot.com/_YA50adQ-7vQ/S1gfR_6ufpI/AAAAAAAAAAk/1ErJGgRWZDg/S45/brett.png"
}' | http POST http://localhost:8080/user/
```

Caso deseje receber alguns erros de validação e verificar as regras implementadas, basta reexecutar o comando acima e o retorno deverá ser:
```json
{"message":"Usuário já existe"}
```

A remoção do usuário foi implementado em soft-delete, pois não estava especificado o comportamento para os posts relacionados ao mesmo. Caso deseje remover o usuário autenticado, deverá ser:
```bash
http DELETE http://localhost:8080/user/me
```

Para o cadastro de um novo post, deve-se utilizar:
```bash
echo '{
  "title": "Latest updates, August 1st",
  "content": "The whole text for the blog post goes here in this key"
}' | http POST http://localhost:8080/post/ 'Authorization: JWT {token}'
```

Caso deseje recuperar um post a partir do ID, utilize `[GET] /post/{pk}`:
```bash
http GET http://localhost:8080/post/1 'Authorization: JWT {token}'
```

Após buscar o post pelo ID, deve-se obter o seguinte retorno:
```json
{
  "content": "The whole text for the blog post goes here in this key",
  "id": 1,
  "published": "2020-12-15T21:25:07.599192",
  "title": "Latest updates, August 1st",
  "updated": "2020-12-15T21:25:07.599199",
  "user": {
      "displayName": "Brett Wiltshire",
      "email": "brett@email.com",
      "id": 1,
      "image": "http://4.bp.blogspot.com/_YA50adQ-7vQ/S1gfR_6ufpI/AAAAAAAAAAk/1ErJGgRWZDg/S45/brett.png"
  }
}
```

Os posts podem ser paginados utilizando a seguinte URL:
```bash
http GET http://localhost:8080/post?page=1 'Authorization: JWT {token}'
```

Caso deseje atualizar o conteudo do post, deve utilizar `[PUT] /post/{pk}`, logo:
```bash
echo '{
  "title": "Latest updates, August 2st",
  "content": "The whole text for the blog post goes here in this key. (Updated)"
}' | http PUT http://localhost:8000/api/v1/survivor/
```

Caso deseje remover o post, deve utilizar `[DELETE] /post/{pk}`, logo:
```bash
http DELETE http://localhost:8080/post/1 'Authorization: JWT {token}'
```

Caso deseje pesquisar entre os blogposts, deve utilizar `[GET] /post/search` com a querystring especificada:
```bash
http GET http://localhost:8080/post/search?q=August 'Authorization: JWT {token}'
```
A pesquisa atuará tanto no campo `title` e `content`. 

## Testes

Para executar os testes escritos para a aplicação, basta executar:

```bash
docker-compose -f docker-compose.test.yaml run web pytest -v -s
```