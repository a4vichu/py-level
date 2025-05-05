# PyLevel Framework

A modern Python web framework inspired by Laravel, providing an elegant and robust foundation for web applications.

## Features

- Laravel-inspired architecture and conventions
- Built-in CLI tool for common development tasks
- MVC architecture with routing and controllers
- Database migrations and ORM support
- Template engine for views
- Modern async support with FastAPI
- Comprehensive configuration management
- Built-in development server

## Installation

You can install PyLevel Framework using pip:

```bash
pip install pylevelframework
```

Or install from source:

```bash
git clone https://github.com/yourusername/pylevelframework.git
cd pylevelframework
pip install -e .
```

## Quick Start

1. Create a new project:
```bash
pylevel create myapp
cd myapp
```

2. Install dependencies:
```bash
pip install -e .
```

3. Start the development server:
```bash
pylevel serve
```

Visit http://localhost:8000 to see your application.

## Creating a Controller

```bash
pylevel make_controller UserController
```

This will create a new controller in `app/controllers/UserController.py` with basic CRUD methods.

## Project Structure

```
myapp/
├── app/
│   ├── controllers/    # Controller classes
│   ├── models/        # Database models
│   └── views/         # View templates
├── config/           # Configuration files
├── database/
│   └── migrations/   # Database migrations
├── public/          # Static files
├── resources/
│   └── views/       # View templates
├── routes/          # Route definitions
├── storage/
│   └── logs/       # Application logs
├── tests/          # Test files
└── .env            # Environment configuration
```

## Documentation

For detailed documentation, please visit:

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Routing](docs/routing.md)
- [Controllers](docs/controllers.md)
- [Database](docs/database.md)
- [Views](docs/views.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 