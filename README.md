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

- Autenticação de usuários
- Cadastro e categorização de produtos
- Entrada de produtos no estoque
- Saída de produtos por compras

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`DB_URI`

`SECRET_KEY`

# Como usar os Endpoints

Falar um pouco sobre o esquema de endpoints e pa e sei que la

## Autenticação

Explicar como funciona a autenticação e o JWT

### POST/signup

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
  "email": string,
}
```

### POST/signin

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

## Produtos

Explicar como funciona o cadastro de produtos e tal

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

Explicar sobre a paginação e pa

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

Explicar quais dados podem ser alterados e pa

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

## Categorias

Explicar como funciona a criação de categorias

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

Explicar o que é retornado

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

## Compras para o Estoque

Explicar como funciona a criação de itens no estoque

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

Explicar denovo sobre a paginação

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

Explicar que a rota exclui todos os registros

**_Sem Resposta_**

## Compra de produtos por clientes

Explicar a saída de produtos do estoque quando ocorre uma compra

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

Explicar a tal da paginação mais uma vez

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

Explicar que dados podem ser alterados

```json
{
  "order": [
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

Explicar o que acontece quando mandar um delete

_Resposta:_

```json
{
  "msg": "order deleted"
}​
```

## Estoque

Explicar como funciona a criação de itens no estoque

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

Explicar que dados podem ser alterados

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

Explicar que os atributos são zerados

_Resposta:_

```json
{
  "id": number,
  "value": number,
  "quantity": number
}​
```

## Melhorias

Que melhorias você fez no seu código? Ex: refatorações, melhorias de performance, acessibilidade, etc

## Aprendizados

O que você aprendeu construindo esse projeto? Quais desafios você enfrentou e como você superou-os?
