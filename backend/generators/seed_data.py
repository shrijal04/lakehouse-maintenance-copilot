"""
Static master/reference data for the Retail Lakehouse project.
These datasets rarely change and are loaded once during initialization.
"""

CATEGORIES = [
    "Laptop",
    "Desktop",
    "Monitor",
    "Storage",
    "Networking",
    "Accessories",
    "Printer",
    "Audio",
    "Mobile",
    "Tablet"
]

BRANDS = [
    {"name": "Dell", "country": "USA"},
    {"name": "HP", "country": "USA"},
    {"name": "Lenovo", "country": "China"},
    {"name": "Apple", "country": "USA"},
    {"name": "Samsung", "country": "South Korea"},
    {"name": "Logitech", "country": "Switzerland"},
    {"name": "ASUS", "country": "Taiwan"},
    {"name": "Acer", "country": "Taiwan"},
    {"name": "Canon", "country": "Japan"},
    {"name": "Sony", "country": "Japan"},
    {"name": "Kingston", "country": "USA"},
    {"name": "Western Digital", "country": "USA"}
]

STORES = [
    {
        "store_name": "Kathmandu Central",
        "city": "Kathmandu",
        "country": "Nepal",
        "manager": "Rajesh Sharma"
    },
    {
        "store_name": "Lalitpur Plaza",
        "city": "Lalitpur",
        "country": "Nepal",
        "manager": "Anita Karki"
    },
    {
        "store_name": "Pokhara Lakeside",
        "city": "Pokhara",
        "country": "Nepal",
        "manager": "Suman Gurung"
    },
    {
        "store_name": "Bhaktapur Heritage",
        "city": "Bhaktapur",
        "country": "Nepal",
        "manager": "Nabin Shrestha"
    },
    {
        "store_name": "Biratnagar East",
        "city": "Biratnagar",
        "country": "Nepal",
        "manager": "Prakash Rai"
    },
    {
        "store_name": "Butwal Trade Center",
        "city": "Butwal",
        "country": "Nepal",
        "manager": "Rita Thapa"
    },
    {
        "store_name": "Chitwan Junction",
        "city": "Bharatpur",
        "country": "Nepal",
        "manager": "Bikash Adhikari"
    },
    {
        "store_name": "Nepalgunj Mall",
        "city": "Nepalgunj",
        "country": "Nepal",
        "manager": "Deepa KC"
    }
]

PRODUCT_CATALOG = [

    # ---------------- Laptops ----------------
    {"name": "Dell XPS 13", "brand": "Dell", "category": "Laptop"},
    {"name": "Dell Latitude 7440", "brand": "Dell", "category": "Laptop"},
    {"name": "Dell Inspiron 15", "brand": "Dell", "category": "Laptop"},
    {"name": "HP EliteBook 840 G10", "brand": "HP", "category": "Laptop"},
    {"name": "HP Pavilion 15", "brand": "HP", "category": "Laptop"},
    {"name": "Lenovo ThinkPad E14", "brand": "Lenovo", "category": "Laptop"},
    {"name": "Lenovo IdeaPad Slim 5", "brand": "Lenovo", "category": "Laptop"},
    {"name": "Apple MacBook Air M3", "brand": "Apple", "category": "Laptop"},
    {"name": "Apple MacBook Pro 14", "brand": "Apple", "category": "Laptop"},
    {"name": "ASUS ZenBook 14", "brand": "ASUS", "category": "Laptop"},

    # ---------------- Desktop ----------------
    {"name": "Dell OptiPlex 7010", "brand": "Dell", "category": "Desktop"},
    {"name": "HP ProDesk 400", "brand": "HP", "category": "Desktop"},
    {"name": "Lenovo ThinkCentre M70", "brand": "Lenovo", "category": "Desktop"},
    {"name": "Apple Mac Mini M4", "brand": "Apple", "category": "Desktop"},
    {"name": "Acer Aspire TC", "brand": "Acer", "category": "Desktop"},

    # ---------------- Monitor ----------------
    {"name": "Dell UltraSharp U2723QE", "brand": "Dell", "category": "Monitor"},
    {"name": "Dell 27 Monitor", "brand": "Dell", "category": "Monitor"},
    {"name": "Samsung Odyssey G5", "brand": "Samsung", "category": "Monitor"},
    {"name": "Samsung ViewFinity S8", "brand": "Samsung", "category": "Monitor"},
    {"name": "ASUS ProArt Display", "brand": "ASUS", "category": "Monitor"},
    {"name": "Acer Nitro XV272U", "brand": "Acer", "category": "Monitor"},

    # ---------------- Storage ----------------
    {"name": "Samsung 990 Pro 1TB SSD", "brand": "Samsung", "category": "Storage"},
    {"name": "Samsung T7 Portable SSD", "brand": "Samsung", "category": "Storage"},
    {"name": "WD Blue 2TB HDD", "brand": "Western Digital", "category": "Storage"},
    {"name": "WD Black SN850X", "brand": "Western Digital", "category": "Storage"},
    {"name": "Kingston NV2 1TB SSD", "brand": "Kingston", "category": "Storage"},
    {"name": "Kingston XS1000 SSD", "brand": "Kingston", "category": "Storage"},

    # ---------------- Networking ----------------
    {"name": "ASUS RT-AX58U Router", "brand": "ASUS", "category": "Networking"},
    {"name": "TP-Link Archer AX55", "brand": "ASUS", "category": "Networking"},
    {"name": "Netgear Nighthawk AX6", "brand": "ASUS", "category": "Networking"},
    {"name": "ASUS ZenWiFi XT8", "brand": "ASUS", "category": "Networking"},

    # ---------------- Accessories ----------------
    {"name": "Logitech MX Master 3S", "brand": "Logitech", "category": "Accessories"},
    {"name": "Logitech MX Keys", "brand": "Logitech", "category": "Accessories"},
    {"name": "Logitech Brio Webcam", "brand": "Logitech", "category": "Accessories"},
    {"name": "Logitech G502 Mouse", "brand": "Logitech", "category": "Accessories"},
    {"name": "Dell Wireless Mouse", "brand": "Dell", "category": "Accessories"},
    {"name": "HP USB Keyboard", "brand": "HP", "category": "Accessories"},
    {"name": "Samsung USB-C Hub", "brand": "Samsung", "category": "Accessories"},
    {"name": "Apple Magic Mouse", "brand": "Apple", "category": "Accessories"},

    # ---------------- Audio ----------------
    {"name": "Sony WH-1000XM5", "brand": "Sony", "category": "Audio"},
    {"name": "Sony WF-1000XM5", "brand": "Sony", "category": "Audio"},
    {"name": "Samsung Galaxy Buds2 Pro", "brand": "Samsung", "category": "Audio"},
    {"name": "Logitech Z407 Speakers", "brand": "Logitech", "category": "Audio"},

    # ---------------- Printer ----------------
    {"name": "Canon PIXMA G3010", "brand": "Canon", "category": "Printer"},
    {"name": "Canon imageCLASS MF3010", "brand": "Canon", "category": "Printer"},
    {"name": "HP LaserJet M211", "brand": "HP", "category": "Printer"},

    # ---------------- Mobile ----------------
    {"name": "Samsung Galaxy S25", "brand": "Samsung", "category": "Mobile"},
    {"name": "Apple iPhone 17", "brand": "Apple", "category": "Mobile"},

    # ---------------- Tablet ----------------
    {"name": "Apple iPad Air", "brand": "Apple", "category": "Tablet"},
    {"name": "Samsung Galaxy Tab S10", "brand": "Samsung", "category": "Tablet"},
]