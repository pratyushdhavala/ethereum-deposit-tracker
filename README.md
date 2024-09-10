### Video Demonstration Link :- https://drive.google.com/file/d/1r1iA0EMNmxqDQMEZyYomMu_zoOoOanWU/view?usp=sharing


# Ethereum Deposit Tracker

The **Ethereum Deposit Tracker** is a robust application designed to monitor and record ETH deposits on the Beacon Deposit Contract. It tracks deposits in real-time or over a specified range of blocks, storing relevant details in a PostgreSQL database. 

## Features

- **Real-time Tracking**: Monitors the latest blocks on the Ethereum network for any ETH deposits on the Beacon Deposit Contract.
- **Range Tracking**: Tracks deposits between specific blocks.
- **Data Storage**: Stores relevant transaction and deposit details, such as `pubkey`, `withdrawal_credentials`, and `amount` in a PostgreSQL database.
- **Logging**: Error tracking and deposit information are logged to a file for debugging and analysis.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Usage](#usage)
  - [Real-time Tracking](#real-time-tracking)
  - [Block Range Tracking](#block-range-tracking)

---

## Installation

To install and run the project, follow the steps below:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pratyushdhavala/ethereum-deposit-tracker.git
   cd ethereum-deposit-tracker
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

    ```bash
   pip install web3 psycopg2 python-dotenv
   ```
4. Set up PostgreSQL: Ensure that PostgreSQL is installed and running. You'll need to create a database called `ethereum`:


```bash
   createdb ethereum
   ```

5. Environment Variables: Create a .env file in the root directory to store the environment variables:

   ```bash
   INFURA_URL=<your-infura-url>
   POSTGRES_USER=<your-postgres-username>
   POSTGRES_PASSWORD=<your-postgres-password>
   ```

6. Database Setup: Create the necessary table in PostgreSQL:

   ```bash

   CREATE TABLE deposits (
    id SERIAL PRIMARY KEY,
    block_number INTEGER,
    transaction_hash TEXT,
    sender_address TEXT,
    receiver_address TEXT,
    value DECIMAL,
    gas_used INTEGER,
    timestamp TIMESTAMP,
    pubkey TEXT[],
    withdrawal_credentials TEXT[],
    amount DECIMAL[],
    signature TEXT[],
    deposit_index INTEGER[]
);


## Configuration
* INFURA_URL: You'll need an Infura project ID to interact with the Ethereum network. Add this to your .env file.
* CONTRACT_ADDRESS: The Beacon Deposit Contract address is pre-configured in config.py.
* PostgreSQL Credentials: Ensure that the credentials for PostgreSQL are correctly set in your .env file.

## Usage

1. Activate the virtual environment:
  ```bash
   source venv/bin/activate
   ```
2. Run the application:
    ```bash
   python main.py
   ```
3. You will be prompted to choose between real-time or range-based tracking.

### Real-time Tracking

```bash
   Enter 'real-time' to track in real-time or 'range' to track a block range: real-time
   Tracking deposits in real-time...
   ```

### Block Range Tracking

```bash
   Enter 'real-time' to track in real-time or 'range' to track a block range: range
   Enter the starting block number: <start_block>
   Enter the ending block number (or press Enter to track up to the latest block): <end_block>
   Tracking deposits from block <start_block> to <end_block or latest>...
   ```
