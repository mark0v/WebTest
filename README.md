# Website Uptime Monitor

A modern web application for monitoring website uptime and response times. Built with Flask and Docker.

## Features

- Real-time website status monitoring
- Response time tracking
- Customizable website names
- Dark theme with modern UI
- Docker support for easy deployment
- Automatic HTTPS support for local IPs

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd website-monitor
```

2. Build and start the container:
```bash
docker-compose up --build -d
```

The application will be available at `http://localhost:5000`

### Manual Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd website-monitor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## Usage

1. Add websites by entering their URLs
2. Monitor their status in real-time
3. Customize website names by clicking on them
4. View response times and last check timestamps
5. Remove websites using the delete button

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- SQLite (Database)
- Docker (Containerization)
- HTML5/CSS3 (Frontend)
- JavaScript (Frontend interactions)

## License

MIT License 