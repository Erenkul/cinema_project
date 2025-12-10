// navbar.js - Custom Navbar Component

class CustomNavbar extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <nav class="bg-gradient-to-r from-red-700 via-red-600 to-red-500 shadow-lg border-b border-red-900 sticky top-0 z-50">
        <div class="container mx-auto px-4">
          <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <a href="/" class="flex items-center space-x-3">
              <img src="https://cdn.pixabay.com/photo/2022/07/17/19/22/movie-7328179_1280.png" alt="ERN Cinema Logo" class="w-10 h-10 rounded-lg shadow-md border border-white/20">
              <span class="text-xl font-extrabold text-white tracking-wide hover:text-amber-400 transition">
                ERN Cinema
              </span>
            </a>

            <!-- Desktop Navigation -->
            <div class="hidden md:flex items-center space-x-8">
              <a href="/" class="nav-link glow-on-hover ${this.isActive('/')}">
                <i data-feather="home" class="w-4 h-4"></i>
                <span>Home</span>
              </a>
              <a href="/movies" class="nav-link glow-on-hover ${this.isActive('/movies')}">
                <i data-feather="film" class="w-4 h-4"></i>
                <span>Movies</span>
              </a>
              <a href="/suggestions" class="nav-link glow-on-hover ${this.isActive('/suggestions')}">
                <i data-feather="star" class="w-4 h-4"></i>
                <span>Suggestions</span>
              </a>
              <a href="/customers" class="nav-link glow-on-hover${this.isActive('/customers')}">
                <i data-feather="users" class="w-4 h-4"></i>
                <span>Customers</span>
              </a>
              <a href="#" class="nav-link glow-on-hover">
                <i data-feather="info" class="w-4 h-4"></i>
                <span>About</span>
              </a>
            </div>

            <!-- Book Now Button -->
            <a href="/movies" class="hidden md:block bg-secondary hover:bg-secondary/90 text-white px-6 py-3 rounded-lg font-medium text-center transition-all shadow-lg hover:shadow-xl glow-on-hover">
              Book Tickets
            </a>

            <!-- Mobile Menu Button -->
            <button id="mobile-menu-button" class="md:hidden text-white hover:text-amber-400 focus:outline-none">
              <i data-feather="menu" class="w-6 h-6"></i>
            </button>
          </div>

          <!-- Mobile Navigation -->
          <div id="mobile-menu" class="hidden md:hidden pb-4 mt-2 bg-black/20 rounded-lg">
            <div class="flex flex-col space-y-2">
              <a href="/" class="mobile-nav-link ${this.isActive('/')}">
                <i data-feather="home" class="w-4 h-4"></i>
                <span>Home</span>
              </a>
              <a href="/movies" class="mobile-nav-link ${this.isActive('/movies')}">
                <i data-feather="film" class="w-4 h-4"></i>
                <span>Movies</span>
              </a>
              <a href="/suggestions" class="mobile-nav-link ${this.isActive('/suggestions')}">
                <i data-feather="star" class="w-4 h-4"></i>
                <span>Suggestions</span>
              </a>
              <a href="/customers" class="mobile-nav-link ${this.isActive('/customers')}">
                <i data-feather="users" class="w-4 h-4"></i>
                <span>Customers</span>
              </a>
              <a href="#" class="mobile-nav-link">
                <i data-feather="info" class="w-4 h-4"></i>
                <span>About</span>
              </a>
              <a href="/" class="text-amber-400 hover:bg-secondary/90 text-white px-6 py-2 rounded-lg font-medium text-center">
                Book Now
              </a>
            </div>
          </div>
        </div>
      </nav>

      <style>
        .nav-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #ffffffff;
          font-weight: 500;
          transition: all 0.3s ease-in-out;
          padding: 0.5rem 0.75rem;
          border-radius: 0.375rem;
          position: relative;
        }

        .nav-link:hover {
          color: #ffd166;
          background-color: rgba(229, 62, 62, 0.1);
        }

        .nav-link.active {
          color: #ff8400ff;
          background-color: rgba(229, 62, 62, 0.1);
        }

        .mobile-nav-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #ffffffff;
          font-weight: 500;
          transition: all 0.25s ease-in-out;
          padding: 0.75rem 1rem;
          border-radius: 0.5rem;
        }

        .mobile-nav-link:hover {
          color: #ffd166;
          background-color: rgba(255, 162, 0, 1);
        }

        .mobile-nav-link.active {
          color: #ff8400ff;
          background-color: rgba(255, 162, 0, 1);
        }
      </style>
    `;

    // Mobile menu toggle
    const menuButton = this.querySelector('#mobile-menu-button');
    const mobileMenu = this.querySelector('#mobile-menu');

    menuButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });

    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
      feather.replace();
    }
  }

  isActive(path) {
    const currentPath = window.location.pathname;
    if (path === '/') {
      return currentPath === '/' ? 'active' : '';
    }
    return currentPath.startsWith(path) ? 'active' : '';
  }
}

customElements.define('custom-navbar', CustomNavbar);