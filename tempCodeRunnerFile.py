
        CREATE TABLE IF NOT EXISTS products (
            farmername VARCHAR(255) NOT NULL,
            phone INT NOT NULL,
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(1000) NOT NULL,
            quantity DECIMAL(10, 2) NOT NULL,
            expiry_date DATE NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """