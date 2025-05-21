# Discovering Paradise - Travel Website

A comprehensive travel and destination guide website built with Python and Django.

## Features

- **Destination Browsing**: Explore destinations by continent, search for specific locations
- **Accommodation Booking**: View and book accommodations at various destinations
- **Activity Information**: Discover activities available at each destination
- **User Reviews**: Read and write reviews for destinations, accommodations, and activities
- **User Authentication**: Register and login to access personalized features
- **Responsive Design**: Fully responsive website that works on all devices

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development)
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/discovering-paradise.git
   cd discovering-paradise
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the website at http://127.0.0.1:8000/

## Project Structure

- **accounts**: User authentication and profile management
- **core**: Core functionality and homepage
- **destinations**: Destination, accommodation, and activity models and views
- **reviews**: Review system for destinations and services
- **templates**: HTML templates for the website

## Screenshots

*Coming soon*
![image](https://github.com/user-attachments/assets/a995df1f-60c5-4623-bfb4-28ec12b58445)
![Screenshot 2025-05-18 221804](https://github.com/user-attachments/assets/3edc9d7e-f123-4491-893a-5c50c4277f1b)
![Screenshot 2025-05-18 221827](https://github.com/user-attachments/assets/efd38b00-5df4-42a2-8755-d482588ce2c8)
![Screenshot 2025-05-18 221904](https://github.com/user-attachments/assets/f360a677-a313-4015-a62f-3fbda9c7c4fc)






## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design framework
- Font Awesome for the icons
- Django community for the excellent documentation
