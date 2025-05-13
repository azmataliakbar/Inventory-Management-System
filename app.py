import streamlit as st
import json
from datetime import datetime
from abc import ABC, abstractmethod
import os
import pandas as pd
from pathlib import Path


# Set page configuration
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

# Constants
SELECT_PRODUCT_LABEL = "Select Product"
DEFAULT_FILENAME = Path("C:/Users/WWW.SZLAIWIIT.COM/Downloads/inventory.json")
METRIC_CARD_START = '<div class="metric-card">'
METRIC_CARD_END = '</div>'
# Define constant at top of your file
PREPARED_BY_HTML = """
    <div style='text-align: center; color: #1F51FF; font-weight: bold; font-size: 1.2rem; margin-top: 30px;'>
        Prepared By : Azmat Ali
    </div>
"""

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
        border-bottom: 2px solid #1E88E5;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        color: #0D47A1;
        padding: 0.5rem;
        border-left: 4px solid #1E88E5;
        background-color: #E3F2FD;
        border-radius: 0 5px 5px 0;
        margin: 1.5rem 0 1rem 0;
    }
    .sub-header {
        font-size: 2.0rem;
        font-weight: bold;
        color: red;
        padding: 0.3rem 0;
        border-bottom: 1px solid #90CAF9;
        margin: 1rem 0;
    }
    .product-card {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        color: #0D47A1;
        background-color:lightblue;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #1E88E5;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #0D47A1;
        background-color: lightgreen;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .sidebar-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F51FF;
        text-align: center;
        padding: 0.5rem;
        border-bottom: 1px solid #90CAF9;
        margin-bottom: 1rem;
    }
    .success-text {
        color: lightgreen;
        font-size: 2.0rem;
        font-weight: bold;
    }
    .warning-text {
        color: #FF6F00;
        font-weight: bold;
    }
    .error-text {
        color: green;
        font-weight: bold;
    }
    .info-box {
        font-size: 2.0rem;
        font-weight: bold;
        text-align: center;
        color: green;
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        font-size: 2.0rem;
        font-weight: bold;
        color: #0D47A1;
        background-color: lightblue;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #FFC107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Abstract Base Class: Product
class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock
    
    def restock(self, amount):
        if amount > 0:
            self._quantity_in_stock += amount
            return True
        return False
    
    def sell(self, quantity):
        if quantity <= self._quantity_in_stock and quantity > 0:
            self._quantity_in_stock -= quantity
            return True
        return False
    
    def get_total_value(self):
        return self._price * self._quantity_in_stock
    
    @abstractmethod
    def __str__(self):
        pass
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock
        }

# Subclass: Electronics
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, warranty_years, brand):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand
    
    def __str__(self):
        return f"Electronics: {self._name} ({self._brand}), Rs.{self._price}, Stock: {self._quantity_in_stock}, Warranty: {self._warranty_years} yrs"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "warranty_years": self._warranty_years,
            "brand": self._brand
        })
        return data

# Subclass: Grocery
class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date
    
    def is_expired(self):
        today = datetime.today().date()
        expiry = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
        return today > expiry
    
    def __str__(self):
        status = " (Expired)" if self.is_expired() else ""
        return f"Grocery: {self._name}, Rs.{self._price}, Stock: {self._quantity_in_stock}, Expiry: {self._expiry_date}{status}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "expiry_date": self._expiry_date
        })
        return data

# Subclass: Clothing
class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material
    
    def __str__(self):
        return f"Clothing: {self._name}, Rs.{self._price}, Stock: {self._quantity_in_stock}, Size: {self._size}, Material: {self._material}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "size": self._size,
            "material": self._material
        })
        return data

# Custom Exceptions
class InsufficientStockError(Exception):
    pass

class DuplicateProductError(Exception):
    pass

class InvalidDataError(Exception):
    pass

# Inventory Class
class Inventory:
    def __init__(self):
        self._products = {}
    
    def add_product(self, product):
        if product._product_id in self._products:
            raise DuplicateProductError(f"Product with ID {product._product_id} already exists")
        self._products[product._product_id] = product
    
    def remove_product(self, product_id):
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False
    
    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]
    
    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__ == product_type]
    
    def list_all_products(self):
        return list(self._products.values())
    
    def sell_product(self, product_id, quantity):
        if product_id not in self._products:
            return False, "Product not found"
        
        product = self._products[product_id]
        try:
            if product._quantity_in_stock < quantity:
                raise InsufficientStockError(f"Not enough stock. Available: {product._quantity_in_stock}")
            
            product.sell(quantity)
            return True, f"Sold {quantity} units of {product._name}"
        except InsufficientStockError as e:
            return False, str(e)
    
    def restock_product(self, product_id, quantity):
        if product_id not in self._products:
            return False, "Product not found"
        
        product = self._products[product_id]
        if quantity <= 0:
            return False, "Quantity must be positive"
        
        product.restock(quantity)
        return True, f"Restocked {quantity} units of {product._name}"
    
    def total_inventory_value(self):
        return sum(product.get_total_value() for product in self._products.values())
    
    def remove_expired_products(self):
        expired_products = []
        for pid, product in list(self._products.items()):
            if isinstance(product, Grocery) and product.is_expired():
                expired_products.append(product._name)
                del self._products[pid]
        return expired_products
    
    def save_to_file(self, filename):
        try:
            data = [product.to_dict() for product in self._products.values()]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True, "Inventory saved successfully"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def load_from_file(self, filename):
        try:
            if not os.path.exists(filename):
                return False, f"File {filename} does not exist"
            
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Clear existing inventory
            self._products.clear()
            
            for item in data:
                ptype = item["type"]
                try:
                    if ptype == "Electronics":
                        product = Electronics(
                            item["product_id"],
                            item["name"],
                            item["price"],
                            item["quantity_in_stock"],
                            item["warranty_years"],
                            item["brand"]
                        )
                    elif ptype == "Grocery":
                        product = Grocery(
                            item["product_id"],
                            item["name"],
                            item["price"],
                            item["quantity_in_stock"],
                            item["expiry_date"]
                        )
                    elif ptype == "Clothing":
                        product = Clothing(
                            item["product_id"],
                            item["name"],
                            item["price"],
                            item["quantity_in_stock"],
                            item["size"],
                            item["material"]
                        )
                    else:
                        raise InvalidDataError(f"Unknown product type: {ptype}")
                    
                    self._products[product._product_id] = product
                except KeyError as e:
                    raise InvalidDataError(f"Missing required field: {str(e)}")
            
            return True, "Inventory loaded successfully"
        except json.JSONDecodeError:
            return False, "Invalid JSON file"
        except InvalidDataError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error loading file: {str(e)}"

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = Inventory()
if 'notification' not in st.session_state:
    st.session_state.notification = None
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = None

# Function to display notification
def show_notification():
    if st.session_state.notification:
        if st.session_state.notification_type == "success":
            st.success(st.session_state.notification)
        elif st.session_state.notification_type == "error":
            st.error(st.session_state.notification)
        elif st.session_state.notification_type == "info":
            st.info(st.session_state.notification)
        elif st.session_state.notification_type == "warning":
            st.warning(st.session_state.notification)
        
        # Clear notification after displaying
        st.session_state.notification = None
        st.session_state.notification_type = None

# Set notification
def set_notification(message, type="info"):
    st.session_state.notification = message
    st.session_state.notification_type = type

# Helper functions for dashboard
def display_summary_metrics(inventory):
    """Display summary metrics in the dashboard."""
    products = inventory.list_all_products()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(METRIC_CARD_START, unsafe_allow_html=True)
        st.metric("Total Products", len(products))
        st.markdown(METRIC_CARD_END, unsafe_allow_html=True)
    
    with col2:
        st.markdown(METRIC_CARD_START, unsafe_allow_html=True)
        st.metric("Total Inventory Value", f"Rs. {inventory.total_inventory_value():.2f}")
        st.markdown(METRIC_CARD_END, unsafe_allow_html=True)
    
    with col3:
        expired_count = len([p for p in products if isinstance(p, Grocery) and p.is_expired()])
        st.markdown(METRIC_CARD_START, unsafe_allow_html=True)
        st.metric("Expired Products", expired_count)
        st.markdown(METRIC_CARD_END, unsafe_allow_html=True)

def display_product_distribution(inventory):
    """Display product type distribution chart."""
    electronics = len(inventory.search_by_type("Electronics"))
    grocery = len(inventory.search_by_type("Grocery"))
    clothing = len(inventory.search_by_type("Clothing"))
    
    st.markdown('<div class="sub-header">Product Distribution</div>', unsafe_allow_html=True)
    
    # Create a DataFrame for the chart
    chart_data = pd.DataFrame({
        "Type": ["Electronics", "Grocery", "Clothing"],
        "Count": [electronics, grocery, clothing]
    })
    
    # Display the chart - fixed column name
    st.bar_chart(chart_data.set_index("Type"))

def get_product_details(product):
    """Get formatted details for a specific product."""
    if isinstance(product, Electronics):
        return f"Brand: {product._brand}, Warranty: {product._warranty_years} yrs"
    elif isinstance(product, Grocery):
        status = " <span class='error-text'>(EXPIRED)</span>" if product.is_expired() else ""
        return f"Expiry: {product._expiry_date}{status}"
    elif isinstance(product, Clothing):
        return f"Size: {product._size}, Material: {product._material}"
    return ""

def create_product_table_data(products):
    """Create data for the products table."""
    data = []
    for product in products:
        item = {
            "ID": product._product_id,
            "Name": product._name,
            "Type": product.__class__.__name__,
            "Price": f"Rs. {product._price:.2f}",
            "Stock": product._quantity_in_stock,
            "Value": f"Rs. {product.get_total_value():.2f}",
            "Details": get_product_details(product)
        }
        data.append(item)
    return data

def display_product_list(inventory):
    """Display the list of all products."""
    st.markdown('<div class="sub-header">All Products</div>', unsafe_allow_html=True)
    
    products = inventory.list_all_products()
    if not products:
        st.markdown('<div class="info-box">No products in inventory. Add some products to get started!</div>', 
                    unsafe_allow_html=True)
        return
    
    # Create a table of products
    data = create_product_table_data(products)
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

def handle_expired_products(inventory):
    """Handle the removal of expired products."""
    if st.button("Remove Expired Products", key="remove_expired"):
        expired = inventory.remove_expired_products()
        if expired:
            set_notification(f"Removed {len(expired)} expired products: {', '.join(expired)}", "success")
        else:
            set_notification("No expired products found", "info")
        st.experimental_rerun()

# Dashboard Page
def show_dashboard():
    
    st.markdown('<div class="section-header">Dashboard</div>', unsafe_allow_html=True)
    
    inventory = st.session_state.inventory
    
    # Display summary metrics
    display_summary_metrics(inventory)
    
    # Display product distribution
    display_product_distribution(inventory)
    
    # Display product list
    display_product_list(inventory)
    
    # Handle expired products
    handle_expired_products(inventory)


# Add Product Page
def show_add_product():
    st.markdown('<div class="section-header">Add New Product</div>', unsafe_allow_html=True)
    
    with st.form("add_product_form"):
        # Common fields
        product_type = st.selectbox("Product Type", ["Electronics", "Grocery", "Clothing"])
        product_id = st.number_input("Product ID", min_value=1, step=1)
        name = st.text_input("Product Name")
        price = st.number_input("Price (Rs.)", min_value=0.01, step=0.01)
        quantity = st.number_input("Quantity in Stock", min_value=0, step=1)
        
        # Type-specific fields
        if product_type == "Electronics":
            warranty = st.number_input("Warranty (years)", min_value=0, step=1)
            brand = st.text_input("Brand")
            extra_fields = (warranty, brand)
        elif product_type == "Grocery":
            expiry = st.date_input("Expiry Date")
            expiry_str = expiry.strftime("%Y-%m-%d")
            extra_fields = (expiry_str,)
        elif product_type == "Clothing":
            size = st.text_input("Size")
            material = st.text_input("Material")
            extra_fields = (size, material)
        
        submitted = st.form_submit_button("Add_Product")
        
        if submitted:
            try:
                inventory = st.session_state.inventory
                
                # Create product based on type
                if product_type == "Electronics":
                    product = Electronics(product_id, name, price, quantity, extra_fields[0], extra_fields[1])
                elif product_type == "Grocery":
                    product = Grocery(product_id, name, price, quantity, extra_fields[0])
                elif product_type == "Clothing":
                    product = Clothing(product_id, name, price, quantity, extra_fields[0], extra_fields[1])
                
                # Add to inventory
                inventory.add_product(product)
                set_notification(f"Added {product_type}: {name}", "success")
                st.experimental_rerun()
            except DuplicateProductError:
                set_notification(f"Product with ID {product_id} already exists", "error")
            except Exception as e:
                set_notification(f"Error adding product: {str(e)}", "error")




# Manage Products Page
def show_manage_products():
    st.markdown('<div class="section-header">Manage Products</div>', unsafe_allow_html=True)
    
    inventory = st.session_state.inventory
    products = inventory.list_all_products()
    
    if not products:
        st.markdown('<div class="info-box">No products in inventory. Add some products first!</div>', 
                    unsafe_allow_html=True)
        return
    
    # Create tabs for different management functions
    tab1, tab2, tab3 = st.tabs(["Sell Products", "Restock Products", "Remove Products"])
    
    with tab1:
        st.markdown('<div class="sub-header">Sell Products</div>', unsafe_allow_html=True)
        
        with st.form("sell_form"):
            product_options = {f"{p._product_id}: {p._name} (Stock: {p._quantity_in_stock})": p._product_id for p in products}
            selected_product = st.selectbox(SELECT_PRODUCT_LABEL, list(product_options.keys()), key="sell_select")
            product_id = product_options[selected_product]
            
            quantity = st.number_input("Quantity to Sell", min_value=1, step=1, key="sell_qty")
            sell_submitted = st.form_submit_button("Sell")
            
            if sell_submitted:
                success, message = inventory.sell_product(product_id, quantity)
                if success:
                    set_notification(message, "success")
                else:
                    set_notification(message, "error")
                st.experimental_rerun()
    
    with tab2:
        st.markdown('<div class="sub-header">Restock Products</div>', unsafe_allow_html=True)
        
        with st.form("restock_form"):
            product_options = {f"{p._product_id}: {p._name} (Stock: {p._quantity_in_stock})": p._product_id for p in products}
            selected_product = st.selectbox(SELECT_PRODUCT_LABEL, list(product_options.keys()), key="restock_select")
            product_id = product_options[selected_product]
            
            quantity = st.number_input("Quantity to Add", min_value=1, step=1, key="restock_qty")
            restock_submitted = st.form_submit_button("Restock")
            
            if restock_submitted:
                success, message = inventory.restock_product(product_id, quantity)
                if success:
                    set_notification(message, "success")
                else:
                    set_notification(message, "error")
                st.experimental_rerun()
    
    with tab3:
        st.markdown('<div class="sub-header">Remove Products</div>', unsafe_allow_html=True)
        
        with st.form("remove_form"):
            product_options = {f"{p._product_id}: {p._name}": p._product_id for p in products}
            selected_product = st.selectbox(SELECT_PRODUCT_LABEL, list(product_options.keys()), key="remove_select")
            product_id = product_options[selected_product]
            
            remove_submitted = st.form_submit_button("Remove Product")
            
            if remove_submitted:
                if inventory.remove_product(product_id):
                    set_notification("Product removed successfully", "success")
                else:
                    set_notification("Failed to remove product", "error")
                st.experimental_rerun()



# Search Products Page
def show_search_products():
    st.markdown('<div class="section-header">Search Products</div>', unsafe_allow_html=True)
    
    inventory = st.session_state.inventory
    
    # Create tabs for different search methods
    tab1, tab2 = st.tabs(["Search by Name", "Search by Type"])
    
    with tab1:
        st.markdown('<div class="sub-header">Search by Name</div>', unsafe_allow_html=True)
        search_name = st.text_input("Enter product name")
        
        if search_name:
            results = inventory.search_by_name(search_name)
            if results:
                st.markdown(f'<div class="success-text">Found {len(results)} products</div>', unsafe_allow_html=True)
                for product in results:
                    st.markdown(f'<div class="product-card">{str(product)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-box">No products found matching \'{search_name}\'</div>', 
                            unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="sub-header">Search by Type</div>', unsafe_allow_html=True)
        search_type = st.selectbox("Select product type", ["Electronics", "Grocery", "Clothing"])
        
        if st.button("Search"):
            results = inventory.search_by_type(search_type)
            if results:
                st.markdown(f'<div class="success-text">Found {len(results)} {search_type} products</div>', 
                            unsafe_allow_html=True)
                for product in results:
                    st.markdown(f'<div class="product-card">{str(product)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-box">No {search_type} products found</div>', 
                            unsafe_allow_html=True)
                


# Save/Load Page
def show_save_load():
    st.markdown('<div class="section-header">Save / Load Inventory</div>', unsafe_allow_html=True)
    
    inventory = st.session_state.inventory
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Save Inventory</div>', unsafe_allow_html=True)
        save_filename = st.text_input("Filename to save", DEFAULT_FILENAME)
        
        if st.button("Save Inventory"):
            success, message = inventory.save_to_file(save_filename)
            if success:
                set_notification(message, "success")
            else:
                set_notification(message, "error")
            
            #st.experimental_rerun()
    
    with col2:
        st.markdown('<div class="sub-header">Load Inventory</div>', unsafe_allow_html=True)
        load_filename = st.text_input("Filename to load", DEFAULT_FILENAME)
        
        if st.button("Load Inventory"):
            success, message = inventory.load_from_file(load_filename)
            if success:
                set_notification(message, "success")
            else:
                set_notification(message, "error")

            print(""" Please check download folder after save.""")

    st.markdown(
        """
            <div style='text-align: center; color: #AAFF00; font-weight: bold; font-size: 1.2rem;; margin-top: 30px;'>
            Please check the Downloads folder after saving.
            </div>
            """,
            unsafe_allow_html=True
                )
    

            #st.experimental_rerun()


# Main App UI
def main():
    st.markdown('<h1 class="main-header">📦 Inventory Management System</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Product", "Manage Products", "Search Products", "Save/Load"])
    
    # Show notification if any
    show_notification()
    
    # Display the selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Product":
        show_add_product()
    elif page == "Manage Products":
        show_manage_products()
    elif page == "Search Products":
        show_search_products()
    elif page == "Save/Load":
        show_save_load()
        

if __name__ == "__main__":
    main()

    st.markdown(PREPARED_BY_HTML, unsafe_allow_html=True)