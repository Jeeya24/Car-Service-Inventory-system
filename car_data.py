"""
Car brands and models data for dropdown menus
"""

# Dictionary of car brands and their models
CAR_BRANDS_MODELS = {
    "Acura": ["ILX", "MDX", "RDX", "TLX", "NSX"],
    "Alfa Romeo": ["Giulia", "Stelvio", "4C"],
    "Aston Martin": ["DB11", "Vantage", "DBS Superleggera", "DBX"],
    "Audi": ["A3", "A4", "A5", "A6", "A7", "A8", "Q3", "Q5", "Q7", "Q8", "e-tron", "TT", "R8"],
    "Bentley": ["Bentayga", "Continental GT", "Flying Spur"],
    "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i8"],
    "Bugatti": ["Chiron", "Veyron"],
    "Buick": ["Enclave", "Encore", "Envision", "LaCrosse", "Regal"],
    "Cadillac": ["ATS", "CT4", "CT5", "CT6", "CTS", "Escalade", "XT4", "XT5", "XT6"],
    "Chevrolet": ["Bolt", "Camaro", "Colorado", "Corvette", "Cruze", "Equinox", "Impala", "Malibu", "Silverado", "Spark", "Suburban", "Tahoe", "Traverse", "Trax"],
    "Chrysler": ["300", "Pacifica"],
    "Dodge": ["Challenger", "Charger", "Durango", "Grand Caravan", "Journey"],
    "Ferrari": ["488", "F8 Tributo", "812 Superfast", "Roma", "SF90 Stradale", "Portofino"],
    "Fiat": ["500", "500X", "124 Spider"],
    "Ford": ["Bronco", "EcoSport", "Edge", "Escape", "Expedition", "Explorer", "F-150", "F-250", "F-350", "Fiesta", "Focus", "Fusion", "Mustang", "Ranger", "Transit"],
    "Genesis": ["G70", "G80", "G90", "GV80"],
    "GMC": ["Acadia", "Canyon", "Sierra", "Terrain", "Yukon"],
    "Honda": ["Accord", "Civic", "CR-V", "Fit", "HR-V", "Insight", "Odyssey", "Passport", "Pilot", "Ridgeline"],
    "Hyundai": ["Accent", "Elantra", "Ioniq", "Kona", "Palisade", "Santa Fe", "Sonata", "Tucson", "Veloster", "Venue"],
    "Infiniti": ["Q50", "Q60", "QX50", "QX60", "QX80"],
    "Jaguar": ["E-Pace", "F-Pace", "F-Type", "I-Pace", "XE", "XF", "XJ"],
    "Jeep": ["Cherokee", "Compass", "Gladiator", "Grand Cherokee", "Renegade", "Wrangler"],
    "Kia": ["Forte", "K5", "Niro", "Optima", "Rio", "Sedona", "Seltos", "Sorento", "Soul", "Sportage", "Stinger", "Telluride"],
    "Lamborghini": ["Aventador", "Huracan", "Urus"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Evoque", "Range Rover Sport", "Range Rover Velar"],
    "Lexus": ["ES", "GS", "GX", "IS", "LC", "LS", "LX", "NX", "RC", "RX", "UX"],
    "Lincoln": ["Aviator", "Continental", "Corsair", "MKZ", "Nautilus", "Navigator"],
    "Maserati": ["Ghibli", "Levante", "Quattroporte"],
    "Mazda": ["CX-3", "CX-30", "CX-5", "CX-9", "Mazda3", "Mazda6", "MX-5 Miata"],
    "McLaren": ["570S", "720S", "GT", "Senna"],
    "Mercedes-Benz": ["A-Class", "C-Class", "CLA", "CLS", "E-Class", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "S-Class", "SL", "SLC"],
    "Mini": ["Clubman", "Convertible", "Countryman", "Hardtop"],
    "Mitsubishi": ["Eclipse Cross", "Mirage", "Outlander", "Outlander Sport"],
    "Nissan": ["Altima", "Armada", "Frontier", "GT-R", "Kicks", "Leaf", "Maxima", "Murano", "Pathfinder", "Rogue", "Sentra", "Titan", "Versa"],
    "Porsche": ["911", "718 Boxster", "718 Cayman", "Cayenne", "Macan", "Panamera", "Taycan"],
    "Ram": ["1500", "2500", "3500", "ProMaster", "ProMaster City"],
    "Rolls-Royce": ["Cullinan", "Dawn", "Ghost", "Phantom", "Wraith"],
    "Subaru": ["Ascent", "BRZ", "Crosstrek", "Forester", "Impreza", "Legacy", "Outback", "WRX"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Toyota": ["4Runner", "86", "Avalon", "Camry", "C-HR", "Corolla", "Highlander", "Land Cruiser", "Prius", "RAV4", "Sequoia", "Sienna", "Tacoma", "Tundra", "Yaris"],
    "Volkswagen": ["Arteon", "Atlas", "Golf", "ID.4", "Jetta", "Passat", "Tiguan"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90"]
}

# List of car brands (sorted alphabetically)
CAR_BRANDS = sorted(CAR_BRANDS_MODELS.keys())

def get_models_for_brand(brand):
    """
    Get the list of models for a specific brand
    
    Args:
        brand (str): The car brand
        
    Returns:
        list: List of models for the brand, or empty list if brand not found
    """
    return CAR_BRANDS_MODELS.get(brand, [])
