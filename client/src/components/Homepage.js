import React from "react";
import { Link } from "react-router-dom";

import hi from "../assets/1.png";

const Homepage = () => {
  return (
    <div id="homepage">
      <div className="image-container">
        <header id="header">
          <p>LOGO</p>

          <nav className="header-nav">
            <div>
              <Link to="#">تسجيل دخول</Link>
              <span> | </span>
              <Link to="#">مستخدم جديد</Link>
            </div>
            <Link to="#">الاستفسارات</Link>
            <Link to="#">اتصل بنا</Link>
          </nav>
        </header>

        <section>
          <h1>خدمة توصيل الوجبات</h1>
          <p className="slogan">أسرع خدمة توصيل وجبات في العالم العربي</p>

          <button>اطلــــــب الآن</button>
        </section>
      </div>
    </div>
  );
};

export default Homepage;
