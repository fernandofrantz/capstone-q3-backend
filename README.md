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
    "access_token": str
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
    "access_token": str
}
```
​
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
## `POST/products`
​
Registro do Produto. Precisa de acesso.
​

Requisição:
```json
{
    "name": str,
    "category": str,
    "price": str
}
```
​
Resposta:
```json
{
    "id": int,
    "name": str,
    "category": str,
    "price": str
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
    "category": str,
    "price": str
}
```
​
Resposta:
```json
{
    "id": int,
    "name": str,
    "category": str,
    "price": str
}
```

- Registra a categoria caso ela ainda não exista.

## `DELETE/products/id`
​
Remoção do Produto. Precisa de acesso.
​

Resposta:
```json
{
    "id": int,
    "name": str,
    "category": str,
    "price": str
}
```
​
# CATEGORIAS
​
## `GET/categories`
​
Apenas para visualização de categorias existentes.
​

Resposta:

```json
{
    "categories": [
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
    "nome_da_categoria": [
        {Products}
    ]
}
```
​
### ESTOQUE
​
## `GET/inventory`
​
Apenas visualização do estoque (id, qtde e CMM), deve mostrar alguns apenas e aceitar query. Precisa de acesso.
​

Resposta:
```json
{
    "inventory": [
        {id, qtde, CMM}
    ]
}
```
​
## `GET/inventory/id`
​
Visualiza estoque de um produto específico. Precisa de acesso.
​

Resposta:
```json
{
    "id": int,
    "qtde": int,
    "cmm": int
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
## `GET/order/id`
​
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
- Deve atualizar o estoque novamente
- Erro: nova quantidade não está disponível
​
## `DELETE/order/id`
​
Remoção da compra do cliente. Precisa de acesso.

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

- Voltar a quantidade de produto para estoque
​
### COMPRAS
​
## `POST/purchase`
​
Compra de novos produtos para estoque. Precisa de acesso.

​
Requisição:

```json
{
    "products": [
        {id, qtde, valor_custo}
    ]
}
```
​
Resposta:

```json
{
    "products": [
        {id, qtde, valor_custo}
    ],
    "total": float
}
```

- Deve atualizar a quantidade do produto no estoque
- Deve atualizar o custo de produto em estoque (média)
- Erro: necessário produto já ter cadastro para ser comprado
​
## `GET/purchase/id`
​
Mostra informações do pedido de compra para estoque. Precisa de acesso.

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
## `PATCH/purchase/id`
​
Atualização informações do pedido de compra para estoque. Precisa de acesso.

​
Requisição:

```json
{
    "order": [
        {id, qtde}
    ]
}
```
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

- Deve atualizar a quantidade do produto no estoque
- Deve atualizar o custo de produto em estoque (média)

## `DELETE/purchase/id`​

Remoção do pedido de compra para estoque. Precisa de acesso.

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

- Deve atualizar a quantidade do produto no estoque
- Deve atualizar o custo de produto em estoque (média)