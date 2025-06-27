from uuid import uuid4

from framework.http.request import Request
from framework.http.responses import JsonResponse
from framework.handler.base import BaseAPIHandler

PRODUCTS = []


class ProductHandler(BaseAPIHandler):

    lookup_field = "product_id"

    def create_product(self, request: Request):
        req_data = request.body

        if "product_name" not in req_data:
            return JsonResponse(
                data={
                    "message": "Missing 'product_name' field",
                }
            )

        product = {
            "product_id": str(uuid4()),
            "product_name": req_data["product_name"],
        }
        PRODUCTS.append(product)

        return JsonResponse(data=product)

    def get_product_obj(self, request: Request, product_id):

        for product in PRODUCTS:
            if product["product_id"] == product_id:
                return JsonResponse(data={"product": product})

        return JsonResponse(data={"message": "Product not found"})

    def get_all_products(self, request: Request):
        return JsonResponse(data={"data": PRODUCTS})

    def update_product(self, request: Request, product_id):

        req_data = request.body
        if "product_name" not in req_data:
            return JsonResponse(data={"message": "Missing 'product_name' field"})

        for product in PRODUCTS:
            if product["product_id"] == product_id:
                product["product_name"] = req_data["product_name"]
                return JsonResponse(
                    data={"message": "Product updated", "product": product}
                )
        return JsonResponse(data={"message": "Product not found"})

    def delete_product(self, request: Request, product_id):

        for idx, product in enumerate(PRODUCTS):
            if product["product_id"] == product_id:
                deleted_product = PRODUCTS.pop(idx)
                return JsonResponse(
                    data={"message": "Product deleted", "product": deleted_product}
                )

        return JsonResponse(data={"message": "Product not found"})
