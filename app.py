import requests
import streamlit as st

# Configure Page
st.set_page_config(page_title="Sleek product Management API", layout="centered")
st.title("🎓 Sleek product Management API")

# Backend API Base URL Configuration
API_URL = st.sidebar.text_input("Backend API Base URL", value="https://sleek-product-management-api.onrender.com")

# Navigation Menu
option = st.sidebar.selectbox(
    "Select Action",
    [
        "View All Products",
        "View Product by ID",
        "Add New Product",
        "Update Product",
        "Delete Product",
    ],
)

# ==============================================================================
# 1. READ ALL PRODUCTS
# ==============================================================================
if option == "View All Products":
    st.subheader("📋 All Product Records")

    category_filter = st.text_input(
        "Filter by Category (Optional)", placeholder="e.g., Electronics"
    )

    if st.button("Fetch Products"):
        try:
            params = {"category": category_filter} if category_filter else {}
            response = requests.get(f"{API_URL}/products/", params=params)
            data = response.json()

            if data:
                st.json(data)
            else:
                st.info("No products found.")
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")

# ==============================================================================
# 2. READ SINGLE PRODUCT
# ==============================================================================
elif option == "View Product by ID":
    st.subheader("🔍 Search Product by ID")

    product_id = st.number_input("Enter Product ID", min_value=1, step=1)

    if st.button("Get Details"):
        try:
            response = requests.get(f"{API_URL}/products/{product_id}")
            data = response.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.success("Product Found!")
                st.json(data)
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")

# ==============================================================================
# 3. CREATE PRODUCT (POST)
# ==============================================================================
elif option == "Add New Product":
    st.subheader("➕ Add New Product")

    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        category = st.text_input("Category")

        submit_button = st.form_submit_button("Create Product")

        if submit_button:
            if not name or not category:
                st.warning("Please fill in all fields.")
            else:
                payload = {"name": name, "price": price, "category": category}
                try:
                    response = requests.post(
                        f"{API_URL}/products/", json=payload
                    )
                    st.success("Product created successfully!")
                    st.json(response.json())
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ==============================================================================
# 4. UPDATE PRODUCT (PUT)
# ==============================================================================
elif option == "Update Product":
    st.subheader("✏️ Update Existing Product")

    product_id = st.number_input(
        "Enter Product ID to Update", min_value=1, step=1
    )

    with st.form("update_product_form"):
        name = st.text_input("Updated Name")
        price = st.number_input("Updated Price", min_value=0.0, step=0.01)
        category = st.text_input("Updated Category")

        submit_button = st.form_submit_button("Update Product")

        if submit_button:
            payload = {"name": name, "price": price, "category": category}
            try:
                response = requests.put(
                    f"{API_URL}/products/{product_id}", json=payload
                )
                data = response.json()

                if "error" in data:
                    st.warning(data["error"])
                else:
                    st.success(f"Product #{product_id} updated successfully!")
                    st.json(data)
            except Exception as e:
                st.error(f"Connection error: {e}")

# ==============================================================================
# 5. DELETE PRODUCT (DELETE)
# ==============================================================================
elif option == "Delete Product":
    st.subheader("🗑️ Delete Product Record")

    product_id = st.number_input(
        "Enter Product ID to Delete", min_value=1, step=1
    )

    if st.button("Delete Product", type="primary"):
        try:
            response = requests.delete(f"{API_URL}/products/{product_id}")
            data = response.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.success(f"Product #{product_id} deleted successfully!")
                st.json(data)
        except Exception as e:
            st.error(f"Connection error: {e}")
