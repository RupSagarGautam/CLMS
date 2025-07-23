# CLMS (Client Management System)

## Overview
CLMS is a secure client management system with role-based access control. It enables administrators to manage staff accounts and allows staff members to handle client data with strict privacy controls.

## Key Features

### Admin Capabilities
- Create and manage staff accounts
- Access all client data across the system
- Monitor staff activities
- System-wide data management

### Staff Features
- Secure login with admin-provided credentials
- Add and manage client details
- View and edit their own client entries
- Data privacy - staff can only access their own entries

## Security Features
- Role-based access control (Admin/Staff)
- Data isolation between staff members
- Secure authentication system
- Protected client information

## System Requirements
- [Specify backend requirements]
- [Specify database requirements]
- [Specify frontend requirements]

# CLMS (Client Management System)

## Installation

1. Clone the repository
```bash
git clone [https://github.com/RupSagarGautam/CLMS]
cd CLMS
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
On Windows Use: 
```bash
.venv\Scripts\Activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```

6. Start the development server
```bash
python manage.py runserver
```

## Usage
1. Admin login to create staff accounts
2. Provide credentials to staff members
3. Staff can log in and manage their client data
4. Admin can oversee all operations

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the [License Name] - see the LICENSE file