from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import csv
import io
from app.database import product_collection, order_collection, category_collection
from app.routes.get_current_user_for_rest import get_current_admin
from datetime import datetime, timezone, timedelta

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
    
    
@router.get("/export/recent-orders")
async def export_recent_orders(days: int, admin=Depends(get_current_admin)):
    
    # 1. Valid days check
    if days not in [1, 7, 30, 60, 90]:
        raise HTTPException(status_code=400, detail="Days 1, 7, 30, 60, 90 mein se hona chahiye")
    
    # 2. Date range banao
    now = datetime.now(timezone.utc)
    
    from_date = now - timedelta(days=days)
    
    
    # 3. Orders fetch karo
    orders = await order_collection.find(
        {"created_at": {"$gte": from_date}}
    ).to_list(length=None)
    
    if not orders:
        raise HTTPException(status_code=404, detail="Is period mein koi order nahi mila")
    
    # 4. CSV banao
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Order ID",
        "Order Number", 
        "Product Name",
        "Quantity",
        "Price",
        "Subtotal",
        "Shipping",
        "Total",
        "Payment Status",
        "Delivery Status",
        "Customer Name",
        "City",
        "State",
        "Created At"
    ])
    
    # Rows
    for order in orders:
        item = order["items"][0]
        address = order["delivery_address"]
        writer.writerow([
            str(order["_id"]),
            order["order_number"],
            item["name"],
            item["quantity"],
            item["price"],
            order["subtotal"],
            order["shipping"],
            order["total"],
            order["payment_status"],
            order["status"],
            address["full_name"],
            address["city"],
            address["state"],
            str(order["created_at"])
        ])
    
    output.seek(0)
    
    # 5. File download
    filename = f"voltmart_orders_last_{days}_days.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
    
    
@router.get("/export/category")
async def export_category_csv(admin=Depends(get_current_admin)):
    categories = await category_collection.find({}).to_list(length=None)
    
    if not categories:
        raise HTTPException(status_code=404, detail="Koi category nahi mili")
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Category ID",
        "Name",
        "Slug",
        "Description",
        "Is Active",
    ])
    
    # Rows
    for category in categories:
        writer.writerow([
            str(category["_id"]),
            category.get("name", ""),
            category.get("slug", ""),
            category.get("description", ""),
            category.get("is_active", True),
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=categories.csv"}
    )