import './style/nav.css'
import { FiHome } from "react-icons/fi";
import { IoPersonOutline } from "react-icons/io5";
import { LiaPhoneSquareSolid } from "react-icons/lia";
import { Link } from 'react-router-dom';

function Nav() {
    return (
        <div className="Nav">
            <header className="header">
                <nav className="header-nav">
                    <ul className="header-links">
                        <li className="header-link left">
                            <Link to="/" className="link-container">
                                <FiHome size={40}/>
                                <span>Home</span>
                            </Link>
                        </li>
                        <li className="header-link center">
                            <Link to="/about" className="link-container">
                                <IoPersonOutline size={40}/>
                                <span>About Us</span>
                            </Link>
                        </li>
                        <li className="header-link right">
                            <Link to="/contact" className="link-container">
                                <LiaPhoneSquareSolid size={40}/>
                                <span>Contact Us</span>
                            </Link>
                        </li>
                    </ul>
                </nav>
            </header>
        </div>
    );
}

export default Nav;