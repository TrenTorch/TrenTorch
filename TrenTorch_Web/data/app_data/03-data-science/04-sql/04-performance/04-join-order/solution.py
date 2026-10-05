SELECT customers.name FROM regions CROSS JOIN customers ON customers.region_id = regions.id WHERE regions.name = 'EU';
