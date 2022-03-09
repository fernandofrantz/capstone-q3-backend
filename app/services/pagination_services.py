from flask_sqlalchemy import Pagination


def serialize_pagination(pagination: Pagination, url_route: str):
    base_url = f"https://q3-capstock.herokuapp.com/{url_route}"
    response = {
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }

    if pagination.has_next:
        response["next_page"] = f"{base_url}?page={pagination.next_num}"

    if pagination.has_prev:
        response["prev_page"] = f"{base_url}?page={pagination.prev_num}"

    response[url_route] = pagination.items

    return response