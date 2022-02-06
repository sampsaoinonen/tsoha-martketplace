CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    description TEXT,
    password TEXT,

);

CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    phone TEXT,    
    email TEXT,
    location TEXT,
    price DECIMAL(6,2),
    sent_at TIMESTAMP DEFAULT NOW(),
    user_id INTEGER REFERENCES users,
    cate_id INTEGER REFERENCES categories,    

);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,    
    cate_name TEXT UNIQUE
);

CREATE TABLE userimages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    image DATA
);

CREATE TABLE adimages (
    id INTEGER PRIMARY KEY,
    ad_id INTEGER REFERENCES ads,
    image DATA
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    user_from INTEGER REFERENCES users,
    user_to INTEGER REFERENCES users,
    message TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),
    seen BOOLEAN DEFAULT false
);
