CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    description TEXT,
    password TEXT,
    admin BOOLEAN DEFAULT false
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
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    cat_id INTEGER REFERENCES categories,
    type_id INTEGER REFERENCES ad_types
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,    
    cat_name TEXT UNIQUE
);

CREATE TABLE ad_types (
    id SERIAL PRIMARY KEY,    
    type_name TEXT UNIQUE
);

CREATE TABLE user_images (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    data BYTEA
);

CREATE TABLE ad_images (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    ad_id INTEGER REFERENCES ads ON DELETE CASCADE,
    data BYTEA
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_from INTEGER REFERENCES users ON DELETE SET NULL,
    user_to INTEGER REFERENCES users ON DELETE SET NULL,
    subject TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),
    seen BOOLEAN DEFAULT false
);

CREATE TABLE ad_comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),    
    ad_id INTEGER REFERENCES ads ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE	
);

CREATE TABLE user_comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP DEFAULT NOW(),
    commentator_id INTEGER REFERENCES users ON DELETE CASCADE,
    profile_id INTEGER REFERENCES users ON DELETE CASCADE	
);
