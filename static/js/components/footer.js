class CustomFooter extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        footer {
          background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(40, 40, 40, 0.95) 100%);
          color: white;
          padding: 3rem 2rem;
          margin-top: auto;
          border-top: 1px solid rgba(229, 62, 62, 0.1);
        }
        
        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 2rem;
        }
        
        .footer-logo {
          font-size: 1.5rem;
          font-weight: bold;
          margin-bottom: 1rem;
          display: flex;
          align-items: center;
        }
        
        .footer-logo-icon {
          color: #e53e3e;
          margin-right: 0.5rem;
        }
        
        .footer-description {
          color: #a0a0a0;
          margin-bottom: 1.5rem;
          line-height: 1.6;
        }
        
        .social-links {
          display: flex;
          gap: 1rem;
        }
        
        .social-link {
          color: white;
          background-color: rgba(255, 255, 255, 0.1);
          width: 2.5rem;
          height: 2.5rem;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
        }
        
        .social-link:hover {
          background-color: #e53e3e;
          transform: translateY(-3px);
        }
        
        .footer-heading {
          font-size: 1.2rem;
          font-weight: 600;
          margin-bottom: 1.5rem;
          position: relative;
          padding-bottom: 0.5rem;
        }
        
        .footer-heading::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 40px;
          height: 2px;
          background-color: #e53e3e;
        }
        
        .footer-links {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        
        .footer-link-item {
          margin-bottom: 0.8rem;
        }
        
        .footer-link {
          color: #a0a0a0;
          text-decoration: none;
          transition: color 0.2s;
        }
        
        .footer-link:hover {
          color: #e53e3e;
        }
        
        .footer-bottom {
          max-width: 1200px;
          margin: 3rem auto 0;
          padding-top: 2rem;
          border-top: 1px solid rgba(255, 255, 255, 0.05);
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;
          align-items: center;
        }
        
        .copyright {
          color: #a0a0a0;
          font-size: 0.9rem;
        }
        
        .footer-legal-links {
          display: flex;
          gap: 1.5rem;
        }
        
        .footer-legal-link {
          color: #a0a0a0;
          text-decoration: none;
          font-size: 0.9rem;
          transition: color 0.2s;
        }
        
        .footer-legal-link:hover {
          color: #e53e3e;
        }
        
        @media (max-width: 768px) {
          .footer-content {
            grid-template-columns: 1fr;
          }
          
          .footer-bottom {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }
        }
      </style>
      <footer>
        <div class="footer-content">
          <div class="footer-about">
            <div class="footer-logo">
              <i data-feather="film" class="footer-logo-icon"></i>
              ALP EREN KUL
            </div>
            <p class="footer-description">
              Experience the magic of movies in our state of the art theaters with premium sound and picture quality.
            </p>
            <div class="social-links">
              <a href="#" class="social-link">
                <i data-feather="facebook"></i>
              </a>
              <a href="#" class="social-link">
                <i data-feather="twitter"></i>
              </a>
              <a href="#" class="social-link">
                <i data-feather="instagram"></i>
              </a>
              <a href="#" class="social-link">
                <i data-feather="youtube"></i>
              </a>
            </div>
          </div>
          
          <div class="footer-links-section">
            <h3 class="footer-heading">Quick Links</h3>
            <ul class="footer-links">
              <li class="footer-link-item"><a href="#" class="footer-link">Home</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Movies</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Theaters</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Promotions</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">About Us</a></li>
            </ul>
          </div>
          
          <div class="footer-links-section">
            <h3 class="footer-heading">Categories</h3>
            <ul class="footer-links">
              <li class="footer-link-item"><a href="#" class="footer-link">Horror</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Thriller</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Fantasy</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Sci-Fi</a></li>
              <li class="footer-link-item"><a href="#" class="footer-link">Mystery</a></li>
            </ul>
          </div>
          
          <div class="footer-links-section">
            <h3 class="footer-heading">Contact</h3>
            <ul class="footer-links">
              <li class="footer-link-item">
                <i data-feather="map-pin" style="width: 16px; height: 16px; margin-right: 8px;"></i>
                Incek, Ankara, Turkey
              </li>
              <li class="footer-link-item">
                <i data-feather="phone" style="width: 16px; height: 16px; margin-right: 8px;"></i>
                534 708 7432
              </li>
              <li class="footer-link-item">
                <i data-feather="Mail:" style="width: 16px; height: 16px; margin-right: 8px;"></i>
                mail: kul.alperen@student.atilim.edu.tr
              </li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p class="copyright">© 2025 ERN CINEMA. All rights reserved.</p>
          <div class="footer-legal-links">
            <a href="#" class="footer-legal-link">Privacy Policy</a>
            <a href="#" class="footer-legal-link">Terms of Service</a>
            <a href="#" class="footer-legal-link">Cookie Policy</a>
          </div>
        </div>
      </footer>
    `;
  }
}
customElements.define('custom-footer', CustomFooter);