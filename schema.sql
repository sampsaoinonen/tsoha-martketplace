CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    description TEXT,
    password TEXT
);

CREATE TABLE ads (
    id SERIAL PRIMARY KEY,    
    title TEXT,
    description TEXT,
    phone TEXT,    
    email TEXT,
    location TEXT,
    price DECIMAL(7,2),
    expires INTEGER,
    sent_at TIMESTAMP DEFAULT NOW(),
    user_id INTEGER REFERENCES users,
    cat_id INTEGER REFERENCES categories,
    type_id INTEGER REFERENCES adtypes
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,    
    cat_name TEXT UNIQUE
);

CREATE TABLE adtypes (
    id SERIAL PRIMARY KEY,    
    type_name TEXT UNIQUE
);

CREATE TABLE userimages (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    user_id INTEGER REFERENCES users,
    data BYTEA
);

CREATE TABLE adimages (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    ad_id INTEGER REFERENCES ads,
    data BYTEA
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_from INTEGER REFERENCES users,
    user_to INTEGER REFERENCES users,
    subject TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),
    seen BOOLEAN DEFAULT false
);
