## cross-chain

### System Dependency

    - python3.8+
    - postgres

### Deploy

#### 1. Set Production Config

    $ vim ./config.yaml
    config.yaml 
    tip:When you change the configuration, you need to restart the service to take effect
    
    $ vim ./.env
    .env
    
    $ vim ./src/migrations/database.sql
    update contract config
#### 2. Create table sql

    update models

    path:  ./src/migrations/*.sql

#### 3. Install Python Dependency

    $ pip3 install -r ./requirements.txt

#### 4. Start Project

    $ python ./src/main.py

### Test

#### 1. start

    $ pytest
