from flask_sqlalchemy import Pagination


def serialize_pagination(pagination: Pagination, url_route: str, list_name: str):
    base_url = f"http://127.0.0.1:5000/{url_route}"
    response = {
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }

    if pagination.has_next:
        response["next_page"] = f"{base_url}?page={pagination.next_num}"

    if pagination.has_prev:
        response["prev_page"] = f"{base_url}?page={pagination.prev_num}"

    response[list_name] = pagination.items

    return response