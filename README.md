# 👷‍♂️🚧 PROJECT IS WORK IN PROGRESS 🚧👷‍♂️

## Project Description

Welcome to **SignUp**. The minimalist website designed for event management. The main features include:

- **Event Sign-Up**: Users can sign up for various events.
- **User Dashboard**: Users can check which events they have signed up for.
- **Primary and Reserve Lists**: Users can see if they are on the primary or reserve list for events, names will automatically be added to the Primary list if someone "Unsigns" from the primary list, depending on position on the Reserve list.

## Features

- **Minimalist Design**: The website features a clean and simple design for ease of use.
- **Responsive Layout**: The design is responsive, ensuring a good experience on both desktop and mobile devices.
- **User-Friendly Interface**: The interface is intuitive, making it easy for users to navigate and use the website.

## Technologies Used

- **HTML**
- **CSS**
- **Flask**
- **SQLite**

## Local builds

1. Clone the repository:
   ```sh
   git clone https://github.com/Aetheridon/SignUp.git
   ```

2. Change directory to the appropriate folder:
   ```sh
   cd SignUp
   ```

3. It is recommended to create a virtual environment like so:
   ```sh
   python3 -m venv venv
   ```

   And to then activate it with...

   ```sh
   source venv/bin/activate
   ```

4. Now, install all needed dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```

5. Now, run the main Flask application:
   ```sh
   python3 src/main.py
   ```
  
  and the website should be avaliable locally at [127.0.0.1:5000](http://127.0.0.1:5000/)