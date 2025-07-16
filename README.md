Django Shopping Site 

A clean, responsive shopping website built with Django, MongoDB, Tailwin, JS and HTMX. It supports user sign-up, item listings, cart functionality, checkout, and a role-based dashboard for both normal users and admins.

🔧 Features

- 🛍️ Item listing and detailed view
- 🛒 Cart system (add, update, remove items)
- ✅ Checkout system with chapa payment system (save orders)
- 👤 User authentication (signup/login/logout)
- 🧾 Admin dashboard:
  - View new, paid, and all orders
  - Mark new orders as seen
  - View active users
- 👥 Normal user dashboard:
  - View personal orders only
- 💻 Responsive layout using Tailwind CSS
- ⚡ Dashboard interactivity using plain JavaScript



 🚀 Live Demo

[ale-shopping.onrender.com](https://ale-shopping.onrender.com)

## 🧰 Tech Stack

- **Backend:** Django (Python, HTMX)
- **Database:** MongoDB (`mongoengine==0.29.1`)
- **Frontend:** HTML, Tailwind CSS, JS, HTMX
- **payment:** Chapa
- **Sessions:** Signed cookies (`SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`)
  
🙏 Acknowledgments
- Django & Tailwind docs
- Chapa API docs
- HTMX docs
- ChatGPT (for bug pair programming and mental support )


