# Capstone Q3 - Capstock

Capstock é uma API desenvolvida em Python, utilizando o microframework Flask e tem
como objetivo incentivar a prática de conceitos básicos de Backend e trabalho em
grupo.

A aplicação é baseada no conceito de um e-commerce, reproduzindo um fluxo de tanto
de entrada quanto saída de produtos. Essas funcionalidades são complementadas por
um sistema de autenticação de clientes e funcionários e pelo registro de produtos
e valores em estoque.

## Integrantes do grupo

- [Daniel Francisco](https://www.github.com/daniell18) - Product Owner
- [Gabriel de Azevedo](https://www.github.com/azgabe) - Scrum Master
- [Fernando Frantz](https://www.github.com/fernandofrantz) - Developer
- [Ivan Rowlands de Macedo](https://www.github.com/ivanrowlands) - Developer
- [Rodrigo Hardt](https://www.github.com/rodhardt) - Tech Lead
- [Lourivan Rodrigues](https://www.github.com/lourivanluz) - Developer

## Funcionalidades

- Autenticação
- Cadastro e categorização de produtos
- Adição de produtos ao estoque
- Realização de compras
- Supervisão e manutenção dos dados

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`DB_URI`

`SECRET_KEY`

# Como usar os Endpoints

As rotas da aplicação podem ser dividas em três categorias básicas:

- Rotas públicas
- Rotas para clientes
- Rotas para funcionários

Recursos como a visualização de produtos e categorias e a criação de usuários podem
ser utilizados sem nenhum tipo de token de acesso, enquanto outros como a adição
de produtos ao estoque só podem ser usados por funcionários.

Esse tipo de validação é feita pelo envio de um Bearer Token no Header nas
requisições protegidas. Esse tokens seguem o padrão JSON Web Token e são gerados
automaticamente pela aplicação durante o login de um usuário.

Logo abaixo seguem exemplos de cada rota aceita pela aplicação, junto com seu
comportamento esperado, os campos necessários para sua utilização e o que será
retornado pelo servidor.

## Autenticação

Ao criar uma conta, a senha do usuário é haseada e registrada de forma segura no
banco de dados. Por padrão, um usuário será criado como **cliente** e não terá acesso
à recursos de funcionários. Porém um **cliente** pode logar no site e, por meio do
token JWT retornado, realizar pedidos de compras atráves da rota **_/orders_** .

### POST/user/signup

```json
{
  "name": string,
  "email": string,
  "password": string
}​
```

_Resposta:_

```json
{
  "name": string,
  "email": string
}
```

### POST/user/signin

```json
{
  "email": string,
  "password": string
}​
```

_Resposta:_

```json
{
  "access_token": string
}
```

### PATCH/user

Um usário também pode usar seu token JWT para alterar dados da própria conta. No
momento, esses dados são apenas seu **name** e **email**.

```json
{
  "name": string,
  "email": string
}​
```

_Resposta:_

```json
{
  "id": number,
  "name": string,
  "email": string
}
```

## Cadastro de Produtos

Antes mesmo de ser adicionado ao **estoque**, todo produto precisa estar cadastrado
no banco de dados. Ao efetuar esse cadastro, também será alocado um espaço no
**estoque** para o produto, porém sua quantidade e outros dados relevantes estarão zerados.

### POST/products

```json
{
  "name": string,
  "price": float,
  "category": string,
  "description": string
}​
```

_Resposta:_

```json
{
  "id": number,
  "name": string,
  "price": number,
  "category_id": number,
  "description": string
}
```

### GET/products

Dados cadastrados em maior quantidade, como produtos e itens no estoque, possuem um
sistema de paginação, onde são retornados em partes e podem ser acessados seguindo
os links nos campos **next_page** e **prev_page**, que representam a próxima página
e a anterior, respectivamente.

_Resposta:_

```json
{
  "total_pages": number,
  "current_page": number,
  "next_page": string,
  "prev_page": string,
  "products": [
    {
      "id": number,
      "name": string,
      "price": number,
      "category_id": number,
      "description": string
    }
  ]
}
```

### GET/products/id: integer

_Resposta:_

```json
{
  "id": number,
  "name": string,
  "price": number,
  "category_id": number,
  "description": string
}
```

### PATCH/products/id: integer

Qualquer um dos dados na requisição de exemplo pode ser enviado, tanto
individualmente quanto em qualquer combinação.

```json
{
  "name": string,
  "price": float,
  "category": string,
  "description": string
}​
```

_Resposta:_

```json
{
  "id": number,
  "name": string,
  "price": number,
  "category_id": number,
  "description": string
}
```

## Categorização de Produtos

Se uma categoria enviada na **criação de um produto** não existir, essa será criada
e registrada no banco de dados automaticamente. Ainda assim, as informações de uma
categoria podem ser acessadas e editadas separadamente.

### GET/categories

_Resposta:_

```json
{
  "categories": [
    {
      "id": number,
      "name": string
    }
  ]
}​
```

### GET/categories/id: integer

Essa rota retornará o nome da categoria (substituindo o campo **category_name**),
junto de todos os produtos relacionados à ela cadastrados no banco de dados.

_Resposta:_

```json
{
  "category_name": [
    {
      "id": number,
      "name": string,
      "price": number,
      "description": string
    }
  ]
}
```

### PATCH/categories/id: integer

```json
{
	"name": string
}
```

_Resposta:_

```json
{
  "id": number,
  "name": string
}
```

## Adição de Produtos ao Estoque

Ao cadastrar a entrada de produtos no estoque, todos os valores e quantidades de
produtos serão registrados individualmente. Além disso, também será possível
visualizar o total desses dados através da rota **_/orders_**.

### POST/purchases

```json
{
  "products": [
    {
      "product_id": integer,
      "quantity": integer,
      "value": float
    }
  ]
}​
```

_Resposta:_

```json
{
  "id": number,
  "date": string,
  "products": [
    {
      "product_id": number,
      "quantity": number,
      "value": float
    }
  ]
}​
```

### GET/purchases

Essa rota possue um sistema de paginação, onde os dados são retornados em partes e
podem ser acessados seguindo os links nos campos next_page e prev_page, que
representam a próxima página e a anterior, respectivamente.

_Resposta:_

```json
{
  "total_pages": number,
  "current_page": number,
  "next_page": string,
  "prev_page": string,
  "purchases": [
    {
      "id": number,
      "date": string,
      "products": [
        {
          "product_id": number,
          "quantity": number,
          "value": number
        }
      ]
    }
  ]
}​
```

### GET/purchases/id: integer

_Resposta:_

```json
{
  "id": number,
  "date": string,
  "products": [
    {
      "product_id": number,
      "quantity": number,
      "value": number
    }
  ]
}
```

### DELETE/purchases/id: integer

Ao deletar uma purchase, todos os dados referentes à entrada dos produtos são
revertidos, incluindo as alterações no **estoque**.

**_Sem Resposta_**

## Realização de Compras

Ao realizar uma compra, o estoque será automaticamente atualizado de acordo com os
produtos( identificados por seu **id**), tanto sua quantidade em estoque quanto o
valor total em produtos.

### POST/orders

```json
{
  "order": [
    {
      "id": integer,
	  "quantity": integer
	}
  ]
}​
```

_Resposta:_

```json
{
  "id": number,
  "name": string,
  "order_date": string,
  "quantity": number,
  "status": string,
  "total": number,
  "products": [
    {
      "id": number,
      "name": string,
      "price": number,
      "category_id": number,
      "description": string
    }
  ]
}​
```

### GET/orders/

Essa rota possue um sistema de paginação, onde os dados são retornados em partes e
podem ser acessados seguindo os links nos campos next_page e prev_page, que
representam a próxima página e a anterior, respectivamente.

_Resposta:_

```json
{
  "total_pages": number,
  "current_page": number,
  "orders": [
    {
      "id": number,
      "order_date": string,
      "products": [
        {
          "id": number,
          "name": string,
          "price": number,
          "category_id": number,
          "description": string
        }
      ]
    }
  ]
}​
```

### GET/orders/id: integer

_Resposta:_

```json
{
  "id": number,
  "order_date": string,
  "quantity": number,
  "status": string,
  "total": number,
  "products": [
    {
      "id": number,
      "name": string,
      "price": number,
      "category_id": number,
      "description": string
    }
  ]
}
```

### PATCH/orders/id: integer

Uma order também pode ser alterada por um funcionário, caso necessário. Para
alterar a quantidade de um ou mais produtos, deve ser enviada uma lista dentro do
campo **products**. O **status** da compra também pode ser modificado, porém, os
únicos valores aceitos são **"complete"** ou **"active"**.

```json
{
  "products": [
	{
      "id": integer,
      "quantity": integer
	}
  ],
  "status": string
}​
```

_Resposta:_

```json
{
  "id": number,
  "order_date": string,
  "quantity": number,
  "status": string,
  "total": number,
  "products": [
    {
      "id": number,
      "name": string,
      "price": number,
      "category_id": number,
      "description": string
    }
  ]
}​
```

### DELETE/orders/id: integer

Ao deletar uma order, os valores em **estoque** são revertidos e o **status** da
compra é alterado para **"deleted"**.

_Resposta:_

```json
{
  "msg": "order deleted"
}​
```

## Estoque

Essa rota possue um sistema de paginação, onde os dados são retornados em partes e
podem ser acessados seguindo os links nos campos next_page e prev_page, que
representam a próxima página e a anterior, respectivamente.

### GET/inventory

Explicar denovo sobre a paginação

_Resposta:_

```json
{
  "total_pages": number,
  "current_page": number,
  "next_page": string,
  "prev_page": string,
  "inventory": [
    {
      "id": number,
      "value": number,
      "quantity": number
    }
  ]
}​
```

### GET/inventory/id: integer

_Resposta:_

```json
{
  "id": number,
  "value": number,
  "quantity": number
}​
```

### PATCH/inventory/id: integer

Qualquer um dos dados na requisição de exemplo pode ser enviado, tanto
individualmente quanto em qualquer combinação.

```json
{
  "value": number,
  "quantity": number
}​
```

_Resposta:_

```json
{
  "id": number,
  "value": number,
  "quantity": number
}​
```

### DELETE/inventory/id: integer

Ao deletar um item no estoque, seus valores serão zerados. Porém, seus registros e
conexões com produtos serão mantidos.

_Resposta:_

```json
{
  "id": number,
  "value": number,
  "quantity": number
}​
```

## Melhorias

Seria necessário implementar um sistema de criação de **funcionários**.
No momento, apenas **clientes** podem ser criados através das rotas, sendo
necessário alterar o código para registrar usuário do tipo **funcionário**.
