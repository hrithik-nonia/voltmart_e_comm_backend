from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import csv
import io
from app.database import product_collection
from app.routes.get_current_user_for_rest import get_current_admin

router = APIRouter()

@router.get("/export/products")
async def export_products(admin = Depends(get_current_admin)):
    
    # Saare products fetch karo
    products = await product_collection.find({}).to_list(length=None)
    
    # CSV banao
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Name", "Price", 
        "Sale Price", "Stock", 
        "SKU", "Status", "Created At"
    ])
    
    # Rows
    for product in products:
        writer.writerow([
            str(product["_id"]),
            product["product_name"],
            product.get("price", ""),
            product.get("sale_price", ""),
            product.get("stock", ""),
            product.get("sku", ""),
            "Active" if product.get("is_active") else "Inactive",
            str(product.get("created_at", ""))
        ])
    
    output.seek(0)
    
    # File download response
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=voltmart_products.csv"
        }
    )