# Inventory Management System
###  Inventory Management System in Python that can manage different types of products, handle stock operations, sales, and persist data. This OOP concepts makes confidence in applying them in real-world use cases.
###  *1. Abstract Base Class: Product*

Use the abc module to make Product an abstract base class.

Attributes (with encapsulation):

* _product_id
* _name
* _price
* _quantity_in_stock

Methods (abstract & concrete):

* restock(amount)
* sell(quantity)
* get_total_value() --> price \ stock
* __str__() --> formatted product info

###  *2. Subclasses of Product:*

Create at least 3 different product types, each with extra attributes and overridden behavior where needed:

* *Electronics* --> warranty_years, brand

* *Grocery* --> expiry_date, is_expired()

* *Clothing*  --> size, material

Each subclass must override __str__() to include their specific info.

###  *3. Class: Inventory*

This class will manage a collection of products.

Attributes:

* _products --> a dict or list of products

Methods:

* add_product(product: Product)
* remove_product(product_id)
* search_by_name(name)
* search_by_type(product_type)
* list_all_products()
* sell_product(product_id, quantity)
* restock_product(product_id, quantity)
* total_inventory_value()
* remove_expired_products() (for groceries only)

###  4. Bonus / Extra Features (Optional but encouraged):

Added the ability to save and *load inventory data* in JSON format:

* save_to_file(filename)
* load_from_file(filename)

Ensure you store all relevant attributes and reconstruct subclasses properly when loading.

* Implement custom exceptions for cases like:

  * Selling more than available stock
  * Adding products with duplicate IDs
  * Loading invalid product data from file.

* Added CLI Menu using a while loop for interaction:

  * Add product
  * Sell product
  * Search/view product
  * Save/Load inventory
  * Exit

###  



# Link of  Inventory Management System at Google Collab

🔗 [Inventory Management System](https://colab.research.google.com/drive/1rMWZ-YiABvnX9Z7ogm7t-fdgFNdHyUQD)
