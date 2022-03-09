# capstone-q3-backend

# API E-COMMERCE

​
A ideia da API é simular um e-commerce de ponta a ponta, desde a venda ao cliente até a compra para estoque.
​

# ENDPOINTS

​

# CLIENT

​

## `POST/signup`

​
Register Client.

​
Requisition:

```json
{
    "name": str,
    "email": str,
    "password": str
}​
```

Response:

```json
{
  "id": int,
  "name": str,
  "email": str
}
```

​

## `POST/signin`

​
Login do cliente.
​

Requisição:

```json
{
    "email": str,
    "password": str
}
```

​
Resposta:

```json
{
    "api_key": str
}
```

## `PATCH/user/<user_id>`

​
Atualização do cliente.

Requisição:

```json
{
    "name": str,
    "email": str
}
```

​
Resposta:

`No body returned for response, 200 OK`

# PRODUTOS

​

## `GET/products`

​
Lista apenas alguns produtos, deve aceitar queries de page `"?page=2&per_page=4"` e de categorias (filtrar por uma apenas)
​

Resposta:

```json
{
    "products": [
        {product}
    ]
}
```

​

## `GET/products/{id}`

​
Lista apenas alguns produtos, deve aceitar queries de page `"?page=2&per_page=4"` e de categorias (filtrar por uma apenas)
​

Resposta:

```json
{
  "id": int,
  "name": str,
  "price": float,
  "category_id": int,
  "description": str
}
```

## `POST/products`

​
Registro do Produto. Precisa de acesso.
​

Requisição:

```json
{
    "name": str,
    "category": str,
    "price": float,
    "description": str
}
```

​
Resposta:

```json
{
    "id": int,
    "name": str,
    "category_id": int,
    "price": float,
    "description": str
}
```

- Registra a categoria caso ela ainda não exista
- Cria na tabela de inventory com estoque incial 0
  ​

## `PATCH/products/id`

​
Atualização do Produto. Precisa de acesso.

​
Requisição:

```json
{
    "name": str,
    "category_id": int,
    "price": str,
    "description": str
}
```

​
Resposta:

```json
{
  "id": int,
  "name": str,
  "price": float,
  "category_id": int,
  "description": str
}
```

- Registra a categoria caso ela ainda não exista.

# CATEGORIAS

​

## `GET/categories`

​
Apenas para visualização de categorias existentes.
​

Resposta:

```json
{
    "category": [
        {id, nome}
    ]
}
```

​

## `GET/categories/id`

​
Visualização dos produtos de uma categoria.
​

Resposta:

```json
{
    "category_name": [
        {Products}
    ]
}
```

## `PATCH/categories/id`

​
Visualização dos produtos de uma categoria.
​

Resposta:

```json
{
    "category_name": [
        {Products}
    ]
}
```

### ESTOQUE

​

## `GET/inventory`

​
Apenas visualização do estoque (id, quantity e value), deve mostrar alguns apenas e fazer paginação. Precisa de acesso como funcionário.
​

Resposta:

```json
{
  "page": int,
  "per_page": int,
  "data": [
    {
      "id": int,
      "quantity": int,
      "value": float
    }
  ]
}
```

​

## `GET/inventory/id`

​
Visualiza estoque de um produto específico. Precisa de acesso como funcionário.
​

Resposta:

```json

{
  "inventory": [
    {
      "id": int,
      "quantity": int,
      "value": float
    }
  ]
}
```

## `PATCH/inventory/id`

​
Visualiza estoque de um produto específico. Precisa de acesso como funcionário.
​

Resposta:

```json
{
  "id": int,
  "qtde": int,
  "value": floar
}
```

## `DELETE/inventory/id`

​
Zera o estoque de um produto específico. Precisa de acesso como funcionário.
​

Resposta:

```json
{
  "id": int,
  "qtde": 0,
  "value": 0
}
```

​

### VENDAS

​

## `POST/order`

​
Registro da compra do cliente. Opcional valor de desconto da compra. Precisa de acesso.
​

Requisição:

```json
{
    "order": [
        {id, qtde}
    ],
    "discount": "20%"
}
```

​
Resposta:

E-MAIL

```json
{
    "order": [
        {id, qtde}
    ],
    "total": float
}
```

​

- Deve registrar o pedido com o preço atual do produto, que pode mudar em outros momentos.
- Deve retirar a quantidade comprada de estoque.
- Erros: produto inexistente ou sem quantidade disponível.
  ​

## `GET/order`

Lista apenas alguns produtos, deve aceitar queries de page "?page=2&per_page=4".​

Resposta:

```json
{
    "orders": [
        {orders}
    ]
}
```

​

## `GET/order/id`

Mostra informações da compra do cliente. Precisa de acesso.
​

Resposta:

```json
{
    "order": [
        {id, qtde}
    ],
    "total": float
}
```

​

## `PATCH/order/id`

​
Atualização da compra do cliente. Precisa de acesso.
Rota aceita dois tipos de request e deve ser feito APENAS UM de cada vez.

​
Requisição para mudança de status, aceita apenas as opções "active" ou "completed":

```json
{
    "status": "active" OR "completed"
}
```

​
Resposta:

```json
{
    Order
}
```

Requisição para atualizar quantidades de produtos existentes no order:

```json
{
    "products": [
		{"id": int, "quantity": int}
	]
}
```

Resposta:

```json
{
    Order
}
```

## `DELETE/order/id`

​
Cancela um pedido e altera seu status para "deleted". Precisa de acesso.

​
Resposta:

E-MAIL

```json
{ "msg": "order deleted" }
```

- Voltar a quantidade de produto para estoque
  ​

### COMPRAS

​

## `POST/purchases`

​
Compra de novos produtos para estoque. Usuário deve ser um funcionário.

​
Requisição:

```json
{
  "products": [
    {
      "product_id": integer,
	  "quantity": integer,
	  "value": float
	}
  ]
}
```

​
Resposta:

```json
{
  "id": integer,
  "date": string,
  "products": [
    {
      "product_id": integer,
      "quantity": integer,
      "value": float
    }
  ]
}
```

- Deve atualizar a quantidade do produto no estoque
- Deve atualizar o custo de produto em estoque (média)
- Erro: necessário produto já ter cadastro para ser comprado
  ​

## `GET/purchases`

​
Mostra todos os pedidos de compra para estoque. Usuário deve ser um funcionário.

Resposta:

```json
{
  "total_pages": integer,
  "current_page": integer,
  "next_page": string,
  "prev_page": string,
  "purchases": {
    "id": integer,
    "date": string,
    "products": [
      {
        "product_id": integer,
        "quantity": integer,
        "value": float
      }
    ]
  }
}
```

​

## `GET/purchases/id`

​
Mostra informações de um pedido de compra específico. Usuário deve ser um funcionário.

​
Resposta:

```json
{
  "id": integer,
  "date": string,
  "products": [
    {
      "product_id": integer,
      "quantity": integer,
      "value": float
    }
  ]
}
```

​

## `DELETE/purchases/id`​

Remoção do pedido de compra para estoque. Usuário deve ser um funcionário.

​
Sem Resposta
